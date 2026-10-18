
'use strict';
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const page = document.body.dataset.page;
const params = new URLSearchParams(location.search);
const KEY = 'napkin2code.projects.v1';
const ACTIVE = 'napkin2code.active.v1';
let projects = [];
let project = null;
let busy = false;
let toastTimer;
let storageOK = true;
function toast(message) {
  const box = $('#toast'); box.textContent = message; box.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => box.hidden = true, 5000);
}
function error(message) {
  const box = $('#page-error');
  if (box) { box.textContent = message; box.hidden = false; box.scrollIntoView({behavior:'smooth',block:'nearest'}); }
  else toast(message);
}
function clearError() { const box = $('#page-error'); if (box) box.hidden = true; }
function bind(id, event, fn) {
  const node = $(id);
  if (node) node.addEventListener(event, async e => {
    try { await fn(e); } catch (err) { error(err.message || 'Something went wrong. Please try again.'); }
  });
}
function node(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
}
function isSpec(spec) {
  return spec && typeof spec === 'object' && typeof spec.title === 'string' &&
    spec.title.trim().length > 0 && spec.title.length <= 200 &&
    Array.isArray(spec.elements) && spec.elements.length > 0 && spec.elements.length <= 100 &&
    spec.elements.every(e => e && typeof e === 'object' && typeof e.type === 'string' && e.type.trim());
}
function validProject(p) {
  return p && typeof p.id === 'string' && /^[a-zA-Z0-9-]{1,80}$/.test(p.id) &&
    typeof p.title === 'string' && p.title.length <= 200 &&
    (!p.spec || isSpec(p.spec)) && typeof p.html === 'string' && p.html.length <= 1e6 &&
    typeof p.image === 'string' && (!p.image || /^data:image\/(jpeg|png|webp);base64,/.test(p.image)) &&
    p.image.length < 3e6 && Array.isArray(p.versions) && p.versions.length <= 8 &&
    p.versions.every(v => v && typeof v.html === 'string' && v.html.length <= 1e6 &&
      typeof v.label === 'string' && typeof v.time === 'number');
}
function loadProjects() {
  try {
    const data = JSON.parse(localStorage.getItem(KEY) || '[]');
    projects = Array.isArray(data) ? data.filter(validProject) : [];
    const active = localStorage.getItem(ACTIVE);
    project = projects.find(p => p.id === (params.get('project') || active)) || null;
  } catch (_) { storageOK = false; error('Browser storage is unavailable. Enable site storage to save projects.'); }
}
function saveProject() {
  if (!project) return false;
  project.updated = Date.now();
  const index = projects.findIndex(p => p.id === project.id);
  if (index < 0) projects.unshift(project); else projects[index] = project;
  try {
    localStorage.setItem(KEY, JSON.stringify(projects));
    localStorage.setItem(ACTIVE, project.id);
    storageOK = true;
    if ($('#save-status')) $('#save-status').textContent = 'Saved in this browser';
    return true;
  } catch (_) {
    storageOK = false;
    if ($('#save-status')) $('#save-status').textContent = 'Not saved — download your HTML';
    error('Browser storage is full or unavailable. Download your HTML or export a project backup before leaving this page.');
    return false;
  }
}
function newProject() {
  project = {id: crypto.randomUUID(),title:'Untitled sketch',image:'',spec:null,html:'',versions:[],
    instruction:'',updated:Date.now(),archived:false};
  return project;
}
async function api(path, body) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 420000);
  try {
    const headers = {'X-Napkin-Request':'1'};
    if (body && !(body instanceof FormData)) headers['Content-Type'] = 'application/json';
    const response = await fetch('/api/' + path, {method:body === undefined ? 'GET':'POST',headers,
      body:body === undefined ? undefined : body instanceof FormData ? body : JSON.stringify(body),
      signal:controller.signal});
    const data = await response.json().catch(() => ({error:'The server returned an unreadable response.'}));
    if (!response.ok) throw new Error(data.error || 'The request could not be completed.');
    return data;
  } catch (err) {
    if (err.name === 'AbortError') throw new Error('This request took too long. Check your API connection and try again.');
    if (err instanceof TypeError) throw new Error('Cannot reach the local server. Start python app.py and try again.');
    throw err;
  } finally { clearTimeout(timer); }
}
async function runBusy(title, fn) {
  if (busy) return;
  busy = true; clearError();
  const cover = $('#busy-cover'); $('#busy-title').textContent = title; cover.hidden = false;
  const start = Date.now(); $('#busy-time').textContent = '0s elapsed';
  const timer = setInterval(() => $('#busy-time').textContent = Math.floor((Date.now()-start)/1000) + 's elapsed',1000);
  document.querySelector('main')?.setAttribute('aria-busy','true');
  try { return await fn(); }
  finally { busy = false; clearInterval(timer); cover.hidden = true; document.querySelector('main')?.removeAttribute('aria-busy'); }
}
async function health() {
  try {
    const result = await api('health');
    const label = {ready:'Model configured',needs_key:'API key needed',needs_model:'Discover model'}[result.status] || 'Check setup';
    $$('[data-health]').forEach(el => el.textContent = label);
    $$('[data-model]').forEach(el => el.textContent = result.model || 'No model selected');
  } catch (_) { $$('[data-health]').forEach(el => el.textContent = 'Server unavailable'); }
}
function download(text, name, type='text/html') {
  const url = URL.createObjectURL(new Blob([text], {type}));
  const link = node('a'); link.href = url; link.download = name; document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
async function copy(text) {
  try { await navigator.clipboard.writeText(text); toast('Copied to clipboard.'); }
  catch (_) { throw new Error('Clipboard access was blocked. Select the code and copy it manually.'); }
}
function filename(title) { return (title.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,70) || 'napkin2code') + '.html'; }
async function resizeImage(file) {
  if (!file || file.size > 10 * 1024 * 1024) throw new Error('Choose an image smaller than 10 MB.');
  if (!['image/png','image/jpeg','image/webp'].includes(file.type)) throw new Error('Choose a JPG, PNG or WebP image.');
  let bitmap;
  try { bitmap = await createImageBitmap(file); } catch (_) { throw new Error('This image could not be read. Try another photo.'); }
  if (bitmap.width * bitmap.height > 25000000) { bitmap.close(); throw new Error('This image is too large. Resize it below 25 megapixels.'); }
  const scale = Math.min(1, 1024 / Math.max(bitmap.width,bitmap.height));
  const canvas = document.createElement('canvas');
  canvas.width = Math.max(1,Math.round(bitmap.width*scale)); canvas.height = Math.max(1,Math.round(bitmap.height*scale));
  const ctx = canvas.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.drawImage(bitmap,0,0,canvas.width,canvas.height); bitmap.close();
  return {data:canvas.toDataURL('image/jpeg',.88),width:canvas.width,height:canvas.height};
}
async function imageBlob(dataURL) { const binary = atob(dataURL.split(',')[1]); return new Blob([Uint8Array.from(binary, c => c.charCodeAt(0))], {type:'image/jpeg'}); }
function formForImage(dataURL) {
  return imageBlob(dataURL).then(blob => { const form = new FormData(); form.append('image',blob,'sketch.jpg'); return form; });
}
function setupProjects() {
  let filter = 'all';
  function render() {
    const query = $('#project-search').value.toLowerCase();
    let shown = projects.filter(p => filter === 'archived' ? p.archived : !p.archived)
      .filter(p => p.title.toLowerCase().includes(query)).sort((a,b) => b.updated-a.updated);
    if (filter === 'recent') shown = shown.slice(0,6);
    $('#project-count').textContent = projects.filter(p => !p.archived).length;
    $('#project-grid').replaceChildren(); $('#projects-empty').hidden = shown.length > 0;
    if (!shown.length && projects.length) {
      $('#projects-empty h2').textContent = 'No matching projects.';
      $('#projects-empty p').textContent = 'Try another search or switch the project filter.';
    }
    for (const p of shown) {
      const card = node('article','card project-card');
      const thumb = node('div','project-thumb'); const image = node('img');
      image.src = p.image || '/samples/login-sketch.png'; image.alt = 'Sketch for ' + p.title; thumb.append(image);
      const content = node('div','project-content');
      content.append(node('span','tiny-tag',p.html ? 'READY TO PREVIEW' : p.spec ? 'READY TO GENERATE' : 'DRAFT'),
        node('h2','',p.title),node('p','',new Date(p.updated).toLocaleString()));
      const actions = node('div','actions'); const open = node('a','button primary small','Open workspace');
      open.href = '/' + (p.html ? 'builder' : p.spec ? 'review' : 'scan') + '?project=' + encodeURIComponent(p.id);
      const archive = node('button','archive-button',p.archived?'Restore':'Archive');
      archive.addEventListener('click',() => { project = p; p.archived = !p.archived; saveProject(); render(); });
      actions.append(open,archive); content.append(actions); card.append(thumb,content); $('#project-grid').append(card);
    }
  }
  $$('[data-filter]').forEach(btn => btn.addEventListener('click',() => {
    filter = btn.dataset.filter; $$('[data-filter]').forEach(b => b.classList.toggle('active',b===btn)); render();
  }));
  bind('#project-search','input',render); render();
}
async function setupScan() {
  const editMode = params.get('mode') === 'edit';
  let stream = null, selected = '', cameraRequest = 0;
  if (!project || params.has('new') || params.has('sample')) newProject();
  $('#project-title').value = project.title === 'Untitled sketch' ? '' : project.title;
  $('#project-instruction').value = project.instruction || '';
  if (editMode && !project.html) { error('Generate a website before applying sketch edits.'); }
  if (editMode && project.html) {
    $('#analyze-sketch').textContent = 'Apply edit from sketch';
    $('#project-instruction').value = '';
    $('#project-title').readOnly = true;
    $('.flow-heading h1').textContent = 'Show us what changed.';
  }
  function stopCamera() {
    cameraRequest++;
    stream?.getTracks().forEach(t => t.stop()); stream = null;
    $('#camera-video').srcObject = null; $('#camera-video').hidden = true;
    $('#camera-guide').hidden = true; $('#camera-controls').hidden = true;
    $('#camera-empty').hidden = !!selected;
    $('#capture-status').textContent = selected ? 'Image selected' : 'Ready to capture';
  }
  function display(data, width, height) {
    stopCamera(); selected = data; $('#capture-image').src = data; $('#capture-image').hidden = false;
    $('#camera-empty').hidden = true; $('#retake').hidden = false;
    $('#analyze-sketch').disabled = editMode && !project.html;
    $('#capture-status').textContent = 'Image selected';
    $('#image-info').textContent = width ? width + ' × ' + height + ' px' : 'Ready to analyze';
  }
  async function choose(file) {
    clearError(); const img = await resizeImage(file); display(img.data,img.width,img.height);
  }
  async function startCamera(deviceId) {
    stopCamera(); const requestId = cameraRequest; clearError();
    if (!navigator.mediaDevices?.getUserMedia) throw new Error('Camera access needs localhost or HTTPS. You can upload a photo instead.');
    try {
      const acquired = await navigator.mediaDevices.getUserMedia({video:deviceId ? {deviceId:{exact:deviceId}} : {facingMode:'environment',width:{ideal:1600}},audio:false});
      if (requestId !== cameraRequest) { acquired.getTracks().forEach(t=>t.stop()); return; }
      stream = acquired; const video = $('#camera-video'); video.srcObject = stream;
      await video.play(); video.hidden = false; $('#capture-image').hidden = true; $('#camera-empty').hidden = true;
      $('#camera-guide').hidden = false; $('#camera-controls').hidden = false;
      $('#capture-status').textContent = 'Live preview — capture to analyze';
      const cameras = (await navigator.mediaDevices.enumerateDevices()).filter(d => d.kind === 'videoinput');
      $('#camera-select').replaceChildren(...cameras.map((d,i) => {
        const option = node('option','',d.label || 'Camera '+(i+1)); option.value = d.deviceId; return option;
      }));
      $('#camera-select').value = stream.getVideoTracks()[0].getSettings().deviceId || '';
    } catch (err) {
      stopCamera();
      throw new Error(err.name === 'NotAllowedError' ? 'Camera permission was denied. Allow access in your browser or upload a photo.' :
        err.name === 'NotFoundError' ? 'No camera was found. Upload a sketch photo instead.' :
        'The camera could not start. Close other camera apps or upload a photo.');
    }
  }
  bind('#start-camera','click',()=>startCamera());
  bind('#camera-select','change',e=>startCamera(e.target.value));
  bind('#stop-camera','click',stopCamera);
  bind('#capture-photo','click',async()=>{
    const video=$('#camera-video'); if (!video.videoWidth) throw new Error('Wait for the camera to start.');
    const canvas=document.createElement('canvas'); canvas.width=video.videoWidth; canvas.height=video.videoHeight;
    canvas.getContext('2d').drawImage(video,0,0);
    const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.9)); await choose(blob);
  });
  bind('#retake','click',()=>{stopCamera(); selected=''; $('#capture-image').hidden=true; $('#camera-empty').hidden=false;
    $('#analyze-sketch').disabled=true; $('#retake').hidden=true; $('#image-info').textContent=''; $('#sketch-file').value='';});
  bind('#sketch-file','change',e=>e.target.files[0] && choose(e.target.files[0]));
  const drop=$('#dropzone');
  for (const type of ['dragenter','dragover']) drop.addEventListener(type,e=>{e.preventDefault();drop.classList.add('dragging');});
  for (const type of ['dragleave','drop']) drop.addEventListener(type,e=>{e.preventDefault();drop.classList.remove('dragging');});
  bind('#dropzone','drop',e=>e.dataTransfer.files[0] && choose(e.dataTransfer.files[0]));
  async function sample() {
    const response=await fetch('/samples/login-sketch.png'); if (!response.ok) throw new Error('The sample sketch could not be loaded.');
    await choose(await response.blob()); if (!$('#project-title').value) $('#project-title').value='Simple login page';
    toast('Sample loaded. Analyze it when you are ready.');
  }
  bind('#sample-sketch','click',sample);
  bind('#analyze-sketch','click',()=>runBusy(editMode?'Reading your annotations…':'Reading your sketch…',async()=>{
    if (!selected) throw new Error('Capture or upload a sketch first.');
    const form=await formForImage(selected);
    if (editMode) {
      form.append('html',project.html); form.append('instruction',$('#project-instruction').value);
      const result=await api('edit',form); addVersion(result.html,'Edit from sketch');
      if(saveProject()) location.href='/builder';
    } else {
      form.append('title',$('#project-title').value); form.append('instruction',$('#project-instruction').value);
      const result=await api('analyze',form); project.image=selected; project.spec=result.spec;
      project.title=result.spec.title; project.instruction=$('#project-instruction').value;
      if(saveProject()) location.href='/review';
    }
  }));
  window.addEventListener('pagehide',stopCamera);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stopCamera();});
  if(project.image && !editMode) display(project.image);
  if(params.has('sample')) await sample();
}
function setupReview() {
  if(!project?.spec){$('#review-empty').hidden=false;$('#review-workspace').hidden=true;$('#review-actions').hidden=true;return;}
  $('#review-image').src=project.image;
  let spec=structuredClone(project.spec), tab='outline';
  function render() {
    $('#visual-outline').replaceChildren();
    const titleCard=node('div','card spec-card'); const label=node('label','','Page title'); label.htmlFor='outline-title';
    const input=node('input');input.id='outline-title';input.value=spec.title;input.maxLength=200;
    input.addEventListener('input',()=>spec.title=input.value);titleCard.append(label,input);$('#visual-outline').append(titleCard);
    spec.elements.forEach((el,index)=>{
      const card=node('details','card spec-card');card.open=true;
      const summary=node('summary');summary.append(node('span','number',String(index+1).padStart(2,'0')),node('span','',el.type));
      card.append(summary);
      for(const [key,value] of Object.entries(el)){
        const label=node('label','',key.replaceAll('_',' ')); const id='element-'+index+'-'+key.replace(/[^a-z0-9]/gi,'');
        label.htmlFor=id; const field=node(typeof value==='object'?'textarea':'input');field.id=id;
        field.value=typeof value==='object'?JSON.stringify(value,null,2):String(value);
        field.addEventListener('change',()=>{
          if(typeof value==='object'){try{el[key]=JSON.parse(field.value);field.setCustomValidity('');}catch(_){field.setCustomValidity('Enter valid JSON.');field.reportValidity();}}
          else el[key]=field.value;
        });card.append(label,field);
      }
      $('#visual-outline').append(card);
    });
    $('#spec-json').value=JSON.stringify(spec,null,2);
    const notes=Array.isArray(spec.notes)?spec.notes.map(n=>typeof n==='string'?n:JSON.stringify(n)).join(' '):typeof spec.notes==='string'?spec.notes:'';
    $('#spec-notes').hidden=!notes;$('#spec-notes').textContent=notes;
  }
  function readJson() { let parsed; try{parsed=JSON.parse($('#spec-json').value);}catch(_){throw new Error('The JSON has a syntax error. Fix it before continuing.');}
    if(!isSpec(parsed))throw new Error('The specification needs a title and at least one element with a type.');spec=parsed;}
  $$('[data-review-tab]').forEach(btn=>btn.addEventListener('click',()=>{
    try{if(tab==='json')readJson();if(tab==='outline')$('#spec-json').value=JSON.stringify(spec,null,2);
      tab=btn.dataset.reviewTab;if(tab==='outline')render();
      $('#visual-outline').hidden=tab!=='outline';$('#json-panel').hidden=tab!=='json';
      $$('[data-review-tab]').forEach(b=>{b.classList.toggle('active',b===btn);b.setAttribute('aria-selected',b===btn);});clearError();
    }catch(err){error(err.message);}
  }));
  bind('#contrast-toggle','click',e=>{const active=$('.source-panel').classList.toggle('contrast');e.currentTarget.setAttribute('aria-pressed',active);});
  bind('#generate-website','click',()=>runBusy('Building your website…',async()=>{
    if(tab==='json')readJson();
    const invalid=$('#visual-outline :invalid');if(invalid){invalid.reportValidity();throw new Error('Fix the highlighted specification field.');}
    if(!isSpec(spec))throw new Error('Add a page title and valid elements before generating.');
    const result=await api('generate',{spec});project.spec=result.spec;project.title=spec.title;project.model=result.model;
    addVersion(result.html,'Generated from sketch');if(saveProject())location.href='/builder';
  }));
  render();
}
function addVersion(html,label) {
  if(!/<html[\s>]/i.test(html)||!/<\/html\s*>/i.test(html))throw new Error('The response is not a complete HTML document.');
  if(project.html)project.versions.unshift({html:project.html,label:project.versionLabel||'Previous version',time:project.versionTime||Date.now()});
  project.versions=project.versions.slice(0,5);project.html=html;project.versionLabel=label;project.versionTime=Date.now();
}
async function setupBuilder() {
  if(!project?.html){$('#builder-empty').hidden=false;$('#builder-workspace').hidden=true;return;}
  let editImage=null,previewId=0;
  async function render() {
    $('#builder-title').textContent=project.title;$('#code-editor').value=project.html;
    $('#builder-spec').textContent=JSON.stringify(project.spec,null,2);$('#undo-edit').disabled=!project.versions.length;
    $('#version-list').replaceChildren();
    for(const version of [{label:project.versionLabel||'Current version',time:project.versionTime||project.updated},...project.versions]){
      const item=node('li','',version.label);item.append(node('small','',new Date(version.time).toLocaleString()));$('#version-list').append(item);
    }
    const token=++previewId;const result=await api('preview',{html:project.html});
    if(token===previewId)$('#live-preview').src=result.url;
  }
  function device(mode) {
    $('.preview-stage').classList.toggle('mobile',mode==='mobile');
    for(const kind of ['desktop','mobile']){const btn=$('#'+kind+'-view');btn.classList.toggle('active',kind===mode);btn.setAttribute('aria-pressed',kind===mode);}
  }
  try{device(localStorage.getItem('napkin2code.preview')||'desktop');}catch(_){}
  bind('#desktop-view','click',()=>device('desktop'));bind('#mobile-view','click',()=>device('mobile'));
  $$('[data-builder-tab]').forEach(btn=>btn.addEventListener('click',()=>{
    for(const b of $$('[data-builder-tab]')){const active=b===btn;b.classList.toggle('active',active);b.setAttribute('aria-selected',active);
      $('#'+b.dataset.builderTab+'-panel').hidden=!active;}
    $('.device-buttons').hidden=btn.dataset.builderTab!=='preview';
  }));
  bind('#download-html','click',()=>{download(project.html,filename(project.title));toast('HTML download started.');});
  bind('#copy-code','click',()=>copy($('#code-editor').value));bind('#copy-spec','click',()=>copy(JSON.stringify(project.spec,null,2)));
  bind('#apply-code','click',async()=>{addVersion($('#code-editor').value,'Manual code edit');saveProject();await render();toast('Code changes applied.');});
  bind('#undo-edit','click',async()=>{
    if(!project.versions.length)return;const previous=project.versions.shift();project.html=previous.html;
    project.versionLabel=previous.label;project.versionTime=previous.time;saveProject();await render();toast('Previous version restored.');
  });
  async function applyEdit(sketch) {
    const instruction=$('#edit-instruction').value.trim();
    if(!instruction&&!sketch)throw new Error('Describe the change you want to make.');
    if(sketch&&!editImage)throw new Error('Choose an annotated sketch first.');
    await runBusy(sketch?'Reading your annotations…':'Applying your changes…',async()=>{
      let payload={html:project.html,instruction};
      if(sketch){payload=await formForImage(editImage);payload.append('html',project.html);payload.append('instruction',instruction);}
      const result=await api('edit',payload);addVersion(result.html,sketch?'Edit from sketch':instruction.slice(0,80));
      saveProject();await render();$('#edit-instruction').value='';toast('Your changes are ready.');
    });
  }
  bind('#apply-edit','click',()=>applyEdit(false));bind('#apply-sketch-edit','click',()=>applyEdit(true));
  bind('#edit-file','change',async e=>{const file=e.target.files[0];if(!file)return;const image=await resizeImage(file);
    editImage=image.data;$('#edit-file-name').textContent=file.name;$('#apply-sketch-edit').disabled=false;});
  await render();
}
function setupSettings() {
  function usage(){let size=0;try{size=new Blob([localStorage.getItem(KEY)||'']).size;}catch(_){}
    $('#storage-usage').textContent=projects.length+' projects · '+(size/1024).toFixed(0)+' KB saved';}
  bind('#export-projects','click',()=>download(JSON.stringify({format:'napkin2code-v1',projects},null,2),'napkin2code-backup.json','application/json'));
  bind('#import-projects','change',async e=>{
    const file=e.target.files[0];if(!file)return;if(file.size>10*1024*1024)throw new Error('Choose a project backup smaller than 10 MB.');
    let data;try{data=JSON.parse(await file.text());}catch(_){throw new Error('This backup is not valid JSON.');}
    if(data.format!=='napkin2code-v1'||!Array.isArray(data.projects)||data.projects.length>100||!data.projects.every(validProject))
      throw new Error('This file is not a valid Napkin2Code project backup.');
    const merged=new Map(projects.map(p=>[p.id,p]));for(const p of data.projects)merged.set(p.id,p);
    const next=[...merged.values()];try{localStorage.setItem(KEY,JSON.stringify(next));}catch(_){throw new Error('There is not enough browser storage for this backup.');}
    projects=next;usage();toast('Project backup restored.');
  });
  try{$('#default-preview').value=localStorage.getItem('napkin2code.preview')||'desktop';}catch(_){}
  bind('#default-preview','change',e=>{localStorage.setItem('napkin2code.preview',e.target.value);toast('Preview preference saved.');});usage();
}
async function main(){
  loadProjects(); await health();
  if(page==='projects')setupProjects();
  if(page==='scan')await setupScan();
  if(page==='review')setupReview();
  if(page==='builder')await setupBuilder();
  if(page==='settings')setupSettings();
  bind('#discover-models','click',()=>runBusy('Discovering an image-capable Gemma model…',async()=>{
    const result=await api('discover',{});$('#discovery-result').textContent='Image input verified. Selected: '+result.name;
    $('#discovery-result').hidden=false;await health();
  }));
}
main().catch(err=>error(err.message));
