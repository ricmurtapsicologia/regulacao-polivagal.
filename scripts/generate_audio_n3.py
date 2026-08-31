from __future__ import annotations

import asyncio, hashlib, json, re, shutil, sys
from pathlib import Path
import edge_tts
from pydub import AudioSegment, effects

ROOT=Path(__file__).resolve().parents[1];SOURCE=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/regulacao-audio.json')
OUT=ROOT/'audio/n3';TMP=ROOT/'.tmp_audio_n3';VOICE='pt-BR-AntonioNeural';VERSION='n3-20260831';TARGET=-18.0
SOFT={'mas','porém','porem','contudo','entretanto','porque','quando','enquanto','então','entao','assim','agora','portanto','se','como','além','alem','ainda','depois','antes','embora'}
INSTR=('observe','imagine','pense','respire','inspire','expire','exale','perceba','note','sinta','coloque','apoie','mantenha','deixe','permita','guarde','faça','faca','tente','olhe','escute','volte','pressione','una','mova','gire','segure','nomeie','identifique','pergunte','escolha','repita','solte')
REFL=('por enquanto','agora','às vezes','as vezes','vale lembrar','repare','considere','uma urgência','uma urgencia','o que importa','qual é','qual e')
PRON={r'\bTCC-I\b':'T C C I',r'\bTCC\b':'T C C',r'\bRPD\b':'R P D',r'\bPSP\b':'P S P',r'\bATS\b':'A T S',r'\bCBMMG\b':'C B M M G',r'\bOMS\b':'O M S',r'\bACT\b':'A C T'}

def norm(t):return re.sub(r'\s+',' ',t or '').strip()
def tok(t):return re.findall(r'[\wÀ-ÿ]+',t.lower(),flags=re.UNICODE)
def speakable(t):
 out=t
 for pat,repl in PRON.items():out=re.sub(pat,repl,out,flags=re.I)
 return norm(out)
def stable(t,lo,hi,s):
 h=hashlib.sha256((s+'|'+norm(t)).encode()).digest();u=int.from_bytes(h[:4],'big')/0xffffffff;return lo+int(round(u*(hi-lo)))
def intent(t):
 x=norm(t);l=x.lower()
 if x.endswith('?'):return 'question'
 if l.startswith(INSTR):return 'instruction'
 if l.startswith(REFL):return 'reflective'
 if x.endswith('!'):return 'emphasis'
 return 'explain'
def units(text):
 text=norm(text);out=[]
 for sent in [s.strip() for s in re.split(r'(?<=[.!?…])\s+',text) if s.strip()]:
  w=sent.split()
  if len(w)<=18:out.append(sent);continue
  start=0
  while len(w)-start>18:
   lo=start+8;hi=min(start+18,len(w));target=min(start+12,hi);cand=[]
   for i in range(lo,hi):
    ww=re.sub(r'^[^\wÀ-ÿ]+|[^\wÀ-ÿ]+$','',w[i].lower())
    if ww in SOFT:cand.append(i)
   cut=min(cand,key=lambda i:abs(i-target)) if cand else target
   u=' '.join(w[start:cut]).strip()
   if u and not u.endswith((',', ';', ':', '.', '?', '!', '…')):u+=','
   out.append(u);start=cut
  if start<len(w):out.append(' '.join(w[start:]).strip())
 if tok(' '.join(out))!=tok(text):raise RuntimeError('Gate lexical N3 falhou')
 return out
def prosody(text):
 i=intent(text);rate=-9+{'explain':0,'question':1,'instruction':-3,'reflective':-3,'emphasis':1}[i];pitch=-2+{'explain':0,'question':2,'instruction':-1,'reflective':-1,'emphasis':1}[i]
 rate+=stable(text,-1,1,'rate');pitch+=stable(text,-1,1,'pitch');ranges={'explain':(700,1100),'question':(1000,1600),'instruction':(1600,3000),'reflective':(1300,2400),'emphasis':(800,1200)};lo,hi=ranges[i]
 return i,f'{max(-14,min(2,rate)):+d}%',f'{max(-5,min(4,pitch)):+d}Hz',stable(text,lo,hi,'pause')
