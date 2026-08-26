(()=>{'use strict';
const VERSION='n2-20260825';
let manifest=null;
let player=null;
let currentKey='';
function ensurePlayer(){
  if(player)return player;
  player=new Audio();
  player.preload='auto';
  player.addEventListener('error',()=>showUnavailable());
  return player;
}
function showUnavailable(){
  const step=document.getElementById('guideStep');
  if(!step)return;
  const dialog=step.closest('dialog');
  let note=dialog?.querySelector('.audio-n2-status');
  if(!note&&dialog){note=document.createElement('small');note.className='audio-n2-status';note.setAttribute('role','status');step.insertAdjacentElement('afterend',note)}
  if(note)note.textContent='Áudio temporariamente indisponível.';
}
function clearStatus(){document.querySelectorAll('.audio-n2-status').forEach(x=>x.remove())}
async function loadManifest(){
  try{
    const r=await fetch(`./audio/n2/manifest.json?v=${VERSION}`,{cache:'no-store'});
    if(!r.ok)throw new Error(String(r.status));
    manifest=await r.json();
  }catch(e){manifest=null}
}
loadManifest();
function playSrc(src,key){
  if(!src){showUnavailable();return}
  clearStatus();
  const a=ensurePlayer();
  if(currentKey!==key){a.pause();a.currentTime=0;a.src=src;currentKey=key}
  a.play().catch(()=>showUnavailable());
}
function play(practiceId,stepIndex,text=''){
  if(!manifest){showUnavailable();loadManifest();return}
  if(/^Prática concluída\./i.test(text)){
    const c=manifest.complete;
    return playSrc(c?.url,'complete');
  }
  const p=manifest.practices?.[practiceId];
  const s=p?.steps?.find(x=>Number(x.index)===Number(stepIndex));
  playSrc(s?.url,`${practiceId}:${stepIndex}`);
}
function stop(){if(player){player.pause();player.currentTime=0}currentKey='';clearStatus()}
window.RC_AUDIO_N2={play,stop,reload:loadManifest,get manifest(){return manifest}};
})();
