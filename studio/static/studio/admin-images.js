document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.image-editor').forEach(editor => {
    const file = editor.querySelector('input[type=file]');
    const preview = editor.querySelector('.crop-preview');
    const zoom = editor.querySelector('.crop-zoom');
    const ratio = editor.querySelector('.crop-ratio');
    const data = editor.querySelector('.crop-data');
    const status = editor.querySelector('.crop-status');
    let source, objectURL, x = .5, y = .5, dragging, originalRatio;
    let fixed = editor.dataset.fixedRatio;
    if (fixed) ratio.closest('label').hidden = true;
    const frame = document.createElement('div');
    frame.className = 'crop-frame';
    preview.replaceWith(frame); frame.append(preview);
    function update(commit = true) {
      if (!source) return;
      const iw = source.naturalWidth, ih = source.naturalHeight;
      const r = fixed ? (fixed === 'original' ? originalRatio || iw/ih : Number(fixed)) : ratio.value === 'original' ? iw/ih : Number(ratio.value), z = Number(zoom.value);
      let w = Math.min(iw, ih*r)/z, h = w/r;
      const left = (iw-w)*x, top = (ih-h)*y;
      frame.style.aspectRatio = String(r);
      preview.style.width = `${iw/w*100}%`;
      preview.style.height = `${ih/h*100}%`;
      preview.style.left = `${-left/w*100}%`;
      preview.style.top = `${-top/h*100}%`;
      if (commit) {
        data.value = JSON.stringify({x:left/iw,y:top/ih,w:w/iw,h:h/ih});
        status.textContent = 'This crop will be saved. The original stored file is kept.';
      }
    }
    function load(url, replacement = false) {
      source = new Image(); source.onload = () => {
        if (!originalRatio) originalRatio = source.naturalWidth/source.naturalHeight;
        preview.src = url; x=y=.5; zoom.value=1; ratio.value='original'; data.value=''; update(false);
        if (replacement && fixed) update();
      };
      source.onerror = () => { status.textContent='Preview unavailable. You can still upload a replacement.'; };
      source.src = url;
    }
    if (editor.dataset.preview) load(editor.dataset.preview);
    editor.addEventListener('photo-frame', e => {
      fixed = String(e.detail); editor.dataset.fixedRatio = fixed;
      update(Boolean(file.files.length || data.value));
    });
    file.addEventListener('change', () => {
      if (!file.files[0]) return;
      if (objectURL) URL.revokeObjectURL(objectURL);
      objectURL = URL.createObjectURL(file.files[0]); load(objectURL, true);
      status.textContent='Image selected. Adjust the crop or save the full image.';
    });
    ['dragenter', 'dragover'].forEach(event => editor.addEventListener(event, e => {
      e.preventDefault(); editor.classList.add('is-dragging');
    }));
    editor.addEventListener('dragleave', () => editor.classList.remove('is-dragging'));
    editor.addEventListener('drop', e => {
      e.preventDefault(); editor.classList.remove('is-dragging');
      if (e.dataTransfer.files.length) {
        const transfer = new DataTransfer(); transfer.items.add(e.dataTransfer.files[0]);
        file.files = transfer.files; file.dispatchEvent(new Event('change'));
      }
    });
    frame.tabIndex = 0; frame.setAttribute('role', 'group');
    frame.setAttribute('aria-label', 'Image crop. Drag or use arrow keys to reposition.');
    frame.addEventListener('keydown', e => {
      const directions = {ArrowLeft:[.03,0],ArrowRight:[-.03,0],ArrowUp:[0,.03],ArrowDown:[0,-.03]};
      if (!directions[e.key]) return;
      e.preventDefault(); x=Math.max(0,Math.min(1,x+directions[e.key][0])); y=Math.max(0,Math.min(1,y+directions[e.key][1])); update();
    });
    zoom.addEventListener('input', () => update());
    ratio.addEventListener('change', () => update());
    frame.addEventListener('pointerdown', e => {
      if (!source) return;
      dragging={px:e.clientX,py:e.clientY,x,y}; frame.setPointerCapture(e.pointerId);
    });
    frame.addEventListener('pointermove', e => {
      if (!dragging) return;
      x=Math.max(0,Math.min(1,dragging.x-(e.clientX-dragging.px)/frame.clientWidth));
      y=Math.max(0,Math.min(1,dragging.y-(e.clientY-dragging.py)/frame.clientHeight)); update();
    });
    frame.addEventListener('pointerup', () => dragging=null);
    frame.addEventListener('pointercancel', () => dragging=null);
    editor.querySelector('.crop-reset').addEventListener('click', () => {
      x=y=.5; zoom.value=1; ratio.value='original'; update(Boolean(fixed)); if (!fixed) data.value=''; status.textContent='Crop centered and zoom reset.';
    });
  });
});
