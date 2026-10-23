/* Diagram geometry observed from the supplied MotherDuck reference with REA.
   Labels and destinations connect to the existing Dev Opps curriculum. */
function devOppsMap() {
  const slabPaths = [
    'M121.796 4.07608C132.75 -0.0253605 144.835 -0.0253605 155.79 4.07608L271.392 47.3574C274.824 48.6425 276.555 51.6792 276.586 54.7313C276.586 54.7852 276.586 54.8391 276.586 54.893C276.556 57.9451 274.824 60.9818 271.392 62.2669L155.79 105.548C144.835 109.65 132.75 109.65 121.796 105.548L6.19351 62.2669C2.96542 61.0583 1.24254 58.3003 1.02384 55.4374C0.773368 52.1584 2.49626 48.7417 6.19351 47.3574L121.796 4.07608Z',
    'M271.392 62.2669L155.79 105.548C144.835 109.65 132.75 109.65 121.796 105.548L6.19351 62.2669C2.96542 61.0583 1.24254 58.3003 1.02384 55.4374V94.6482C1.24467 97.5088 2.96789 100.263 6.19351 101.471L121.796 144.753C132.75 148.854 144.835 148.854 155.79 144.753L271.392 101.471C274.823 100.186 276.554 97.1512 276.586 94.1001V54.893C276.556 57.9451 274.824 60.9818 271.392 62.2669Z',
    'M276.586 54.893C276.555 57.9451 274.824 60.9818 271.392 62.2669L155.79 105.548C144.835 109.65 132.75 109.65 121.796 105.548L6.19351 62.2669C2.96542 61.0583 1.24254 58.3003 1.02384 55.4374C0.773368 52.1584 2.49626 48.7417 6.19351 47.3574L121.796 4.07608C132.75 -0.0253604 144.835 -0.0253604 155.79 4.07608L271.392 47.3574C274.824 48.6425 276.555 51.6792 276.586 54.7313M276.586 54.7313V54.893M276.586 54.7313C276.586 54.7852 276.586 54.8391 276.586 54.893M1.02384 55.4374V94.6482C1.24467 97.5088 2.96789 100.263 6.19351 101.471L121.796 144.752C132.75 148.854 144.835 148.854 155.79 144.752L271.392 101.471C274.823 100.186 276.554 97.1512 276.586 94.1001V54.893'
  ];
  const slab = (id, week, left, right, hint, x, y, yellow = false) => `
    <a class="map-slab map-slab-${id}${yellow ? ' map-slab-yellow' : ''}" href="#week-${week}" aria-label="${left} ${right}: ${hint}. Open week ${week}" style="--map-x:${x / 12.6}%;--map-y:${y / 6.4}%">
      <svg viewBox="0 0 278 149" aria-hidden="true" focusable="false">
        <path class="map-slab-top" d="${slabPaths[0]}"/>
        <path class="map-slab-side" d="${slabPaths[1]}"/>
        <path class="map-slab-edge" d="${slabPaths[2]}"/>
      </svg>
      <span class="map-slab-word map-slab-left">${left}</span><span class="map-slab-word map-slab-right">${right}</span>
      <span class="map-slab-hint">${hint}<b>Open week ${String(week).padStart(2, '0')} ↗</b></span>
    </a>`;
  const row = (week, icon, label, color = '') => `<a class="map-small-link ${color}" href="#week-${week}"><span class="map-row-icon" aria-hidden="true">${icon}</span><span>${label}</span><span class="map-row-arrow" aria-hidden="true">↗</span></a>`;
  return `
    <section class="devopps-map" aria-labelledby="devopps-map-title">
      <div class="map-heading"><h2 id="devopps-map-title">Everything is connected.</h2><p>One project. Every moving part. Pick a component to jump into its level.</p></div>
      <div class="map-canvas">
        <svg class="map-connections" viewBox="0 0 1260 640" aria-hidden="true" focusable="false">
          <g fill="none" stroke="#383838" stroke-width="2">
            <path d="M237.983 275.252C336.303 265.05 373.698 366.321 482.496 366.321"/>
            <path class="map-yellow-wire" d="M238.945 178.972C302.142 171.03 373.726 266.12 483.152 256.468"/>
            <path d="M275.234 107.258C264.551 145.721 309.425 133.968 344.546 161.714"/>
            <path d="M895.994 159.224C920.813 131.567 988.355 135.917 997.449 100.449"/>
            <path class="map-yellow-wire" d="M754.972 258.431C802.504 267.706 892.632 200.973 942.485 213.726"/>
            <path d="M737.198 358.23C842.305 348.996 873.211 440.346 924.381 452.165"/>
            <path d="M397 476C412.294 464.181 449.272 476.059 482.152 464.24"/>
          </g>
        </svg>
        <div class="map-stack" aria-label="The DevOps project stack">
          ${slab('cloud', 13, 'CLOUD', 'FOUNDATIONS', 'Build the infrastructure your applications run on', 481.72, 389.3)}
          ${slab('runtime', 25, 'RUNTIME', 'KUBERNETES', 'Deploy and operate containerized workloads', 481.72, 282.47)}
          ${slab('automation', 17, 'INFRA', 'AUTOMATION', 'Make infrastructure repeatable with code', 481.72, 175.64, true)}
          ${slab('code', 1, 'CODE', '& TESTS', 'Start with Linux, networking, Git and scripting', 339.88, 88.81)}
          ${slab('delivery', 9, 'BUILD', '& DELIVER', 'Turn source code into a tested delivery pipeline', 624.54, 88.81)}
        </div>
        <section class="map-panel map-tools" aria-label="Tools and languages">
          <h3>Tools &amp; languages</h3>
          <div class="map-tool-grid">
            <a href="#week-1" aria-label="Git foundations, week 1"><span class="map-tool-git" aria-hidden="true"><svg viewBox="0 0 36 36" focusable="false"><rect x="5" y="5" width="26" height="26" rx="3" fill="#ef6044" transform="rotate(45 18 18)"/><path d="M13 9v15m0-11 11 11" fill="none" stroke="#fff" stroke-width="2.5"/><g fill="#fff"><circle cx="13" cy="11" r="2.6"/><circle cx="13" cy="25" r="2.6"/><circle cx="24" cy="24" r="2.6"/></g></svg></span><span>Git</span></a>
            <a href="#week-1" aria-label="Python and scripting foundations, week 1"><span class="map-tool-python" aria-hidden="true"><svg viewBox="0 0 36 36" focusable="false"><path d="M18 2C8 2 9 6 9 10h10v2H6C0 12 0 27 7 27h3v-7c0-3 3-5 6-5h11V8c0-4-4-6-9-6Z" fill="#3776ab"/><path d="M18 34c10 0 9-4 9-8H17v-2h13c6 0 6-15-1-15h-3v7c0 3-3 5-6 5H9v7c0 4 4 6 9 6Z" fill="#ffd343"/><circle cx="14" cy="7" r="1.7" fill="#fff"/><circle cx="22" cy="29" r="1.7" fill="#fff"/></svg></span><span>Python</span></a>
            <a href="#week-1" aria-label="Bash and Linux foundations, week 1"><span class="map-tool-bash" aria-hidden="true">&gt;_</span><span>Bash</span></a>
            <a href="#week-5" aria-label="Containers, week 5"><span class="map-tool-docker" aria-hidden="true"><svg viewBox="0 0 38 36" focusable="false"><g fill="#229ad5"><path d="M2 19h27c2-3 4-4 7-2-1 3-3 4-6 4-3 9-10 12-19 10C5 30 2 25 2 19Z"/><path d="M29 18c-2-4-1-7 1-9 3 3 3 6 2 9Z"/><path d="M7 13h5v5H7zm6 0h5v5h-5zm6 0h5v5h-5zM13 7h5v5h-5zm6 0h5v5h-5zM19 1h5v5h-5z"/></g><circle cx="8" cy="23" r="1" fill="#fff"/></svg></span><span>Docker</span></a>
            <a href="#week-9" aria-label="Continuous integration and delivery, week 9"><span class="map-tool-ci" aria-hidden="true"><svg viewBox="0 0 36 36" focusable="false"><path d="M9 10v16m0-8h11c5 0 7-3 7-7" fill="none" stroke="#705497" stroke-width="3"/><g fill="#fff" stroke="#705497" stroke-width="3"><circle cx="9" cy="7" r="4"/><circle cx="9" cy="29" r="4"/><circle cx="27" cy="7" r="4"/></g></svg></span><span>CI/CD</span></a>
          </div>
        </section>
        <a class="map-panel map-note map-containers" href="#week-5">
          <span class="map-note-icon" aria-hidden="true">▱</span>
          <div><h3>Containers</h3><p>Package an application.<br>Run it anywhere.</p><span class="map-note-cta">Open level 02 →</span></div>
        </a>
        <a class="map-panel map-note map-delivery map-note-yellow" href="#week-9">
          <span class="map-note-icon" aria-hidden="true">⚑</span>
          <div><h3>CI/CD pipelines</h3><p>From a Git commit to<br>a repeatable release.</p><span class="map-note-cta">Open level 03 →</span></div>
        </a>
        <section class="map-panel map-cloud" aria-label="Infrastructure and cloud">
          <h3>Infrastructure</h3>
          <div class="map-small-links">
            ${row(17, '◈', 'Terraform')}
            ${row(21, 'Ⓐ', 'Ansible')}
            ${row(13, '☁', 'AWS foundations')}
            ${row(37, '◇', 'GCP & networking')}
          </div>
        </section>
        <section class="map-panel map-interfaces" aria-label="Kubernetes interfaces">
          <h3><span class="map-kube-icon" aria-hidden="true">⎈</span> Kubernetes</h3>
          <div class="map-interface-links">
            <a href="#week-25">kubectl</a><a href="#week-25">Deploy</a><a href="#week-29">Operate</a>
          </div>
        </section>
        <a class="map-panel map-note map-reliability map-note-yellow" href="#week-33">
          <span class="map-note-icon" aria-hidden="true">▤</span>
          <div><h3>Observability &amp; SRE</h3><p>See what is happening.<br>Keep your systems reliable.</p><span class="map-note-cta">Open level 09 →</span></div>
        </a>
        <section class="map-panel map-operate" aria-label="Operate and scale">
          <h3>Operate. Secure. Scale.</h3><p class="map-panel-caption">Bring every layer together.</p>
          <div class="map-operation-links">
            ${row(29, '⎈', 'Kubernetes operations', 'map-row-sky')}
            ${row(33, '◉', 'Observability & SRE', 'map-row-mint')}
            ${row(41, '⌾', 'Security', 'map-row-pink')}
            ${row(45, '⚙', 'Platform engineering', 'map-row-sky')}
            ${row(49, '⚑', 'Capstone project', 'map-row-yellow')}
          </div>
        </section>
      </div>
      <p class="map-footnote"><span aria-hidden="true">↗</span> Every component is a shortcut. Follow the full journey below.</p>
    </section>`;
}
