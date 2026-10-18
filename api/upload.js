// Issues short-lived client tokens so the contact form can upload files straight
// to Vercel Blob. The browser never sends file bytes through a function, which is
// what lets uploads go past the 4.5 MB function body limit.
import { handleUpload } from "@vercel/blob/client";

const MAX_FILE_BYTES = 200 * 1024 * 1024;

export default async function handler(req, res) {
  // GET is a setup check: says which settings exist, never their values
  if (req.method === "GET") {
    const has = (k) => Boolean(process.env[k]);
    const blobVars = Object.keys(process.env).filter((k) => /BLOB/i.test(k)).sort();
    return res.status(200).json({
      functionRuns: true,
      BLOB_READ_WRITE_TOKEN: has("BLOB_READ_WRITE_TOKEN"),
      RESEND_API_KEY: has("RESEND_API_KEY"),
      blobVariableNames: blobVars,
    });
  }
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  try {
    const result = await handleUpload({
      request: req,
      body: req.body,
      onBeforeGenerateToken: async (pathname) => {
        if (!pathname.startsWith("inbox/") || pathname.includes("..")) {
          throw new Error("Invalid upload path");
        }
        return {
          maximumSizeInBytes: MAX_FILE_BYTES,
          addRandomSuffix: true,
          validUntil: Date.now() + 15 * 60 * 1000,
        };
      },
    });
    return res.status(200).json(result);
  } catch (err) {
    console.error("upload token failed", err);
    return res.status(400).json({ error: err.message });
  }
}
