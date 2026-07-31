const IDX=__INDEX__, FIRST="__FIRST__", ORDER=__ORDER__, QUIZ=__QUIZ__, COMPENDIUM=__COMPENDIUM__, DOMAINS=__DOMAINS__, GLOSS=__GLOSSARY__;
let CUR=FIRST, LASTQ="", SUPPRESS=false, SEL=-1, CFILT={cls:"",mod:"",q:""};
/* ---- personal layer (bookmarks, reading progress, recently viewed) ---- */
let BM=new Set(), READ=new Set(), RECENT=[], MA_ARM=false;
function _lsGet(k){try{return JSON.parse(localStorage.getItem(k)||'[]');}catch(e){return [];}}
function _lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
function loadPersonal(){BM=new Set(_lsGet('nma-bm'));READ=new Set(_lsGet('nma-read'));RECENT=_lsGet('nma-recent');}
function trackVisit(id){if(id==='home')return;READ.add(id);_lsSet('nma-read',[...READ]);RECENT=RECENT.filter(x=>x!==id);RECENT.unshift(id);if(RECENT.length>18)RECENT=RECENT.slice(0,18);_lsSet('nma-recent',RECENT);}
function syncStar(id){const el=document.getElementById('bm-'+id);if(el){const on=BM.has(id);el.classList.toggle('on',on);el.textContent=on?'★':'☆';el.title=on?'Bookmarked — click to remove':'Bookmark this page';}}
function toggleBM(id){if(BM.has(id))BM.delete(id);else BM.add(id);_lsSet('nma-bm',[...BM]);syncStar(id);}
function _titleMap(){const T={};IDX.forEach(x=>T[x.id]=x.title);return T;}
function openMyAtlas(){loadPersonal();document.getElementById('myatlas').classList.add('on');document.body.style.overflow='hidden';renderMyAtlas();}
function closeMyAtlas(){document.getElementById('myatlas').classList.remove('on');document.body.style.overflow='';MA_ARM=false;}
function renderMyAtlas(){
 const T=_titleMap();
 const total=DOMAINS.reduce((a,d)=>a+d.ids.length,0);
 const readCount=DOMAINS.reduce((a,d)=>a+d.ids.filter(id=>READ.has(id)).length,0);
 const pct=total?Math.round(100*readCount/total):0;
 const bars=DOMAINS.map(d=>{const r=d.ids.filter(id=>READ.has(id)).length,p=d.ids.length?Math.round(100*r/d.ids.length):0;
  return '<div class="ma-bar"><div class="ma-bl"><span>'+d.label+'</span><span>'+r+'/'+d.ids.length+'</span></div><div class="ma-track"><div class="ma-fill" style="width:'+p+'%"></div></div></div>';}).join('');
 const list=arr=>arr.filter(id=>T[id]).map(id=>'<div class="ma-item"><a onclick="closeMyAtlas();go(\''+id+'\')">'+T[id]+'</a></div>').join('');
 const bms=[...BM].filter(id=>T[id]);
 const bmHtml=bms.length?list(bms):'<p class="ma-empty">No bookmarks yet — tap the &#9734; beside any page title.</p>';
 const rcHtml=RECENT.filter(id=>T[id]).length?list(RECENT):'<p class="ma-empty">Nothing viewed yet.</p>';
 document.getElementById('myatlas-body').innerHTML=
  '<h2>My Atlas</h2>'+
  '<div class="ma-overall"><div class="ma-big">'+readCount+'<span>/'+total+'</span></div><div class="ma-osub">pages viewed &middot; '+pct+'%</div></div>'+
  '<div class="ma-sec"><div class="ma-h">Progress by domain</div>'+bars+'</div>'+
  '<div class="ma-sec"><div class="ma-h">Bookmarks ('+bms.length+')</div>'+bmHtml+'</div>'+
  '<div class="ma-sec"><div class="ma-h">Recently viewed</div>'+rcHtml+'</div>'+
  '<div class="ma-reset"><button onclick="maReset(this)">Reset my data</button></div>';
}
function maReset(btn){if(!MA_ARM){MA_ARM=true;btn.textContent='Click again to confirm';return;}
 BM=new Set();READ=new Set();RECENT=[];_lsSet('nma-bm',[]);_lsSet('nma-read',[]);_lsSet('nma-recent',[]);MA_ARM=false;renderMyAtlas();
 document.querySelectorAll('.bm.on').forEach(el=>{el.classList.remove('on');el.textContent='☆';});}
/* ---- A–Z Index ---- */
function firstLetter(t){const m=t.match(/[A-Za-z]/);return m?m[0].toUpperCase():'#';}
function openIndex(){document.getElementById('index-ov').classList.add('on');document.body.style.overflow='hidden';var _h=document.getElementById('idx-h');if(_h)_h.textContent='A–Z Index';renderIndex('');setTimeout(()=>{const q=document.getElementById('idx-q');if(q){q.value='';q.focus();}},30);}
function closeIndex(){document.getElementById('index-ov').classList.remove('on');document.body.style.overflow='';}
function renderIndex(f){
 f=(f||'').toLowerCase();
 const items=IDX.filter(x=>x.id!=='home'&&(!f||x.title.toLowerCase().includes(f))).slice()
   .sort((a,b)=>a.title.toLowerCase()<b.title.toLowerCase()?-1:a.title.toLowerCase()>b.title.toLowerCase()?1:0);
 const groups={};
 items.forEach(x=>{const L=firstLetter(x.title);(groups[L]=groups[L]||[]).push(x);});
 const letters=Object.keys(groups).sort();
 const jb=document.getElementById('idx-jump'); if(jb)jb.innerHTML=letters.map(L=>'<a onclick="jumpLetter(\''+L+'\')">'+L+'</a>').join('');
 const secs=letters.map(L=>'<div class="idx-sec" id="idxL-'+L+'"><div class="idx-letter">'+L+'</div>'+
   groups[L].map(x=>'<div class="idx-item"><a onclick="closeIndex();go(\''+x.id+'\')">'+x.title+'</a><span class="idx-ch">'+x.group+'</span></div>').join('')+'</div>').join('');
 const lst=document.getElementById('idx-list'); if(lst)lst.innerHTML=secs||'<p class="ma-empty">No matches.</p>';
 const c=document.getElementById('idx-count'); if(c)c.textContent=items.length+' entries';
}
function jumpLetter(L){const el=document.getElementById('idxL-'+L);if(el)el.scrollIntoView({block:'start'});}
/* ---- figure lightbox ---- */
function lightbox(fig){const m=fig.querySelector('.fig-media'),c=fig.querySelector('figcaption'),ov=document.getElementById('lightbox');
 if(!m||!ov)return;ov.querySelector('.lb-media').innerHTML=m.innerHTML;ov.querySelector('.lb-cap').innerHTML=c?c.innerHTML:'';
 ov.classList.add('on');document.body.style.overflow='hidden';}
