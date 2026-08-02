(()=>{'use strict';
const css=document.createElement('link');css.rel='stylesheet';css.href='./fixes.css?v=2.0.1';document.head.appendChild(css);
const section=document.querySelector('.video-section');
if(section){
  const kicker=section.querySelector('.kicker');if(kicker)kicker.textContent='VÍDEO EDUCATIVO';
  const title=section.querySelector('.section-head h2');if(title)title.textContent='Mindfulness e atenção plena: uma introdução da TV UFMG';
  const intro=section.querySelector('.section-head p:last-child');if(intro)intro.textContent='Use este conteúdo quando houver estabilidade suficiente para assistir com atenção. No pico de uma crise, prefira as habilidades curtas da área “Agora”.';
  const frame=section.querySelector('iframe');if(frame){frame.src='https://www.youtube-nocookie.com/embed/grrlRy34MRg';frame.title='Projeto Práticas Meditativas da FALE UFMG oferece sessões on-line de mindfulness — TV UFMG';}
  const note=section.querySelector('.source-note');
  if(note){
    note.textContent='Conteúdo externo: TV UFMG · Projeto Práticas Meditativas da Faculdade de Letras da UFMG.';
    if(!section.querySelector('.video-meta')){
      const meta=document.createElement('div');meta.className='video-meta';
      note.parentNode.insertBefore(meta,note);meta.appendChild(note);
      const a=document.createElement('a');a.className='btn subtle video-fallback';a.href='https://www.youtube.com/watch?v=grrlRy34MRg';a.target='_blank';a.rel='noopener noreferrer';a.textContent='Abrir vídeo no YouTube';meta.appendChild(a);
    }
  }
}
const install=document.getElementById('installBtn');if(install&&install.parentElement)install.parentElement.classList.add('install-row');
const core=document.createElement('script');core.src='./app-core.js?v=2.0.1';core.async=false;document.head.appendChild(core);
})();
