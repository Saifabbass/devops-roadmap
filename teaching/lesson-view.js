/* Guided lesson rendering. Course data stays in the embedded, offline payload. */
const lessonParagraphs = values => (Array.isArray(values) ? values : [values]).filter(Boolean).map(value => `<p>${lessonInline(value)}</p>`).join("");
function lessonInline(value){return esc(value).replace(/`([^`]+)`/g,"<code>$1</code>");}
function lessonList(values){return `<ul>${(values||[]).map(x=>`<li>${lessonInline(x)}</li>`).join("")}</ul>`;}
function lessonCommand(command){
 if(!command)return "";
 return `<div class="lesson-command"><div class="lesson-command-top"><span>${esc(command.shell||"Bash · Ubuntu lab")}</span><button type="button" class="command-copy" onclick="copyLessonCommand(this)" aria-label="Copy this command">Copy</button></div><pre><code>${esc(command.code)}</code></pre><div class="command-explanation"><h5>What each part does</h5>${lessonList(command.explain)}<h5>What you should see</h5>${lessonParagraphs(command.expected)}${command.troubleshoot?`<details class="lesson-help"><summary>If your result differs</summary>${lessonParagraphs(command.troubleshoot)}</details>`:""}</div></div>`;
}
async function copyLessonCommand(button){
 const text=button.closest('.lesson-command').querySelector('pre code').textContent;
 try{await navigator.clipboard.writeText(text);button.textContent="Copied";setTimeout(()=>button.textContent="Copy",1800);}
 catch(_){const range=document.createRange();range.selectNodeContents(button.closest('.lesson-command').querySelector('pre code'));const selected=window.getSelection();selected.removeAllRanges();selected.addRange(range);button.textContent="Selected — press Ctrl+C";}
}
function lessonAnswer(title,body){return `<details class="lesson-answer"><summary>${esc(title)}<span aria-hidden="true">+</span></summary><div>${body}</div></details>`;}
function scrollLessonSection(id){
 const section=document.getElementById(id);if(!section)return;
 let parent=section.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}
 section.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
}
function lessonSection(id,title,body){return `<section class="lesson-section" id="${id}"><h3>${esc(title)}</h3>${body}</section>`;}
function freePractice(track){
 return `<section class="lesson-section free-practice"><div class="eyebrow">Core route · no cloud bill</div><h3>${esc(track.title)}</h3>${lessonParagraphs(track.objective)}<h4>Before you start</h4>${lessonList(track.prerequisites)}${(track.commands||[]).map(lessonCommand).join("")}<h4>Prove your local practice</h4>${lessonList(track.acceptance)}<p><strong>Keep the claim precise.</strong> ${lessonInline(track.limits)}</p><p><strong>Clean up.</strong> ${lessonInline(track.cleanup)}</p><a href="#read-free-learning">How the free learning route works →</a></section>`;
}
function lessonEvidence(w){
 const r=record(w.week);
 return `<div class="record"><h3>Your evidence record</h3><label for="weekStatus">Current state</label><select id="weekStatus">${statuses.map(s=>`<option${r.status===s?" selected":""}>${s}</option>`).join("")}</select><label for="evidenceNote">Evidence, findings and next action</label><textarea id="evidenceNote" maxlength="20000" placeholder="Record the command you ran, the result, why it matters, and what you still need to investigate.">${esc(r.note)}</textarea><p class="caption">Choose Proved after completing your route’s acceptance checks and explaining the recovery. For local cloud alternatives, label your evidence “local route” and leave provider execution unclaimed. Save links to your own evidence, without credentials or private data.</p><button class="btn small" id="saveWeek">Save progress</button><div class="saved" id="saveMessage" role="status">${r.updated?"Last saved: "+esc(r.updated):""}</div></div><div class="week-footer">${w.week>1?`<a class="btn secondary small" href="#week-${w.week-1}">← Week ${w.week-1}</a>`:"<span></span>"}${w.week<52?`<a class="btn secondary small" href="#week-${w.week+1}">Week ${w.week+1} →</a>`:"<a class='btn secondary small' href='#progress'>Review your year →</a>"}</div>`;
}
function repositoryPattern(pattern, showWeeks=false){
 return `<div class="lesson-repo"><h4>${esc(pattern.title)}</h4><p class="caption">From ${esc(pattern.repo)}</p>${lessonParagraphs(pattern.teaching)}<p><strong>Try the principle.</strong> ${lessonInline(pattern.beginnerExercise)}</p>${lessonAnswer(pattern.question,lessonParagraphs(pattern.answer))}${lessonAnswer("Extend the exercise when the core lesson passes",lessonParagraphs(pattern.extendedExercise)+`<p><strong>Evidence.</strong> ${lessonInline(pattern.expectedEvidence)}</p>`)}<p class="caption"><strong>Apply with care.</strong> ${lessonInline(pattern.doNotCopy)}</p>${showWeeks?`<p class="pattern-weeks">Learn it in ${pattern.weeks.map(n=>`<a href="#week-${n}">Week ${n}</a>`).join(" · ")}</p>`:""}</div>`;
}
function repositoryTeaching(repo){const pattern=(D.repoLessons||[]).find(p=>p.repo===repo);return pattern?repositoryPattern(pattern,true):"";}
function weekBody(w,withRecord=true){
 const lesson=D.lessons?.[w.week];
 if(!lesson)return legacyWeekBody(w,withRecord);
 const prefix=`lesson-${w.week}`;
 const r=record(w.week);
 const commands=items=>(items||[]).map(lessonCommand).join("");
 const failure=lesson.failure;
 const exercise=lesson.exercise;
 const cap=lesson.capstone;
 const free=lesson.freeTrack;
 const patterns=(D.repoLessons||[]).filter(p=>p.weeks.includes(w.week));
 const references=[...lesson.references];
 const seen=new Set(references.map(x=>x.url));
 patterns.forEach(p=>p.primarySources.forEach((source,i)=>{if(!seen.has(source.url)){references.push({url:source.url,title:p.repo+(i?" · inspected source":""),usedFor:p.title+". "+source.scope});seen.add(source.url);}}));
 const referenceLink=(url,title)=>typeof devOppsResourceBadge==="function"?devOppsResourceBadge(url,title):ext(url,title);
 return `<div class="guided-lesson"><div class="eyebrow">Week ${String(w.week).padStart(2,"0")} / ${esc(w.phase)}</div><h2>${esc(w.title)}</h2><p class="outcome">${esc(w.outcome)}</p><div class="tags"><span class="tag">14 hours · work at your pace</span><span class="tag">${esc(r.status)}</span>${cap?'<span class="tag">Level capstone</span>':""}</div>
 <div class="lesson-introduction">${lessonParagraphs(lesson.introduction)}</div>
 ${free?freePractice(free):""}
 ${free?'<details class="lesson-answer"><summary>Prerequisites for the optional provider lab</summary><div>':""}<div class="lesson-prerequisites"><h3>Before you start</h3>${lessonList(lesson.prerequisites)}<a href="#read-lab-setup">Open the in-course setup guide →</a><p class="caption">Read the explanation, predict the result, run the command, then compare the evidence. Commands run in your own lab; this page does not execute them.</p></div>${free?'</div></details>':""}
 <nav class="lesson-toc" aria-label="Sections in this lesson">${[["understand","Understand"],["build","Build"],["failure","Diagnose"],["practice",cap?"Capstone":"Practice"],["questions","Check yourself"],["sources","Sources"]].map(([id,label])=>`<button type="button" onclick="scrollLessonSection('${prefix}-${id}')">${label}</button>`).join("")}</nav>
 ${lessonSection(prefix+"-understand","1. Understand the system",(lesson.concepts||[]).map(c=>`<div class="lesson-concept"><h4>${esc(c.title)}</h4>${lessonParagraphs(c.paragraphs)}${c.example?`<div class="lesson-example"><strong>A concrete example</strong>${lessonParagraphs(c.example)}</div>`:""}${c.judgment?`<p class="lesson-judgment"><strong>The engineering decision.</strong> ${lessonInline(c.judgment)}</p>`:""}</div>`).join(""))}
 ${free?'<details class="lesson-answer optional-cloud"><summary>Optional provider lab · may incur charges</summary><div><p>The free route above is sufficient for core course progress. These provider exercises require your own account and a deliberate budget; skip them for a zero-cost journey.</p>':""}
 ${lessonSection(prefix+"-build","2. Build it, one step at a time",(lesson.steps||[]).map((s,i)=>`<section class="lesson-step"><div class="lesson-step-label">STEP ${String(i+1).padStart(2,"0")}</div><h4>${esc(s.title)}</h4>${lessonParagraphs(s.purpose)}${commands(s.commands)}<p class="lesson-checkpoint"><strong>Stop and check.</strong> ${lessonInline(s.checkpoint)}</p></section>`).join(""))}
 ${lessonSection(prefix+"-failure","3. Break it safely. Explain the evidence.",`<h4>${esc(failure.title)}</h4>${lessonParagraphs(failure.boundary)}<h4>Introduce the fault</h4>${commands(failure.inject)}<h4>Investigate before changing anything</h4>${commands(failure.investigate)}${lessonAnswer("Show a diagnostic hint",lessonList(failure.hints))}${lessonAnswer("Reveal the diagnosis and recovery",lessonParagraphs(failure.answer.explanation)+commands(failure.answer.recover)+"<h4>Prove the recovery</h4>"+lessonCommand(failure.answer.verification))}`)}
 ${lessonSection(prefix+"-practice",cap?"4. Your level capstone":"4. Try it independently",cap?`<h4>${esc(cap.title)}</h4>${lessonParagraphs(cap.scenario)}<p><strong>Starting point.</strong> ${lessonInline(cap.startingPoint)}</p><h4>Your brief</h4>${lessonList(cap.requirements)}<h4>Acceptance checks</h4>${lessonList(cap.acceptance)}${commands(cap.runbook)}${lessonAnswer("Show capstone hints",lessonList(cap.hints))}${lessonAnswer("Review a reference approach",lessonList(cap.solution))}<h4>Assess the evidence</h4><div class="table-wrap"><table><thead><tr><th>Criterion</th><th>Evidence to collect</th><th>Pass condition</th></tr></thead><tbody>${cap.rubric.map(x=>`<tr><td>${esc(x.criterion)}</td><td>${esc(x.evidence)}</td><td>${esc(x.pass)}</td></tr>`).join("")}</tbody></table></div>${cap.stretch?.length?lessonAnswer("Optional extension after the core passes",lessonList(cap.stretch)):""}`:`${lessonParagraphs(exercise.brief)}<h4>Constraints</h4>${lessonList(exercise.constraints)}<h4>What to hand in</h4>${lessonList(exercise.deliverables)}<h4>You have finished when</h4>${lessonList(exercise.acceptance)}${lessonAnswer("Show practice hints",lessonList(exercise.hints))}${lessonAnswer("Review a reference approach",lessonList(exercise.solution))}`)}
 ${free?'</div></details>':""}
 ${lessonSection(prefix+"-questions","5. Explain it without the commands",(lesson.questions||[]).map((q,i)=>`<div class="lesson-question"><h4>${i+1}. ${esc(q.prompt)}</h4>${lessonAnswer("Hint",lessonParagraphs(q.hint))}${lessonAnswer("Reasoned answer",lessonParagraphs(q.answer))}</div>`).join(""))}
 ${free?'<details class="lesson-answer optional-cloud"><summary>Cleanup for the optional provider lab</summary><div>':""}
 ${lessonSection(prefix+"-cleanup","6. Leave the lab in a known state",commands(lesson.cleanup)+`<p><strong>Evidence to keep.</strong> ${esc(w.deliverable)}</p>`)}
 ${free?'</div></details>':""}
 ${patterns.length?lessonSection(prefix+"-repository-patterns","Apply patterns from real projects",patterns.map(p=>repositoryPattern(p)).join("")):""}
 ${lesson.repoConnections?.length?lessonSection(prefix+"-patterns","Patterns from real projects",lesson.repoConnections.map(x=>`<div class="lesson-repo"><h4>${esc(x.repo)}</h4>${lessonParagraphs(x.principle)}${lessonParagraphs(x.application)}</div>`).join("")):""}
 ${lessonSection(prefix+"-sources","Sources and further reading",`<p>You have the core lesson above. These sources document the behavior used here and provide deeper reference.</p><div class="lesson-sources">${references.map(x=>`<div>${referenceLink(x.url,x.title)}<p>${esc(x.usedFor)}</p></div>`).join("")}</div>${lesson.notes?.length?lessonAnswer("Lab validation and limitations",lessonList(lesson.notes)):""}`)}
 ${withRecord?lessonEvidence(w):""}</div>`;
}