function closeLightbox(){const ov=document.getElementById('lightbox');if(ov)ov.classList.remove('on');document.body.style.overflow='';}
/* ---- inline glossary tooltips (first occurrence of each term per page) ---- */
let GLOSS_KEYS=null;
function _escRe(s){return s.replace(/[.*+?^${}()|[\]\\/-]/g,'\\$&');}
function applyGlossary(id){
 const body=document.querySelector('#page-'+id+' .body'); if(!body||body.dataset.gloss)return;
 body.dataset.gloss='1';
 if(!GLOSS_KEYS)GLOSS_KEYS=Object.keys(GLOSS).sort((a,b)=>b.length-a.length);
 for(const term of GLOSS_KEYS){
  const re=new RegExp('(^|[^A-Za-z0-9])('+_escRe(term)+')(?![A-Za-z0-9])');
  const walk=document.createTreeWalker(body,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
   const p=n.parentNode;
   if(!p||p.closest('a,code,abbr,h1,h2,h3,h4,summary,.rel-chip,.tool,figure,.gloss,.cite'))return NodeFilter.FILTER_REJECT;
   return re.test(n.nodeValue)?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_SKIP;
  }});
  const node=walk.nextNode(); if(!node)continue;
  const m=re.exec(node.nodeValue); if(!m)continue;
  const txt=node.nodeValue, idx=m.index+m[1].length;
  const frag=document.createDocumentFragment();
  const before=txt.slice(0,idx), mid=txt.slice(idx,idx+term.length), after=txt.slice(idx+term.length);
  if(before)frag.appendChild(document.createTextNode(before));
  const ab=document.createElement('abbr'); ab.className='gloss'; ab.setAttribute('data-def',GLOSS[term]); ab.textContent=mid; frag.appendChild(ab);
  if(after)frag.appendChild(document.createTextNode(after));
  node.parentNode.replaceChild(frag,node);
 }
}
/* robust glossary tooltip: one shared element, appended to <body>, positioned by
   JS and clamped to the viewport — so it can never be clipped by an ancestor's
   overflow or pushed off-screen (the old CSS ::after tooltip could be). */
