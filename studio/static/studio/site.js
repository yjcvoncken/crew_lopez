window.initCrewSite = function () {
  const controller = new AbortController();
  const listen = (target, name, callback) => target?.addEventListener(name, callback, {signal: controller.signal});
  const menu = document.querySelector('.menu');
  const nav = document.querySelector('nav');
  const group = document.querySelector('.nav-group');
  const trigger = document.querySelector('.nav-trigger');
  const closeSubmenu = () => {group?.classList.remove('expanded'); trigger?.setAttribute('aria-expanded', 'false');};
  const closeMenu = () => {nav?.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); if(menu)menu.textContent='☰';closeSubmenu();};
  listen(menu, 'click', () => {const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'×':'☰';});
  listen(trigger, 'click', () => {const open=group.classList.toggle('expanded');trigger.setAttribute('aria-expanded',String(open));});
  listen(document,'keydown',e=>{if(e.key==='Escape')closeMenu();});
  listen(document,'click',e=>{if(!e.target.closest('header'))closeMenu();else if(!e.target.closest('.nav-group'))closeSubmenu();});
  nav?.querySelectorAll('a').forEach(a=>listen(a,'click',closeMenu));

  const preferenceKey='crew-external-media';
  let allowed=false;
  try{allowed=localStorage.getItem(preferenceKey)==='true';}catch{}
  const map=document.querySelector('[data-map]');
  const placeholder=map?.innerHTML;
  const loadMap=()=>{
    if(!map || !map.dataset.embedUrl || map.querySelector('iframe'))return;
    const iframe=document.createElement('iframe');
    iframe.title='Crew Lopez Surfhouse in Lajares — interactive Google map';
    iframe.src=map.dataset.embedUrl;
    iframe.referrerPolicy='strict-origin-when-cross-origin';
    iframe.allowFullscreen=true;
    map.replaceChildren(iframe);map.classList.add('loaded');
  };
  const save=(value)=>{
    allowed=value;
    try{localStorage.setItem(preferenceKey,String(value));}catch{}
    if(value)loadMap();
    else if(map){map.innerHTML=placeholder;map.classList.remove('loaded');}
  };
  listen(map,'click',e=>{if(e.target.closest('.load-map'))save(true);});
  if(allowed)loadMap();
  let dialog;
  listen(document.querySelector('.cookie-settings'),'click',()=>{
    dialog?.remove();
    dialog=document.createElement('dialog');
    dialog.className='cookie-dialog';
    dialog.setAttribute('aria-labelledby','cookie-dialog-title');
    dialog.innerHTML='<h3 id="cookie-dialog-title">Your privacy, your choice.</h3><p>No advertising or analytics trackers are included. The optional Google map connects to Google only when you allow it.</p><p>External map content is currently <strong>'+(allowed?'enabled':'disabled')+'</strong>.</p><div class="cookie-actions"><button class="button" data-choice="allow">Allow map content</button><button class="button secondary" data-choice="reject">Disable map content</button><button class="button secondary" data-choice="close">Close</button></div>';
    document.body.appendChild(dialog);
    listen(dialog,'click',e=>{const choice=e.target.closest('[data-choice]')?.dataset.choice;if(!choice)return;if(choice!=='close')save(choice==='allow');dialog.close();dialog.remove();dialog=null;});
    dialog.showModal();
  });
  return () => {controller.abort();dialog?.remove();};
};
if(document.querySelector('header'))window.initCrewSite();
