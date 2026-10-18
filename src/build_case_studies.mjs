/** Focused refresh of the existing seven-slide bilingual case-study template.
 * Canonical CSVs and dashboard assets are read only. No synthetic data or periods.
 * Set CODEX_RUNTIME_NODE_MODULES and CODEX_RUNTIME_PYTHON for another machine.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {spawnSync} from 'node:child_process';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const RUNTIME=process.env.CODEX_RUNTIME_DIR ?? path.resolve(ROOT,'.local-runtime');
const MODULES=process.env.CODEX_RUNTIME_NODE_MODULES ?? path.join(RUNTIME,'node/node_modules');
const PYTHON=process.env.CODEX_RUNTIME_PYTHON ?? path.join(RUNTIME,'python/bin/python3');
const SKILL=process.env.CODEX_PRESENTATION_SKILL ?? path.resolve(ROOT,'.local-presentation-skill');
process.env.RUNTIME_NODE_MODULES ??= MODULES;
const require=createRequire(path.join(MODULES,'package.json'));
const {createCanvas,loadImage}=require('@napi-rs/canvas');
const measure=createCanvas(10,10).getContext('2d');
function wrapText(text,width,font,size,bold=false){
 measure.font=`${bold?'bold ':''}${size}px "${font}"`;
 return text.split('\n').map(line=>{
  const words=/[\u3400-\u9fff]/.test(line)?(line.match(/[A-Za-z0-9][A-Za-z0-9/%.:+_-]*|\s+|[^\x00-\x7f]|./g)||[]):line.match(/\S+\s*/g)||[];
  let result=[],current='';
  for(let w of words){if(!current)w=w.trimStart();if(current&&measure.measureText(current+w).width>width&&!/^[，。；：！？、,.]/.test(w)){result.push(current.trimEnd());current=w.trimStart();}else current+=w;}
  if(current)result.push(current.trimEnd());return result.join('\n');
 }).join('\n');
}
const {FileBlob,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const BUILD=path.join(ROOT,'.build/case-studies');
const OUT=path.join(ROOT,'.build/final-output');
await fs.mkdir(BUILD,{recursive:true});await fs.mkdir(OUT,{recursive:true});
const runId=Date.now().toString();
function attachLinks(format,file){const result=spawnSync(PYTHON,[path.join(ROOT,'src/finalize_case_study_links.py'),format,file,'--links',path.join(ROOT,'docs/portfolio_links.json')],{encoding:'utf8'});if(result.status!==0)throw new Error(result.stderr||result.stdout);console.log(result.stdout.trim());}
const CN='Hiragino Sans GB', EN='Arial';
function csvRows(s){
 let rows=[],r=[],v='',q=false;
 for(let i=0;i<s.length;i++){let c=s[i];if(c==='"'){if(q&&s[i+1]==='"'){v+='"';i++;}else q=!q;}else if(c===','&&!q){r.push(v);v='';}else if(c==='\n'&&!q){r.push(v.replace(/\r$/,''));rows.push(r);r=[];v='';}else v+=c;}
 if(v||r.length){r.push(v.replace(/\r$/,''));rows.push(r);}const heads=rows.shift();return rows.filter(r=>r.length===heads.length).map(r=>Object.fromEntries(heads.map((h,i)=>[h,r[i]])));
}
const manifest=csvRows(await fs.readFile(path.join(ROOT,'docs/source_manifest.csv'),'utf8'));
const corporateSources=manifest.filter(r=>r.dataset==='quarterly_performance').map(r=>`${r.period}: ${r.source_name}\n${r.original_url}`).join('\n\n');
const sourceNotes=`Corporate evidence: official Duolingo IR/SEC disclosures only, Q1 2023-Q4 2025. Analysis as of March 2026. Raw values preserved at disclosed precision; all ratios and growth are transparent calculations.\n\n${corporateSources}\n\nDefinitions/formulas: docs/methodology.md and docs/data_dictionary.md. Corporate source lineage: docs/source_manifest.csv. Competitor website snapshot: February 2026; social snapshot: March 2026. Inherited historical coursework values; original dated captures are absent and historical provenance cannot be independently verified. These are contextual snapshots, not a longitudinal dataset, market share, conversion or retention evidence. No current observations replace these dates.`;
const portfolioLinks=JSON.parse(await fs.readFile(path.join(ROOT,'docs/portfolio_links.json'),'utf8'));
const publicUrl=portfolioLinks.tableau_public_url;
const displayPublicUrl=portfolioLinks.tableau_public_display_url ?? publicUrl?.split('?')[0];
if(publicUrl && !/^https:\/\/public\.tableau\.com\//.test(publicUrl))throw new Error('Expected a Tableau Public URL');
const copy={
 en:{
  cover:"As Duolingo's audience grew, did engagement and monetisation strengthen too? Across 2023-2025, daily activity and monetisation grew faster than MAU. This case translates that pattern into priorities for product, user and growth operations.",
  context:'Audience growth alone gives an incomplete view of operating performance. This project compares reach with daily activity, paid subscribers and revenue to identify what an operations team should monitor and investigate next.',
  qs:['How did audience, daily activity and monetisation change across 12 quarters?','Did DAU, paid subscribers and revenue grow faster than MAU?','What does the historical competitor context add?','Which operational priorities need further internal evidence?'],
  scope:['12 quarters: Q1 2023-Q4 2025. Official Duolingo IR / SEC disclosures.','Compare DAU/MAU, QoQ, YoY and indexed growth (Q1 2023 = 100).','Website: February 2026. Social: March 2026. Historical context only.','Source alignment and SQL / Python checks support two final Tableau pages.'],
  findings:[
   'DAU grew 160% versus MAU 83% from Q1 2023 to Q4 2025. DAU/MAU rose from 28.0% to 39.6% (+11.6 pp), indicating deeper aggregate activity.',
   'Paid subscribers grew 154% and quarterly revenue 145%, both faster than MAU. The data supports further review of monetisation drivers.',
   'By Q4 2025, MAU growth moderated to 14% YoY while DAU, paid subscribers and revenue grew 30%, 28% and 35%.',
   'The inherited February/March 2026 snapshots show greater Duolingo digital reach among the three observed brands. This is context only, with unverified historical captures.'
  ],
  recs:[
   ['Protect engagement quality','Investigate the drivers behind DAU growth outpacing MAU and monitor whether stronger activity intensity is sustained.'],
   ['Strengthen premium value communication','Test clearer subscription value messaging and targeted trial opportunities rather than assuming faster revenue growth reflects better conversion.'],
   ['Balance growth with user control','Maintain configurable engagement settings and monitor user response as activity and monetisation continue to scale.']
  ],
  methods:['Official disclosures cover six corporate metrics across 12 quarters. Sources and definitions are documented.','Compare period growth, QoQ, YoY, DAU/MAU and indexed growth. Rate gaps use percentage points.','SQL and Python checks reconcile the 16 derived fields and preserve unavailable comparisons as missing.','Two completed Tableau dashboards are the final visualisation. Both language versions use the same views.'],
  limits:['Public aggregates cannot measure cohort retention or a free-to-paid funnel.','Competitor snapshots have no original dated captures and provide context only.','DAU/MAU describes aggregate activity. Paid and revenue growth do not isolate conversion or pricing.','Relationships are descriptive. Recommendations have no measured business impact.'],
  positioning:'The project delivers operational priorities and a monitoring framework. Proposed reviews and experiments require internal data and validation.',
  footer:'Sources: Duolingo IR / SEC. Definitions and full links: methodology, source manifest and speaker notes',
 },
 cn:{
  cover:'Duolingo 的用户规模扩大时，活跃与商业化是否同步增强？2023-2025 年，日常活跃与商业化增长均快于 MAU。本案例据此提出产品运营、用户运营与增长运营的监控和调查重点。',
  context:'仅看用户规模，无法完整判断经营表现。本项目结合日常活跃、付费订阅和收入，判断增长结构，并提出运营团队下一步应持续监控和深入调查的问题。',
  qs:['12 个季度内，用户规模、日常活跃与商业化如何变化？','DAU、付费订阅和收入是否增长得比 MAU 更快？','历史竞品快照能补充什么背景？','哪些运营重点需要内部数据继续验证？'],
  scope:['12 个季度：2023 Q1-2025 Q4，来自 Duolingo IR / SEC 官方披露。','比较 DAU/MAU、环比、同比及增长指数（2023 Q1 = 100）。','网站：2026 年 2 月；社媒：2026 年 3 月，仅作历史背景。','来源核对及 SQL / Python 校验支持两页最终 Tableau Dashboard。'],
  findings:[
   '2023 Q1 至 2025 Q4，DAU 增长 160%，MAU 增长 83%。DAU/MAU 从 28.0% 升至 39.6%（+11.6 个百分点），汇总活跃强度提升。',
   '付费订阅用户增长 154%，季度收入增长 145%，均快于 MAU，值得进一步调查商业化驱动因素。',
   '到 2025 Q4，MAU 同比增速放缓至 14%，DAU、付费订阅用户和收入分别增长 30%、28% 和 35%。',
   '沿用的 2026 年 2-3 月快照显示，三个观察品牌中 Duolingo 数字触达更大。原始历史截图未核实，仅作背景。'
  ],
  recs:[
   ['保护活跃质量','调查 DAU 增长快于 MAU 的驱动因素，并持续观察更高的活跃强度能否维持。'],
   ['强化会员价值沟通','测试更清晰的订阅价值沟通与定向试用机会，不能将更快的收入增长直接解释为更高的转化效率。'],
   ['兼顾增长与用户自主控制','保留可配置的互动设置，并在活跃与商业化扩大的过程中持续监控用户反应。']
  ],
  methods:['官方披露覆盖 12 个季度、6 项公司指标，来源和定义均有记录。','比较期间增长、同比、环比、DAU/MAU 与增长指数，增速差用百分点表示。','SQL / Python 核对 16 个衍生字段，不可用的前期比较保留为空值。','两页已完成的 Tableau Dashboard 为最终可视化，中英文案例共用同一组页面。'],
  limits:['公开汇总数据无法衡量 cohort 留存或真实的免费到付费漏斗。','竞品快照缺少原始带日期截图，仅用于背景。','DAU/MAU 描述汇总活跃强度，付费与收入增长无法隔离转化或定价影响。','结论为描述性关系，建议尚无实际业务效果验证。'],
  positioning:'项目产出是运营重点与监控框架。拟议的调查和实验需要内部数据，并经过验证后再行动。',
  footer:'来源：Duolingo IR / SEC。定义与完整链接见方法说明、来源清单及演讲者备注',
 }
};
function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');}
async function html(lang){
 const c=copy[lang],cn=lang==='cn';
 const title=cn?'Duolingo 增长与营销运营分析':'Duolingo Growth & Marketing Operations Analytics';
 const sub=cn?'产品运营 / 用户运营 / 增长运营 / 综合运营':'Product Operations / User Operations / Growth Operations / General Operations';
 const scope=cn?'分析时点：2026 年 3 月。公司表现：2023 Q1-2025 Q4。':'Analysis as of March 2026. Corporate performance: Q1 2023-Q4 2025.';
 const H=cn?['业务问题','数据与方法','关键发现','运营含义','分析局限']:['Business question','Data & method','Key findings','Operational implications','Limitations'];
 const dashboardTitle=cn?'最终 Tableau Dashboard':'Final Tableau dashboards';
 const publicLink=publicUrl?`<a class="primary" href="${esc(publicUrl)}" target="_blank" rel="noopener">${cn?'打开 Tableau Public 交互式 Dashboard':'Open the interactive Tableau Public dashboard'}</a>`:`<span class="link-slot">${cn?'Tableau Public 分享链接位置已预留':'Tableau Public share URL slot reserved'}</span>`;
 const linkNote=publicUrl?'':`<p class="small">${cn?'两页 Tableau Dashboard 已完成，分享链接可补入此处。':'Two completed Tableau dashboards. The share URL can be added here.'}</p>`;
 const role=cn?'项目工作：明确业务问题，统一公开指标口径，核对来源与计算，完成两页 Tableau 展示，并将发现转成运营调查重点。':'Project work: framed the business questions, aligned public metric definitions, checked source values and calculations, and translated the two Tableau views into operational priorities.';
 const rounding=cn?'增长率按披露数值计算并四舍五入。MAU、DAU 为季度平均人数，付费订阅为期末人数，收入为季度金额。':'Growth rates use disclosed values and rounded presentation. MAU and DAU are quarterly averages, paid subscribers are period-end counts, and revenue covers each quarter.';
 const caveat=cn?'网站与社媒数值沿用历史课程快照。原始带日期截图、准确采集日期与社媒账户链接缺失，历史来源无法独立核实。不能据此推断市场份额、转化、留存或长期趋势。':'Website and social figures come from inherited coursework snapshots. Original dated captures, exact observation dates and social account links are unavailable. They cannot establish market share, conversion, retention or long-term trends.';
 const tech=cn?'SQL 公式通过 SQLite 兼容适配核对，未验证原生 MySQL 执行。原始数据、处理后 CSV、指标定义与已冻结结论均保留。':'SQL formulas were checked through a SQLite compatibility adaptation. Native MySQL execution remains unverified. The raw data, processed CSVs, metric definitions and frozen conclusions are preserved.';
 const suffix=lang.toUpperCase();
 const label=cn?['来源清单','方法说明','数据字典','PDF','可编辑 PPTX','English']:['Source manifest','Methodology','Data dictionary','PDF','Editable PPTX','中文'];
 const urls=['../docs/source_manifest.csv','../docs/methodology.md','../docs/data_dictionary.md',`Duolingo_Growth_Operations_Case_Study_${suffix}.pdf`,`Duolingo_Growth_Operations_Case_Study_${suffix}.pptx`,`case_study_${cn?'en':'cn'}.html`];
 const text=`<!doctype html>
<html lang="${cn?'zh-CN':'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>
:root{--ink:#172b4d;--green:#28752a;--muted:#5c6775;--line:#dfe6e8}*{box-sizing:border-box}body{font-family:Arial,'Hiragino Sans GB',sans-serif;margin:0;background:#f7f9fa;color:#263238;line-height:1.65}.wrap{max-width:1080px;margin:auto;padding:52px 30px 64px}h1{font-size:40px;line-height:1.18;margin:12px 0 18px;color:var(--ink);max-width:950px}h2{font-size:25px;line-height:1.3;color:var(--ink);margin:0 0 18px}h3{font-size:18px;color:var(--ink);margin:22px 0 6px}.eyebrow{color:var(--green);font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.sub,.scope,.small{color:var(--muted)}.scope,.small{font-size:13px}.lead{font-size:21px;max-width:930px;line-height:1.6;margin:24px 0}.role{max-width:940px;font-size:15px}section{border-top:1px solid var(--line);padding:32px 0 8px;margin-top:28px}nav{display:flex;gap:17px;flex-wrap:wrap;font-size:14px;margin:22px 0}a{color:var(--green);text-underline-offset:3px}.primary,.link-slot{display:inline-block;margin-top:12px;font-size:15px;font-weight:700}.primary{border-bottom:2px solid var(--green);text-decoration:none}.link-slot{color:var(--muted)}p,li{max-width:950px}li{margin-bottom:12px}ul,ol{padding-left:24px}.findings li{margin-bottom:18px}figure{margin:20px 0 30px}figure img{display:block;width:100%;height:auto;border:1px solid var(--line);background:white}figcaption{font-size:13px;color:var(--muted);margin-top:9px}details{font-size:14px;margin-top:18px}summary{cursor:pointer;color:var(--green)}footer{font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:20px;margin-top:36px}@media(max-width:700px){.wrap{padding:30px 19px}h1{font-size:31px}.lead{font-size:18px}h2{font-size:23px}}@media print{body{background:white}.wrap{padding:0;max-width:none}nav,.primary,details{display:none}section{break-inside:avoid}figure{break-inside:avoid}h1{font-size:29px}.lead{font-size:17px}}
</style></head><body><main class="wrap"><div class="eyebrow">Portfolio case study</div><h1>${esc(title)}</h1><p class="sub">${sub}</p><p class="scope">${scope}</p><p class="lead">${esc(c.cover)}</p><p class="role">${esc(role)}</p>${publicLink}${linkNote}<nav>${urls.map((u,i)=>`<a href="${u}">${label[i]}</a>`).join('')}</nav>
<section id="question"><h2>01 / ${H[0]}</h2><p>${esc(c.context)}</p><ol>${c.qs.map(t=>`<li>${esc(t)}</li>`).join('')}</ol></section>
<section id="method"><h2>02 / ${H[1]}</h2><ul>${c.scope.map(t=>`<li>${esc(t)}</li>`).join('')}</ul><p class="small">${rounding}</p><details><summary>${cn?'计算与工具细节':'Calculation and tooling details'}</summary><p>${tech}</p><p>${cn?'口径提醒：DAU/MAU 是汇总活跃强度；增速差使用百分点；增长指数以 2023 Q1 = 100。':'Definitions: DAU/MAU measures aggregate activity intensity, growth-rate gaps use percentage points, and growth indexes use Q1 2023 = 100.'}</p></details></section>
<section id="findings"><h2>03 / ${H[2]}</h2><ol class="findings">${c.findings.map(t=>`<li>${esc(t)}</li>`).join('')}</ol></section>
<section id="dashboards"><h2>${dashboardTitle}</h2><p class="small">${cn?'两页最终英文 Tableau 页面，中英文案例共用；点击图片可查看完整尺寸。':'Both language versions use the same two final English Tableau views. Open each image for full-size inspection.'}</p>${[1,2].map((i)=>`<figure><a href="../dashboard/final/tableau_page${i}.png"><img src="../dashboard/final/tableau_page${i}.png" alt="Tableau Page ${i}: ${i===1?'Growth and Monetisation Overview':'Growth Diagnostics and Strategic Context'}"></a><figcaption>${i===1?(cn?'Page 1：规模、活跃与商业化趋势。':'Page 1: audience, daily activity and monetisation trends.'):(cn?'Page 2：增长差异、历史竞品背景与运营含义。':'Page 2: growth differences, historical competitive context and operational implications.')}</figcaption></figure>`).join('')}</section>
<section id="operations"><h2>04 / ${H[3]}</h2><p class="small">${cn?'以下为拟议运营重点，需要获授权的内部证据、控制评估与免费体验保护指标；尚未实施或验证业务效果。':'These are proposed priorities requiring authorised internal evidence and controlled evaluation, with free-experience guardrails. No implementation or measured business impact is claimed.'}</p>${c.recs.map(([h,b])=>`<h3>${esc(h)}</h3><p>${esc(b)}</p>`).join('')}</section>
<section id="limits"><h2>05 / ${H[4]}</h2><ul>${c.limits.map(t=>`<li>${esc(t)}</li>`).join('')}</ul><p class="small">${caveat}</p><p class="small">${cn?'公司 MAU/DAU 使用其自有分析定义和估算，未经本项目独立测量。':'Company MAU/DAU use Duolingo\'s own analytics definitions and estimates, without independent measurement by this project.'}</p></section><footer>${esc(c.footer)}</footer></main></body></html>`;
 await fs.writeFile(path.join(ROOT,`case_study/case_study_${lang}.html`),text);
}
async function deck(lang){
 const cn=lang==='cn',c=copy[lang],suffix=lang.toUpperCase();
 const template=path.join(BUILD,`template_${suffix}.pptx`);
 const stable=path.join(ROOT,`case_study/Duolingo_Growth_Operations_Case_Study_${suffix}.pptx`);
 const source=stable;
 const p=await PresentationFile.importPptx(await FileBlob.load(source));
 for(let si=0;si<p.slides.items.length;si++)await fs.writeFile(path.join(BUILD,`${suffix}-source-${si+1}.png`),new Uint8Array(await(await p.slides.items[si].export({format:'png',scale:1})).arrayBuffer()));
 const before=await p.inspect({kind:'slide,textbox,shape,image,layout',maxChars:100000});
 await fs.writeFile(path.join(BUILD,`${suffix}-before.ndjson`),before.ndjson);
 const records=before.ndjson.split('\n').filter(Boolean).map(s=>JSON.parse(s));
 function target(slide,name){const r=records.find(r=>r.slideIndex===slide&&r.name===name&&r.id?.startsWith('sh/'));if(!r)throw new Error(`Missing ${slide} ${name}`);return p.resolve(r.id);}
 function set(slide,name,text){const t=target(slide,name);t.text=text;return t;}
 const font=cn?CN:EN;
 for(const r of records.filter(r=>r.id?.startsWith('sh/'))){const t=p.resolve(r.id);t.text.style={typeface:font,wrap:'square',autoFit:'none'};}
 set(0,'TextBox 4',c.cover);
 set(0,'TextBox 6',cn?'12 个季度':'12 quarters');set(0,'TextBox 8',cn?'公开数据':'Public data');set(0,'TextBox 10','Tableau');
 set(0,'TextBox 15',cn?'打开已发布的 Tableau 交互式 Dashboard':'Open the published interactive Tableau dashboard');
 target(0,'TextBox 15').text.style={fontSize:11};
 set(0,'TextBox 2',cn?'案例研究 / 产品运营 / 用户运营 / 增长运营 / 综合运营':'Case Study / Product Operations / User Operations / Growth Operations / General Operations');
 set(1,'TextBox 1',cn?'1. 业务问题、数据与方法':'1. Business Question, Data & Method');
 set(1,'TextBox 3',c.context);
 set(1,'TextBox 9',cn?'数据与方法':'Data & method');
 c.scope.forEach((t,i)=>set(1,`TextBox ${10+i}`,t));
 set(5,'TextBox 1',cn?'5. 运营含义':'5. Operational Implications');
 set(6,'TextBox 1',cn?'6. 方法与分析局限':'6. Method & Limitations');
 c.qs.forEach((t,i)=>set(1,`TextBox ${5+i}`,`${i+1}. ${t}`));
 set(4,'TextBox 4',c.findings[0]);set(4,'TextBox 7',c.findings[1]);set(4,'TextBox 10',c.findings[2]);set(4,'TextBox 13',c.findings[3]);
 c.recs.forEach(([h,b],i)=>{set(5,`TextBox ${4+i*4}`,h);set(5,`TextBox ${5+i*4}`,b);});
 c.methods.forEach((t,i)=>set(6,`TextBox ${3+i}`,'• '+t));c.limits.forEach((t,i)=>set(6,`TextBox ${8+i}`,'• '+t));
 set(6,'TextBox 13',c.positioning);
 // Imported geometry and styles are retained. Artifact text edits can auto-size
 // imported textboxes; restore original frames after every content/style setter.
 const frames=new Map(records.filter(r=>r.id?.startsWith('sh/')).map(r=>[r.id,{...r.position}]));
 function fit(slide,name,change){const r=records.find(r=>r.slideIndex===slide&&r.name===name);frames.set(r.id,{...r.position,...change});}
 fit(0,'TextBox 4',{height:140});
 fit(1,'TextBox 3',{top:137,height:78});
 for(const name of ['TextBox 4','TextBox 7','TextBox 10','TextBox 13'])fit(4,name,{height:102});
 for(const name of ['TextBox 5','TextBox 9','TextBox 13'])fit(5,name,{height:212});
 for(let n of [3,4,5,6,8,9,10,11])fit(6,`TextBox ${n}`,{height:59});
 target(6,'TextBox 13').text.style={fontSize:20};
 for(const r of records.filter(r=>r.kind==='textbox')){
  const t=p.resolve(r.id),frame=frames.get(r.id);
  const size=r.slideIndex===6&&r.name==='TextBox 13'?20:r.slideIndex===0&&r.name==='TextBox 15'?16:r.style.fontSize;
  const value=t.text.toString();
  t.text=/^0[123]$/.test(value)?value:wrapText(value,frame.width-32,font,size,r.style.bold);
  t.text.style={...r.style,typeface:font,fontSize:size,wrap:'none',autoFit:'none'};
  t.position=frame;
 }
 const coverLink=target(0,'TextBox 15');coverLink.text.get(coverLink.text.toString()).link={uri:publicUrl,isExternal:true};
 for(const si of [2,3]){
  const r=records.find(r=>r.kind==='image'&&r.slideIndex===si);if(!r)throw new Error('Dashboard image missing');const im=p.resolve(r.id);
  const png=path.join(ROOT,`dashboard/final/tableau_page${si-1}.png`);
  im.replace({blob:await fs.readFile(png),contentType:'image/png',alt:`Final published Tableau Page ${si-1}: ${si===2?'Growth & Monetisation Overview':'Q4 growth-gap cards; Indexed Growth Comparison; Engagement Growth Gap; Monetisation Growth Gaps; separate Website Traffic and Social Audience snapshots; Operational Priorities'}`,fit:'contain'});
  const imageInfo=await loadImage(png);const w=Math.min(1148,616*imageInfo.width/imageInfo.height),h=w*imageInfo.height/imageInfo.width;
  im.frame={left:(1280-w)/2,top:76,width:w,height:h};im.crop={left:0,top:0,right:0,bottom:0};im.fit='contain';
 }
 for(let si=0;si<7;si++){
  const slide=p.slides.items[si];
  if([2,3].includes(si)){let caption=slide.shapes.items.find(x=>x.name==='Published Tableau link');if(!caption)caption=slide.shapes.add({geometry:'textbox',name:'Published Tableau link',position:{left:108,top:59,width:1064,height:16},fill:'none',line:{fill:'none',width:0}});caption.text=cn?'最终已发布的 Tableau 页面。点击打开交互式 Dashboard':'Final published Tableau view. Click to open the interactive dashboard';caption.text.style={fontSize:12,typeface:font,color:'#28752A',wrap:'none',autoFit:'none',insets:0};caption.text.get(caption.text.toString()).link={uri:publicUrl,isExternal:true};}slide.speakerNotes.text=sourceNotes+'\n\nFinal visualisation: two completed Tableau dashboards. '+(publicUrl?'Tableau Public: '+publicUrl:'Share URL slot: docs/portfolio_links.json. Publication confirmed by project owner; share URL not independently checked.')+'\n\nSQL formulas checked through a SQLite compatibility adaptation; native MySQL execution unverified.\n\n'+(si===5?'Recommendations are proposed internal reviews, not claims that Duolingo lacks tracking or that any tactic is effective.':'');
  if(![0,2,3].includes(si)){
   let footer=slide.shapes.items.find(x=>x.name==='Evidence footer');
   if(!footer)footer=slide.shapes.add({geometry:'textbox',name:'Evidence footer',position:{left:68,top:675,width:1140,height:24},fill:'none',line:{fill:'none',width:0}});
   footer.text=c.footer;footer.text.style={fontSize:12,typeface:font,color:'#68737D',wrap:'square',autoFit:'none',insets:0};
  }
  await fs.writeFile(path.join(BUILD,`${suffix}-after-${si+1}.png`),new Uint8Array(await (await slide.export({format:'png',scale:1})).arrayBuffer()));
  await fs.writeFile(path.join(BUILD,`${suffix}-layout-${si+1}.json`),await (await slide.export({format:'layout'})).text());
 }
 const after=await p.inspect({kind:'slide,textbox,image,notes',maxChars:100000});await fs.writeFile(path.join(BUILD,`${suffix}-after.ndjson`),after.ndjson);
 const candidate=path.join(BUILD,`${suffix}-${runId}-candidate.pptx`);await(await PresentationFile.exportPptx(p)).save(candidate);

 const final=path.join(OUT,`${suffix}-${runId}-verified.pptx`);
 const report=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12191695,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:7,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(BUILD,`${suffix}-${runId}.validation.json`)});
 console.log(suffix,'validated',report.finalPath??final);
 await fs.copyFile(final,stable);
}
for(const lang of ['en','cn']){await html(lang);await deck(lang);}
// Fontconfig must see system fonts in this headless LibreOffice distribution.
const fc=path.join(BUILD,'fonts.conf');const cache=path.join(BUILD,'font-cache');await fs.mkdir(cache,{recursive:true});
await fs.writeFile(fc,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>/System/Library/Fonts</dir><dir>/System/Library/Fonts/Supplemental</dir><cachedir>${cache}</cachedir></fontconfig>`);
const soffice=process.env.CODEX_SOFFICE ?? path.join(RUNTIME,'bin/override/soffice');
const pdfStage=path.join(OUT,`pdf-${runId}`);await fs.mkdir(pdfStage,{recursive:true});
for(const suffix of ['EN','CN']){
 const filename=`Duolingo_Growth_Operations_Case_Study_${suffix}`;
 const r=spawnSync(soffice,['--headless','--convert-to','pdf','--outdir',pdfStage,path.join(ROOT,`case_study/${filename}.pptx`)],{env:{...process.env,FONTCONFIG_FILE:fc},encoding:'utf8'});
 if(r.status!==0)throw new Error(`PDF conversion failed: ${r.stderr}`);
 const pdf=path.join(pdfStage,`${filename}.pdf`);await fs.access(pdf);attachLinks('pdf',pdf);await fs.copyFile(pdf,path.join(ROOT,`case_study/${filename}.pdf`));console.log(suffix,'PDF exported from actual edited PPTX');
}
console.log('Case studies refreshed. Inspect final PDF page renders before accepting visual QA.');