let _gtip=null;
function _ensureGtip(){if(_gtip)return _gtip;_gtip=document.createElement('div');_gtip.id='gtip';_gtip.setAttribute('role','tooltip');document.body.appendChild(_gtip);return _gtip;}
function _showGtip(el){
 if(document.body.classList.contains('hy-on'))return;           // suppressed in high-yield mode
 const def=el.getAttribute('data-def'); if(!def)return;
 const t=_ensureGtip(); t.textContent=def; t.style.display='block'; t.style.left='-9999px'; t.style.top='0';
 const r=el.getBoundingClientRect(), tw=t.offsetWidth, th=t.offsetHeight;
 let left=r.left; if(left+tw>innerWidth-8)left=innerWidth-tw-8; if(left<8)left=8;
 let top=r.bottom+7; if(top+th>innerHeight-8)top=r.top-th-7;     // flip above if near the bottom
 t.style.left=left+'px'; t.style.top=Math.max(8,top)+'px'; t.classList.add('on');
}
function _hideGtip(){if(_gtip){_gtip.classList.remove('on');_gtip.style.display='none';}}
document.addEventListener('mouseover',function(e){const g=e.target.closest&&e.target.closest('.gloss'); if(g)_showGtip(g);});
document.addEventListener('mouseout',function(e){const g=e.target.closest&&e.target.closest('.gloss'); if(g)_hideGtip();});
// Touch/tap support: hover doesn't exist on phones, so tap a term to toggle its definition,
// and tap anywhere else to dismiss it.
let _gtipEl=null;
document.addEventListener('click',function(e){
 const g=e.target.closest&&e.target.closest('.gloss');
 if(g){e.preventDefault();
  if(_gtip&&_gtip.classList.contains('on')&&_gtipEl===g){_hideGtip();_gtipEl=null;}
  else{_showGtip(g);_gtipEl=g;}
 }else if(_gtip&&_gtip.classList.contains('on')){_hideGtip();_gtipEl=null;}
});
window.addEventListener('scroll',_hideGtip,true);
function chapterOf(id){var it=document.querySelector('.nav-item[data-id="'+id+'"]');return it?it.closest('.nav-ch'):null;}
// Reliable jump to the top of the page. iOS Safari sometimes performs its own scroll
// (from an anchor tap or layout reflow) just after our handler, so we scroll now AND on
// the next animation frame, and set every scroll root, to make sure it sticks.
function _scrollTop(){try{window.scrollTo(0,0);document.documentElement.scrollTop=0;document.body.scrollTop=0;}catch(e){}}
function go(id,fromHash){
 clearHL(); _hideGtip();
 var _lg=document.getElementById('legend'); if(_lg)_lg.style.display=(id==='home')?'':'none';
 document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
 const el=document.getElementById('page-'+id); if(el)el.classList.add('active');
 CUR=id; updatePager();
 if(!fromHash){SUPPRESS=true;location.hash='/'+id;setTimeout(()=>{SUPPRESS=false;},0);}
 document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.id===id));
 const home=document.querySelector('.nav-home'); if(home)home.classList.toggle('active',id==='home');
 // accordion: open the chapter containing this page, close the rest
 const ch=chapterOf(id);
 document.querySelectorAll('.nav-ch').forEach(c=>{c.classList.toggle('open',c===ch);c.classList.toggle('hasactive',c===ch);});
 // Only keep the active chapter visible in the desktop sidebar. On mobile the nav is a
 // stacked panel that we're about to close, and scrollIntoView there fights window.scrollTo
 // (on Safari it can win, stranding the reader down inside the long nav list).
 if(ch&&window.innerWidth>1000)ch.scrollIntoView({block:'nearest'});
 _closeNav(); closeSearch(); const q=document.getElementById('q'); if(q)q.value='';
 _scrollTop();
 buildTOC(id);
 if(document.getElementById('compendium-root'))renderCompendium();
 try{applyGlossary(id);}catch(e){}
 trackVisit(id); syncStar(id);
 const _t=titleOf(id);
 document.title = (id==='home'||!_t) ? 'Nuclear Medicine Atlas' : (_t+' · Nuclear Medicine Atlas');
 if(window.requestAnimationFrame){requestAnimationFrame(_scrollTop);}else{setTimeout(_scrollTop,0);}
}
let _TM=null;
function titleOf(id){if(!_TM){_TM={};IDX.forEach(x=>_TM[x.id]=x.title);}return _TM[id]||'';}
/* ---- On this page (section navigator + scroll-spy) ---- */
let TOC_HS=[];
function buildTOC(id){
 const toc=document.getElementById('toc'); if(!toc)return;
 TOC_HS=[];
 const body=document.querySelector('#page-'+id+' .body');
 if(!body){toc.classList.remove('on');toc.innerHTML='';return;}
 const hs=[...body.querySelectorAll(':scope > h2')].filter(h=>h.textContent.trim());
 if(hs.length<3){toc.classList.remove('on');toc.innerHTML='';return;}
 hs.forEach((h,i)=>{if(!h.id)h.id='sec-'+i+'-'+id;});
 TOC_HS=hs;
 toc.innerHTML='<div class="toc-h">On this page</div>'+hs.map(h=>'<a data-sec="'+h.id+'" onclick="jumpSec(event,\''+h.id+'\')">'+h.textContent+'</a>').join('');
 toc.classList.add('on'); spy();
}
function jumpSec(e,sid){if(e)e.preventDefault();const el=document.getElementById(sid);if(el){const y=el.getBoundingClientRect().top+window.scrollY-84;window.scrollTo({top:y,behavior:'smooth'});}}
function spy(){
 if(!TOC_HS.length)return;
 let cur=TOC_HS[0].id;
 for(const h of TOC_HS){if(h.getBoundingClientRect().top<=130)cur=h.id;else break;}
 document.querySelectorAll('#toc a').forEach(a=>a.classList.toggle('cur',a.dataset.sec===cur));
}
window.addEventListener('scroll',spy,{passive:true});
/* ---- keyboard shortcuts help ---- */
function toggleHelp(){const h=document.getElementById('help');if(h)h.classList.toggle('on');}
function closeHelp(){const h=document.getElementById('help');if(h)h.classList.remove('on');}
/* ---- command palette (Ctrl/Cmd-K) ---- */
const PACTIONS=[
 {t:'Go to Home',k:'home start',run:function(){go('home');}},
 {t:'Open Study mode',k:'quiz test board',run:function(){openStudy();}},
 {t:'Open A–Z Index',k:'index alphabetical browse',run:function(){openIndex();}},
 {t:'Open My Atlas (bookmarks & progress)',k:'bookmarks progress recent',run:function(){openMyAtlas();}},
 {t:'Open Radiopharmaceutical Compendium',k:'tracers matrix agents',run:function(){go('radiopharmaceutical-compendium');}},
 {t:'Open Unit Converter',k:'convert mci mbq gy rad',run:function(){go('tool-unit-converter');}},
 {t:'Toggle high-yield mode',k:'cram key points',run:function(){toggleHY();}},
 {t:'Show keyboard shortcuts',k:'help keys',run:function(){toggleHelp();}},
];
let PSEL=0, PITEMS=[];
function togglePalette(){const p=document.getElementById('palette');if(!p)return;p.classList.contains('on')?closePalette():openPalette();}
function openPalette(){const p=document.getElementById('palette');if(!p)return;p.classList.add('on');document.body.style.overflow='hidden';const q=document.getElementById('pal-q');q.value='';renderPalette('');setTimeout(function(){q.focus();},20);}
function closePalette(){const p=document.getElementById('palette');if(p)p.classList.remove('on');document.body.style.overflow='';}
function renderPalette(f){
 f=(f||'').trim().toLowerCase();
 const acts=PACTIONS.filter(a=>!f||a.t.toLowerCase().includes(f)||a.k.includes(f)).map(a=>({type:'act',label:a.t,run:a.run}));
 const T=_titleMap();
 let pages;
 if(!f){pages=(RECENT||[]).slice(0,6).filter(id=>T[id]).map(id=>({type:'page',id:id,label:T[id],group:'recent'}));}
 else{pages=IDX.filter(x=>x.id!=='home'&&x.title.toLowerCase().includes(f)).slice(0,8).map(x=>({type:'page',id:x.id,label:x.title,group:x.group}));}
 PITEMS=acts.concat(pages); PSEL=0;
 const box=document.getElementById('pal-list');
 box.innerHTML=PITEMS.length?PITEMS.map((it,i)=>'<div class="pal-item'+(i===0?' sel':'')+'" data-i="'+i+'" onmousedown="palRun('+i+')"><span class="pal-ic">'+(it.type==='act'?'▸':'›')+'</span><span class="pal-t">'+it.label+'</span><span class="pal-g">'+(it.type==='act'?'action':(it.group||''))+'</span></div>').join(''):'<div class="pal-empty">No matches</div>';
}
function palMove(d){if(!PITEMS.length)return;PSEL=(PSEL+d+PITEMS.length)%PITEMS.length;const els=document.querySelectorAll('.pal-item');els.forEach((el,i)=>el.classList.toggle('sel',i===PSEL));if(els[PSEL])els[PSEL].scrollIntoView({block:'nearest'});}
function palRun(i){const it=PITEMS[i];if(!it)return;closePalette();if(it.type==='page')go(it.id);else it.run();}
/* ---- Radiopharmaceutical Compendium (interactive tracer-target matrix) ---- */
function _clsSlug(c){return 'c-'+c.toLowerCase().replace(/[^a-z]+/g,'');}
function renderCompendium(){
 const root=document.getElementById('compendium-root'); if(!root)return;
 const classes=[...new Set(COMPENDIUM.map(r=>r.cls))].sort();
 const mods=['PET','SPECT','Therapy'];
 if(!root.dataset.built){
  const chip=(v,g,lab)=>`<button class="cmp-chip" data-g="${g}" data-v="${v}" onclick="cmpFilter('${g}','${v}')">${lab}</button>`;
  root.innerHTML=
   `<div class="cmp-controls">`+
   `<input class="cmp-search" id="cmp-q" placeholder="Filter agents, targets, uses…" oninput="cmpFilter('q',this.value)">`+
   `<div class="cmp-chips"><span class="cmp-lbl">Modality</span>${mods.map(m=>chip(m,'mod',m)).join('')}</div>`+
   `<div class="cmp-chips"><span class="cmp-lbl">Mechanism</span>${classes.map(c=>`<button class="cmp-chip ${_clsSlug(c)}" data-g="cls" data-v="${c}" onclick="cmpFilter('cls','${c}')">${c}</button>`).join('')}</div>`+
   `</div><div class="cmp-count" id="cmp-count"></div><div class="cmp-tbl-wrap"><table class="cmp-tbl"><thead><tr><th>Agent</th><th>Isotope</th><th>Modality</th><th>Mechanism</th><th>Target</th><th>Primary use</th></tr></thead><tbody id="cmp-body"></tbody></table></div>`;
  root.dataset.built='1';
 }
 cmpDraw();
}
function cmpFilter(g,v){
 if(g==='q'){CFILT.q=v.toLowerCase();}
 else{CFILT[g]=(CFILT[g]===v?'':v);
  document.querySelectorAll('.cmp-chip[data-g="'+g+'"]').forEach(b=>b.classList.toggle('on',b.dataset.v===CFILT[g]));}
 cmpDraw();
}
function cmpDraw(){
 const body=document.getElementById('cmp-body'); if(!body)return;
 const rows=COMPENDIUM.filter(r=>(!CFILT.cls||r.cls===CFILT.cls)&&(!CFILT.mod||r.mod===CFILT.mod)&&
   (!CFILT.q||(r.n+' '+r.tgt+' '+r.use+' '+r.iso+' '+r.cls).toLowerCase().includes(CFILT.q)));
 body.innerHTML=rows.map(r=>{
  const cell=`<td class="cmp-agent">${r.id?`<a onclick="go('${r.id}')">${r.n}</a>`:r.n}</td>`;
  return `<tr>${cell}<td>${r.iso}</td><td><span class="cmp-mod m-${r.mod.toLowerCase()}">${r.mod}</span></td>`+
   `<td><span class="cmp-badge ${_clsSlug(r.cls)}">${r.cls}</span></td><td class="cmp-tgt">${r.tgt}</td><td>${r.use}</td></tr>`;
 }).join('');
 const c=document.getElementById('cmp-count'); if(c)c.textContent=rows.length+' of '+COMPENDIUM.length+' agents';
}
function goHL(id){go(id);highlight(id,LASTQ);}
function step(d){const i=ORDER.indexOf(CUR);if(i<0)return;const j=i+d;if(j<0||j>=ORDER.length)return;go(ORDER[j]);}
function updatePager(){const i=ORDER.indexOf(CUR),pv=document.getElementById('pgp'),nx=document.getElementById('pgn');
 if(pv)pv.disabled=(i<=0);if(nx)nx.disabled=(i<0||i>=ORDER.length-1);}
