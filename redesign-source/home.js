function devOppsHome() {
  return `<div class="devopps-home">
    <section class="devopps-hero" aria-labelledby="devopps-title">
      <button class="motion-toggle" id="devopps-motion" type="button" aria-pressed="false"><span aria-hidden="true">Ⅱ</span>Motion on</button>
      <h1 class="devopps-title" id="devopps-title" aria-label="Dev Oops!">${Array.from("Dev Oops!").map(letter => letter === " " ? '<span class="devopps-title-space" aria-hidden="true"></span>' : `<span class="devopps-title-char" aria-hidden="true"><span class="devopps-title-glyph">${letter}</span></span>`).join("")}</h1>
      <p class="lead">A year of practical engineering, built around one service and the evidence that you can run it well.</p>
      <p class="devopps-access-note">Free to learn. No account needed to browse or practice.</p>
    </section>
    ${devOppsMap()}
    <div class="actions devopps-primary-actions"><a class="btn" href="#week-${nextWeek()}">Continue with week ${nextWeek()} <span>↗</span></a><a class="btn secondary" href="#read-lab-setup">Set up your learning lab</a></div>
    <nav class="devopps-learning-links" aria-label="Learning approach"><a href="#read-free-learning">Follow the free learning path</a><a href="#read-senior-practice">Practice senior engineering habits</a></nav>
    <div class="stats"><div class="stat"><strong>52</strong><span>weeks of deliberate practice</span></div><div class="stat"><strong>728</strong><span>scheduled learning hours</span></div><div class="stat"><strong>13</strong><span>competency gates</span></div><div class="stat"><strong>40</strong><span>repositories reviewed</span></div></div>
    ${devOppsJourney()}
    <section class="devopps-endmatter" aria-labelledby="practice-title">
      <div class="devopps-endmatter-heading">
        <div><div class="eyebrow">From familiarity to responsibility</div><h2 id="practice-title">Learn to build.<br>Learn to operate.</h2></div>
        <div class="stamp"><div class="eyebrow">Your daily practice</div><div class="big">2h</div><p>Small, consistent sessions.<br>Increasing responsibility.</p><div class="rule"></div><div class="eyebrow">The standard</div><p>Build · diagnose · recover<br>Explain · verify · hand off</p></div>
      </div>
      <div class="note"><strong>Built for your starting point.</strong> Start with a guided Linux lab, even if the terminal is new to you. Each week explains the concepts, walks through the commands, then helps you diagnose a controlled failure. Build evidence at your own pace; cloud labs are separated from local practice.</div>
      <div class="section-line"><h2>One service. A deeper understanding.</h2></div><p class="lead" style="font-size:14px">Taskboard starts as a small API. You will test it, package it, deliver it through GitLab, run it on AWS and Kubernetes, transfer the ideas to GCP, then measure and recover it.</p>
      <div class="flow"><span>Code + tests</span><b>→</b><span>Image + pipeline</span><b>→</b><span>Infrastructure</span><b>→</b><span>Operate + recover</span></div>
      <p class="caption">The curriculum builds progressively. A passed lab demonstrates a specific capability; it does not guarantee production reliability or seniority.</p>
      <div class="actions"><a class="btn secondary" href="downloads/dev-opps-labs.zip" download>Download the lab files</a><a class="btn secondary" href="#read-assessment-and-operations">How you will prove progress</a><a class="btn secondary" href="#read-resource-strategy">How to use the sources</a></div>
    </section>
  </div>`;
}

/* An original, dependency-free interpretation of Elastic Text's interaction:
   widen letters near the pointer and compress their neighbours to hold the line.
   The title remains readable without JavaScript, and its accessible name is plain text. */