async def synth(text,rate,pitch,path,sem):
 async with sem:
  for attempt in range(1,4):
   try:
    c=edge_tts.Communicate(text=speakable(text),voice=VOICE,rate=rate,pitch=pitch,volume='+0%');await asyncio.wait_for(c.save(str(path)),timeout=55);return
   except Exception:
    if attempt==3:raise
    await asyncio.sleep(.9*attempt)
async def render(key,text,sem):
 turns=units(text);work=TMP/key;work.mkdir(parents=True,exist_ok=True);tasks=[];seq=[];intents=[]
 for i,turn in enumerate(turns):
  it,rate,pitch,pause=prosody(turn);part=work/f'{i:03d}.mp3';seq.append((part,0 if i==len(turns)-1 else pause));tasks.append(synth(turn,rate,pitch,part,sem));intents.append(it)
 await asyncio.gather(*tasks);a=AudioSegment.silent(duration=180)
 for part,pause in seq:
  a+=AudioSegment.from_file(part,format='mp3')
  if pause:a+=AudioSegment.silent(duration=pause)
 a+=AudioSegment.silent(duration=360);a=effects.compress_dynamic_range(a,threshold=-20.0,ratio=2.0,attack=8.0,release=70.0)
 if a.dBFS!=float('-inf'):a=a.apply_gain(TARGET-a.dBFS)
 if a.max_dBFS>-1.2:a=a.apply_gain(-1.2-a.max_dBFS)
 OUT.mkdir(parents=True,exist_ok=True);target=OUT/f'{key}.mp3';a.export(target,format='mp3',bitrate='128k',parameters=['-ac','1','-ar','44100'])
 return round(len(a)/1000,1),sorted(set(intents)),len(turns)
async def main():
 data=json.loads(SOURCE.read_text(encoding='utf-8'));practices=data.get('practices',[])
 if len(practices)!=12:raise RuntimeError(f'Esperadas 12 práticas; recebidas {len(practices)}')
 OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True);sem=asyncio.Semaphore(4)
 manifest={'version':VERSION,'voice':VOICE,'profile':'N3-C experiential — Regulação Polivagal','compatibility_alias':'RC_AUDIO_N2 -> RC_AUDIO_N3','pronunciation_dictionary':True,'practices':{}};total=0
 for p in practices:
  entry={'title':p['title'],'steps':[]}
  for i,text in enumerate(p['steps'],start=1):
   key=f"{p['id']}-{i:02d}";seconds,intents,nturns=await render(key,norm(text),sem);entry['steps'].append({'index':i-1,'text':text,'url':f'./audio/n3/{key}.mp3?v={VERSION}','duration_seconds':seconds,'intents':intents,'turns':nturns});total+=1
  manifest['practices'][p['id']]=entry
 complete=norm(data.get('complete','Prática concluída. Observe a intensidade e sua margem de escolha agora.'));seconds,intents,nturns=await render('complete',complete,sem)
 manifest['complete']={'text':complete,'url':f'./audio/n3/complete.mp3?v={VERSION}','duration_seconds':seconds,'intents':intents,'turns':nturns}
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (OUT/'audio-spec.json').write_text(json.dumps({'version':VERSION,'voice':VOICE,'profile':'N3-C experiential','pronunciation_dictionary':True,'ambient_audio':False,'pause_policy':'linguistic + experiential by semantic intent','target_dbfs':TARGET,'peak_ceiling_dbfs':-1.2,'format':'MP3 128 kbps, mono, 44.1 kHz','practice_count':12,'step_audio_count':total,'completion_audio_count':1},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 shutil.rmtree(TMP,ignore_errors=True);print(f'Concluído: {total} etapas + conclusão em N3 experiencial.')
if __name__=='__main__':asyncio.run(main())