/* ---- high-yield reading mode ---- */
function keepHY(el){
 if(el.classList.contains('lead')||el.classList.contains('y1')||el.classList.contains('y2'))return true;
 if(el.classList.contains('y4'))return false;
 const t=el.tagName.toLowerCase();
 if(t==='table'||t==='details')return true;
 if(t==='ul'||t==='ol')return !!el.querySelector(':scope > li.y2');
 if(t==='div')return !!(el.querySelector('.tool,input,select')||el.classList.contains('tool')||el.classList.contains('fig'));
 return false;
}
function trimHY(el){const t=el.tagName.toLowerCase();
 if(t==='ul'||t==='ol')el.querySelectorAll(':scope > li').forEach(li=>{if(!li.classList.contains('y2'))li.classList.add('hy-x');});}
function filterBody(body,on){
 body.querySelectorAll('.hy-x').forEach(e=>e.classList.remove('hy-x'));
 if(!on)return;
 const kids=[...body.children]; let i=0;
 while(i<kids.length){const el=kids[i],t=el.tagName.toLowerCase();
  if(t==='h2'||t==='h3'){let j=i+1;const sec=[];
   while(j<kids.length&&!/^h[23]$/.test(kids[j].tagName.toLowerCase())){sec.push(kids[j]);j++;}
   let any=false; sec.forEach(c=>{if(keepHY(c)){any=true;trimHY(c);}else c.classList.add('hy-x');});
   const ht=el.textContent.trim().toLowerCase();
   if(!any&&ht!=='quick answer'&&ht!=='self-check')el.classList.add('hy-x');
   i=j;
  } else {if(keepHY(el))trimHY(el);else el.classList.add('hy-x');i++;}
 }
}
function applyHY(on){
 document.body.classList.toggle('hy-on',on);
 const b=document.getElementById('hybtn'); if(b){b.classList.toggle('on',on);b.textContent=on?'High-yield: ON':'High-yield mode';}
 document.querySelectorAll('.page > .body').forEach(bd=>filterBody(bd,on));
}
function toggleHY(){const on=!document.body.classList.contains('hy-on');applyHY(on);try{localStorage.setItem('nma-hy',on?'1':'0');}catch(e){}}
/* ---- search-term highlighting ---- */
function clearHL(){document.querySelectorAll('mark.hl').forEach(m=>{const t=document.createTextNode(m.textContent);m.parentNode.replaceChild(t,m);m.parentNode&&m.parentNode.normalize&&m.parentNode.normalize();});}
function highlight(id,term){
 clearHL(); if(!term)return;
 const body=document.querySelector('#page-'+id+' .body'); if(!body)return;
 const terms=term.toLowerCase().split(/\s+/).filter(Boolean); if(!terms.length)return;
 const walk=document.createTreeWalker(body,NodeFilter.SHOW_TEXT,null);
 const nodes=[]; let n; while(n=walk.nextNode())nodes.push(n);
 let first=null;
 nodes.forEach(node=>{
  if(!node.parentNode||node.parentNode.closest('script,style'))return;
  const txt=node.nodeValue, low=txt.toLowerCase();
  let idx=-1,use=null;
  for(const tm of terms){const k=low.indexOf(tm);if(k>=0&&(idx<0||k<idx)){idx=k;use=tm;}}
  if(idx<0)return;
  const frag=document.createDocumentFragment();
  const b=txt.slice(0,idx),mid=txt.slice(idx,idx+use.length),a=txt.slice(idx+use.length);
  if(b)frag.appendChild(document.createTextNode(b));
  const mk=document.createElement('mark');mk.className='hl';mk.textContent=mid;frag.appendChild(mk);
  if(a)frag.appendChild(document.createTextNode(a));
  node.parentNode.replaceChild(frag,node);
  if(!first)first=mk;
 });
 if(first)first.scrollIntoView({block:'center',behavior:'smooth'});
}
function esc(x){return x.replace(/[<>&]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]));}
function snippet(s,term){const i=s.indexOf(term);if(i<0)return'';
 const st=Math.max(0,i-40),en=Math.min(s.length,i+term.length+50);
 const pre=s.slice(st,i),hit=s.slice(i,i+term.length),post=s.slice(i+term.length,en);
 return (st>0?'…':'')+esc(pre)+'<b>'+esc(hit)+'</b>'+esc(post)+(en<s.length?'…':'');}
