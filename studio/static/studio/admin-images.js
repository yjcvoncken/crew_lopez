document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.image-editor').forEach(editor => {
    const file = editor.querySelector('input[type=file]');
    const preview = editor.querySelector('.crop-preview');
    const zoom = editor.querySelector('.crop-zoom');
    const ratio = editor.querySelector('.crop-ratio');
    const data = editor.querySelector('.crop-data');
    const status = editor.querySelector('.crop-status');
    let source, objectURL, x = .5, y = .5, dragging;
    const frame = document.createElement('div');
    frame.className = 'crop-frame';
    preview.replaceWith(frame); frame.append(preview);
    function update(commit = true) {
      if (!source) return;
      const r = Number(ratio.value), z = Number(zoom.value);
      const iw = source.naturalWidth, ih = source.naturalHeight;
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
    function load(url) {
      source = new Image(); source.onload = () => {
        preview.src = url; x=y=.5; zoom.value=1; data.value=''; update(false);
      };
      source.onerror = () => { status.textContent='Preview unavailable. You can still upload a replacement.'; };
      source.src = url;
    }
    if (file.name === 'homepage_photo') ratio.value='1.7777778';
    if (file.name === 'graphic_element') ratio.value='1';
    if (editor.dataset.preview) load(editor.dataset.preview);
    file.addEventListener('change', () => {
      if (!file.files[0]) return;
      if (objectURL) URL.revokeObjectURL(objectURL);
      objectURL = URL.createObjectURL(file.files[0]); load(objectURL);
      status.textContent='Image selected. Adjust the crop or save the full image.';
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
      x=y=.5; zoom.value=1; update(false); data.value=''; status.textContent='Crop cleared. The full image will be saved.';
    });
  });
});
