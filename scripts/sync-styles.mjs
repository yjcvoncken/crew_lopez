import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
const css = readFileSync('studio/static/studio/styles.css', 'utf8');
const inline = `<style id="crew-site-styles">${css.replaceAll('</style', '<\\/style')}</style>`;
const html = readFileSync('index.html', 'utf8');
writeFileSync('index.html', html.includes('<style id="crew-site-styles">')
  ? html.replace(/<style id="crew-site-styles">[\s\S]*?<\/style>/, () => inline)
  : html.replace('</head>', inline + '</head>'));
mkdirSync('public/static/studio', {recursive: true});
writeFileSync('public/static/studio/styles.css', css);
