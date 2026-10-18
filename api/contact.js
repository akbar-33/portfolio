// Receives the contact form (text plus links to files already uploaded to Blob)
// and emails it through Resend. Env: RESEND_API_KEY, optional CONTACT_TO / CONTACT_FROM.
const TO = process.env.CONTACT_TO || "linkwithakbar@gmail.com";
const FROM = process.env.CONTACT_FROM || "Portfolio inbox <onboarding@resend.dev>";

const MAX_MESSAGE = 50000;
const MAX_FILES = 10;
// Files at or under this size ride along as real attachments; Resend caps an
// email at 40 MB, so the total is kept well below that. Everything is also linked.
const ATTACH_EACH = 10 * 1024 * 1024;
const ATTACH_TOTAL = 25 * 1024 * 1024;

const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const fmtSize = (n) => n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.max(1, Math.round(n / 1024))} KB`;

function isBlobUrl(u) {
  try {
    const url = new URL(u);
    return url.protocol === "https:" && url.hostname.endsWith(".blob.vercel-storage.com");
  } catch {
    return false;
  }
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
  const clean = [];
  for (const f of files) {
    if (!f || !isBlobUrl(f.url)) return res.status(400).json({ error: "Unexpected file link." });
    clean.push({
      url: f.url,
      name: String(f.name || "file").slice(0, 200),
      size: Math.max(0, Number(f.size) || 0),
    });
  }

  const attachments = [];
  let attached = 0;
  for (const f of clean) {
    if (f.size && f.size <= ATTACH_EACH && attached + f.size <= ATTACH_TOTAL) {
      attachments.push({ path: f.url, filename: f.name });
      attached += f.size;
    }
  }

  const who = name ? `${name} <${email}>` : email;
  const fileLines = clean.map((f) => `- ${f.name} (${fmtSize(f.size)}): ${f.url}`).join("\n");
  const text = [
    `From: ${who}`,
    "",
    message || "(no message)",
    clean.length ? `\nFiles:\n${fileLines}` : "",
  ].join("\n");
  const html = `<div style="font-family:system-ui,sans-serif;font-size:15px;line-height:1.55;color:#17181A">
<p style="margin:0 0 12px;color:#6E6C66">From <b style="color:#17181A">${esc(who)}</b></p>
<div style="white-space:pre-wrap;border-left:3px solid #EC3013;padding:4px 0 4px 14px">${esc(message || "(no message)")}</div>
${clean.length ? `<p style="margin:18px 0 6px"><b>Files</b></p><ul style="margin:0;padding-left:18px">${clean
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
