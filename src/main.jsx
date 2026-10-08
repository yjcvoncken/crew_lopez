import React, {useEffect} from 'react';
import {createRoot} from 'react-dom/client';
import pages from './pages.json';
import '../studio/static/studio/site.js';

function App(){
 const route = window.location.pathname.replace(/\/?$/, '/') || '/';
 const page = pages[route];
 useEffect(()=>{
  document.title = page?.title || 'Page not found - Crew Lopez';
  return window.initCrewSite?.();
 },[page]);
 if(!page)return <main className="section"><p className="eyebrow">CREW LOPEZ</p><h1>A little off course.</h1><p>This page doesn’t exist. Let’s get you back to the house.</p><a className="button" href="/">Back home ↗</a></main>;
 return <div dangerouslySetInnerHTML={{__html:page.html}}/>;
}
createRoot(document.getElementById('root')).render(<App/>);
