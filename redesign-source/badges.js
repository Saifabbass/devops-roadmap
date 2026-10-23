/* Resource capsules inspired by TaktForm's GitHub Stars Badge.
   Labels identify the destination. No star count is fabricated or required online. */
function devOppsBadgeInfo(href, label) {
  let url;
  try { url = new URL(href, location.href); } catch { return null; }
  if (!/^https?:$/.test(url.protocol)) return null;
  const host = url.hostname.replace(/^www\./, "");
  const github = host === "github.com";
  const gitlab = host === "gitlab.com" || host.endsWith(".gitlab.com");
  const parts = url.pathname.split("/").filter(Boolean);
  let title = String(label || "").trim();
  if (!title || /^(https?:|www\.|open$|source$|link$)/i.test(title)) {
    title = github && parts.length > 1 ? parts.slice(0, 2).join("/") : host + (parts.length ? " / " + decodeURIComponent(parts[parts.length - 1]).replace(/[-_]/g, " ") : "");
  }
  return { url: url.href, title, kind: github ? "github" : gitlab ? "gitlab" : "reference", provider: github ? "GitHub repository" : gitlab ? "GitLab" : "Reference" };
}
function devOppsBadgeIcon(kind) {
  const glyph = kind === "github"
    ? '<path fill="currentColor" d="M12 .8a11.2 11.2 0 0 0-3.54 21.83c.56.1.77-.24.77-.54v-2.1c-3.12.68-3.78-1.32-3.78-1.32-.51-1.3-1.25-1.65-1.25-1.65-1.02-.7.08-.69.08-.69 1.13.08 1.72 1.16 1.72 1.16 1 1.72 2.62 1.22 3.26.93.1-.73.4-1.23.71-1.52-2.49-.28-5.1-1.25-5.1-5.54 0-1.22.44-2.22 1.15-3-.12-.28-.5-1.42.11-2.97 0 0 .94-.3 3.08 1.15a10.75 10.75 0 0 1 5.6 0c2.14-1.45 3.08-1.15 3.08-1.15.61 1.55.23 2.69.11 2.97.72.78 1.15 1.78 1.15 3 0 4.3-2.62 5.25-5.12 5.53.4.35.76 1.03.76 2.08v3.12c0 .3.2.65.77.54A11.2 11.2 0 0 0 12 .8Z"/>'
    : kind === "gitlab"
    ? '<path fill="currentColor" d="m12 22 4.4-13.5H7.6L12 22Zm0 0L3.8 8.5H.7c-.5 0-.8.5-.6.9L12 22Zm0 0L20.2 8.5h3.1c.5 0 .8.5.6.9L12 22ZM.7 8.5 3.4.5c.1-.4.7-.4.9 0l3.3 8H.7Zm15.7 0 3.3-8c.2-.4.8-.4.9 0l2.7 8h-6.9Z"/>'
    : '<circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M2 12h20M12 2c6 5 6 15 0 20-6-5-6-15 0-20Z" fill="none" stroke="currentColor" stroke-width="1.7"/>';
  return '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">' + glyph + '</svg>';
}
function devOppsBadgeInner(info) {
  return '<span class="resource-badge-icon" aria-hidden="true"><span>' + devOppsBadgeIcon(info.kind) + '</span><span>' + devOppsBadgeIcon(info.kind) + '</span></span><span class="resource-badge-label">' + esc(info.title) + '</span><span class="resource-badge-arrow" aria-hidden="true">↗</span>';
}
function devOppsResourceBadge(href, label) {
  const info = devOppsBadgeInfo(href, label);
  if (!info) return esc(label || href);
  return '<a class="resource-badge" href="' + esc(info.url) + '" target="_blank" rel="noopener noreferrer" title="' + esc(info.provider + ': ' + info.title) + '">' + devOppsBadgeInner(info) + '</a>';
}
function devOppsDecorateResourceLinks(root = document) {
  root.querySelectorAll('a[href^="https://"], a[href^="http://"]').forEach(link => {
    if (link.classList.contains("resource-badge") || link.hasAttribute("data-plain-link") || link.querySelector("img")) return;
    const info = devOppsBadgeInfo(link.href, link.textContent);
    if (!info) return;
    link.classList.add("resource-badge");
    link.innerHTML = devOppsBadgeInner(info);
    link.title = info.provider + ": " + info.title;
    link.setAttribute("aria-label", info.title + " (" + info.provider + ", opens in a new tab)");
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  });
}
