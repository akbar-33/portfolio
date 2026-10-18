// Issues short-lived presigned upload URLs so the contact form can upload files
// straight to Vercel Blob. The browser never sends file bytes through a function,
// which is what lets uploads go past the 4.5 MB function body limit.
// Auth is Vercel OIDC plus BLOB_STORE_ID, which Vercel sets when the store is connected.
import { issueSignedToken } from "@vercel/blob";
import { handleUploadPresigned } from "@vercel/blob/client";

const MAX_FILE_BYTES = 200 * 1024 * 1024;

function checkPath(pathname) {
  if (!pathname.startsWith("inbox/") || pathname.includes("..")) {
    throw new Error("Invalid upload path");
  }
}

export default async function handler(req, res) {
  // GET is a setup check: says which settings exist, never their values
  if (req.method === "GET") {
    let tokenCheck = "ok";
    try {
      await issueSignedToken({ pathname: "inbox/check.txt", operations: ["put"], validUntil: Date.now() + 60 * 1000 });
    } catch (err) {
      tokenCheck = err.message;
    }
    return res.status(200).json({
      functionRuns: true,
      tokenCheck,
      BLOB_STORE_ID: Boolean(process.env.BLOB_STORE_ID),
      BLOB_WEBHOOK_PUBLIC_KEY: Boolean(process.env.BLOB_WEBHOOK_PUBLIC_KEY),
      RESEND_API_KEY: Boolean(process.env.RESEND_API_KEY),
    });
  }
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  try {
    const result = await handleUploadPresigned({
      request: req,
      body: req.body,
      getSignedToken: async (pathname) => {
        checkPath(pathname);
        const validUntil = Date.now() + 15 * 60 * 1000;
        const token = await issueSignedToken({
          pathname,
          operations: ["put"],
          validUntil,
          maximumSizeInBytes: MAX_FILE_BYTES,
        });
        return {
          token,
          urlOptions: { maximumSizeInBytes: MAX_FILE_BYTES, addRandomSuffix: true, validUntil },
        };
      },
    });
    return res.status(200).json(result);
  } catch (err) {
    console.error("upload url failed", err);
    return res.status(400).json({ error: err.message });
  }
}