function toggleCh(ch){
 const c=document.querySelector('.nav-ch[data-ch="'+ch+'"]'); if(!c)return;
 const wasOpen=c.classList.contains('open');
 document.querySelectorAll('.nav-ch').forEach(x=>x.classList.remove('open'));
 if(!wasOpen)c.classList.add('open');
}
function filterBy(q){const inp=document.getElementById('q');if(inp)inp.value=q;search(q);}
/* Theme chips → a full, grouped list of matching topics (not just the search box) */
function themeBrowse(label,q){
 const terms=(q||'').toLowerCase().split(/\s+/).filter(Boolean);
 const hits=IDX.filter(function(x){
  if(x.id==='home')return false;
  if(q==='tool')return x.id.indexOf('tool-')===0;
  var hay=(x.title+' '+x.sub).toLowerCase();
  return terms.some(function(t){return hay.indexOf(t)>=0;});
 }).sort(function(a,b){return a.title.toLowerCase()<b.title.toLowerCase()?-1:1;});
 const groups={};hits.forEach(function(x){(groups[x.group]=groups[x.group]||[]).push(x);});
 const order=Object.keys(groups).sort();
 const html=order.map(function(g){return '<div class="idx-sec"><div class="idx-letter">'+g+'</div>'+
  groups[g].map(function(x){return '<div class="idx-item"><a onclick="closeIndex();go(\''+x.id+'\')">'+x.title+'</a><span class="idx-ch">'+x.group+'</span></div>';}).join('')+'</div>';}).join('');
 const ov=document.getElementById('index-ov');if(!ov)return;
 ov.classList.add('on');document.body.style.overflow='hidden';
 const h=document.getElementById('idx-h');if(h)h.textContent=label+' — topics';
 const jb=document.getElementById('idx-jump');if(jb)jb.innerHTML='';
 const iq=document.getElementById('idx-q');if(iq)iq.value='';
 const c=document.getElementById('idx-count');if(c)c.textContent=hits.length+' topic'+(hits.length===1?'':'s');
 const lst=document.getElementById('idx-list');if(lst)lst.innerHTML=html||'<p class="ma-empty">No matches for '+label+'.</p>';
}
function search(v){
 const t=(v||'').trim().toLowerCase(), box=document.getElementById('sr');
 if(!t){box.classList.remove('open');return}
 const terms=t.split(/\s+/).filter(Boolean); LASTQ=t; SEL=-1;
 const hits=IDX.filter(x=>terms.every(tm=>x.s.includes(tm))).slice(0,14);
 box.innerHTML = hits.length? hits.map(h=>{
   const inTitle=(h.title+' '+h.sub).toLowerCase().includes(terms[0]);
   const snip=inTitle?'':snippet(h.s,terms[0]);
   return `<div class="sri" role="option" data-id="${h.id}" onmousedown="goHL('${h.id}')"><div class="g">${h.group}</div><div class="t">${h.title}</div><div class="s">${h.sub}</div>${snip?`<div class="snip">${snip}</div>`:''}</div>`;
 }).join('')
  : `<div class="sri"><div class="s">No results for “${esc(v)}”.</div></div>`;
 box.classList.add('open');
}
function moveSel(d){const items=[...document.querySelectorAll('#sr .sri[data-id]')];if(!items.length)return;
 SEL=(SEL+d+items.length)%items.length;
 items.forEach((it,i)=>it.classList.toggle('sel',i===SEL));
 items[SEL].scrollIntoView({block:'nearest'});}
