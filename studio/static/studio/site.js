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

  const carouselTimers = [];
  document.querySelectorAll('[data-carousel]').forEach(carousel => {
    const slides = [...carousel.querySelectorAll('[data-slide]')];
    const controls = carousel.querySelector('.carousel-controls');
    if (slides.length < 2) return;
    controls.hidden = carousel.dataset.hideControls === 'true';
    let index = 0, timer, hovering = false, focused = false, requestVersion = 0, finishTransition;
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let paused = motion.matches;
    const autoplay = carousel.dataset.autoplay === 'true';
    const pause = carousel.querySelector('[data-carousel-pause]');
    const status = carousel.querySelector('[data-carousel-status]');
    status.hidden = carousel.dataset.sideControls === 'true';
    pause.hidden = !autoplay || carousel.dataset.sideControls === 'true';
    const prepared = new Map();
    const prepare = i => {
      const slide = slides[(i + slides.length) % slides.length];
      if (!prepared.has(slide)) {
        // Hidden lazy images otherwise start loading only after they appear.
        slide.loading = 'eager';
        prepared.set(slide, slide.decode().then(() => true, () => false));
      }
      return prepared.get(slide);
    };
    // Load one upcoming photo at a time so the first image has priority.
    if (autoplay) {
      (async () => {
        await prepare(0);
        for (let i = 1; i < slides.length && !controller.signal.aborted; i++) {
          await prepare(i);
        }
      })();
    }
    const show = async (next, announce = true) => {
      const target = (next + slides.length) % slides.length;
      const version = ++requestVersion;
      // Keep the current photo visible until the replacement is decoded.
      if (target !== index && !await prepare(target)) return;
      if (version !== requestVersion || controller.signal.aborted) return;
      finishTransition?.();
      const previous = index;
      index = target;
      slides.forEach((slide, i) => {slide.hidden = i !== index;});
      if (autoplay && !announce && previous !== index && !motion.matches && slides[index].animate) {
        const outgoing = slides[previous], incoming = slides[index];
        outgoing.hidden = false;
        carousel.classList.add('is-sliding');
        const options = {duration: 550, easing: 'cubic-bezier(.22,.61,.36,1)', fill: 'both'};
        const animations = [
          outgoing.animate([{transform: 'translateX(0)'}, {transform: 'translateX(-100%)'}], options),
          incoming.animate([{transform: 'translateX(100%)'}, {transform: 'translateX(0)'}], options),
        ];
        const finish = () => {
          if (finishTransition !== finish) return;
          finishTransition = undefined;
          outgoing.hidden = true;
          carousel.classList.remove('is-sliding');
          animations.forEach(animation => animation.cancel());
        };
        finishTransition = finish;
        Promise.allSettled(animations.map(animation => animation.finished)).then(finish);
      }
      status.setAttribute('aria-live', announce ? 'polite' : 'off');
      status.textContent = `${index + 1} / ${slides.length}`;
      prepare(index + 1);
      if (!autoplay) prepare(index - 1);
    };
    const schedule = () => {
      clearInterval(timer);
      pause.textContent = paused ? 'Play slideshow' : 'Pause slideshow';
      if (autoplay && !paused && !hovering && !focused && !document.hidden) {
        timer = setInterval(() => show(index + 1, false), 4000);
      }
    };
    const move = direction => {show(index + direction); schedule();};
    listen(carousel.querySelector('[data-previous]'), 'click', () => move(-1));
    listen(carousel.querySelector('[data-next]'), 'click', () => move(1));
    listen(carousel, 'keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1);
    });
    listen(pause, 'click', () => {paused = !paused; schedule();});
    listen(carousel, 'mouseenter', () => {hovering = true; schedule();});
    listen(carousel, 'mouseleave', () => {hovering = false; schedule();});
    listen(carousel, 'focusin', () => {focused = true; schedule();});
    listen(carousel, 'focusout', event => {focused = carousel.contains(event.relatedTarget); schedule();});
    listen(document, 'visibilitychange', schedule);
    listen(motion, 'change', () => {if(motion.matches) paused = true; schedule();});
    carouselTimers.push(() => {clearInterval(timer); finishTransition?.();});
    show(0, false); schedule();
  });

  const preferenceKey='crew-external-media';
  let allowed=false;
  try{allowed=localStorage.getItem(preferenceKey)==='true';}catch{}
  const map=document.querySelector('[data-map]');
  const placeholder=map?.innerHTML;
  const loadMap=()=>{
    if(!map || !map.dataset.embedUrl || map.querySelector('iframe'))return;
    const iframe=document.createElement('iframe');
    iframe.title='Crew Lopez Surfhouse in Lajares - interactive Google map';
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
  return () => {controller.abort();carouselTimers.forEach(stop => stop());dialog?.remove();};
};
if(document.querySelector('header'))window.initCrewSite();
