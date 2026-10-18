// Opens a private upload from a signed link in the contact email: checks the
// signature, then redirects to a Blob URL that is valid for ten minutes. The
// file streams from Blob, never through this function.
import { issueSignedToken, presignUrl } from "@vercel/blob";
import { verify } from "./_sign.js";

export default async function handler(req, res) {
  const { p, e, s } = req.query;
  if (!verify(p, e, s)) {
    return res.status(403).send("This link is invalid or has expired.");
  }
  try {
    const validUntil = Date.now() + 10 * 60 * 1000;
    const token = await issueSignedToken({ pathname: p, operations: ["get"], validUntil });
    const { presignedUrl } = await presignUrl(token, { operation: "get", pathname: p, validUntil, access: "private" });
    res.setHeader("Cache-Control", "no-store");
    return res.redirect(302, presignedUrl);
  } catch (err) {
    console.error("presign failed", err);
    return res.status(502).send("Could not open this file right now.");
  }
}