function activateSel(){const items=[...document.querySelectorAll('#sr .sri[data-id]')];
 const pick=(SEL>=0&&items[SEL])?items[SEL]:items[0];
 if(pick)goHL(pick.getAttribute('data-id'));}
function closeSearch(){document.getElementById('sr').classList.remove('open')}
/* ---- copy citation ---- */
function copyCite(btn){const s=btn.parentNode.querySelector('.cite-txt');if(!s)return;const t=s.textContent.replace(/\s+/g,' ').trim();
 const done=()=>{btn.textContent='Copied';setTimeout(()=>{btn.textContent='Copy';},1400);};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,done);}else{try{const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();done();}catch(e){}}}
/* ---- Study Mode ---- */
let SQ=[], SI=0, SST={c:0,s:0}, SMISS=new Set(), EXAM=null, EXAMINT=0;
function _mk(q){return q.id+'||'+q.q;}
function loadMiss(){try{SMISS=new Set(JSON.parse(localStorage.getItem('nma-miss')||'[]'));}catch(e){SMISS=new Set();}}
function saveMiss(){try{localStorage.setItem('nma-miss',JSON.stringify([...SMISS]));}catch(e){}}
/* ---- spaced repetition (Leitner) over every graded question ---- */
let SR={};
function loadSR(){try{SR=JSON.parse(localStorage.getItem('nma-sr')||'{}')||{};}catch(e){SR={};}}
function saveSR(){try{localStorage.setItem('nma-sr',JSON.stringify(SR));}catch(e){}}
function _srToday(){return Math.floor(Date.now()/864e5);}
function _srDue(){var t=_srToday();return QUIZ.filter(function(q){var s=SR[_mk(q)];return s&&s.d<=t;});}
function _srUpdate(q,ok){var INT=[1,1,3,7,16,35];var k=_mk(q);var cur=SR[k]||{b:0};var b=ok?Math.min(5,(cur.b||0)+1):1;SR[k]={b:b,d:_srToday()+INT[b]};saveSR();}
function shuf(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const t=a[i];a[i]=a[j];a[j]=t;}return a;}
function openStudy(){loadMiss();loadSR();document.getElementById('study').classList.add('on');document.body.style.overflow='hidden';studyStart();}
function closeStudy(){document.getElementById('study').classList.remove('on');document.body.style.overflow='';if(EXAMINT){clearInterval(EXAMINT);EXAMINT=0;}EXAM=null;}
function _fmtT(ms){var s=Math.floor(ms/1000),m=Math.floor(s/60);return m+':'+('0'+(s%60)).slice(-2);}
function _balancedDraw(n){
 var byd={};QUIZ.forEach(function(q){(byd[q.ch]=byd[q.ch]||[]).push(q);});
 var doms=Object.keys(byd);doms.forEach(function(d){shuf(byd[d]);});
 var out=[],idx={};doms.forEach(function(d){idx[d]=0;});
 var added=true;
 while(out.length<n&&added){added=false;
  for(var i=0;i<doms.length;i++){var d=doms[i];if(idx[d]<byd[d].length){out.push(byd[d][idx[d]++]);added=true;if(out.length>=n)break;}}}
 return shuf(out);
}
function startExam(){
 var n=Math.min(50,QUIZ.length);
 SQ=_balancedDraw(n);SI=0;SST={c:0,s:0};
 EXAM={t0:Date.now(),dom:{},n:SQ.length};
 if(EXAMINT)clearInterval(EXAMINT);
 EXAMINT=setInterval(function(){var el=document.getElementById('ex-timer');if(el&&EXAM)el.textContent=_fmtT(Date.now()-EXAM.t0);},1000);
 if(SQ.length)renderCard();else studyStart();
}
function studyStart(){
 const chs=[...new Set(QUIZ.map(q=>q.ch))];
 const opts=chs.map(c=>`<option value="ch:${c}">${c} (${QUIZ.filter(q=>q.ch===c).length})</option>`).join('');
 document.getElementById('study-body').innerHTML=
  `<div class="st-start"><h2>Study mode</h2>`+
  `<p class="st-sub">${QUIZ.length} self-check questions across the atlas. Draw a set, reveal each answer, and self-score. Every answer is scheduled by <b>spaced repetition</b> — items you get right resurface at growing intervals, missed ones come back sooner; the "Due for spaced review" scope draws what's due today.</p>`+
  `<label>Scope</label><select id="st-scope"><option value="all">All domains (${QUIZ.length})</option>${(function(){const d=_srDue().length;return d?`<option value="due">Due for spaced review (${d})</option>`:'';})()}${opts}${SMISS.size?`<option value="miss">Missed only (${SMISS.size})</option>`:''}</select>`+
  `<label>Questions</label><select id="st-n"><option value="10">10</option><option value="20" selected>20</option><option value="30">30</option><option value="50">50</option><option value="0">All in scope</option></select>`+
  `<button class="st-go" onclick="startStudy()">Start study &rarr;</button>`+
  `<button class="st-go st-exam" onclick="startExam()">Mock exam &middot; ${Math.min(50,QUIZ.length)} Q, timed &rarr;</button>`+
  `<p class="st-examnote">The mock exam draws a comprehensive set balanced across all domains, times you, and reports your score with a per-domain readiness breakdown.</p>`+
  (SMISS.size?`<button class="st-clear" onclick="SMISS.clear();saveMiss();studyStart();">Clear ${SMISS.size} saved missed</button>`:'')+
  `</div>`;
}
function startStudy(){
 EXAM=null;if(EXAMINT){clearInterval(EXAMINT);EXAMINT=0;}
 const scope=document.getElementById('st-scope').value, n=+document.getElementById('st-n').value;
 let pool = scope==='all'?QUIZ.slice() : scope==='due'?_srDue() : scope==='miss'?QUIZ.filter(q=>SMISS.has(_mk(q))) : QUIZ.filter(q=>q.ch===scope.slice(3));
 pool=shuf(pool.slice()); if(n>0)pool=pool.slice(0,n);
 SQ=pool; SI=0; SST={c:0,s:0};
 if(!SQ.length){studyStart();return;} renderCard();
}
function renderCard(){
 if(SI>=SQ.length){renderSummary();return;}
 const q=SQ[SI];
 document.getElementById('study-body').innerHTML=
  `<div class="st-card"><div class="st-top"><span class="st-count">${SI+1} / ${SQ.length}${EXAM?' &middot; <span class="st-exlbl">MOCK EXAM</span>':''}</span>`+
  `<span class="st-score">${EXAM?`<span class="st-timer" id="ex-timer">${_fmtT(Date.now()-EXAM.t0)}</span>`:`${SST.c}/${SST.s}`}</span></div>`+
  `<div class="st-ch">${q.ch}</div><div class="st-topic">${q.t}</div><div class="st-q">${q.q}</div>`+
  `<div class="st-a" id="st-a" hidden><div class="st-alab">Answer</div>${q.a}`+
  `<div class="st-src">&rarr; <a onclick="closeStudy();goHL2('${q.id}')">${q.t}</a></div></div>`+
  `<div class="st-act" id="st-act"><button class="st-reveal" onclick="revealA()">Reveal answer <span class="st-kbd">Space</span></button></div></div>`;
}
function revealA(){const a=document.getElementById('st-a');if(!a||!a.hidden)return;a.hidden=false;
 document.getElementById('st-act').innerHTML=`<button class="st-miss" onclick="grade(0)">Missed <span class="st-kbd">1</span></button><button class="st-got" onclick="grade(1)">Got it <span class="st-kbd">2</span></button>`;}
