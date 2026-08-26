from __future__ import annotations

import asyncio
import json
import re
import shutil
import sys
from pathlib import Path

import edge_tts
from pydub import AudioSegment, effects

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/regulacao-audio.json')
OUT = ROOT / 'audio/n2'
TMP = ROOT / '.tmp_audio_n2'
VOICE = 'pt-BR-AntonioNeural'
VERSION = 'n2-20260825'
OPENING_SILENCE_MS = 130
ENDING_SILENCE_MS = 240
TARGET_DBFS = -18.0
MAX_TURN_CHARS = 560
MAX_CONCURRENT_SYNTH = 4


def clean(text:str)->str:
    return re.sub(r'\s+',' ',text or '').strip()


def split_turns(text:str)->list[str]:
    text=clean(text)
    sentences=re.findall(r'[^.!?]+[.!?]+|[^.!?]+$',text)
    out=[]; cur=''
    for s in map(clean,sentences):
        if not s: continue
        candidate=f'{cur} {s}'.strip()
        if cur and len(candidate)>MAX_TURN_CHARS:
            out.append(cur);cur=s
        else: cur=candidate
    if cur: out.append(cur)
    return out or [text]


def prosody(text:str,index:int):
    # Todas estas faixas são instruções de regulação: usa o perfil calmo do Sono em Dia.
    rate=-9; pitch=-2
    low=text.lower().strip()
    if text.rstrip().endswith('?'):
        rate+=2; pitch+=2; pause=620
    elif text.rstrip().endswith('!'):
        pause=580
    else:
        pause=620
    if low.startswith(('observe','imagine','pense','agora','por enquanto','guarde')):
        rate-=2
    rate+=(-1,0,1,0)[index%4]
    rate=max(-13,min(2,rate));pitch=max(-4,min(4,pitch))
    return f'{rate:+d}%',f'{pitch:+d}Hz',pause


async def synth(text:str,rate:str,pitch:str,path:Path,sem:asyncio.Semaphore):
    async with sem:
        for attempt in range(1,4):
            try:
                c=edge_tts.Communicate(text=text,voice=VOICE,rate=rate,pitch=pitch,volume='+0%')
                await asyncio.wait_for(c.save(str(path)),timeout=55)
                return
            except Exception:
                if attempt==3: raise
                await asyncio.sleep(.9*attempt)


async def render_text(key:str,text:str,sem:asyncio.Semaphore):
    turns=split_turns(text)
    work=TMP/key; work.mkdir(parents=True,exist_ok=True)
    seq=[];tasks=[]
    for i,turn in enumerate(turns):
        rate,pitch,pause=prosody(turn,i)
        part=work/f'{i:03d}.mp3'
        seq.append((part,0 if i==len(turns)-1 else pause))
        tasks.append(synth(turn,rate,pitch,part,sem))
    await asyncio.gather(*tasks)
    audio=AudioSegment.silent(duration=OPENING_SILENCE_MS)
    for part,pause in seq:
        audio+=AudioSegment.from_file(part,format='mp3')
        if pause: audio+=AudioSegment.silent(duration=pause)
    audio+=AudioSegment.silent(duration=ENDING_SILENCE_MS)
    audio=effects.compress_dynamic_range(audio,threshold=-20.0,ratio=2.0,attack=8.0,release=70.0)
    if audio.dBFS!=float('-inf'): audio=audio.apply_gain(TARGET_DBFS-audio.dBFS)
    if audio.max_dBFS>-1.2: audio=audio.apply_gain(-1.2-audio.max_dBFS)
    target=OUT/f'{key}.mp3'
    audio.export(target,format='mp3',bitrate='128k',parameters=['-ac','1','-ar','44100'])
    return round(len(audio)/1000,1)


async def main():
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    practices=data.get('practices',[])
    if len(practices)!=12: raise RuntimeError(f'Esperadas 12 práticas; recebidas {len(practices)}')
    OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
    sem=asyncio.Semaphore(MAX_CONCURRENT_SYNTH)
    manifest={'version':VERSION,'voice':VOICE,'profile':'Padrão Sonoro Clínico Richelmy Murta — Sono em Dia / Ampulheta N2','practices':{}}
    total=0
    for p in practices:
        entry={'title':p['title'],'steps':[]}
        for i,text in enumerate(p['steps'],start=1):
            key=f"{p['id']}-{i:02d}"
            seconds=await render_text(key,text,sem)
            entry['steps'].append({'index':i-1,'text':text,'url':f'./audio/n2/{key}.mp3?v={VERSION}','duration_seconds':seconds})
            total+=1
        manifest['practices'][p['id']]=entry
    complete_text=clean(data.get('complete','Prática concluída. Observe a intensidade e sua margem de escolha agora.'))
    complete_seconds=await render_text('complete',complete_text,sem)
    manifest['complete']={'text':complete_text,'url':f'./audio/n2/complete.mp3?v={VERSION}','duration_seconds':complete_seconds}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'audio-spec.json').write_text(json.dumps({
        'voice':VOICE,'profile':'Sono em Dia / Ampulheta N2 — calm','opening_silence_ms':OPENING_SILENCE_MS,
        'ending_silence_ms':ENDING_SILENCE_MS,'target_dbfs':TARGET_DBFS,'peak_ceiling_dbfs':-1.2,
        'compression':{'threshold_db':-20.0,'ratio':2.0,'attack_ms':8.0,'release_ms':70.0},
        'format':'MP3 128 kbps, mono, 44.1 kHz','practice_count':len(practices),'step_audio_count':total,'completion_audio_count':1
    },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.rmtree(TMP,ignore_errors=True)
    print(f'Concluído: {len(practices)} práticas, {total} etapas + conclusão.')


if __name__=='__main__': asyncio.run(main())
