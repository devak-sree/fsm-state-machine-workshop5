import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Washing Machine | Parallel & Coupled FSM", page_icon="🫧", layout="wide")

st.markdown('''<style>
.block-container{padding-top:1.1rem;max-width:1450px} h1,h2,h3{color:#0b3550}
[data-testid="stAppViewContainer"]{background:#f2f7fb}
[data-testid="stVerticalBlockBorderWrapper"]{background:white;border-radius:14px}
</style>''',unsafe_allow_html=True)

# Diagram is a self-contained interactive SVG. Users click circles/rounded rectangles
# and select labels from a popup. Progression and answer checking are handled in JS.
# Each exercise has its own interactive diagram, with an optional reference view.
HTML = r'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;color:#113b56;background:#fff}
.wrap{display:grid;grid-template-columns:33% 67%;gap:14px;padding:12px;min-height:775px}
.panel{border:1px solid #d4e4ed;border-radius:15px;padding:16px;background:#fff}
h2{margin:0 0 13px;font-size:21px}p{font-size:13px;line-height:1.5;color:#526e82}
.machine{background:#eef6fa;border-radius:12px;padding:15px;text-align:center;margin:10px 0}
.machine svg{width:175px;height:175px}.stage{background:#e4f1f8;padding:12px;border-radius:12px;font-size:13px}
.explain{background:#edf6ff;border:1px solid #cfe6fa;border-radius:11px;padding:13px;margin-top:12px;min-height:148px}
.explain b{font-size:15px}.explain small{color:#31719a;font-weight:700}
button{border:0;border-radius:9px;padding:12px 16px;font-weight:bold;cursor:pointer;background:#1673df;color:white}
button:disabled{background:#a8c7ee;cursor:not-allowed}.secondary{background:#e5eff5;color:#123d59}
.actions{display:flex;gap:8px;margin-top:12px}.actions button{flex:1}
.diagram{border:1px solid #d7e8f0;border-radius:12px;background-color:#f7fcff;background-image:radial-gradient(#d6e8f0 0.8px,transparent 0.8px);background-size:16px 16px;position:relative;overflow:hidden}
.diagram svg{display:block;width:100%;height:auto;max-height:590px}
.node{fill:#e4f6fc;stroke:#117c9d;stroke-width:3}.node.done{fill:#c9f0e4;stroke:#16916d}
.event{fill:#e6f3fa;stroke:#98c9df;stroke-width:1.6}.event.done{fill:#d9f4e6;stroke:#16916d}
.blank{cursor:pointer}.blank:hover{filter:brightness(.95)}.active{stroke:#e9a11a!important;stroke-width:4!important;fill:#fff0c7!important}
.wrong{stroke:#d83b44!important;fill:#ffe3e6!important}
.edge{stroke:#547f98;stroke-width:2.6;fill:none;marker-end:url(#arrow)}
.node-label{font-weight:700;fill:#063c57;font-size:13px;pointer-events:none;text-anchor:middle}
.event-label{font-weight:700;fill:#0e4b6c;font-size:11px;pointer-events:none;text-anchor:middle}
.caption{fill:#53798c;font-size:12px;text-anchor:middle}
.modal{display:none;position:absolute;inset:0;background:#092d416b;align-items:center;justify-content:center;padding:20px;z-index:4}
.modal.open{display:flex}.popup{background:#fff;padding:19px;border-radius:15px;max-width:380px;width:100%;box-shadow:0 12px 35px #1234}
.popup h3{margin:0 0 10px}.choices{display:grid;gap:8px}.choices button{background:#e8f4fb;color:#0b4a6b;text-align:left}.choices button:hover{background:#c9e8f7}
.banner{margin-top:9px;font-size:13px;padding:10px;border-radius:8px;background:#eaf4fb}
@media(max-width:800px){.wrap{grid-template-columns:1fr}.panel{padding:12px}.diagram svg{min-width:540px}.diagram{overflow:auto}}
</style></head><body><div class="wrap">
<div class="panel"><h2>Washing Machine</h2><p>Watch the original machine become easier to understand. Tap the highlighted blank in the diagram to complete each stage.</p>
<div class="machine"><svg viewBox="0 0 180 180" aria-label="Washing machine illustration"><rect x="27" y="8" width="126" height="164" rx="12" fill="#dbeaf2" stroke="#688ca1" stroke-width="3"/><rect x="38" y="22" width="104" height="27" rx="5" fill="#b9d3df"/><circle cx="53" cy="35" r="9" fill="white" stroke="#688ca1" stroke-width="2"/><rect x="76" y="27" width="56" height="16" rx="3" fill="#19536c"/><text x="104" y="39" font-size="9" text-anchor="middle" fill="white" font-weight="bold">READY</text><circle cx="90" cy="105" r="53" fill="#8fb5c8" stroke="#537c91" stroke-width="4"/><circle cx="90" cy="105" r="43" fill="#e5f5fc" stroke="#6b9aad" stroke-width="3"/><path d="M59 112 Q76 91 92 111 Q112 130 124 109 L124 130 Q90 156 59 130Z" fill="#65b7dc"/><path d="M68 91 l13 -14 14 14 -13 14Z" fill="white" stroke="#a3c2d3"/><path d="M100 103 l11 -13 11 13 -11 13Z" fill="white" stroke="#a3c2d3"/></svg>
<div class="stage">Current stage: <b id="stageNumber">1</b> / <b id="stageTotal"></b></div></div>
<div class="explain"><small id="stepLabel"></small><p><b id="stepTitle"></b></p><p id="stepDescription"></p><p id="stepHint"></p></div>
<div class="actions"><button id="next" disabled>Continue →</button><button class="secondary" id="focus">Go to diagram ↓</button></div>
<p style="font-size:12px">Exercise 1 separates responsibilities. Exercise 2 adds the coordination signals between them.</p>
</div>
<div class="panel"><h2 id="exerciseTitle"></h2><p id="exerciseSubtitle"></p>
<div class="diagram" id="diagram"><svg id="svg" viewBox="0 0 900 650" role="img" aria-label="Interactive state machine diagram"></svg>
<div class="modal" id="modal"><div class="popup"><h3 id="modalTitle">Choose a label</h3><div class="choices" id="choices"></div><button class="secondary" style="margin-top:12px;width:100%" id="cancel">Cancel</button></div></div></div>
<div class="actions"><button id="check">✓ Check all answers</button><button class="secondary" id="restart">↻ Restart</button></div><div class="banner" id="feedback">Tap the highlighted circle or rounded rectangle. Each correct choice unlocks the next blank.</div>
</div></div><script>
const MODE=__MODE__;
const CFG={
parallel:{title:'Exercise 1 — Simplify with Parallel FSMs',subtitle:'One large FSM becomes two smaller diagrams. Fill the highlighted state circles and transition boxes.',steps:[
{id:'a1',kind:'state',answer:'FILLING',choices:['FILLING','DOOR LOCKED','SHOW RUNNING'],title:'Separate the wash process',desc:'The washing controller handles the actual washing cycle. What comes after IDLE?',hint:'Choose the state for taking water into the drum.'},
{id:'a2',kind:'event',answer:'Water full',choices:['Water full','Door opened','Display refreshed'],title:'Transition to washing',desc:'What event allows the washing controller to leave FILLING?',hint:'Think about the water level.'},
{id:'a3',kind:'state',answer:'WASHING',choices:['WASHING','SHOW DONE','UNLOCKED'],title:'Continue the wash process',desc:'Once water has filled, what does the wash controller do?',hint:'The drum performs the main wash.'},
{id:'a4',kind:'event',answer:'Wash complete',choices:['Wash complete','Start pressed','Door unlocked'],title:'Finish the washing process',desc:'Which event moves the wash controller into DONE?',hint:'The wash process has finished.'},
{id:'b1',kind:'state',answer:'SHOW RUNNING',choices:['SHOW RUNNING','FILLING','WASHING'],title:'Separate the display responsibility',desc:'The display has its own states, separate from the wash process.',hint:'What should it show during the wash?'},
{id:'b2',kind:'event',answer:'Display timeout',choices:['Display timeout','Water full','Door locked'],title:'Independent display change',desc:'The display may return to its standby screen without changing the physical wash state.',hint:'Choose an event local to the display.'},
{id:'b3',kind:'state',answer:'STANDBY',choices:['STANDBY','SPINNING','DOOR OPEN'],title:'Display returns to standby',desc:'Complete the display controller independently.',hint:'This is a display state, not a washing operation.'}
]},
coupled:{title:'Exercise 2 — Connect with Coupled FSMs',subtitle:'Keep the two smaller controllers. Complete the signals and transition conditions that coordinate safe washing.',steps:[
{id:'d1',kind:'state',answer:'LOCKED',choices:['LOCKED','WASHING','DISPLAY ON'],title:'Door controller state',desc:'After receiving a lock request, the door controller locks the door.',hint:'Choose the safe door state.'},
{id:'d2',kind:'event',answer:'Lock confirmed',choices:['Lock confirmed','Wash complete','Start pressed'],title:'Send confirmation',desc:'What signal does the door controller send after locking?',hint:'The wash controller needs evidence that the lock succeeded.'},
{id:'w1',kind:'event',answer:'Lock confirmed',choices:['Lock confirmed','Start pressed','Water full'],title:'Wait for safe start',desc:'The wash controller must not leave WAITING until it receives the door controller’s signal.',hint:'Match the signal sent by the door controller.'},
{id:'w2',kind:'state',answer:'WASHING',choices:['WASHING','UNLOCKED','SHOW DONE'],title:'Start the cycle safely',desc:'Now that the door is locked, the wash controller can start.',hint:'Choose the next wash state.'},
{id:'w3',kind:'event',answer:'Cycle finished',choices:['Cycle finished','Door opened','Start pressed'],title:'Report completion',desc:'After the full cycle ends and the drum is safe, the wash controller informs the door controller.',hint:'The washing cycle has ended.'},
{id:'d3',kind:'event',answer:'Safe to unlock',choices:['Safe to unlock','Water full','Start pressed'],title:'Release the door safely',desc:'Which condition allows the door controller to unlock?',hint:'Unlock only after the machine reports a safe completed cycle.'},
{id:'d4',kind:'state',answer:'UNLOCKED',choices:['UNLOCKED','WASHING','FILLING'],title:'Complete the coupled system',desc:'The door returns to its unlocked state after the safe-to-unlock signal.',hint:'Choose the accessible door state.'}
]}}
const cfg=CFG[MODE], answers={}, completed=new Set();let step=0, opened=null;
const svg=document.getElementById('svg');
function defs(){return `<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#547f98"/></marker></defs>`}
function edge(x1,y1,x2,y2,dashed=false){return `<path class="edge" ${dashed?'stroke-dasharray="7 5"':''} d="M${x1} ${y1} L${x2} ${y2}"/>`}
function label(s,x,y,klass='caption'){return `<text class="${klass}" x="${x}" y="${y}">${s}</text>`}
function node(id,x,y,defaultLabel='Tap to fill',r=49){let s=cfg.steps.find(q=>q.id===id),val=answers[id]||defaultLabel;let cl=completed.has(id)?'done':step<cfg.steps.length&&cfg.steps[step].id===id?'active':'';return `<g class="blank" data-id="${id}"><circle class="node ${cl}" cx="${x}" cy="${y}" r="${r}"/>${label(val,x,y+4,'node-label')}</g>`}
function event(id,x,y,w=142){let s=cfg.steps.find(q=>q.id===id),val=answers[id]||'Tap event';let cl=completed.has(id)?'done':step<cfg.steps.length&&cfg.steps[step].id===id?'active':'';return `<g class="blank" data-id="${id}"><rect class="event ${cl}" x="${x-w/2}" y="${y-22}" width="${w}" height="44" rx="11"/>${label(val,x,y+4,'event-label')}</g>`}
function fixed(t,x,y,r=48){return `<circle class="node done" cx="${x}" cy="${y}" r="${r}"/>${label(t,x,y+4,'node-label')}`}
function panel(x,y,w,h,title){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="20" fill="#f0f8fc" stroke="#c8e3f0" stroke-width="2"/>${label(title,x+w/2,y+32,'node-label')}`}
function drawParallel(){let s=defs();s+=label('Original: one combined diagram with many state combinations',450,26);s+=`<rect x="170" y="43" width="560" height="55" rx="12" fill="#eaf3f9" stroke="#c6deeb"/>`+label('IDLE + STANDBY → FILLING + RUNNING → WASHING + RUNNING → DONE + STANDBY',450,75,'event-label');s+=edge(450,103,450,130);s+=label('Split into independent responsibilities ↓',450,122);
s+=panel(30,148,402,430,'FSM A — Washing cycle');s+=panel(468,148,402,430,'FSM B — Display');
s+=fixed('IDLE',231,225);s+=edge(231,272,231,295);s+=node('a1',231,344);s+=edge(231,391,231,425);s+=event('a2',231,416);s+=edge(231,438,231,474);s+=node('a3',231,517);s+=edge(280,517,355,517);s+=event('a4',348,470,135);s+=fixed('DONE',352,554,34);
s+=fixed('STANDBY',669,225);s+=edge(669,272,669,295);s+=node('b1',669,344);s+=edge(669,392,669,430);s+=event('b2',669,434);s+=edge(669,456,669,483);s+=node('b3',669,532);
s+=label('Two smaller diagrams are easier to read and maintain.',450,620);return s}
function drawCoupled(){let s=defs();s+=panel(30,45,395,535,'FSM A — Wash controller');s+=panel(475,45,395,535,'FSM B — Door safety');
s+=fixed('IDLE',224,133);s+=edge(224,179,224,211);s+=fixed('WAITING',224,253);s+=edge(224,301,224,369);s+=event('w1',224,335,146);s+=node('w2',224,427);s+=edge(224,477,224,516);s+=event('w3',224,516,146);s+=fixed('DONE',224,565,34);
s+=fixed('UNLOCKED',672,133);s+=edge(672,179,672,211);s+=node('d1',672,253);s+=event('d2',672,333,145);s+=edge(672,302,672,310);s+=edge(672,358,672,394);s+=fixed('WAIT SAFE',672,432);s+=event('d3',672,514,146);s+=edge(672,479,672,491);s+=node('d4',672,567,36);
s+=`<path d="M600 333 C480 333 465 335 307 335" class="edge" stroke-dasharray="7 5"/>`;
s+=`<path d="M305 517 C448 600 530 510 597 514" class="edge" stroke-dasharray="7 5"/>`;
s+=label('LOCK CONFIRMATION →',450,314);s+=label('← CYCLE COMPLETE / SAFE',450,603);return s}
function render(){svg.innerHTML=MODE==='parallel'?drawParallel():drawCoupled();document.getElementById('exerciseTitle').textContent=cfg.title;document.getElementById('exerciseSubtitle').textContent=cfg.subtitle;document.getElementById('stageNumber').textContent=Math.min(step+1,cfg.steps.length);document.getElementById('stageTotal').textContent=cfg.steps.length;
let q=cfg.steps[Math.min(step,cfg.steps.length-1)];document.getElementById('stepLabel').textContent=step===cfg.steps.length?'EXERCISE COMPLETE':`STAGE ${step+1} OF ${cfg.steps.length}`;document.getElementById('stepTitle').textContent=step===cfg.steps.length?'All diagrams completed!':q.title;document.getElementById('stepDescription').textContent=step===cfg.steps.length?'You simplified the model into smaller coordinated parts.':q.desc;document.getElementById('stepHint').textContent=step===cfg.steps.length?'Check all answers or restart to try again.':'Fill 1 highlighted blank to continue. '+q.hint;document.getElementById('next').disabled=step===cfg.steps.length||!completed.has(q.id);
svg.querySelectorAll('.blank').forEach(el=>el.addEventListener('click',()=>openChoice(el.dataset.id)));}
function openChoice(id){let q=cfg.steps[step];if(!q||id!==q.id){document.getElementById('feedback').textContent='Complete the highlighted blank first to unlock the next one.';return}opened=id;document.getElementById('modalTitle').textContent=q.kind==='state'?'Choose a state':'Choose an event or condition';let target=document.getElementById('choices');target.innerHTML='';q.choices.forEach(choice=>{let b=document.createElement('button');b.textContent=choice;b.onclick=()=>{answers[id]=choice;document.getElementById('modal').classList.remove('open');if(choice===q.answer){completed.add(id);document.getElementById('feedback').textContent='✓ Correct! Press Continue to unlock the next blank.'}else{completed.delete(id);document.getElementById('feedback').textContent='✗ Not quite. Tap the highlighted blank and try another label.'}render()};target.appendChild(b)});document.getElementById('modal').classList.add('open')}
document.getElementById('cancel').onclick=()=>document.getElementById('modal').classList.remove('open');document.getElementById('next').onclick=()=>{if(step<cfg.steps.length&&completed.has(cfg.steps[step].id)){step++;render();if(step===cfg.steps.length)document.getElementById('feedback').textContent='🎉 Exercise completed! All required labels and signals are correct.';else document.getElementById('feedback').textContent='Next blank unlocked. Tap the highlighted element.'}};
document.getElementById('focus').onclick=()=>document.getElementById('diagram').scrollIntoView({behavior:'smooth'});
document.getElementById('check').onclick=()=>{let correct=cfg.steps.filter(q=>answers[q.id]===q.answer).length;document.getElementById('feedback').textContent=`${correct} of ${cfg.steps.length} correct. ${correct===cfg.steps.length?'Excellent! You completed the diagram.':'Complete the highlighted blank to continue.'}`};
document.getElementById('restart').onclick=()=>{Object.keys(answers).forEach(k=>delete answers[k]);completed.clear();step=0;document.getElementById('feedback').textContent='Restarted. Tap the highlighted blank to begin.';render()};render();
</script></body></html>'''

st.title("Washing Machine — Parallel & Coupled FSMs")
st.caption("Two interactive diagram-completion exercises • same washing machine • click states and events • progress one stage at a time")
mode = st.radio("Choose exercise", ["1 · Parallel FSMs — simplify", "2 · Coupled FSMs — coordinate"], horizontal=True)
key = "parallel" if mode.startswith("1") else "coupled"
components.html(HTML.replace("__MODE__", json.dumps(key)), height=830, scrolling=True)
st.info("**Workshop message:** Parallel FSMs reduce the complexity of individual diagrams by separating responsibilities. Coupled FSMs exchange signals so those smaller controllers can coordinate. The overall system does not lose its underlying behaviours.")
