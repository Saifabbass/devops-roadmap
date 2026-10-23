/* Authentication is loaded only after an explicit request to save across devices. */
let syncRevision=null, syncUser=null, syncBusy=false, syncListenerAdded=false;
function progressSyncPanel(){
 return `<section class="note" aria-labelledby="sync-title"><h3 id="sync-title">Free to learn. Your progress is yours.</h3><p>Every lesson is open. Save in this browser without an account, or export a backup to move it yourself. Cross-device saving asks you to sign in only when you choose it.</p><div class="actions"><button class="btn secondary" id="syncConnect">Save across devices</button><button class="btn secondary" id="syncLoad" hidden>Load cloud backup</button><button class="btn secondary" id="syncSave" hidden>Save cloud backup</button><button class="btn secondary" id="syncSignOut" hidden>Sign out</button></div><p class="caption" id="syncMessage" role="status">Local saving and downloads always remain available.</p></section>`;
}
function syncMessage(message){const el=document.getElementById('syncMessage');if(el)el.textContent=message;}
function updateSyncControls(){
 const active=!!(window.Clerk?.user&&window.Clerk?.session);
 for(const id of ['syncLoad','syncSave','syncSignOut']){const b=document.getElementById(id);if(b){b.hidden=!active;b.disabled=syncBusy;}}
 const b=document.getElementById('syncConnect');if(b){b.hidden=active;b.disabled=syncBusy;}
}
async function syncRequest(method,body){
 const session=window.Clerk?.session,userId=window.Clerk?.user?.id;
 const unchanged=()=>userId&&window.Clerk?.user?.id===userId&&window.Clerk?.session?.id===session?.id;
 try{
  const token=await session?.getToken();
  if(!token||!unchanged())throw Error('Sign in again to use your cloud backup. Your local record is unchanged.');
  const result=await fetch('/api/progress',{method,headers:{Authorization:`Bearer ${token}`,...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,cache:'no-store',signal:AbortSignal.timeout(12000)});
  if(!unchanged())throw Error('The signed-in account changed. Your local record is unchanged; reconnect before using cloud progress.');
  if(result.status===409){syncRevision=null;throw Error('Your cloud backup changed on another device. Export this local record first, then load the newer cloud backup before saving again.');}
  if(!result.ok)throw Error('Cloud saving is unavailable right now. Keep your local record and export a backup.');
  let cloud;try{cloud=await result.json();}catch{throw Error('Cloud saving is not available on this deployment. Your local record is unchanged.');}
  if(!unchanged())throw Error('The signed-in account changed. Your local record is unchanged; reconnect before using cloud progress.');
  if(!cloud||!Number.isSafeInteger(cloud.revision)||cloud.revision<0||(cloud.progress===null?cloud.revision!==0:cloud.revision===0))throw Error('The cloud backup response was invalid. Your local record is unchanged.');
  if(cloud.progress!==null)cloud.progress=validateProgress(cloud.progress);
  return cloud;
 }catch(error){
  // A failed response may follow a committed write. Force a fresh read next time.
  if(method!=='GET'||!unchanged())syncRevision=null;
  if(error.name==='TimeoutError'||error.name==='AbortError'||error instanceof TypeError)throw Error('Cloud saving could not finish. Keep your local record and try again later, or export a backup.');
  throw error;
 }
}
async function connectProgressSync(){
 if(location.protocol==='file:')throw Error('Cross-device saving is available on the website. You can save and export progress here without an account.');
 const response=await fetch('/sync-config.json',{cache:'no-store',signal:AbortSignal.timeout(12000)});
 const config=response.ok?await response.json():{};
 if(!config.enabled){throw Error('Cross-device accounts are not enabled yet. Save in this browser or export a free backup; no sign-up is needed.');}
 if(config.siteOrigin!==undefined){
  let canonical;
  try{canonical=new URL(config.siteOrigin);}catch{throw Error('Cloud saving is not configured. Local progress and backup still work.');}
  if(typeof config.siteOrigin!=='string'||canonical.protocol!=='https:'||canonical.origin!==config.siteOrigin)throw Error('Cloud saving is not configured. Local progress and backup still work.');
  if(location.origin!==canonical.origin){
   syncMessage(`Cloud saving is available at ${canonical.origin}. Your local record stays in this browser. Export a backup here, then import it on the main site to keep your progress. `);
   const link=document.createElement('a');link.href=canonical.origin;link.textContent='Open Dev Oops!';link.target='_blank';link.rel='noopener noreferrer';
   document.getElementById('syncMessage')?.append(link);
   return;
  }
 }
 if(!/^pk_(live|test)_/.test(config.clerkPublishableKey)||!/^([a-z0-9-]+\.)+[a-z]{2,}$/i.test(config.clerkFrontendApi))throw Error('Cloud saving is not configured. Local progress and backup still work.');
 const loadBundle=path=>new Promise((resolve,reject)=>{
   const script=document.createElement('script');script.async=true;script.crossOrigin='anonymous';
   script.src=`https://${config.clerkFrontendApi}/npm/${path}`;
   script.dataset.clerkPublishableKey=config.clerkPublishableKey;
   const timer=setTimeout(()=>{script.remove();reject(Error('Sign-in took too long to load. Keep learning and export a local backup.'));},15000);
   script.onload=()=>{clearTimeout(timer);resolve();};script.onerror=()=>{clearTimeout(timer);script.remove();reject(Error('Sign-in could not load. Keep learning and export a local backup.'));};
   document.head.append(script);
  });
 if(!window.__internal_ClerkUICtor)await loadBundle('@clerk/ui@1/dist/ui.browser.js');
 if(!window.Clerk)await loadBundle('@clerk/clerk-js@6/dist/clerk.browser.js');
 if(!window.Clerk.loaded){
  let timer;try{await Promise.race([window.Clerk.load({ui:{ClerkUI:window.__internal_ClerkUICtor}}),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('Sign-in could not initialize. Keep your local record and try again later.')),15000);})]);}finally{clearTimeout(timer);}
 }
 if(!syncListenerAdded){
  window.Clerk.addListener(({user})=>{if((user?.id||null)!==syncUser){syncRevision=null;syncUser=user?.id||null;}updateSyncControls();});
  syncListenerAdded=true;
 }
 if(!window.Clerk.user){window.Clerk.openSignIn();syncMessage('After signing in, choose Load cloud backup or Save cloud backup. Nothing is uploaded automatically.');}
 else syncMessage('Signed in. Choose whether to load or save your backup.');
 updateSyncControls();
}
function bindProgressSync(){
 const run=action=>async()=>{if(syncBusy)return;syncBusy=true;updateSyncControls();try{await action();}catch(error){syncMessage(error.message);}finally{syncBusy=false;updateSyncControls();}};
 document.getElementById('syncConnect')?.addEventListener('click',run(connectProgressSync));
 document.getElementById('syncLoad')?.addEventListener('click',run(async()=>{
  const cloud=await syncRequest('GET');
  if(!cloud.progress){syncRevision=cloud.revision;syncMessage('No cloud backup yet. Your local record is unchanged. Choose Save cloud backup to create one.');return;}
  const clean=validateProgress(cloud.progress);
  if(Object.keys(progress.weeks).length&&!confirm("Loading replaces this browser's record. Export it first if you want to keep both. Load your cloud backup?"))return;
  progress=clean;save();syncRevision=cloud.revision;render();syncMessage(storageOK?'Cloud backup loaded and saved in this browser.':'Cloud backup loaded, but browser storage is unavailable. Export a backup to retain it.');
 }));
 document.getElementById('syncSave')?.addEventListener('click',run(async()=>{
  if(syncRevision===null){const cloud=await syncRequest('GET');if(cloud.progress&&JSON.stringify(cloud.progress.weeks)!==JSON.stringify(progress.weeks))throw Error('A different cloud backup exists. Export your local record, then load the cloud backup before saving.');syncRevision=cloud.revision;}
  const result=await syncRequest('PUT',{progress:validateProgress(progress),expectedRevision:syncRevision});syncRevision=result.revision;syncMessage('Cloud backup saved successfully. Future edits stay local until you save again.');
 }));
 document.getElementById('syncSignOut')?.addEventListener('click',run(async()=>{await window.Clerk.signOut();syncRevision=null;syncUser=null;syncMessage('Signed out. The local record remains in this browser.');}));
 updateSyncControls();
}
