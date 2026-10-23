/* Visual navigation over the original curriculum. All learning copy comes from D. */
function devOppsJourneyActivate(preview, event) {
  if (event?.type === "pointerenter" && !matchMedia("(hover: hover)").matches) return;
  if (preview.classList.contains("is-dismissed")) return;
  document.querySelectorAll(".devops-journey .journey-preview.is-active, .devops-journey .journey-preview.is-open").forEach(item => {
    if (item === preview) return;
    item.classList.remove("is-active", "is-open");
    item.querySelector("[data-journey-toggle]")?.setAttribute("aria-expanded", "false");
  });
  preview.classList.add("is-active");
  preview.querySelector("[data-journey-toggle]")?.setAttribute("aria-expanded", "true");
}
function devOppsJourneyLeave(preview, event) {
  const hasFocus = preview.contains(document.activeElement);
  const pointerInside = matchMedia("(hover: hover)").matches && preview.matches(":hover");
  if (event.type === "focusout" && preview.contains(event.relatedTarget)) return;
  if (!hasFocus && !pointerInside && !preview.classList.contains("is-open")) {
    preview.classList.remove("is-active");
    preview.querySelector("[data-journey-toggle]")?.setAttribute("aria-expanded", "false");
  }
  if (!hasFocus && !pointerInside) preview.classList.remove("is-dismissed");
}
function devOppsJourneyToggle(button) {
  const preview = button.closest(".journey-preview");
  const wasOpen = preview.classList.contains("is-open");
  preview.classList.remove("is-dismissed");
  devOppsJourneyActivate(preview);
  preview.classList.toggle("is-open", !wasOpen);
  preview.classList.toggle("is-active", !wasOpen);
  preview.classList.toggle("is-dismissed", wasOpen);
  button.setAttribute("aria-expanded", String(!wasOpen));
}
function devOppsJourneyKey(event) {
  if (event.key !== "Escape") return;
  const preview = event.target.closest(".journey-preview");
  if (!preview) return;
  preview.classList.remove("is-open", "is-active");
  preview.classList.add("is-dismissed");
  const button = preview.querySelector("[data-journey-toggle]");
  button?.setAttribute("aria-expanded", "false");
  button?.focus();
  event.preventDefault();
}

function devOppsJourney() {
  const colors = ["#ed4942", "#3b8ce5", "#ff8b38", "#e8b63c", "#9670ce", "#33b6a3",
    "#2d975d", "#e77fba", "#a4734e", "#4cb8cc", "#8793aa", "#45404d", "#c3ae3e"];
  const previewEvents = `onpointerenter="devOppsJourneyActivate(this,event)" onpointerleave="devOppsJourneyLeave(this,event)" onfocusin="devOppsJourneyActivate(this,event)" onfocusout="devOppsJourneyLeave(this,event)"`;
  const reveal = (id, week) => `<div class="journey-reveal" id="${id}" role="region" aria-labelledby="${id}-title">
    <span class="journey-reveal-kicker">Week ${String(week.week).padStart(2, "0")}</span>
    <h4 id="${id}-title">${esc(week.title)}</h4>
    <p>${esc(week.outcome)}</p>
    <a class="journey-enter" href="#week-${week.week}">Enter week ${week.week}<span aria-hidden="true">↗</span></a>
  </div>`;
  return `<section class="devops-journey" id="journey" aria-labelledby="journey-title" onkeydown="devOppsJourneyKey(event)">
    <div class="journey-heading"><h2 id="journey-title">The path through the year</h2><p>START ANY TIME / ADVANCE WITH EVIDENCE</p></div>
    <div class="journey-rows">${phases.map((phase, index) => {
      const number = String(index + 1).padStart(2, "0");
      const weeks = D.weeks.slice(phase.start - 1, phase.end);
      const gate = weeks[weeks.length - 1];
      const proved = weeks.filter(week => record(week.week).status === "Proved").length;
      const mascotId = `journey-gate-${number}`;
      return `<article class="journey-row" id="journey-level-${number}" style="--journey-color:${colors[index % colors.length]}" aria-labelledby="journey-level-title-${number}">
        <header class="journey-row-heading">
          <div class="journey-level-number" aria-label="Level ${index + 1}">${number}</div>
          <div><p class="journey-range">Weeks ${String(phase.start).padStart(2, "0")}–${String(phase.end).padStart(2, "0")}</p><h3 id="journey-level-title-${number}">${esc(phase.name)}</h3></div>
          <span class="journey-proved">${proved} / 4 proved</span>
        </header>
        <div class="journey-scene">
          <svg class="journey-thread" aria-hidden="true" focusable="false"><path/></svg>
          <div class="journey-preview journey-mascot" ${previewEvents}>
            <button class="journey-mascot-button" type="button" data-journey-toggle aria-expanded="false" aria-controls="${mascotId}" aria-label="Preview ${esc(phase.name)}" onclick="devOppsJourneyToggle(this)">
              <picture><source media="(prefers-reduced-motion: reduce)" srcset="assets/mascots/level-${number}-static.svg"><img src="assets/mascots/level-${number}.svg" alt="" width="180" height="180" loading="lazy"></picture>
              <span class="journey-mascot-plus" aria-hidden="true">+</span>
            </button>
            ${reveal(mascotId, gate)}
          </div>
          <div class="journey-stops">
            ${weeks.map((week, offset) => {
              const id = `journey-week-${week.week}`;
              const isGate = offset === 3;
              const isProved = record(week.week).status === "Proved";
              return `<div class="journey-preview journey-stop${isGate ? " journey-stop-gate" : ""}${isProved ? " journey-stop-proved" : ""}" ${previewEvents}>
                <a class="journey-week-link" href="#week-${week.week}" aria-label="Week ${week.week}: ${esc(week.title)}">
                  <span class="journey-node"><span class="journey-node-caption">WEEK</span><span class="journey-node-number">${String(week.week).padStart(2, "0")}</span>${isProved ? '<span class="journey-check" aria-label="Proved">✓</span>' : ""}</span>
                  <span class="journey-week-title">${esc(week.title)}</span>
                </a>
                <button class="journey-peek" type="button" data-journey-toggle aria-expanded="false" aria-controls="${id}" aria-label="Preview week ${week.week}" onclick="devOppsJourneyToggle(this)"><span aria-hidden="true">+</span></button>
                ${reveal(id, week)}
              </div>`;
            }).join("")}
          </div>
        </div>
      </article>`;
    }).join("")}</div>
  </section>`;
}

