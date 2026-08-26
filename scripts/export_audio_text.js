const fs=require('fs');
const vm=require('vm');
const path=require('path');
const root=path.resolve(__dirname,'..');
const src=fs.readFileSync(path.join(root,'app-core.js'),'utf8');
const start=src.indexOf('const P=[');
const marker='].map(x=>({id:x[0]';
const end=src.indexOf(marker,start);
if(start<0||end<0)throw new Error('Bloco de práticas não localizado.');
const arraySrc=src.slice(start+'const P='.length,end+1);
const rows=vm.runInNewContext('('+arraySrc+')',Object.create(null),{timeout:1000});
const practices=rows.map(x=>({
  id:x[0],title:x[1],framework:x[2],label:x[3],duration:x[4],intro:x[5],steps:x[6],safety:x[7]
}));
if(practices.length!==12)throw new Error(`Esperadas 12 práticas; encontradas ${practices.length}`);
const payload={
  practices,
  complete:'Prática concluída. Observe a intensidade e sua margem de escolha agora.'
};
const out=process.argv[2]||'/tmp/regulacao-audio.json';
fs.writeFileSync(out,JSON.stringify(payload,null,2));
console.log(`Exportadas ${practices.length} práticas para ${out}`);
