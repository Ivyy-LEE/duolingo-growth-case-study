/** Localise the existing seven-slide Chinese case study from one curated source.
 * English deliverables, canonical data and final Tableau assets are read only.
 * Configure CODEX_RUNTIME_DIR / CODEX_PRESENTATION_SKILL on the authoring host.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const RUNTIME=process.env.CODEX_RUNTIME_DIR ?? path.resolve(ROOT,'.local-runtime');
const MODULES=process.env.CODEX_RUNTIME_NODE_MODULES ?? path.join(RUNTIME,'node/node_modules');
const PYTHON=process.env.CODEX_RUNTIME_PYTHON ?? path.join(RUNTIME,'python/bin/python3');
const SKILL=process.env.CODEX_PRESENTATION_SKILL ?? path.resolve(ROOT,'.local-presentation-skill');
process.env.RUNTIME_NODE_MODULES ??= MODULES;
const require=createRequire(path.join(MODULES,'package.json'));
const {createCanvas}=require('@napi-rs/canvas');
const measure=createCanvas(10,10).getContext('2d');
function wrapText(text,width,font,size,bold=false){
 measure.font=`${bold?'bold ':''}${size}px "${font}"`;
 return text.split('\n').map(line=>{
  const words=/[\u3400-\u9fff]/.test(line)?(line.match(/[A-Za-z0-9][A-Za-z0-9/%.:+_-]*|\s+|[^\x00-\x7f]|./g)||[]):line.match(/\S+\s*/g)||[];
  let result=[],current='';
  for(let w of words){if(!current)w=w.trimStart();if(current&&measure.measureText(current+w).width>width&&!/^[，。；：！？、,.）]/.test(w)){result.push(current.trimEnd());current=w.trimStart();}else current+=w;}
  if(current)result.push(current.trimEnd());return result.join('\n');
 }).join('\n');
}
const {FileBlob,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const BUILD=path.join(ROOT,'.build/case-studies');
const OUT=path.join(ROOT,'.build/final-output');
await fs.mkdir(BUILD,{recursive:true});await fs.mkdir(OUT,{recursive:true});
const runId=Date.now().toString(),font='Hiragino Sans GB';
const c=JSON.parse(await fs.readFile(path.join(ROOT,'src/copy_zh_cn.json'),'utf8'));
const links=JSON.parse(await fs.readFile(path.join(ROOT,'docs/portfolio_links.json'),'utf8'));
const publicUrl=links.tableau_public_url;
if(!/^https:\/\/public\.tableau\.com\/views\//.test(publicUrl))throw new Error('Expected the approved Tableau Public URL');
const stable=path.join(ROOT,'case_study/Duolingo_Growth_Operations_Case_Study_CN.pptx');
const source=process.env.CASE_STUDY_TEMPLATE ?? stable;
const pdfStable=path.join(ROOT,'case_study/Duolingo_Growth_Operations_Case_Study_CN.pdf');
const pdfReference=path.join(BUILD,`CN-${runId}-source.pdf`);
await fs.copyFile(pdfStable,pdfReference);
const referenceSha256=createHash('sha256').update(await fs.readFile(source)).digest('hex');
const p=await PresentationFile.importPptx(await FileBlob.load(source));
if(p.slides.items.length!==7)throw new Error('Expected the approved seven-slide template');
const before=await p.inspect({kind:'slide,textbox,shape,image,layout',maxChars:160000});
await fs.writeFile(path.join(BUILD,`CN-${runId}-before.ndjson`),before.ndjson);
const records=before.ndjson.split('\n').filter(Boolean).map(s=>JSON.parse(s));
function record(slide,name){const r=records.find(r=>r.slideIndex===slide&&r.name===name&&r.id?.startsWith('sh/'));if(!r)throw new Error(`Missing ${slide} ${name}`);return r;}
function target(slide,name){return p.resolve(record(slide,name).id);}
function set(slide,name,text){const t=target(slide,name);t.text=text;return t;}
const frames=new Map(records.filter(r=>r.id?.startsWith('sh/')).map(r=>[r.id,{...r.position}]));
const sizes=new Map();
function fit(slide,name,change){const r=record(slide,name);frames.set(r.id,{...r.position,...change});}
function size(slide,name,value){sizes.set(record(slide,name).id,value);}
// Keep the two approved dashboard slides' content, imagery and geometry intact.
for(let si=0;si<7;si++)await fs.writeFile(path.join(BUILD,`CN-source-${si+1}.png`),new Uint8Array(await(await p.slides.items[si].export({format:'png',scale:1})).arrayBuffer()));
set(0,'TextBox 1',c.title);set(0,'TextBox 2',c.labels.slideCover);set(0,'TextBox 4',c.cover);
set(0,'TextBox 6',c.labels.twelveQuarters);set(0,'TextBox 8',c.labels.publicData);set(0,'TextBox 10','Tableau');
set(0,'TextBox 12','2023 Q1–2025 Q4');set(0,'TextBox 14',c.labels.analysisAsOfValue);set(0,'TextBox 15',c.cta.tableau);
fit(0,'TextBox 4',{height:140});size(0,'TextBox 15',16);
set(1,'TextBox 1',c.labels.slideBusiness);set(1,'TextBox 3',c.context);set(1,'TextBox 4',c.labels.businessQuestions);set(1,'TextBox 9',c.labels.method);
c.qs.forEach((t,i)=>set(1,`TextBox ${5+i}`,`${i+1}. ${t}`));
c.scope.forEach((t,i)=>set(1,`TextBox ${10+i}`,t));
fit(1,'TextBox 3',{top:137,height:78});
for(let n=5;n<=8;n++)fit(1,`TextBox ${n}`,{height:63});
for(let n=10;n<=13;n++){fit(1,`TextBox ${n}`,{height:63,width:510});size(1,`TextBox ${n}`,16.5);}
set(4,'TextBox 1',c.labels.slideFindings);
['活跃增长质量','商业化','增长结构','竞争背景'].forEach((t,i)=>set(4,`TextBox ${3+i*3}`,t));
c.findings.forEach((t,i)=>set(4,`TextBox ${4+i*3}`,t));
for(const name of ['Rounded Rectangle 2','Rounded Rectangle 5','Rounded Rectangle 8','Rounded Rectangle 11'])fit(4,name,{height:218});
for(const name of ['TextBox 4','TextBox 7','TextBox 10','TextBox 13'])fit(4,name,{height:128});
set(5,'TextBox 1',c.labels.slideOperations);
c.recs.forEach(([h,b],i)=>{set(5,`TextBox ${4+i*4}`,h);set(5,`TextBox ${5+i*4}`,b);fit(5,`TextBox ${5+i*4}`,{height:212});});
set(6,'TextBox 1',c.labels.slideMethodLimits);set(6,'TextBox 2','分析流程');set(6,'TextBox 7',c.labels.limits);
c.methods.forEach((t,i)=>set(6,`TextBox ${3+i}`,'• '+t));
const slideLimits=[c.limits[0],c.limits[1],c.limits[2]+' '+c.limits[3],c.limits[4]];
slideLimits.forEach((t,i)=>set(6,`TextBox ${8+i}`,'• '+t));
for(let n of [3,4,5,6,8,9,10,11])fit(6,`TextBox ${n}`,{height:62});
set(6,'TextBox 13',c.competitorCaveat+'\n'+c.positioning);fit(6,'TextBox 13',{top:496,height:105});size(6,'TextBox 13',16);
for(const r of records.filter(r=>r.kind==='textbox'&&![2,3].includes(r.slideIndex))){
 const t=p.resolve(r.id),frame=frames.get(r.id),fontsize=sizes.get(r.id)??r.style.fontSize;
 const periodTag=r.slideIndex===0&&r.name==='TextBox 12';
 const value=t.text.toString();t.text=/^0[123]$/.test(value)?value:wrapText(value,frame.width-(periodTag?2:32),font,fontsize,r.style.bold);
 t.text.style={...r.style,typeface:font,fontSize:fontsize,wrap:'none',autoFit:'none',...(periodTag?{insets:0}:{})};t.position=frame;
}
for(const r of records.filter(r=>r.id?.startsWith('sh/')&&r.kind!=='textbox'&&![2,3].includes(r.slideIndex)))p.resolve(r.id).position=frames.get(r.id);
function textShape(slide,name,text,frame,style){
 const s=p.slides.items[slide].shapes.items.find(x=>x.name===name)??p.slides.items[slide].shapes.add({geometry:'textbox',name,position:frame,fill:'none',line:{fill:'none',width:0}});
 s.text=wrapText(text,frame.width,font,style.fontSize,style.bold);s.text.style={typeface:font,wrap:'none',autoFit:'none',insets:0,...style};s.position=frame;return s;
}
textShape(0,'Project work',c.role,{left:108,top:491,width:1064,height:46},{fontSize:14,color:'#68737D'});
textShape(5,'Operations introduction',c.operationsIntro,{left:76,top:94,width:1136,height:46},{fontSize:15,color:'#5C6775'});
textShape(6,'Technical disclosure',c.tech,{left:88,top:625,width:1110,height:34},{fontSize:13,color:'#68737D'});
const coverLink=target(0,'TextBox 15');coverLink.text.get(coverLink.text.toString()).link={uri:publicUrl,isExternal:true};
const sourceNotes=await fs.readFile(path.join(ROOT,'docs/methodology.md'),'utf8');
for(let si=0;si<7;si++){
 const slide=p.slides.items[si];
 if(![2,3].includes(si)){
  slide.speakerNotes.text=[c.longSummary,c.role,c.rounding,c.definitions,c.companyDefinition,c.competitorCaveat,c.tech,c.operationsIntro,c.positioning,'Tableau Public: '+publicUrl,sourceNotes].join('\n\n');
  if(si!==0){const f=slide.shapes.items.find(x=>x.name==='Evidence footer');if(f){f.text=c.footer;f.text.style={fontSize:12,typeface:font,color:'#68737D',wrap:'none',autoFit:'none',insets:0};}}
 }
 await fs.writeFile(path.join(BUILD,`CN-after-${si+1}.png`),new Uint8Array(await(await slide.export({format:'png',scale:1})).arrayBuffer()));
 await fs.writeFile(path.join(BUILD,`CN-layout-${si+1}.json`),await(await slide.export({format:'layout'})).text());
}
const after=await p.inspect({kind:'slide,textbox,image,notes',maxChars:180000});await fs.writeFile(path.join(BUILD,`CN-${runId}-after.ndjson`),after.ndjson);
const candidate=path.join(BUILD,`CN-${runId}-candidate.pptx`);await(await PresentationFile.exportPptx(p)).save(candidate);
const final=path.join(OUT,`CN-${runId}-verified.pptx`);
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12191695,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:7,fontPolicy:{basis:'reference',families:[font],referencePath:source,referenceSha256},verifyArtifactToolImport:true,receiptPath:path.join(BUILD,`CN-${runId}.validation.json`)});
await fs.copyFile(final,stable);
const fc=path.join(BUILD,'fonts.conf'),cache=path.join(BUILD,'font-cache');await fs.mkdir(cache,{recursive:true});
await fs.writeFile(fc,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>/System/Library/Fonts</dir><dir>/System/Library/Fonts/Supplemental</dir><cachedir>${cache}</cachedir></fontconfig>`);
const soffice=process.env.CODEX_SOFFICE??path.join(RUNTIME,'bin/override/soffice');
const stage=path.join(OUT,`pdf-${runId}`);await fs.mkdir(stage,{recursive:true});
const convert=spawnSync(soffice,['--headless','--convert-to','pdf','--outdir',stage,stable],{env:{...process.env,FONTCONFIG_FILE:fc},encoding:'utf8'});
if(convert.status!==0)throw new Error(`PDF conversion failed: ${convert.stderr}`);
const pdf=path.join(stage,path.basename(pdfStable));await fs.access(pdf);
const link=spawnSync(PYTHON,[path.join(ROOT,'src/finalize_case_study_links.py'),'pdf',pdf,'--links',path.join(ROOT,'docs/portfolio_links.json')],{encoding:'utf8'});if(link.status!==0)throw new Error(link.stderr||link.stdout);
// The two dashboard pages have no localised prose changes. Preserve their
// approved PDF page objects to avoid a renderer changing the frozen visuals.
const keep=spawnSync(PYTHON,[path.join(ROOT,'src/preserve_dashboard_pdf_pages.py'),pdfReference,pdf],{encoding:'utf8'});if(keep.status!==0)throw new Error(keep.stderr||keep.stdout);
await fs.copyFile(pdf,pdfStable);
const web=spawnSync(PYTHON,[path.join(ROOT,'src/build_public_pages.py')],{encoding:'utf8'});if(web.status!==0)throw new Error(web.stderr||web.stdout);
const readme=spawnSync(PYTHON,[path.join(ROOT,'src/build_chinese_readme.py')],{encoding:'utf8'});if(readme.status!==0)throw new Error(readme.stderr||readme.stdout);
console.log('Chinese PDF / editable PPTX / web regenerated from src/copy_zh_cn.json. English deliverables and Tableau assets untouched.');