/* A single measured thread joins the mascot and every week in either layout.
   Fixed SVG coordinates drifted away from the artwork at narrower widths and
   when a preview expanded. Read the rendered anchors, including hover transforms. */
(() => {
  const app = document.getElementById("app");
  const mobile = matchMedia("(max-width: 700px)");
  let scenes = [], resize = null, frame = 0, followUntil = 0;

  const geometry = scene => {
    const bounds = scene.getBoundingClientRect();
    const mascot = scene.querySelector(".journey-mascot-button img").getBoundingClientRect();
    const nodes = [...scene.querySelectorAll(".journey-node")].map(node => node.getBoundingClientRect());
    // Start inside the lower body, below the transparent eye cutouts.
    const points = [{x: mascot.left + mascot.width * .5 - bounds.left,
      y: mascot.top + mascot.height * .66 - bounds.top}, ...nodes.map(node => ({
        x: node.left + node.width / 2 - bounds.left,
        y: node.top + node.height / 2 - bounds.top
      }))];
    const round = value => Math.round(value * 100) / 100;
    let path = `M${round(points[0].x)} ${round(points[0].y)}`;
    const parity = scenes.indexOf(scene) % 2 ? -1 : 1;
    points.slice(1).forEach((end, index) => {
      const start = points[index];
      const dx = end.x - start.x, dy = end.y - start.y;
      const direction = (index % 2 ? -1 : 1) * parity;
      if (mobile.matches) {
        const bend = Math.min(28, Math.abs(dy) * .3) * (index === 0 ? -1 : direction);
        path += ` C${round(start.x + bend)} ${round(start.y + dy * .34)} ${round(end.x + bend)} ${round(end.y - dy * .34)} ${round(end.x)} ${round(end.y)}`;
      } else {
        const bend = Math.min(index === 0 ? 25 : 45, Math.abs(dx) * .32) * direction;
        path += ` C${round(start.x + dx * .34)} ${round(start.y + bend)} ${round(end.x - dx * .34)} ${round(end.y + bend)} ${round(end.x)} ${round(end.y)}`;
      }
    });
    return {svg: scene.querySelector(".journey-thread"), width: bounds.width, height: bounds.height, path};
  };
  const draw = time => {
    frame = 0;
    if (!scenes.length || document.hidden) return;
    // Batch layout reads before changing SVG attributes.
    const paths = scenes.filter(scene => scene.isConnected).map(geometry);
    paths.forEach(({svg, width, height, path}) => {
      svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
      svg.querySelector("path").setAttribute("d", path);
    });
    if (time < followUntil) frame = requestAnimationFrame(draw);
  };
  const schedule = (follow = false) => {
    if (follow) followUntil = performance.now() + 350;
    if (!frame) frame = requestAnimationFrame(draw);
  };
  const bind = () => {
    resize?.disconnect();
    scenes = [...app.querySelectorAll(".journey-scene")];
    if (!scenes.length) { cancelAnimationFrame(frame); frame = 0; return; }
    resize = new ResizeObserver(() => schedule());
    scenes.forEach(scene => {
      resize.observe(scene);
      scene.querySelectorAll(".journey-node, .journey-mascot-button").forEach(node => resize.observe(node));
    });
    schedule();
  };
  new MutationObserver(bind).observe(app, {childList: true});
  // ResizeObserver tracks expanding mobile previews. These events also follow
  // the short transform transitions that do not change an element's layout box.
  ["pointerover", "pointerout", "focusin", "focusout", "click", "transitionrun"].forEach(type => {
    app.addEventListener(type, event => {
      if (event.target.closest?.(".journey-scene")) schedule(true);
    }, {passive: true});
  });
  app.addEventListener("load", event => {
    if (event.target.closest?.(".journey-scene")) schedule();
  }, true);
  mobile.addEventListener("change", () => schedule());
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { cancelAnimationFrame(frame); frame = 0; }
    else schedule();
  });
  document.fonts?.ready.then(() => schedule());
  bind();
})();
