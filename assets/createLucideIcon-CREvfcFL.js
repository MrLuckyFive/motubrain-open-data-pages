import{b as m,w as g,m as u}from"./index-tBWaGk-C.js";function w(e,t,r){try{const n=localStorage.getItem(e);return t.find(o=>o===n)??r}catch{return r}}const f=m(w("edp-language",["zh","en"],"en")),k=m(w("edp-theme",["light","dark"],"light"));g(f,e=>{document.documentElement.lang=e==="zh"?"zh-CN":"en";try{localStorage.setItem("edp-language",e)}catch{}},{immediate:!0});g(k,e=>{try{localStorage.setItem("edp-theme",e)}catch{}},{immediate:!0});function U(e,t){return f.value==="zh"?e:t}function v(e="./",t=document.baseURI){const r=new URL(e,t).href;return r.endsWith("/")?r:`${r}/`}function $(e,t=v()){return!e||/^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(e)?e:new URL(e.replace(/^\/+/,""),t).href}/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const I=e=>{for(const t in e)if(t.startsWith("aria-")||t==="role"||t==="title")return!0;return!1};/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const d=e=>e==="";/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const x=(...e)=>e.filter((t,r,n)=>!!t&&t.trim()!==""&&n.indexOf(t)===r).join(" ").trim();/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const h=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const y=e=>e.replace(/^([A-Z])|[\s-_]+(\w)/g,(t,r,n)=>n?n.toUpperCase():r.toLowerCase());/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const z=e=>{const t=y(e);return t.charAt(0).toUpperCase()+t.slice(1)};/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */var a={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const A=({name:e,iconNode:t,absoluteStrokeWidth:r,"absolute-stroke-width":n,strokeWidth:o,"stroke-width":l,size:c=a.width,color:p=a.stroke,...s},{slots:i})=>u("svg",{...a,...s,width:c,height:c,stroke:p,"stroke-width":d(r)||d(n)||r===!0||n===!0?Number(o||l||a["stroke-width"])*24/Number(c):o||l||a["stroke-width"],class:x("lucide",s.class,...e?[`lucide-${h(z(e))}-icon`,`lucide-${h(e)}`]:["lucide-icon"]),...!i.default&&!I(s)&&{"aria-hidden":"true"}},[...t.map(C=>u(...C)),...i.default?[i.default()]:[]]);/**
 * @license lucide-vue-next v0.577.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const P=(e,t)=>(r,{slots:n,attrs:o})=>u(A,{...o,...r,iconNode:t,name:e},n);export{k as a,P as c,f as l,$ as p,U as t};