function grade(ok){const q=SQ[SI];SST.s++;const k=_mk(q);if(ok){SST.c++;SMISS.delete(k);}else{SMISS.add(k);}
 _srUpdate(q,!!ok);
 if(EXAM){const d=EXAM.dom[q.ch]=EXAM.dom[q.ch]||{c:0,s:0};d.s++;if(ok)d.c++;}
 saveMiss();SI++;renderCard();}
function renderSummary(){
 const pct=SST.s?Math.round(100*SST.c/SST.s):0;
 if(EXAM){return renderExamSummary(pct);}
 const missed=SQ.filter(q=>SMISS.has(_mk(q)));
 document.getElementById('study-body').innerHTML=
  `<div class="st-sum"><h2>Session complete</h2>`+
  `<div class="st-big">${SST.c}<span>/${SST.s}</span><em>${pct}%</em></div>`+
  (missed.length?`<div class="st-misslist"><b>Review these ${missed.length}:</b>${missed.map(q=>`<div class="st-mi"><a onclick="closeStudy();goHL2('${q.id}')">${q.t}</a> &middot; ${q.q}</div>`).join('')}</div>`:`<p class="st-perfect">No misses this round.</p>`)+
  `<div class="st-sumbtn"><button onclick="studyStart()">New session</button>${SMISS.size?`<button class="st-drill" onclick="drillMissed()">Drill ${SMISS.size} missed</button>`:''}</div></div>`;
}
function renderExamSummary(pct){
 const elapsed=_fmtT(Date.now()-EXAM.t0);
 if(EXAMINT){clearInterval(EXAMINT);EXAMINT=0;}
 const verdict=pct>=90?['ok','On track — ≥90% board-readiness target']:pct>=75?['warn','Solid — close the gaps below']:['bad','Keep drilling — focus the weak domains'];
 const rows=Object.keys(EXAM.dom).map(function(d){var o=EXAM.dom[d];return{d:d,c:o.c,s:o.s,p:Math.round(100*o.c/o.s)};}).sort(function(a,b){return a.p-b.p;});
 const bars=rows.map(function(r){var cls=r.p>=90?'ok':r.p>=75?'warn':'bad';
  return `<div class="ex-dom"><span class="ex-dn">${r.d}</span><span class="ex-db"><span class="ex-df ${cls}" style="width:${r.p}%"></span></span><span class="ex-dp">${r.c}/${r.s} &middot; ${r.p}%</span></div>`;}).join('');
 const weak=rows.filter(function(r){return r.p<75;}).map(function(r){return r.d;});
 document.getElementById('study-body').innerHTML=
  `<div class="st-sum"><h2>Mock exam complete</h2>`+
  `<div class="st-big">${SST.c}<span>/${SST.s}</span><em>${pct}%</em></div>`+
  `<div class="st-badge ${verdict[0]}" style="margin:0 0 6px">${verdict[1]}</div>`+
  `<p class="st-sub" style="text-align:center">Time ${elapsed} &middot; ${SST.s} questions across ${rows.length} domains</p>`+
  `<div class="ex-doms"><div class="ex-domh">Readiness by domain (weakest first)</div>${bars}</div>`+
  `<div class="st-sumbtn"><button onclick="startExam()">New mock exam</button><button onclick="studyStart()">Study mode</button>${SMISS.size?`<button class="st-drill" onclick="drillMissed()">Drill ${SMISS.size} missed</button>`:''}</div></div>`;
}
function drillMissed(){SQ=shuf(QUIZ.filter(q=>SMISS.has(_mk(q))));SI=0;SST={c:0,s:0};if(SQ.length)renderCard();else studyStart();}
function goHL2(id){go(id);}
function toggleNav(){var r=document.querySelector('.rail');if(!r)return;var open=r.classList.toggle('navopen');
 var b=document.querySelector('.navtoggle');if(b)b.setAttribute('aria-expanded',open?'true':'false');}
