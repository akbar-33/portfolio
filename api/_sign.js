// Signed download links for private blobs. The underscore keeps Vercel from
// treating this file as a function. The key is the Blob read-write token, so
// rotating that token in Vercel revokes every link ever emailed.
import { createHmac, timingSafeEqual } from "node:crypto";

export const LINK_DAYS = 90;

function mac(pathname, expires) {
  return createHmac("sha256", process.env.BLOB_READ_WRITE_TOKEN || "")
    .update(`${pathname}\n${expires}`)
    .digest("base64url");
}

export function signedLink(base, pathname) {
  const e = Date.now() + LINK_DAYS * 86400000;
  const q = new URLSearchParams({ p: pathname, e: String(e), s: mac(pathname, e) });
  return `${base}/api/file?${q}`;
}

export function verify(pathname, expires, sig) {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return false;
  if (!pathname || !sig || !(Number(expires) > Date.now())) return false;
  const want = Buffer.from(mac(pathname, expires));
  const got = Buffer.from(String(sig));
  return want.length === got.length && timingSafeEqual(want, got);
}
