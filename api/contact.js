// Receives the contact form (text plus the paths of files already uploaded to
// private Blob) and emails it through Resend with signed download links.
// Env: RESEND_API_KEY, BLOB_READ_WRITE_TOKEN, optional CONTACT_TO / CONTACT_FROM / SITE_URL.
import { head, issueSignedToken, presignUrl } from "@vercel/blob";
import { signedLink, LINK_DAYS } from "./_sign.js";

const TO = process.env.CONTACT_TO || "akbarthesecond@gmail.com";
const FROM = process.env.CONTACT_FROM || "Portfolio inbox <onboarding@resend.dev>";

const MAX_MESSAGE = 50000;
const MAX_FILES = 10;
// Files at or under this size ride along as real attachments; Resend caps an
// email at 40 MB, so the total is kept well below that. Everything is also linked.
// Resend fetches attachments at send time, from a Blob URL valid for an hour.
const ATTACH_EACH = 10 * 1024 * 1024;
const ATTACH_TOTAL = 25 * 1024 * 1024;

const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const fmtSize = (n) => n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.max(1, Math.round(n / 1024))} KB`;

async function attachUrl(pathname) {
  const validUntil = Date.now() + 60 * 60 * 1000;
  const token = await issueSignedToken({ pathname, operations: ["get"], validUntil });
  return (await presignUrl(token, { operation: "get", pathname, validUntil, access: "private" })).presignedUrl;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  if (!process.env.RESEND_API_KEY) {
    return res.status(500).json({ error: "Inbox is not configured yet." });
  }

  const b = req.body || {};
  // honeypot: real people never see this field
  if (b.website) return res.status(200).json({ ok: true });

  const name = String(b.name || "").trim().slice(0, 200);
  const email = String(b.email || "").trim().slice(0, 320);
  const message = String(b.message || "").trim();
  const files = Array.isArray(b.files) ? b.files : [];

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: "Please enter a valid email so I can reply." });
  }
  if (!message && !files.length) {
    return res.status(400).json({ error: "Add a message or at least one file." });
  }
  if (message.length > MAX_MESSAGE) {
    return res.status(400).json({ error: `Message is over ${MAX_MESSAGE.toLocaleString()} characters.` });
  }
  if (files.length > MAX_FILES) {
    return res.status(400).json({ error: `Up to ${MAX_FILES} files per message.` });
  }
  const base = process.env.SITE_URL || `https://${req.headers["x-forwarded-host"] || req.headers.host}`;
  const clean = [];
  try {
    for (const f of files) {
      const pathname = String((f && f.pathname) || "");
      if (!pathname.startsWith("inbox/") || pathname.includes("..")) {
        return res.status(400).json({ error: "Unexpected file." });
      }
      // the size comes from Blob, not the browser; this also proves the upload exists
      const meta = await head(pathname);
      clean.push({
        pathname,
        url: signedLink(base, pathname),
        name: String(f.name || pathname.split("/").pop()).slice(0, 200),
        size: meta.size,
      });
    }
  } catch (err) {
    console.error("blob lookup failed", err);
    return res.status(400).json({ error: "An uploaded file could not be found. Please try again." });
  }

  const attachments = [];
  let attached = 0;
  try {
    for (const f of clean) {
      if (f.size <= ATTACH_EACH && attached + f.size <= ATTACH_TOTAL) {
        attachments.push({ path: await attachUrl(f.pathname), filename: f.name });
        attached += f.size;
      }
    }
  } catch (err) {
    // the links still work, so send without attachments rather than fail
    console.error("attachment presign failed", err);
    attachments.length = 0;
  }

  const who = name ? `${name} <${email}>` : email;
  const fileLines = clean.map((f) => `- ${f.name} (${fmtSize(f.size)}): ${f.url}`).join("\n");
  const text = [
    `From: ${who}`,
    "",
    message || "(no message)",
    clean.length ? `\nFiles (links work for ${LINK_DAYS} days):\n${fileLines}` : "",
  ].join("\n");
  const html = `<div style="font-family:system-ui,sans-serif;font-size:15px;line-height:1.55;color:#17181A">
<p style="margin:0 0 12px;color:#6E6C66">From <b style="color:#17181A">${esc(who)}</b></p>
<div style="white-space:pre-wrap;border-left:3px solid #EC3013;padding:4px 0 4px 14px">${esc(message || "(no message)")}</div>
${clean.length ? `<p style="margin:18px 0 6px"><b>Files</b> <span style="color:#6E6C66">· links work for ${LINK_DAYS} days</span></p><ul style="margin:0;padding-left:18px">${clean
    .map((f) => `<li><a href="${esc(f.url)}">${esc(f.name)}</a> <span style="color:#6E6C66">(${fmtSize(f.size)})</span></li>`)
    .join("")}</ul>` : ""}
</div>`;

  const subjectBit = message ? message.split("\n")[0].slice(0, 60) : `${clean.length} file${clean.length === 1 ? "" : "s"}`;
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: FROM,
      to: [TO],
      reply_to: email,
      subject: `Portfolio: ${name || email} · ${subjectBit}`,
      text,
      html,
      ...(attachments.length ? { attachments } : {}),
    }),
  });

  if (!r.ok) {
    console.error("resend failed", r.status, await r.text());
    return res.status(502).json({ error: "Could not send right now. Please try again in a minute." });
  }
  return res.status(200).json({ ok: true });
}