function _closeNav(){var r=document.querySelector('.rail');if(r)r.classList.remove('navopen');
 var b=document.querySelector('.navtoggle');if(b)b.setAttribute('aria-expanded','false');}
function toggleTheme(){var dark=document.documentElement.getAttribute('data-theme')==='dark';
 if(dark)document.documentElement.removeAttribute('data-theme');else document.documentElement.setAttribute('data-theme','dark');
 try{localStorage.setItem('nma-theme',dark?'light':'dark');}catch(e){}
 _syncTheme();}
function _syncTheme(){var dark=document.documentElement.getAttribute('data-theme')==='dark';
 var b=document.getElementById('themebtn');if(b)b.textContent=dark?'Light':'Dark';
 var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',dark?'#0F1216':'#4A3A82');}
// Keyboard access for click-driven nav/chips (Enter or Space activates the focused item)
document.addEventListener('keydown',function(e){
 if(e.key!=='Enter'&&e.key!==' ')return;
 var t=e.target;if(t&&t.matches&&t.matches('.nav-item,.nav-ch-h,.nav-home,.rel-chip')){e.preventDefault();t.click();}
});
document.addEventListener('click',e=>{if(!e.target.closest('.sb'))closeSearch()});
// Delegated navigation: nav items and home cards are <a href="#page-ID"> (so they work
// with no JS, via :target). With JS we intercept the click here — one reliable place to
// preventDefault and route through go() — instead of a fragile inline onclick that Safari
// can run out of order with its own anchor scroll.
document.addEventListener('click',function(e){
 var a=e.target.closest&&e.target.closest('a[href^="#page-"]');
 if(!a)return;
 e.preventDefault();
 go(a.getAttribute('href').slice(6));
});
document.addEventListener('keydown',e=>{
 const el=e.target, typing=el&&(el.tagName==='INPUT'||el.tagName==='TEXTAREA'||el.isContentEditable);
 // Command palette (Ctrl/Cmd-K) — works from anywhere
 if((e.key==='k'||e.key==='K')&&(e.metaKey||e.ctrlKey)){e.preventDefault();togglePalette();return;}
 const pal=document.getElementById('palette');
 if(pal&&pal.classList.contains('on')){
  if(e.key==='Escape'){closePalette();return;}
  if(e.key==='ArrowDown'){e.preventDefault();palMove(1);return;}
  if(e.key==='ArrowUp'){e.preventDefault();palMove(-1);return;}
  if(e.key==='Enter'){e.preventDefault();palRun(PSEL);return;}
  return;
 }
 // Study Mode captures keys while open
 if(document.getElementById('study')&&document.getElementById('study').classList.contains('on')){
  if(e.key==='Escape'){closeStudy();return;}
  if(typing)return;
  const aEl=document.getElementById('st-a'), answered=aEl&&!aEl.hidden;
  if((e.key===' '||e.key==='Enter')&&document.querySelector('.st-reveal')){e.preventDefault();revealA();return;}
  if(answered&&e.key==='1'){e.preventDefault();grade(0);return;}
  if(answered&&e.key==='2'){e.preventDefault();grade(1);return;}
  return;
 }
 if(typing){
  if(el.id==='q'){
   if(e.key==='ArrowDown'){e.preventDefault();moveSel(1);return;}
   if(e.key==='ArrowUp'){e.preventDefault();moveSel(-1);return;}
   if(e.key==='Enter'){e.preventDefault();activateSel();return;}
  }
  if(e.key==='Escape'){el.blur();closeSearch();var _iv=document.getElementById('index-ov');if(_iv&&_iv.classList.contains('on'))closeIndex();}
  return;
 }
 const helpOpen=document.getElementById('help')&&document.getElementById('help').classList.contains('on');
 if(e.key==='Escape'&&helpOpen){closeHelp();return;}
 if(e.key==='?'||(e.key==='/'&&e.shiftKey)){e.preventDefault();toggleHelp();return;}
 if(e.key==='/'){e.preventDefault();const q=document.getElementById('q');if(q)q.focus();}
 else if(e.key==='ArrowRight')step(1);
 else if(e.key==='ArrowLeft')step(-1);
 else if(e.key==='Escape'){clearHL();closeSearch();closeHelp();closeMyAtlas();closeIndex();closeLightbox();}
});
window.addEventListener('hashchange',()=>{if(SUPPRESS)return;const id=location.hash.replace(/^#\/?/,'');if(id&&document.getElementById('page-'+id))go(id,true);});
try{if(localStorage.getItem('nma-hy')==='1')applyHY(true);}catch(e){}
loadPersonal();
(function(){const h=location.hash.replace(/^#\/?/,'');if(h&&document.getElementById('page-'+h))go(h,true);else go(FIRST);_syncTheme();})();