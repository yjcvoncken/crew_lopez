document.addEventListener('DOMContentLoaded', () => {
  const cards = [...document.querySelectorAll('[data-photo-page]')];
  let generation = 0;
  let frames = [];
  function measure(width) {
    const current = ++generation;
    frames.forEach(frame => frame.remove()); frames = [];
    [...new Set(cards.map(card => card.dataset.photoPage))].forEach(page => {
      const iframe = document.createElement('iframe');
      iframe.src = page; iframe.tabIndex = -1; iframe.setAttribute('aria-hidden', 'true');
      iframe.style.cssText = `position:absolute;left:-20000px;top:0;width:${width}px;height:1000px;border:0;visibility:hidden;pointer-events:none`;
      iframe.addEventListener('load', () => {
        if (current !== generation) return;
        const doc = iframe.contentDocument;
        cards.filter(card => card.dataset.photoPage === page).forEach(card => {
          const editor = card.querySelector('.image-editor');
          const url = editor.dataset.preview;
          let image = card.dataset.photoSelector ? doc.querySelector(card.dataset.photoSelector) : null;
          if (!image && url) {
            const pathname = new URL(url, location.origin).pathname;
            image = [...doc.images].find(candidate => new URL(candidate.src, location.origin).pathname === pathname);
          }
          if (!image) return;
          const box = image.getBoundingClientRect();
          if (box.width && box.height) editor.dispatchEvent(new CustomEvent('photo-frame', {detail:box.width/box.height}));
        });
      });
      document.body.append(iframe); frames.push(iframe);
    });
  }
  document.querySelectorAll('[data-photo-width]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-photo-width]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    measure(Number(button.dataset.photoWidth));
  }));
  measure(1440);
});