function devOopsElasticTitle(title, paused) {
  const slots = [...title.children];
  const letters = slots.map(slot => ({slot, glyph: slot.firstElementChild, width: 0, scale: 1, velocity: 0}));
  const controller = new AbortController();
  const signal = controller.signal;
  const touch = matchMedia("(hover: none)");
  let frame = 0, previousTime = 0, naturalWidth = 1, fit = 1, visible = true;
  let pointer = null, fontSize = 1, disposed = false;

  const draw = () => {
    const stretched = letters.reduce((sum, letter) => sum + letter.width * letter.scale, 0);
    const normalize = naturalWidth / stretched;
    for (const letter of letters) {
      const scale = letter.scale * normalize * fit;
      letter.slot.style.width = `${letter.width * scale}px`;
      if (letter.glyph) {
        letter.glyph.style.transform = `scaleX(${scale})`;
        letter.glyph.style.webkitTextStrokeWidth = `${fontSize * (.045 + Math.max(0, letter.scale - 1) * .027)}px`;
      }
    }
  };
  const animate = time => {
    frame = 0;
    if (disposed || paused || !visible || document.hidden) return;
    const step = Math.min((time - (previousTime || time - 16.67)) / 16.67, 2);
    previousTime = time;
    const width = naturalWidth * fit;
    const wave = touch.matches && pointer === null;
    const focus = pointer ?? (wave ? (.5 + Math.sin(time / 1150) * .62) * width : null);
    let position = 0, unsettled = false;
    for (const letter of letters) {
      const center = position + letter.width * fit / 2;
      const distance = focus === null ? Infinity : (center - focus) / (width * .21);
      const target = letter.glyph ? 1 + .9 * Math.exp(-distance * distance) : 1;
      letter.velocity = (letter.velocity + (target - letter.scale) * .13 * step) * Math.pow(.68, step);
      letter.scale += letter.velocity * step;
      if (Math.abs(target - letter.scale) > .0005 || Math.abs(letter.velocity) > .0005) unsettled = true;
      else { letter.scale = target; letter.velocity = 0; }
      position += letter.width * fit;
    }
    draw();
    if (wave || unsettled) frame = requestAnimationFrame(animate);
  };
  const wake = () => {
    if (!paused && visible && !document.hidden && !frame && !disposed) {
      previousTime = 0;
      frame = requestAnimationFrame(animate);
    }
  };
  const measure = () => {
    if (disposed || !title.isConnected) return;
    for (const letter of letters) {
      letter.slot.style.width = "";
      if (letter.glyph) letter.glyph.style.transform = "";
    }
    fontSize = parseFloat(getComputedStyle(title).fontSize);
    letters.forEach(letter => { letter.width = letter.slot.getBoundingClientRect().width; });
    naturalWidth = letters.reduce((sum, letter) => sum + letter.width, 0) || 1;
    fit = Math.min(1, title.clientWidth * .97 / naturalWidth);
    draw();
    wake();
  };
  const trackPointer = event => {
    const bounds = title.getBoundingClientRect();
    pointer = event.clientX - bounds.left - (bounds.width - naturalWidth * fit) / 2;
    wake();
  };
  const release = () => { pointer = null; wake(); };
  if (!paused) {
    title.addEventListener("pointermove", trackPointer, {signal, passive: true});
    title.addEventListener("pointerdown", trackPointer, {signal, passive: true});
    title.addEventListener("pointerleave", release, {signal});
    title.addEventListener("pointercancel", release, {signal});
    title.addEventListener("pointerup", event => { if (event.pointerType !== "mouse") release(); }, {signal});
  }
  const resize = new ResizeObserver(measure);
  // Observe the frame, whose size does not change when the letters stretch.
  resize.observe(title.parentElement);
  const intersection = new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    if (visible) wake();
    else { cancelAnimationFrame(frame); frame = 0; }
  });
  intersection.observe(title);
  document.fonts?.ready.then(measure);
  measure();
  return () => {
    disposed = true;
    cancelAnimationFrame(frame);
    controller.abort();
    resize.disconnect();
    intersection.disconnect();
  };
}

/* Rebind visual effects only when the original app replaces the page. */
(() => {
  const media = window.matchMedia("(prefers-reduced-motion: reduce)");
  const motionKey = "dev-opps-motion";
  let stored = null;
  try { stored = localStorage.getItem(motionKey); } catch (_) {}
  let paused = stored ? stored === "paused" : media.matches;
  let disposeTitle = () => {};
  const stop = () => { disposeTitle(); disposeTitle = () => {}; };
  const start = () => {
    stop();
    document.documentElement.dataset.motion = paused ? "paused" : "running";
    document.querySelectorAll('.journey-mascot-button img').forEach(img => {
      img.src = img.getAttribute("src").replace(/(?:-static)?\.svg$/, paused ? "-static.svg" : ".svg");
      const source = img.closest("picture")?.querySelector("source");
      if (source) source.media = paused ? "all" : "not all";
    });
    const title = document.getElementById("devopps-title");
    const toggle = document.getElementById("devopps-motion");
    if (!title || !toggle) return;
    toggle.setAttribute("aria-pressed", String(paused));
    toggle.setAttribute("aria-label", paused ? "Turn animations on" : "Pause animations");
    toggle.innerHTML = `<span aria-hidden="true">${paused ? "▷" : "Ⅱ"}</span>Motion ${paused ? "off" : "on"}`;
    toggle.onclick = () => {
      paused = !paused;
      try { localStorage.setItem(motionKey, paused ? "paused" : "running"); } catch (_) {}
      start();
    };
    disposeTitle = devOopsElasticTitle(title, paused);
  };
  new MutationObserver(start).observe(document.getElementById("app"), {childList:true});
  media.addEventListener("change", event => {
    let preference = null;
    try { preference = localStorage.getItem(motionKey); } catch (_) {}
    if (!preference) paused = event.matches;
    start();
  });
  document.addEventListener("visibilitychange", () => document.hidden ? stop() : start());
  document.addEventListener("click", event => {
    const menu = document.querySelector(".nav-library");
    if (menu && (!menu.contains(event.target) || event.target.closest("a"))) menu.open = false;
  });
  document.addEventListener("keydown", event => {
    if (event.key !== "Escape") return;
    const menu = document.querySelector(".nav-library[open]");
    if (menu) {
      menu.open = false;
      menu.querySelector("summary").focus();
    }
  });
})();
