/* Contact form: files go straight to private Vercel Blob, then the text and file paths go to /api/contact. */
import { upload } from "/vendor/blob-client.js";

var MAX_FILES = 10;
var MAX_BYTES = 200 * 1024 * 1024;

var form = document.getElementById("contact-form");
var input = document.getElementById("cf-files");
var drop = document.getElementById("cf-drop");
var list = document.getElementById("cf-list");
var status = document.getElementById("cf-status");
var button = form.querySelector(".cf-send");
var picked = [];

function size(n) {
  return n >= 1048576 ? (n / 1048576).toFixed(1) + " MB" : Math.max(1, Math.round(n / 1024)) + " KB";
}

function say(msg, isError) {
  status.textContent = msg;
  status.classList.toggle("is-error", !!isError);
}

function render() {
  list.innerHTML = "";
  picked.forEach(function (f, i) {
    var li = document.createElement("li");
    li.innerHTML = '<span class="cf-name"></span><span class="cf-size"></span><span class="cf-bar"><i></i></span><button type="button" aria-label="Remove">&times;</button>';
    li.querySelector(".cf-name").textContent = f.name;
    li.querySelector(".cf-size").textContent = size(f.size);
    li.querySelector("button").onclick = function () { picked.splice(i, 1); render(); };
    list.appendChild(li);
  });
}

function add(files) {
  var skipped = [];
  Array.prototype.forEach.call(files, function (f) {
    if (f.size > MAX_BYTES) skipped.push(f.name + " is over 200 MB");
    else if (picked.length >= MAX_FILES) skipped.push(f.name + ": 10 files max");
    else picked.push(f);
  });
  render();
  say(skipped.join(" · "), skipped.length > 0);
}

input.addEventListener("change", function () { add(input.files); input.value = ""; });
["dragenter", "dragover"].forEach(function (t) {
  drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add("is-over"); });
});
["dragleave", "drop"].forEach(function (t) {
  drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.remove("is-over"); });
});
drop.addEventListener("drop", function (e) { add(e.dataTransfer.files); });

form.addEventListener("submit", async function (e) {
  e.preventDefault();
  var data = new FormData(form);
  var email = String(data.get("email") || "").trim();
  var message = String(data.get("message") || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return say("Please enter a valid email so I can reply.", true);
  if (!message && !picked.length) return say("Add a message or at least one file.", true);

  button.disabled = true;
  var bars = list.querySelectorAll(".cf-bar i");
  try {
    var uploaded = [];
    for (var i = 0; i < picked.length; i++) {
      var f = picked[i];
      say("Uploading " + (i + 1) + " of " + picked.length + ": " + f.name);
      var bar = bars[i];
      var safe = f.name.replace(/[^\w.\-]+/g, "_").slice(-120) || "file";
      var blob = await upload("inbox/" + safe, f, {
        access: "private",
        handleUploadUrl: "/api/upload",
        multipart: f.size > 20 * 1024 * 1024,
        onUploadProgress: function (p) { if (bar) bar.style.width = p.percentage + "%"; }
      });
      uploaded.push({ pathname: blob.pathname, name: f.name });
    }
    say("Sending…");
    var r = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: data.get("name"), email: email, message: message,
        website: data.get("website"), files: uploaded
      })
    });
    var out = await r.json().catch(function () { return {}; });
    if (!r.ok) throw new Error(out.error || "Something went wrong.");
    form.reset();
    picked = [];
    render();
    say("Sent. Thank you, I'll reply to " + email + ".");
  } catch (err) {
    say(err.message || "Something went wrong. Please try again.", true);
  } finally {
    button.disabled = false;
  }
});
