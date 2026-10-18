// Signed download links for private blobs. The underscore keeps Vercel from
// treating this file as a function. The key is LINK_SECRET if set, else the
// Resend API key; rotating whichever is used revokes every link ever emailed.
import { createHmac, timingSafeEqual } from "node:crypto";

export const LINK_DAYS = 90;

const secret = () => process.env.LINK_SECRET || process.env.RESEND_API_KEY || "";

function mac(pathname, expires) {
  return createHmac("sha256", secret())
    .update(`${pathname}\n${expires}`)
    .digest("base64url");
}

export function signedLink(base, pathname) {
  const e = Date.now() + LINK_DAYS * 86400000;
  const q = new URLSearchParams({ p: pathname, e: String(e), s: mac(pathname, e) });
  return `${base}/api/file?${q}`;
}

export function verify(pathname, expires, sig) {
  if (!secret()) return false;
  if (!pathname || !sig || !(Number(expires) > Date.now())) return false;
  const want = Buffer.from(mac(pathname, expires));
  const got = Buffer.from(String(sig));
  return want.length === got.length && timingSafeEqual(want, got);
}
