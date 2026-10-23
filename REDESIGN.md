# Dev Opps — design and teaching update

The current visual identity is preserved: animated Dev Opps title, clickable isometric map, 13 distinct mascot journeys, squiggly connections, outcome previews and responsive layouts. Mascot connectors begin outside the eye area, previews avoid overlapping labels, and the watch-montage links are removed. Existing exported montage files remain available in the asset archive.

The teaching expansion adds 52 guided lessons and 13 capstones without replacing the original 52-week sequence. Each lesson includes concepts, explained commands, expected results, controlled failure diagnosis, expandable hints and recovery, independent practice, recall questions, cleanup and source references. All 40 reviewed repositories have original explanations and exercises inside matching lessons and catalog entries.

The pre-redesign interface is retained locally in `redesign-backup/`. The version immediately before teaching expansion is retained in `teaching-backup/`. These author backups are excluded from publication. The former payload hash in earlier notes refers to the historical design-only revision, not the expanded edition.

Progress retains the original `devops-fieldbook-progress-v1` storage key and schema. Browser/origin changes still require exporting and importing progress. The website does not execute learner commands or create cloud resources.

Rebuild with `python tools/build_fieldbook.py`. Current presentation sources are in `redesign-source/`; the guided renderer is in `teaching/lesson-view.js` and `.css`; each authored week is in `teaching/lessons`. The former `prepare_redesign.py` entry point now invokes the current builder, so it cannot reset the teaching expansion to an older baseline.

## Asset provenance

Mascots were exported using the user-requested [Bloub interface](https://bloub.vercel.app/). The asset manifest records the native source and presentation variants. Animated SVG and static reduced-motion versions are served locally. No image generation was used for this teaching update.

The title follows the supplied [animated typography reference](https://animated-colour-typo-componente.framer.website/). Amarna's upstream font license is included as `assets/Amarna-OFL.txt`; its project is [Amarna](https://github.com/ijvanl/Amarna). Source badges follow the supplied [GitHub Stars Badge reference](https://www.framer.com/marketplace/components/github-stars-badge/) with source-specific icons and no invented star counts.

See `VALIDATION.md` for current checks and their execution limits.
