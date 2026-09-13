(function(){const n=document.createElement("link").relList;if(n&&n.supports&&n.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))a(r);new MutationObserver(r=>{for(const i of r)if(i.type==="childList")for(const o of i.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&a(o)}).observe(document,{childList:!0,subtree:!0});function t(r){const i={};return r.integrity&&(i.integrity=r.integrity),r.referrerPolicy&&(i.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?i.credentials="include":r.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function a(r){if(r.ep)return;r.ep=!0;const i=t(r);fetch(r.href,i)}})();var we={exports:{}},Ee={exports:{}},Ae={exports:{}};/*!
  * Bootstrap data.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var wa=Ae.exports,It;function Ea(){return It||(It=1,function(e,n){(function(t,a){e.exports=a()})(wa,function(){const t=new Map;return{set(r,i,o){t.has(r)||t.set(r,new Map);const s=t.get(r);if(!s.has(i)&&s.size!==0){console.error(`Bootstrap doesn't allow more than one instance per element. Bound instance: ${Array.from(s.keys())[0]}.`);return}s.set(i,o)},get(r,i){return t.has(r)&&t.get(r).get(i)||null},remove(r,i){if(!t.has(r))return;const o=t.get(r);o.delete(i),o.size===0&&t.delete(r)}}})}(Ae)),Ae.exports}var Ce={exports:{}},ce={exports:{}};/*!
  * Bootstrap index.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Aa=ce.exports,Pt;function ne(){return Pt||(Pt=1,function(e,n){(function(t,a){a(n)})(Aa,function(t){const i="transitionend",o=c=>(c&&window.CSS&&window.CSS.escape&&(c=c.replace(/#([^\s"#']+)/g,(g,h)=>`#${CSS.escape(h)}`)),c),s=c=>c==null?`${c}`:Object.prototype.toString.call(c).match(/\s([a-z]+)/i)[1].toLowerCase(),l=c=>{do c+=Math.floor(Math.random()*1e6);while(document.getElementById(c));return c},f=c=>{if(!c)return 0;let{transitionDuration:g,transitionDelay:h}=window.getComputedStyle(c);const y=Number.parseFloat(g),C=Number.parseFloat(h);return!y&&!C?0:(g=g.split(",")[0],h=h.split(",")[0],(Number.parseFloat(g)+Number.parseFloat(h))*1e3)},d=c=>{c.dispatchEvent(new Event(i))},m=c=>!c||typeof c!="object"?!1:(typeof c.jquery<"u"&&(c=c[0]),typeof c.nodeType<"u"),S=c=>m(c)?c.jquery?c[0]:c:typeof c=="string"&&c.length>0?document.querySelector(o(c)):null,x=c=>{if(!m(c)||c.getClientRects().length===0)return!1;const g=getComputedStyle(c).getPropertyValue("visibility")==="visible",h=c.closest("details:not([open])");if(!h)return g;if(h!==c){const y=c.closest("summary");if(y&&y.parentNode!==h||y===null)return!1}return g},T=c=>!c||c.nodeType!==Node.ELEMENT_NODE||c.classList.contains("disabled")?!0:typeof c.disabled<"u"?c.disabled:c.hasAttribute("disabled")&&c.getAttribute("disabled")!=="false",w=c=>{if(!document.documentElement.attachShadow)return null;if(typeof c.getRootNode=="function"){const g=c.getRootNode();return g instanceof ShadowRoot?g:null}return c instanceof ShadowRoot?c:c.parentNode?w(c.parentNode):null},I=()=>{},k=c=>{c.offsetHeight},F=()=>window.jQuery&&!document.body.hasAttribute("data-bs-no-jquery")?window.jQuery:null,N=[],L=c=>{document.readyState==="loading"?(N.length||document.addEventListener("DOMContentLoaded",()=>{for(const g of N)g()}),N.push(c)):c()},M=()=>document.documentElement.dir==="rtl",p=c=>{L(()=>{const g=F();if(g){const h=c.NAME,y=g.fn[h];g.fn[h]=c.jQueryInterface,g.fn[h].Constructor=c,g.fn[h].noConflict=()=>(g.fn[h]=y,c.jQueryInterface)}})},v=(c,g=[],h=c)=>typeof c=="function"?c.call(...g):h,E=(c,g,h=!0)=>{if(!h){v(c);return}const C=f(g)+5;let _=!1;const D=({target:j})=>{j===g&&(_=!0,g.removeEventListener(i,D),v(c))};g.addEventListener(i,D),setTimeout(()=>{_||d(g)},C)},P=(c,g,h,y)=>{const C=c.length;let _=c.indexOf(g);return _===-1?!h&&y?c[C-1]:c[0]:(_+=h?1:-1,y&&(_=(_+C)%C),c[Math.max(0,Math.min(_,C-1))])};t.defineJQueryPlugin=p,t.execute=v,t.executeAfterTransition=E,t.findShadowRoot=w,t.getElement=S,t.getNextActiveElement=P,t.getTransitionDurationFromElement=f,t.getUID=l,t.getjQuery=F,t.isDisabled=T,t.isElement=m,t.isRTL=M,t.isVisible=x,t.noop=I,t.onDOMContentLoaded=L,t.parseSelector=o,t.reflow=k,t.toType=s,t.triggerTransitionEnd=d,Object.defineProperty(t,Symbol.toStringTag,{value:"Module"})})}(ce,ce.exports)),ce.exports}/*!
  * Bootstrap event-handler.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Ca=Ce.exports,kt;function $e(){return kt||(kt=1,function(e,n){(function(t,a){e.exports=a(ne())})(Ca,function(t){const a=/[^.]*(?=\..*)\.|.*/,r=/\..*/,i=/::\d+$/,o={};let s=1;const l={mouseenter:"mouseover",mouseleave:"mouseout"},f=new Set(["click","dblclick","mouseup","mousedown","contextmenu","mousewheel","DOMMouseScroll","mouseover","mouseout","mousemove","selectstart","selectend","keydown","keypress","keyup","orientationchange","touchstart","touchmove","touchend","touchcancel","pointerdown","pointermove","pointerup","pointerleave","pointercancel","gesturestart","gesturechange","gestureend","focus","blur","change","reset","select","submit","focusin","focusout","load","unload","beforeunload","resize","move","DOMContentLoaded","readystatechange","error","abort","scroll"]);function d(p,v){return v&&`${v}::${s++}`||p.uidEvent||s++}function m(p){const v=d(p);return p.uidEvent=v,o[v]=o[v]||{},o[v]}function S(p,v){return function E(P){return M(P,{delegateTarget:p}),E.oneOff&&L.off(p,P.type,v),v.apply(p,[P])}}function x(p,v,E){return function P(c){const g=p.querySelectorAll(v);for(let{target:h}=c;h&&h!==this;h=h.parentNode)for(const y of g)if(y===h)return M(c,{delegateTarget:h}),P.oneOff&&L.off(p,c.type,v,E),E.apply(h,[c])}}function T(p,v,E=null){return Object.values(p).find(P=>P.callable===v&&P.delegationSelector===E)}function w(p,v,E){const P=typeof v=="string",c=P?E:v||E;let g=N(p);return f.has(g)||(g=p),[P,c,g]}function I(p,v,E,P,c){if(typeof v!="string"||!p)return;let[g,h,y]=w(v,E,P);v in l&&(h=(xa=>function(ae){if(!ae.relatedTarget||ae.relatedTarget!==ae.delegateTarget&&!ae.delegateTarget.contains(ae.relatedTarget))return xa.call(this,ae)})(h));const C=m(p),_=C[y]||(C[y]={}),D=T(_,h,g?E:null);if(D){D.oneOff=D.oneOff&&c;return}const j=d(h,v.replace(a,"")),R=g?x(p,E,h):S(p,h);R.delegationSelector=g?E:null,R.callable=h,R.oneOff=c,R.uidEvent=j,_[j]=R,p.addEventListener(y,R,g)}function k(p,v,E,P,c){const g=T(v[E],P,c);g&&(p.removeEventListener(E,g,!!c),delete v[E][g.uidEvent])}function F(p,v,E,P){const c=v[E]||{};for(const[g,h]of Object.entries(c))g.includes(P)&&k(p,v,E,h.callable,h.delegationSelector)}function N(p){return p=p.replace(r,""),l[p]||p}const L={on(p,v,E,P){I(p,v,E,P,!1)},one(p,v,E,P){I(p,v,E,P,!0)},off(p,v,E,P){if(typeof v!="string"||!p)return;const[c,g,h]=w(v,E,P),y=h!==v,C=m(p),_=C[h]||{},D=v.startsWith(".");if(typeof g<"u"){if(!Object.keys(_).length)return;k(p,C,h,g,c?E:null);return}if(D)for(const j of Object.keys(C))F(p,C,j,v.slice(1));for(const[j,R]of Object.entries(_)){const H=j.replace(i,"");(!y||v.includes(H))&&k(p,C,h,R.callable,R.delegationSelector)}},trigger(p,v,E){if(typeof v!="string"||!p)return null;const P=t.getjQuery(),c=N(v),g=v!==c;let h=null,y=!0,C=!0,_=!1;g&&P&&(h=P.Event(v,E),P(p).trigger(h),y=!h.isPropagationStopped(),C=!h.isImmediatePropagationStopped(),_=h.isDefaultPrevented());const D=M(new Event(v,{bubbles:y,cancelable:!0}),E);return _&&D.preventDefault(),C&&p.dispatchEvent(D),D.defaultPrevented&&h&&h.preventDefault(),D}};function M(p,v={}){for(const[E,P]of Object.entries(v))try{p[E]=P}catch{Object.defineProperty(p,E,{configurable:!0,get(){return P}})}return p}return L})}(Ce)),Ce.exports}var _e={exports:{}},Ie={exports:{}};/*!
  * Bootstrap manipulator.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var _a=Ie.exports,Tt;function Ia(){return Tt||(Tt=1,function(e,n){(function(t,a){e.exports=a()})(_a,function(){function t(i){if(i==="true")return!0;if(i==="false")return!1;if(i===Number(i).toString())return Number(i);if(i===""||i==="null")return null;if(typeof i!="string")return i;try{return JSON.parse(decodeURIComponent(i))}catch{return i}}function a(i){return i.replace(/[A-Z]/g,o=>`-${o.toLowerCase()}`)}return{setDataAttribute(i,o,s){i.setAttribute(`data-bs-${a(o)}`,s)},removeDataAttribute(i,o){i.removeAttribute(`data-bs-${a(o)}`)},getDataAttributes(i){if(!i)return{};const o={},s=Object.keys(i.dataset).filter(l=>l.startsWith("bs")&&!l.startsWith("bsConfig"));for(const l of s){let f=l.replace(/^bs/,"");f=f.charAt(0).toLowerCase()+f.slice(1),o[f]=t(i.dataset[l])}return o},getDataAttribute(i,o){return t(i.getAttribute(`data-bs-${a(o)}`))}}})}(Ie)),Ie.exports}/*!
  * Bootstrap config.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Pa=_e.exports,Nt;function ka(){return Nt||(Nt=1,function(e,n){(function(t,a){e.exports=a(Ia(),ne())})(Pa,function(t,a){class r{static get Default(){return{}}static get DefaultType(){return{}}static get NAME(){throw new Error('You have to implement the static method "NAME", for each component!')}_getConfig(o){return o=this._mergeConfigObj(o),o=this._configAfterMerge(o),this._typeCheckConfig(o),o}_configAfterMerge(o){return o}_mergeConfigObj(o,s){const l=a.isElement(s)?t.getDataAttribute(s,"config"):{};return{...this.constructor.Default,...typeof l=="object"?l:{},...a.isElement(s)?t.getDataAttributes(s):{},...typeof o=="object"?o:{}}}_typeCheckConfig(o,s=this.constructor.DefaultType){for(const[l,f]of Object.entries(s)){const d=o[l],m=a.isElement(d)?"element":a.toType(d);if(!new RegExp(f).test(m))throw new TypeError(`${this.constructor.NAME.toUpperCase()}: Option "${l}" provided type "${m}" but expected type "${f}".`)}}}return r})}(_e)),_e.exports}/*!
  * Bootstrap base-component.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Ta=Ee.exports,Ft;function hn(){return Ft||(Ft=1,function(e,n){(function(t,a){e.exports=a(Ea(),$e(),ka(),ne())})(Ta,function(t,a,r,i){const o="5.3.6";class s extends r{constructor(f,d){super(),f=i.getElement(f),f&&(this._element=f,this._config=this._getConfig(d),t.set(this._element,this.constructor.DATA_KEY,this))}dispose(){t.remove(this._element,this.constructor.DATA_KEY),a.off(this._element,this.constructor.EVENT_KEY);for(const f of Object.getOwnPropertyNames(this))this[f]=null}_queueCallback(f,d,m=!0){i.executeAfterTransition(f,d,m)}_getConfig(f){return f=this._mergeConfigObj(f,this._element),f=this._configAfterMerge(f),this._typeCheckConfig(f),f}static getInstance(f){return t.get(i.getElement(f),this.DATA_KEY)}static getOrCreateInstance(f,d={}){return this.getInstance(f)||new this(f,typeof d=="object"?d:null)}static get VERSION(){return o}static get DATA_KEY(){return`bs.${this.NAME}`}static get EVENT_KEY(){return`.${this.DATA_KEY}`}static eventName(f){return`${f}${this.EVENT_KEY}`}}return s})}(Ee)),Ee.exports}var Pe={exports:{}};/*!
  * Bootstrap selector-engine.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Na=Pe.exports,Ot;function gn(){return Ot||(Ot=1,function(e,n){(function(t,a){e.exports=a(ne())})(Na,function(t){const a=i=>{let o=i.getAttribute("data-bs-target");if(!o||o==="#"){let s=i.getAttribute("href");if(!s||!s.includes("#")&&!s.startsWith("."))return null;s.includes("#")&&!s.startsWith("#")&&(s=`#${s.split("#")[1]}`),o=s&&s!=="#"?s.trim():null}return o?o.split(",").map(s=>t.parseSelector(s)).join(","):null},r={find(i,o=document.documentElement){return[].concat(...Element.prototype.querySelectorAll.call(o,i))},findOne(i,o=document.documentElement){return Element.prototype.querySelector.call(o,i)},children(i,o){return[].concat(...i.children).filter(s=>s.matches(o))},parents(i,o){const s=[];let l=i.parentNode.closest(o);for(;l;)s.push(l),l=l.parentNode.closest(o);return s},prev(i,o){let s=i.previousElementSibling;for(;s;){if(s.matches(o))return[s];s=s.previousElementSibling}return[]},next(i,o){let s=i.nextElementSibling;for(;s;){if(s.matches(o))return[s];s=s.nextElementSibling}return[]},focusableChildren(i){const o=["a","button","input","textarea","select","details","[tabindex]",'[contenteditable="true"]'].map(s=>`${s}:not([tabindex^="-"])`).join(",");return this.find(o,i).filter(s=>!t.isDisabled(s)&&t.isVisible(s))},getSelectorFromElement(i){const o=a(i);return o&&r.findOne(o)?o:null},getElementFromSelector(i){const o=a(i);return o?r.findOne(o):null},getMultipleElementsFromSelector(i){const o=a(i);return o?r.find(o):[]}};return r})}(Pe)),Pe.exports}/*!
  * Bootstrap collapse.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Fa=we.exports,Dt;function Oa(){return Dt||(Dt=1,function(e,n){(function(t,a){e.exports=a(hn(),$e(),gn(),ne())})(Fa,function(t,a,r,i){const o="collapse",l=".bs.collapse",f=".data-api",d=`show${l}`,m=`shown${l}`,S=`hide${l}`,x=`hidden${l}`,T=`click${l}${f}`,w="show",I="collapse",k="collapsing",F="collapsed",N=`:scope .${I} .${I}`,L="collapse-horizontal",M="width",p="height",v=".collapse.show, .collapse.collapsing",E='[data-bs-toggle="collapse"]',P={parent:null,toggle:!0},c={parent:"(null|element)",toggle:"boolean"};class g extends t{constructor(y,C){super(y,C),this._isTransitioning=!1,this._triggerArray=[];const _=r.find(E);for(const D of _){const j=r.getSelectorFromElement(D),R=r.find(j).filter(H=>H===this._element);j!==null&&R.length&&this._triggerArray.push(D)}this._initializeChildren(),this._config.parent||this._addAriaAndCollapsedClass(this._triggerArray,this._isShown()),this._config.toggle&&this.toggle()}static get Default(){return P}static get DefaultType(){return c}static get NAME(){return o}toggle(){this._isShown()?this.hide():this.show()}show(){if(this._isTransitioning||this._isShown())return;let y=[];if(this._config.parent&&(y=this._getFirstLevelChildren(v).filter(H=>H!==this._element).map(H=>g.getOrCreateInstance(H,{toggle:!1}))),y.length&&y[0]._isTransitioning||a.trigger(this._element,d).defaultPrevented)return;for(const H of y)H.hide();const _=this._getDimension();this._element.classList.remove(I),this._element.classList.add(k),this._element.style[_]=0,this._addAriaAndCollapsedClass(this._triggerArray,!0),this._isTransitioning=!0;const D=()=>{this._isTransitioning=!1,this._element.classList.remove(k),this._element.classList.add(I,w),this._element.style[_]="",a.trigger(this._element,m)},R=`scroll${_[0].toUpperCase()+_.slice(1)}`;this._queueCallback(D,this._element,!0),this._element.style[_]=`${this._element[R]}px`}hide(){if(this._isTransitioning||!this._isShown()||a.trigger(this._element,S).defaultPrevented)return;const C=this._getDimension();this._element.style[C]=`${this._element.getBoundingClientRect()[C]}px`,i.reflow(this._element),this._element.classList.add(k),this._element.classList.remove(I,w);for(const D of this._triggerArray){const j=r.getElementFromSelector(D);j&&!this._isShown(j)&&this._addAriaAndCollapsedClass([D],!1)}this._isTransitioning=!0;const _=()=>{this._isTransitioning=!1,this._element.classList.remove(k),this._element.classList.add(I),a.trigger(this._element,x)};this._element.style[C]="",this._queueCallback(_,this._element,!0)}_isShown(y=this._element){return y.classList.contains(w)}_configAfterMerge(y){return y.toggle=!!y.toggle,y.parent=i.getElement(y.parent),y}_getDimension(){return this._element.classList.contains(L)?M:p}_initializeChildren(){if(!this._config.parent)return;const y=this._getFirstLevelChildren(E);for(const C of y){const _=r.getElementFromSelector(C);_&&this._addAriaAndCollapsedClass([C],this._isShown(_))}}_getFirstLevelChildren(y){const C=r.find(N,this._config.parent);return r.find(y,this._config.parent).filter(_=>!C.includes(_))}_addAriaAndCollapsedClass(y,C){if(y.length)for(const _ of y)_.classList.toggle(F,!C),_.setAttribute("aria-expanded",C)}static jQueryInterface(y){const C={};return typeof y=="string"&&/show|hide/.test(y)&&(C.toggle=!1),this.each(function(){const _=g.getOrCreateInstance(this,C);if(typeof y=="string"){if(typeof _[y]>"u")throw new TypeError(`No method named "${y}"`);_[y]()}})}}return a.on(document,T,E,function(h){(h.target.tagName==="A"||h.delegateTarget&&h.delegateTarget.tagName==="A")&&h.preventDefault();for(const y of r.getMultipleElementsFromSelector(this))g.getOrCreateInstance(y,{toggle:!1}).toggle()}),i.defineJQueryPlugin(g),g})}(we)),we.exports}Oa();var ke={exports:{}},ue={exports:{}};/*!
  * Bootstrap component-functions.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Da=ue.exports,Lt;function La(){return Lt||(Lt=1,function(e,n){(function(t,a){a(n,$e(),gn(),ne())})(Da,function(t,a,r,i){const o=(s,l="hide")=>{const f=`click.dismiss${s.EVENT_KEY}`,d=s.NAME;a.on(document,f,`[data-bs-dismiss="${d}"]`,function(m){if(["A","AREA"].includes(this.tagName)&&m.preventDefault(),i.isDisabled(this))return;const S=r.getElementFromSelector(this)||this.closest(`.${d}`);s.getOrCreateInstance(S)[l]()})};t.enableDismissTrigger=o,Object.defineProperty(t,Symbol.toStringTag,{value:"Module"})})}(ue,ue.exports)),ue.exports}/*!
  * Bootstrap alert.js v5.3.6 (https://getbootstrap.com/)
  * Copyright 2011-2025 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */var Ma=ke.exports,Mt;function $a(){return Mt||(Mt=1,function(e,n){(function(t,a){e.exports=a(hn(),$e(),La(),ne())})(Ma,function(t,a,r,i){const o="alert",l=".bs.alert",f=`close${l}`,d=`closed${l}`,m="fade",S="show";class x extends t{static get NAME(){return o}close(){if(a.trigger(this._element,f).defaultPrevented)return;this._element.classList.remove(S);const I=this._element.classList.contains(m);this._queueCallback(()=>this._destroyElement(),this._element,I)}_destroyElement(){this._element.remove(),a.trigger(this._element,d),this.dispose()}static jQueryInterface(w){return this.each(function(){const I=x.getOrCreateInstance(this);if(typeof w=="string"){if(I[w]===void 0||w.startsWith("_")||w==="constructor")throw new TypeError(`No method named "${w}"`);I[w](this)}})}}return r.enableDismissTrigger(x,"close"),i.defineJQueryPlugin(x),x})}(ke)),ke.exports}$a();/*!
 * Font Awesome Free 7.2.0 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2026 Fonticons, Inc.
 */function Je(e,n){(n==null||n>e.length)&&(n=e.length);for(var t=0,a=Array(n);t<n;t++)a[t]=e[t];return a}function ja(e){if(Array.isArray(e))return e}function Ra(e){if(Array.isArray(e))return Je(e)}function Wa(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function za(e,n){for(var t=0;t<n.length;t++){var a=n[t];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,pn(a.key),a)}}function Ua(e,n,t){return n&&za(e.prototype,n),Object.defineProperty(e,"prototype",{writable:!1}),e}function Te(e,n){var t=typeof Symbol<"u"&&e[Symbol.iterator]||e["@@iterator"];if(!t){if(Array.isArray(e)||(t=mt(e))||n){t&&(e=t);var a=0,r=function(){};return{s:r,n:function(){return a>=e.length?{done:!0}:{done:!1,value:e[a++]}},e:function(l){throw l},f:r}}throw new TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var i,o=!0,s=!1;return{s:function(){t=t.call(e)},n:function(){var l=t.next();return o=l.done,l},e:function(l){s=!0,i=l},f:function(){try{o||t.return==null||t.return()}finally{if(s)throw i}}}}function A(e,n,t){return(n=pn(n))in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function Ya(e){if(typeof Symbol<"u"&&e[Symbol.iterator]!=null||e["@@iterator"]!=null)return Array.from(e)}function Ha(e,n){var t=e==null?null:typeof Symbol<"u"&&e[Symbol.iterator]||e["@@iterator"];if(t!=null){var a,r,i,o,s=[],l=!0,f=!1;try{if(i=(t=t.call(e)).next,n===0){if(Object(t)!==t)return;l=!1}else for(;!(l=(a=i.call(t)).done)&&(s.push(a.value),s.length!==n);l=!0);}catch(d){f=!0,r=d}finally{try{if(!l&&t.return!=null&&(o=t.return(),Object(o)!==o))return}finally{if(f)throw r}}return s}}function qa(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Ba(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function $t(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter(function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable})),t.push.apply(t,a)}return t}function u(e){for(var n=1;n<arguments.length;n++){var t=arguments[n]!=null?arguments[n]:{};n%2?$t(Object(t),!0).forEach(function(a){A(e,a,t[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):$t(Object(t)).forEach(function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))})}return e}function je(e,n){return ja(e)||Ha(e,n)||mt(e,n)||qa()}function Y(e){return Ra(e)||Ya(e)||mt(e)||Ba()}function Ka(e,n){if(typeof e!="object"||!e)return e;var t=e[Symbol.toPrimitive];if(t!==void 0){var a=t.call(e,n);if(typeof a!="object")return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return(n==="string"?String:Number)(e)}function pn(e){var n=Ka(e,"string");return typeof n=="symbol"?n:n+""}function De(e){"@babel/helpers - typeof";return De=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(n){return typeof n}:function(n){return n&&typeof Symbol=="function"&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},De(e)}function mt(e,n){if(e){if(typeof e=="string")return Je(e,n);var t={}.toString.call(e).slice(8,-1);return t==="Object"&&e.constructor&&(t=e.constructor.name),t==="Map"||t==="Set"?Array.from(e):t==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?Je(e,n):void 0}}var jt=function(){},ht={},vn={},bn=null,yn={mark:jt,measure:jt};try{typeof window<"u"&&(ht=window),typeof document<"u"&&(vn=document),typeof MutationObserver<"u"&&(bn=MutationObserver),typeof performance<"u"&&(yn=performance)}catch{}var Va=ht.navigator||{},Rt=Va.userAgent,Wt=Rt===void 0?"":Rt,X=ht,O=vn,zt=bn,Se=yn;X.document;var G=!!O.documentElement&&!!O.head&&typeof O.addEventListener=="function"&&typeof O.createElement=="function",Sn=~Wt.indexOf("MSIE")||~Wt.indexOf("Trident/"),Ye,Ga=/fa(k|kd|s|r|l|t|d|dr|dl|dt|b|slr|slpr|wsb|tl|ns|nds|es|gt|jr|jfr|jdr|usb|ufsb|udsb|cr|ss|sr|sl|st|sds|sdr|sdl|sdt)?[\-\ ]/,Xa=/Font ?Awesome ?([567 ]*)(Solid|Regular|Light|Thin|Duotone|Brands|Free|Pro|Sharp Duotone|Sharp|Kit|Notdog Duo|Notdog|Chisel|Etch|Graphite|Thumbprint|Jelly Fill|Jelly Duo|Jelly|Utility|Utility Fill|Utility Duo|Slab Press|Slab|Whiteboard)?.*/i,xn={classic:{fa:"solid",fas:"solid","fa-solid":"solid",far:"regular","fa-regular":"regular",fal:"light","fa-light":"light",fat:"thin","fa-thin":"thin",fab:"brands","fa-brands":"brands"},duotone:{fa:"solid",fad:"solid","fa-solid":"solid","fa-duotone":"solid",fadr:"regular","fa-regular":"regular",fadl:"light","fa-light":"light",fadt:"thin","fa-thin":"thin"},sharp:{fa:"solid",fass:"solid","fa-solid":"solid",fasr:"regular","fa-regular":"regular",fasl:"light","fa-light":"light",fast:"thin","fa-thin":"thin"},"sharp-duotone":{fa:"solid",fasds:"solid","fa-solid":"solid",fasdr:"regular","fa-regular":"regular",fasdl:"light","fa-light":"light",fasdt:"thin","fa-thin":"thin"},slab:{"fa-regular":"regular",faslr:"regular"},"slab-press":{"fa-regular":"regular",faslpr:"regular"},thumbprint:{"fa-light":"light",fatl:"light"},whiteboard:{"fa-semibold":"semibold",fawsb:"semibold"},notdog:{"fa-solid":"solid",fans:"solid"},"notdog-duo":{"fa-solid":"solid",fands:"solid"},etch:{"fa-solid":"solid",faes:"solid"},graphite:{"fa-thin":"thin",fagt:"thin"},jelly:{"fa-regular":"regular",fajr:"regular"},"jelly-fill":{"fa-regular":"regular",fajfr:"regular"},"jelly-duo":{"fa-regular":"regular",fajdr:"regular"},chisel:{"fa-regular":"regular",facr:"regular"},utility:{"fa-semibold":"semibold",fausb:"semibold"},"utility-duo":{"fa-semibold":"semibold",faudsb:"semibold"},"utility-fill":{"fa-semibold":"semibold",faufsb:"semibold"}},Ja={GROUP:"duotone-group",PRIMARY:"primary",SECONDARY:"secondary"},wn=["fa-classic","fa-duotone","fa-sharp","fa-sharp-duotone","fa-thumbprint","fa-whiteboard","fa-notdog","fa-notdog-duo","fa-chisel","fa-etch","fa-graphite","fa-jelly","fa-jelly-fill","fa-jelly-duo","fa-slab","fa-slab-press","fa-utility","fa-utility-duo","fa-utility-fill"],$="classic",ve="duotone",En="sharp",An="sharp-duotone",Cn="chisel",_n="etch",In="graphite",Pn="jelly",kn="jelly-duo",Tn="jelly-fill",Nn="notdog",Fn="notdog-duo",On="slab",Dn="slab-press",Ln="thumbprint",Mn="utility",$n="utility-duo",jn="utility-fill",Rn="whiteboard",Qa="Classic",Za="Duotone",er="Sharp",tr="Sharp Duotone",nr="Chisel",ar="Etch",rr="Graphite",ir="Jelly",or="Jelly Duo",sr="Jelly Fill",lr="Notdog",fr="Notdog Duo",cr="Slab",ur="Slab Press",dr="Thumbprint",mr="Utility",hr="Utility Duo",gr="Utility Fill",pr="Whiteboard",Wn=[$,ve,En,An,Cn,_n,In,Pn,kn,Tn,Nn,Fn,On,Dn,Ln,Mn,$n,jn,Rn];Ye={},A(A(A(A(A(A(A(A(A(A(Ye,$,Qa),ve,Za),En,er),An,tr),Cn,nr),_n,ar),In,rr),Pn,ir),kn,or),Tn,sr),A(A(A(A(A(A(A(A(A(Ye,Nn,lr),Fn,fr),On,cr),Dn,ur),Ln,dr),Mn,mr),$n,hr),jn,gr),Rn,pr);var vr={classic:{900:"fas",400:"far",normal:"far",300:"fal",100:"fat"},duotone:{900:"fad",400:"fadr",300:"fadl",100:"fadt"},sharp:{900:"fass",400:"fasr",300:"fasl",100:"fast"},"sharp-duotone":{900:"fasds",400:"fasdr",300:"fasdl",100:"fasdt"},slab:{400:"faslr"},"slab-press":{400:"faslpr"},whiteboard:{600:"fawsb"},thumbprint:{300:"fatl"},notdog:{900:"fans"},"notdog-duo":{900:"fands"},etch:{900:"faes"},graphite:{100:"fagt"},chisel:{400:"facr"},jelly:{400:"fajr"},"jelly-fill":{400:"fajfr"},"jelly-duo":{400:"fajdr"},utility:{600:"fausb"},"utility-duo":{600:"faudsb"},"utility-fill":{600:"faufsb"}},br={"Font Awesome 7 Free":{900:"fas",400:"far"},"Font Awesome 7 Pro":{900:"fas",400:"far",normal:"far",300:"fal",100:"fat"},"Font Awesome 7 Brands":{400:"fab",normal:"fab"},"Font Awesome 7 Duotone":{900:"fad",400:"fadr",normal:"fadr",300:"fadl",100:"fadt"},"Font Awesome 7 Sharp":{900:"fass",400:"fasr",normal:"fasr",300:"fasl",100:"fast"},"Font Awesome 7 Sharp Duotone":{900:"fasds",400:"fasdr",normal:"fasdr",300:"fasdl",100:"fasdt"},"Font Awesome 7 Jelly":{400:"fajr",normal:"fajr"},"Font Awesome 7 Jelly Fill":{400:"fajfr",normal:"fajfr"},"Font Awesome 7 Jelly Duo":{400:"fajdr",normal:"fajdr"},"Font Awesome 7 Slab":{400:"faslr",normal:"faslr"},"Font Awesome 7 Slab Press":{400:"faslpr",normal:"faslpr"},"Font Awesome 7 Thumbprint":{300:"fatl",normal:"fatl"},"Font Awesome 7 Notdog":{900:"fans",normal:"fans"},"Font Awesome 7 Notdog Duo":{900:"fands",normal:"fands"},"Font Awesome 7 Etch":{900:"faes",normal:"faes"},"Font Awesome 7 Graphite":{100:"fagt",normal:"fagt"},"Font Awesome 7 Chisel":{400:"facr",normal:"facr"},"Font Awesome 7 Whiteboard":{600:"fawsb",normal:"fawsb"},"Font Awesome 7 Utility":{600:"fausb",normal:"fausb"},"Font Awesome 7 Utility Duo":{600:"faudsb",normal:"faudsb"},"Font Awesome 7 Utility Fill":{600:"faufsb",normal:"faufsb"}},yr=new Map([["classic",{defaultShortPrefixId:"fas",defaultStyleId:"solid",styleIds:["solid","regular","light","thin","brands"],futureStyleIds:[],defaultFontWeight:900}],["duotone",{defaultShortPrefixId:"fad",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["sharp",{defaultShortPrefixId:"fass",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["sharp-duotone",{defaultShortPrefixId:"fasds",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["chisel",{defaultShortPrefixId:"facr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["etch",{defaultShortPrefixId:"faes",defaultStyleId:"solid",styleIds:["solid"],futureStyleIds:[],defaultFontWeight:900}],["graphite",{defaultShortPrefixId:"fagt",defaultStyleId:"thin",styleIds:["thin"],futureStyleIds:[],defaultFontWeight:100}],["jelly",{defaultShortPrefixId:"fajr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["jelly-duo",{defaultShortPrefixId:"fajdr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["jelly-fill",{defaultShortPrefixId:"fajfr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["notdog",{defaultShortPrefixId:"fans",defaultStyleId:"solid",styleIds:["solid"],futureStyleIds:[],defaultFontWeight:900}],["notdog-duo",{defaultShortPrefixId:"fands",defaultStyleId:"solid",styleIds:["solid"],futureStyleIds:[],defaultFontWeight:900}],["slab",{defaultShortPrefixId:"faslr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["slab-press",{defaultShortPrefixId:"faslpr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["thumbprint",{defaultShortPrefixId:"fatl",defaultStyleId:"light",styleIds:["light"],futureStyleIds:[],defaultFontWeight:300}],["utility",{defaultShortPrefixId:"fausb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}],["utility-duo",{defaultShortPrefixId:"faudsb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}],["utility-fill",{defaultShortPrefixId:"faufsb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}],["whiteboard",{defaultShortPrefixId:"fawsb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}]]),Sr={chisel:{regular:"facr"},classic:{brands:"fab",light:"fal",regular:"far",solid:"fas",thin:"fat"},duotone:{light:"fadl",regular:"fadr",solid:"fad",thin:"fadt"},etch:{solid:"faes"},graphite:{thin:"fagt"},jelly:{regular:"fajr"},"jelly-duo":{regular:"fajdr"},"jelly-fill":{regular:"fajfr"},notdog:{solid:"fans"},"notdog-duo":{solid:"fands"},sharp:{light:"fasl",regular:"fasr",solid:"fass",thin:"fast"},"sharp-duotone":{light:"fasdl",regular:"fasdr",solid:"fasds",thin:"fasdt"},slab:{regular:"faslr"},"slab-press":{regular:"faslpr"},thumbprint:{light:"fatl"},utility:{semibold:"fausb"},"utility-duo":{semibold:"faudsb"},"utility-fill":{semibold:"faufsb"},whiteboard:{semibold:"fawsb"}},zn=["fak","fa-kit","fakd","fa-kit-duotone"],Ut={kit:{fak:"kit","fa-kit":"kit"},"kit-duotone":{fakd:"kit-duotone","fa-kit-duotone":"kit-duotone"}},xr=["kit"],wr="kit",Er="kit-duotone",Ar="Kit",Cr="Kit Duotone";A(A({},wr,Ar),Er,Cr);var _r={kit:{"fa-kit":"fak"}},Ir={"Font Awesome Kit":{400:"fak",normal:"fak"},"Font Awesome Kit Duotone":{400:"fakd",normal:"fakd"}},Pr={kit:{fak:"fa-kit"}},Yt={kit:{kit:"fak"},"kit-duotone":{"kit-duotone":"fakd"}},He,xe={GROUP:"duotone-group",SWAP_OPACITY:"swap-opacity",PRIMARY:"primary",SECONDARY:"secondary"},kr=["fa-classic","fa-duotone","fa-sharp","fa-sharp-duotone","fa-thumbprint","fa-whiteboard","fa-notdog","fa-notdog-duo","fa-chisel","fa-etch","fa-graphite","fa-jelly","fa-jelly-fill","fa-jelly-duo","fa-slab","fa-slab-press","fa-utility","fa-utility-duo","fa-utility-fill"],Tr="classic",Nr="duotone",Fr="sharp",Or="sharp-duotone",Dr="chisel",Lr="etch",Mr="graphite",$r="jelly",jr="jelly-duo",Rr="jelly-fill",Wr="notdog",zr="notdog-duo",Ur="slab",Yr="slab-press",Hr="thumbprint",qr="utility",Br="utility-duo",Kr="utility-fill",Vr="whiteboard",Gr="Classic",Xr="Duotone",Jr="Sharp",Qr="Sharp Duotone",Zr="Chisel",ei="Etch",ti="Graphite",ni="Jelly",ai="Jelly Duo",ri="Jelly Fill",ii="Notdog",oi="Notdog Duo",si="Slab",li="Slab Press",fi="Thumbprint",ci="Utility",ui="Utility Duo",di="Utility Fill",mi="Whiteboard";He={},A(A(A(A(A(A(A(A(A(A(He,Tr,Gr),Nr,Xr),Fr,Jr),Or,Qr),Dr,Zr),Lr,ei),Mr,ti),$r,ni),jr,ai),Rr,ri),A(A(A(A(A(A(A(A(A(He,Wr,ii),zr,oi),Ur,si),Yr,li),Hr,fi),qr,ci),Br,ui),Kr,di),Vr,mi);var hi="kit",gi="kit-duotone",pi="Kit",vi="Kit Duotone";A(A({},hi,pi),gi,vi);var bi={classic:{"fa-brands":"fab","fa-duotone":"fad","fa-light":"fal","fa-regular":"far","fa-solid":"fas","fa-thin":"fat"},duotone:{"fa-regular":"fadr","fa-light":"fadl","fa-thin":"fadt"},sharp:{"fa-solid":"fass","fa-regular":"fasr","fa-light":"fasl","fa-thin":"fast"},"sharp-duotone":{"fa-solid":"fasds","fa-regular":"fasdr","fa-light":"fasdl","fa-thin":"fasdt"},slab:{"fa-regular":"faslr"},"slab-press":{"fa-regular":"faslpr"},whiteboard:{"fa-semibold":"fawsb"},thumbprint:{"fa-light":"fatl"},notdog:{"fa-solid":"fans"},"notdog-duo":{"fa-solid":"fands"},etch:{"fa-solid":"faes"},graphite:{"fa-thin":"fagt"},jelly:{"fa-regular":"fajr"},"jelly-fill":{"fa-regular":"fajfr"},"jelly-duo":{"fa-regular":"fajdr"},chisel:{"fa-regular":"facr"},utility:{"fa-semibold":"fausb"},"utility-duo":{"fa-semibold":"faudsb"},"utility-fill":{"fa-semibold":"faufsb"}},yi={classic:["fas","far","fal","fat","fad"],duotone:["fadr","fadl","fadt"],sharp:["fass","fasr","fasl","fast"],"sharp-duotone":["fasds","fasdr","fasdl","fasdt"],slab:["faslr"],"slab-press":["faslpr"],whiteboard:["fawsb"],thumbprint:["fatl"],notdog:["fans"],"notdog-duo":["fands"],etch:["faes"],graphite:["fagt"],jelly:["fajr"],"jelly-fill":["fajfr"],"jelly-duo":["fajdr"],chisel:["facr"],utility:["fausb"],"utility-duo":["faudsb"],"utility-fill":["faufsb"]},Qe={classic:{fab:"fa-brands",fad:"fa-duotone",fal:"fa-light",far:"fa-regular",fas:"fa-solid",fat:"fa-thin"},duotone:{fadr:"fa-regular",fadl:"fa-light",fadt:"fa-thin"},sharp:{fass:"fa-solid",fasr:"fa-regular",fasl:"fa-light",fast:"fa-thin"},"sharp-duotone":{fasds:"fa-solid",fasdr:"fa-regular",fasdl:"fa-light",fasdt:"fa-thin"},slab:{faslr:"fa-regular"},"slab-press":{faslpr:"fa-regular"},whiteboard:{fawsb:"fa-semibold"},thumbprint:{fatl:"fa-light"},notdog:{fans:"fa-solid"},"notdog-duo":{fands:"fa-solid"},etch:{faes:"fa-solid"},graphite:{fagt:"fa-thin"},jelly:{fajr:"fa-regular"},"jelly-fill":{fajfr:"fa-regular"},"jelly-duo":{fajdr:"fa-regular"},chisel:{facr:"fa-regular"},utility:{fausb:"fa-semibold"},"utility-duo":{faudsb:"fa-semibold"},"utility-fill":{faufsb:"fa-semibold"}},Si=["fa-solid","fa-regular","fa-light","fa-thin","fa-duotone","fa-brands","fa-semibold"],Un=["fa","fas","far","fal","fat","fad","fadr","fadl","fadt","fab","fass","fasr","fasl","fast","fasds","fasdr","fasdl","fasdt","faslr","faslpr","fawsb","fatl","fans","fands","faes","fagt","fajr","fajfr","fajdr","facr","fausb","faudsb","faufsb"].concat(kr,Si),xi=["solid","regular","light","thin","duotone","brands","semibold"],Yn=[1,2,3,4,5,6,7,8,9,10],wi=Yn.concat([11,12,13,14,15,16,17,18,19,20]),Ei=["aw","fw","pull-left","pull-right"],Ai=[].concat(Y(Object.keys(yi)),xi,Ei,["2xs","xs","sm","lg","xl","2xl","beat","border","fade","beat-fade","bounce","flip-both","flip-horizontal","flip-vertical","flip","inverse","layers","layers-bottom-left","layers-bottom-right","layers-counter","layers-text","layers-top-left","layers-top-right","li","pull-end","pull-start","pulse","rotate-180","rotate-270","rotate-90","rotate-by","shake","spin-pulse","spin-reverse","spin","stack-1x","stack-2x","stack","ul","width-auto","width-fixed",xe.GROUP,xe.SWAP_OPACITY,xe.PRIMARY,xe.SECONDARY]).concat(Yn.map(function(e){return"".concat(e,"x")})).concat(wi.map(function(e){return"w-".concat(e)})),Ci={"Font Awesome 5 Free":{900:"fas",400:"far"},"Font Awesome 5 Pro":{900:"fas",400:"far",normal:"far",300:"fal"},"Font Awesome 5 Brands":{400:"fab",normal:"fab"},"Font Awesome 5 Duotone":{900:"fad"}},K="___FONT_AWESOME___",Ze=16,Hn="fa",qn="svg-inline--fa",ee="data-fa-i2svg",et="data-fa-pseudo-element",_i="data-fa-pseudo-element-pending",gt="data-prefix",pt="data-icon",Ht="fontawesome-i2svg",Ii="async",Pi=["HTML","HEAD","STYLE","SCRIPT"],Bn=["::before","::after",":before",":after"],Kn=function(){try{return!0}catch{return!1}}();function be(e){return new Proxy(e,{get:function(t,a){return a in t?t[a]:t[$]}})}var Vn=u({},xn);Vn[$]=u(u(u(u({},{"fa-duotone":"duotone"}),xn[$]),Ut.kit),Ut["kit-duotone"]);var ki=be(Vn),tt=u({},Sr);tt[$]=u(u(u(u({},{duotone:"fad"}),tt[$]),Yt.kit),Yt["kit-duotone"]);var qt=be(tt),nt=u({},Qe);nt[$]=u(u({},nt[$]),Pr.kit);var vt=be(nt),at=u({},bi);at[$]=u(u({},at[$]),_r.kit);be(at);var Ti=Ga,Gn="fa-layers-text",Ni=Xa,Fi=u({},vr);be(Fi);var Oi=["class","data-prefix","data-icon","data-fa-transform","data-fa-mask"],qe=Ja,Di=[].concat(Y(xr),Y(Ai)),me=X.FontAwesomeConfig||{};function Li(e){var n=O.querySelector("script["+e+"]");if(n)return n.getAttribute(e)}function Mi(e){return e===""?!0:e==="false"?!1:e==="true"?!0:e}if(O&&typeof O.querySelector=="function"){var $i=[["data-family-prefix","familyPrefix"],["data-css-prefix","cssPrefix"],["data-family-default","familyDefault"],["data-style-default","styleDefault"],["data-replacement-class","replacementClass"],["data-auto-replace-svg","autoReplaceSvg"],["data-auto-add-css","autoAddCss"],["data-search-pseudo-elements","searchPseudoElements"],["data-search-pseudo-elements-warnings","searchPseudoElementsWarnings"],["data-search-pseudo-elements-full-scan","searchPseudoElementsFullScan"],["data-observe-mutations","observeMutations"],["data-mutate-approach","mutateApproach"],["data-keep-original-source","keepOriginalSource"],["data-measure-performance","measurePerformance"],["data-show-missing-icons","showMissingIcons"]];$i.forEach(function(e){var n=je(e,2),t=n[0],a=n[1],r=Mi(Li(t));r!=null&&(me[a]=r)})}var Xn={styleDefault:"solid",familyDefault:$,cssPrefix:Hn,replacementClass:qn,autoReplaceSvg:!0,autoAddCss:!0,searchPseudoElements:!1,searchPseudoElementsWarnings:!0,searchPseudoElementsFullScan:!1,observeMutations:!0,mutateApproach:"async",keepOriginalSource:!0,measurePerformance:!1,showMissingIcons:!0};me.familyPrefix&&(me.cssPrefix=me.familyPrefix);var le=u(u({},Xn),me);le.autoReplaceSvg||(le.observeMutations=!1);var b={};Object.keys(Xn).forEach(function(e){Object.defineProperty(b,e,{enumerable:!0,set:function(t){le[e]=t,he.forEach(function(a){return a(b)})},get:function(){return le[e]}})});Object.defineProperty(b,"familyPrefix",{enumerable:!0,set:function(n){le.cssPrefix=n,he.forEach(function(t){return t(b)})},get:function(){return le.cssPrefix}});X.FontAwesomeConfig=b;var he=[];function ji(e){return he.push(e),function(){he.splice(he.indexOf(e),1)}}var re=Ze,q={size:16,x:0,y:0,rotate:0,flipX:!1,flipY:!1};function Ri(e){if(!(!e||!G)){var n=O.createElement("style");n.setAttribute("type","text/css"),n.innerHTML=e;for(var t=O.head.childNodes,a=null,r=t.length-1;r>-1;r--){var i=t[r],o=(i.tagName||"").toUpperCase();["STYLE","LINK"].indexOf(o)>-1&&(a=i)}return O.head.insertBefore(n,a),e}}var Wi="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";function Bt(){for(var e=12,n="";e-- >0;)n+=Wi[Math.random()*62|0];return n}function fe(e){for(var n=[],t=(e||[]).length>>>0;t--;)n[t]=e[t];return n}function bt(e){return e.classList?fe(e.classList):(e.getAttribute("class")||"").split(" ").filter(function(n){return n})}function Jn(e){return"".concat(e).replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/'/g,"&#39;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}function zi(e){return Object.keys(e||{}).reduce(function(n,t){return n+"".concat(t,'="').concat(Jn(e[t]),'" ')},"").trim()}function Re(e){return Object.keys(e||{}).reduce(function(n,t){return n+"".concat(t,": ").concat(e[t].trim(),";")},"")}function yt(e){return e.size!==q.size||e.x!==q.x||e.y!==q.y||e.rotate!==q.rotate||e.flipX||e.flipY}function Ui(e){var n=e.transform,t=e.containerWidth,a=e.iconWidth,r={transform:"translate(".concat(t/2," 256)")},i="translate(".concat(n.x*32,", ").concat(n.y*32,") "),o="scale(".concat(n.size/16*(n.flipX?-1:1),", ").concat(n.size/16*(n.flipY?-1:1),") "),s="rotate(".concat(n.rotate," 0 0)"),l={transform:"".concat(i," ").concat(o," ").concat(s)},f={transform:"translate(".concat(a/2*-1," -256)")};return{outer:r,inner:l,path:f}}function Yi(e){var n=e.transform,t=e.width,a=t===void 0?Ze:t,r=e.height,i=r===void 0?Ze:r,o="";return Sn?o+="translate(".concat(n.x/re-a/2,"em, ").concat(n.y/re-i/2,"em) "):o+="translate(calc(-50% + ".concat(n.x/re,"em), calc(-50% + ").concat(n.y/re,"em)) "),o+="scale(".concat(n.size/re*(n.flipX?-1:1),", ").concat(n.size/re*(n.flipY?-1:1),") "),o+="rotate(".concat(n.rotate,"deg) "),o}var Hi=`:root, :host {
  --fa-font-solid: normal 900 1em/1 'Font Awesome 7 Free';
  --fa-font-regular: normal 400 1em/1 'Font Awesome 7 Free';
  --fa-font-light: normal 300 1em/1 'Font Awesome 7 Pro';
  --fa-font-thin: normal 100 1em/1 'Font Awesome 7 Pro';
  --fa-font-duotone: normal 900 1em/1 'Font Awesome 7 Duotone';
  --fa-font-duotone-regular: normal 400 1em/1 'Font Awesome 7 Duotone';
  --fa-font-duotone-light: normal 300 1em/1 'Font Awesome 7 Duotone';
  --fa-font-duotone-thin: normal 100 1em/1 'Font Awesome 7 Duotone';
  --fa-font-brands: normal 400 1em/1 'Font Awesome 7 Brands';
  --fa-font-sharp-solid: normal 900 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-regular: normal 400 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-light: normal 300 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-thin: normal 100 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-duotone-solid: normal 900 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-sharp-duotone-regular: normal 400 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-sharp-duotone-light: normal 300 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-sharp-duotone-thin: normal 100 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-slab-regular: normal 400 1em/1 'Font Awesome 7 Slab';
  --fa-font-slab-press-regular: normal 400 1em/1 'Font Awesome 7 Slab Press';
  --fa-font-whiteboard-semibold: normal 600 1em/1 'Font Awesome 7 Whiteboard';
  --fa-font-thumbprint-light: normal 300 1em/1 'Font Awesome 7 Thumbprint';
  --fa-font-notdog-solid: normal 900 1em/1 'Font Awesome 7 Notdog';
  --fa-font-notdog-duo-solid: normal 900 1em/1 'Font Awesome 7 Notdog Duo';
  --fa-font-etch-solid: normal 900 1em/1 'Font Awesome 7 Etch';
  --fa-font-graphite-thin: normal 100 1em/1 'Font Awesome 7 Graphite';
  --fa-font-jelly-regular: normal 400 1em/1 'Font Awesome 7 Jelly';
  --fa-font-jelly-fill-regular: normal 400 1em/1 'Font Awesome 7 Jelly Fill';
  --fa-font-jelly-duo-regular: normal 400 1em/1 'Font Awesome 7 Jelly Duo';
  --fa-font-chisel-regular: normal 400 1em/1 'Font Awesome 7 Chisel';
  --fa-font-utility-semibold: normal 600 1em/1 'Font Awesome 7 Utility';
  --fa-font-utility-duo-semibold: normal 600 1em/1 'Font Awesome 7 Utility Duo';
  --fa-font-utility-fill-semibold: normal 600 1em/1 'Font Awesome 7 Utility Fill';
}

.svg-inline--fa {
  box-sizing: content-box;
  display: var(--fa-display, inline-block);
  height: 1em;
  overflow: visible;
  vertical-align: -0.125em;
  width: var(--fa-width, 1.25em);
}
.svg-inline--fa.fa-2xs {
  vertical-align: 0.1em;
}
.svg-inline--fa.fa-xs {
  vertical-align: 0em;
}
.svg-inline--fa.fa-sm {
  vertical-align: -0.0714285714em;
}
.svg-inline--fa.fa-lg {
  vertical-align: -0.2em;
}
.svg-inline--fa.fa-xl {
  vertical-align: -0.25em;
}
.svg-inline--fa.fa-2xl {
  vertical-align: -0.3125em;
}
.svg-inline--fa.fa-pull-left,
.svg-inline--fa .fa-pull-start {
  float: inline-start;
  margin-inline-end: var(--fa-pull-margin, 0.3em);
}
.svg-inline--fa.fa-pull-right,
.svg-inline--fa .fa-pull-end {
  float: inline-end;
  margin-inline-start: var(--fa-pull-margin, 0.3em);
}
.svg-inline--fa.fa-li {
  width: var(--fa-li-width, 2em);
  inset-inline-start: calc(-1 * var(--fa-li-width, 2em));
  inset-block-start: 0.25em; /* syncing vertical alignment with Web Font rendering */
}

.fa-layers-counter, .fa-layers-text {
  display: inline-block;
  position: absolute;
  text-align: center;
}

.fa-layers {
  display: inline-block;
  height: 1em;
  position: relative;
  text-align: center;
  vertical-align: -0.125em;
  width: var(--fa-width, 1.25em);
}
.fa-layers .svg-inline--fa {
  inset: 0;
  margin: auto;
  position: absolute;
  transform-origin: center center;
}

.fa-layers-text {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  transform-origin: center center;
}

.fa-layers-counter {
  background-color: var(--fa-counter-background-color, #ff253a);
  border-radius: var(--fa-counter-border-radius, 1em);
  box-sizing: border-box;
  color: var(--fa-inverse, #fff);
  line-height: var(--fa-counter-line-height, 1);
  max-width: var(--fa-counter-max-width, 5em);
  min-width: var(--fa-counter-min-width, 1.5em);
  overflow: hidden;
  padding: var(--fa-counter-padding, 0.25em 0.5em);
  right: var(--fa-right, 0);
  text-overflow: ellipsis;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-counter-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-bottom-right {
  bottom: var(--fa-bottom, 0);
  right: var(--fa-right, 0);
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom right;
}

.fa-layers-bottom-left {
  bottom: var(--fa-bottom, 0);
  left: var(--fa-left, 0);
  right: auto;
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom left;
}

.fa-layers-top-right {
  top: var(--fa-top, 0);
  right: var(--fa-right, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-top-left {
  left: var(--fa-left, 0);
  right: auto;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top left;
}

.fa-1x {
  font-size: 1em;
}

.fa-2x {
  font-size: 2em;
}

.fa-3x {
  font-size: 3em;
}

.fa-4x {
  font-size: 4em;
}

.fa-5x {
  font-size: 5em;
}

.fa-6x {
  font-size: 6em;
}

.fa-7x {
  font-size: 7em;
}

.fa-8x {
  font-size: 8em;
}

.fa-9x {
  font-size: 9em;
}

.fa-10x {
  font-size: 10em;
}

.fa-2xs {
  font-size: calc(10 / 16 * 1em); /* converts a 10px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 10 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 10 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-xs {
  font-size: calc(12 / 16 * 1em); /* converts a 12px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 12 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 12 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-sm {
  font-size: calc(14 / 16 * 1em); /* converts a 14px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 14 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 14 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-lg {
  font-size: calc(20 / 16 * 1em); /* converts a 20px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 20 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 20 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-xl {
  font-size: calc(24 / 16 * 1em); /* converts a 24px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 24 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 24 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-2xl {
  font-size: calc(32 / 16 * 1em); /* converts a 32px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 32 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 32 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-width-auto {
  --fa-width: auto;
}

.fa-fw,
.fa-width-fixed {
  --fa-width: 1.25em;
}

.fa-ul {
  list-style-type: none;
  margin-inline-start: var(--fa-li-margin, 2.5em);
  padding-inline-start: 0;
}
.fa-ul > li {
  position: relative;
}

.fa-li {
  inset-inline-start: calc(-1 * var(--fa-li-width, 2em));
  position: absolute;
  text-align: center;
  width: var(--fa-li-width, 2em);
  line-height: inherit;
}

/* Heads Up: Bordered Icons will not be supported in the future!
  - This feature will be deprecated in the next major release of Font Awesome (v8)!
  - You may continue to use it in this version *v7), but it will not be supported in Font Awesome v8.
*/
/* Notes:
* --@{v.$css-prefix}-border-width = 1/16 by default (to render as ~1px based on a 16px default font-size)
* --@{v.$css-prefix}-border-padding =
  ** 3/16 for vertical padding (to give ~2px of vertical whitespace around an icon considering it's vertical alignment)
  ** 4/16 for horizontal padding (to give ~4px of horizontal whitespace around an icon)
*/
.fa-border {
  border-color: var(--fa-border-color, #eee);
  border-radius: var(--fa-border-radius, 0.1em);
  border-style: var(--fa-border-style, solid);
  border-width: var(--fa-border-width, 0.0625em);
  box-sizing: var(--fa-border-box-sizing, content-box);
  padding: var(--fa-border-padding, 0.1875em 0.25em);
}

.fa-pull-left,
.fa-pull-start {
  float: inline-start;
  margin-inline-end: var(--fa-pull-margin, 0.3em);
}

.fa-pull-right,
.fa-pull-end {
  float: inline-end;
  margin-inline-start: var(--fa-pull-margin, 0.3em);
}

.fa-beat {
  animation-name: fa-beat;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-bounce {
  animation-name: fa-bounce;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));
}

.fa-fade {
  animation-name: fa-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-beat-fade {
  animation-name: fa-beat-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-flip {
  animation-name: fa-flip;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-shake {
  animation-name: fa-shake;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin {
  animation-name: fa-spin;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 2s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin-reverse {
  --fa-animation-direction: reverse;
}

.fa-pulse,
.fa-spin-pulse {
  animation-name: fa-spin;
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, steps(8));
}

@media (prefers-reduced-motion: reduce) {
  .fa-beat,
  .fa-bounce,
  .fa-fade,
  .fa-beat-fade,
  .fa-flip,
  .fa-pulse,
  .fa-shake,
  .fa-spin,
  .fa-spin-pulse {
    animation: none !important;
    transition: none !important;
  }
}
@keyframes fa-beat {
  0%, 90% {
    transform: scale(1);
  }
  45% {
    transform: scale(var(--fa-beat-scale, 1.25));
  }
}
@keyframes fa-bounce {
  0% {
    transform: scale(1, 1) translateY(0);
  }
  10% {
    transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
  }
  30% {
    transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
  }
  50% {
    transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
  }
  57% {
    transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
  }
  64% {
    transform: scale(1, 1) translateY(0);
  }
  100% {
    transform: scale(1, 1) translateY(0);
  }
}
@keyframes fa-fade {
  50% {
    opacity: var(--fa-fade-opacity, 0.4);
  }
}
@keyframes fa-beat-fade {
  0%, 100% {
    opacity: var(--fa-beat-fade-opacity, 0.4);
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(var(--fa-beat-fade-scale, 1.125));
  }
}
@keyframes fa-flip {
  50% {
    transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
  }
}
@keyframes fa-shake {
  0% {
    transform: rotate(-15deg);
  }
  4% {
    transform: rotate(15deg);
  }
  8%, 24% {
    transform: rotate(-18deg);
  }
  12%, 28% {
    transform: rotate(18deg);
  }
  16% {
    transform: rotate(-22deg);
  }
  20% {
    transform: rotate(22deg);
  }
  32% {
    transform: rotate(-12deg);
  }
  36% {
    transform: rotate(12deg);
  }
  40%, 100% {
    transform: rotate(0deg);
  }
}
@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.fa-rotate-90 {
  transform: rotate(90deg);
}

.fa-rotate-180 {
  transform: rotate(180deg);
}

.fa-rotate-270 {
  transform: rotate(270deg);
}

.fa-flip-horizontal {
  transform: scale(-1, 1);
}

.fa-flip-vertical {
  transform: scale(1, -1);
}

.fa-flip-both,
.fa-flip-horizontal.fa-flip-vertical {
  transform: scale(-1, -1);
}

.fa-rotate-by {
  transform: rotate(var(--fa-rotate-angle, 0));
}

.svg-inline--fa .fa-primary {
  fill: var(--fa-primary-color, currentColor);
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa .fa-secondary {
  fill: var(--fa-secondary-color, currentColor);
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-primary {
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-secondary {
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa mask .fa-primary,
.svg-inline--fa mask .fa-secondary {
  fill: black;
}

.svg-inline--fa.fa-inverse {
  fill: var(--fa-inverse, #fff);
}

.fa-stack {
  display: inline-block;
  height: 2em;
  line-height: 2em;
  position: relative;
  vertical-align: middle;
  width: 2.5em;
}

.fa-inverse {
  color: var(--fa-inverse, #fff);
}

.svg-inline--fa.fa-stack-1x {
  --fa-width: 1.25em;
  height: 1em;
  width: var(--fa-width);
}
.svg-inline--fa.fa-stack-2x {
  --fa-width: 2.5em;
  height: 2em;
  width: var(--fa-width);
}

.fa-stack-1x,
.fa-stack-2x {
  inset: 0;
  margin: auto;
  position: absolute;
  z-index: var(--fa-stack-z-index, auto);
}`;function Qn(){var e=Hn,n=qn,t=b.cssPrefix,a=b.replacementClass,r=Hi;if(t!==e||a!==n){var i=new RegExp("\\.".concat(e,"\\-"),"g"),o=new RegExp("\\--".concat(e,"\\-"),"g"),s=new RegExp("\\.".concat(n),"g");r=r.replace(i,".".concat(t,"-")).replace(o,"--".concat(t,"-")).replace(s,".".concat(a))}return r}var Kt=!1;function Be(){b.autoAddCss&&!Kt&&(Ri(Qn()),Kt=!0)}var qi={mixout:function(){return{dom:{css:Qn,insertCss:Be}}},hooks:function(){return{beforeDOMElementCreation:function(){Be()},beforeI2svg:function(){Be()}}}},V=X||{};V[K]||(V[K]={});V[K].styles||(V[K].styles={});V[K].hooks||(V[K].hooks={});V[K].shims||(V[K].shims=[]);var U=V[K],Zn=[],ea=function(){O.removeEventListener("DOMContentLoaded",ea),Le=1,Zn.map(function(n){return n()})},Le=!1;G&&(Le=(O.documentElement.doScroll?/^loaded|^c/:/^loaded|^i|^c/).test(O.readyState),Le||O.addEventListener("DOMContentLoaded",ea));function Bi(e){G&&(Le?setTimeout(e,0):Zn.push(e))}function ye(e){var n=e.tag,t=e.attributes,a=t===void 0?{}:t,r=e.children,i=r===void 0?[]:r;return typeof e=="string"?Jn(e):"<".concat(n," ").concat(zi(a),">").concat(i.map(ye).join(""),"</").concat(n,">")}function Vt(e,n,t){if(e&&e[n]&&e[n][t])return{prefix:n,iconName:t,icon:e[n][t]}}var Ke=function(n,t,a,r){var i=Object.keys(n),o=i.length,s=t,l,f,d;for(a===void 0?(l=1,d=n[i[0]]):(l=0,d=a);l<o;l++)f=i[l],d=s(d,n[f],f,n);return d};function ta(e){return Y(e).length!==1?null:e.codePointAt(0).toString(16)}function Gt(e){return Object.keys(e).reduce(function(n,t){var a=e[t],r=!!a.icon;return r?n[a.iconName]=a.icon:n[t]=a,n},{})}function rt(e,n){var t=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},a=t.skipHooks,r=a===void 0?!1:a,i=Gt(n);typeof U.hooks.addPack=="function"&&!r?U.hooks.addPack(e,Gt(n)):U.styles[e]=u(u({},U.styles[e]||{}),i),e==="fas"&&rt("fa",n)}var ge=U.styles,Ki=U.shims,na=Object.keys(vt),Vi=na.reduce(function(e,n){return e[n]=Object.keys(vt[n]),e},{}),St=null,aa={},ra={},ia={},oa={},sa={};function Gi(e){return~Di.indexOf(e)}function Xi(e,n){var t=n.split("-"),a=t[0],r=t.slice(1).join("-");return a===e&&r!==""&&!Gi(r)?r:null}var la=function(){var n=function(i){return Ke(ge,function(o,s,l){return o[l]=Ke(s,i,{}),o},{})};aa=n(function(r,i,o){if(i[3]&&(r[i[3]]=o),i[2]){var s=i[2].filter(function(l){return typeof l=="number"});s.forEach(function(l){r[l.toString(16)]=o})}return r}),ra=n(function(r,i,o){if(r[o]=o,i[2]){var s=i[2].filter(function(l){return typeof l=="string"});s.forEach(function(l){r[l]=o})}return r}),sa=n(function(r,i,o){var s=i[2];return r[o]=o,s.forEach(function(l){r[l]=o}),r});var t="far"in ge||b.autoFetchSvg,a=Ke(Ki,function(r,i){var o=i[0],s=i[1],l=i[2];return s==="far"&&!t&&(s="fas"),typeof o=="string"&&(r.names[o]={prefix:s,iconName:l}),typeof o=="number"&&(r.unicodes[o.toString(16)]={prefix:s,iconName:l}),r},{names:{},unicodes:{}});ia=a.names,oa=a.unicodes,St=We(b.styleDefault,{family:b.familyDefault})};ji(function(e){St=We(e.styleDefault,{family:b.familyDefault})});la();function xt(e,n){return(aa[e]||{})[n]}function Ji(e,n){return(ra[e]||{})[n]}function Z(e,n){return(sa[e]||{})[n]}function fa(e){return ia[e]||{prefix:null,iconName:null}}function Qi(e){var n=oa[e],t=xt("fas",e);return n||(t?{prefix:"fas",iconName:t}:null)||{prefix:null,iconName:null}}function J(){return St}var ca=function(){return{prefix:null,iconName:null,rest:[]}};function Zi(e){var n=$,t=na.reduce(function(a,r){return a[r]="".concat(b.cssPrefix,"-").concat(r),a},{});return Wn.forEach(function(a){(e.includes(t[a])||e.some(function(r){return Vi[a].includes(r)}))&&(n=a)}),n}function We(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},t=n.family,a=t===void 0?$:t,r=ki[a][e];if(a===ve&&!e)return"fad";var i=qt[a][e]||qt[a][r],o=e in U.styles?e:null,s=i||o||null;return s}function eo(e){var n=[],t=null;return e.forEach(function(a){var r=Xi(b.cssPrefix,a);r?t=r:a&&n.push(a)}),{iconName:t,rest:n}}function Xt(e){return e.sort().filter(function(n,t,a){return a.indexOf(n)===t})}var Jt=Un.concat(zn);function ze(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},t=n.skipLookups,a=t===void 0?!1:t,r=null,i=Xt(e.filter(function(x){return Jt.includes(x)})),o=Xt(e.filter(function(x){return!Jt.includes(x)})),s=i.filter(function(x){return r=x,!wn.includes(x)}),l=je(s,1),f=l[0],d=f===void 0?null:f,m=Zi(i),S=u(u({},eo(o)),{},{prefix:We(d,{family:m})});return u(u(u({},S),ro({values:e,family:m,styles:ge,config:b,canonical:S,givenPrefix:r})),to(a,r,S))}function to(e,n,t){var a=t.prefix,r=t.iconName;if(e||!a||!r)return{prefix:a,iconName:r};var i=n==="fa"?fa(r):{},o=Z(a,r);return r=i.iconName||o||r,a=i.prefix||a,a==="far"&&!ge.far&&ge.fas&&!b.autoFetchSvg&&(a="fas"),{prefix:a,iconName:r}}var no=Wn.filter(function(e){return e!==$||e!==ve}),ao=Object.keys(Qe).filter(function(e){return e!==$}).map(function(e){return Object.keys(Qe[e])}).flat();function ro(e){var n=e.values,t=e.family,a=e.canonical,r=e.givenPrefix,i=r===void 0?"":r,o=e.styles,s=o===void 0?{}:o,l=e.config,f=l===void 0?{}:l,d=t===ve,m=n.includes("fa-duotone")||n.includes("fad"),S=f.familyDefault==="duotone",x=a.prefix==="fad"||a.prefix==="fa-duotone";if(!d&&(m||S||x)&&(a.prefix="fad"),(n.includes("fa-brands")||n.includes("fab"))&&(a.prefix="fab"),!a.prefix&&no.includes(t)){var T=Object.keys(s).find(function(I){return ao.includes(I)});if(T||f.autoFetchSvg){var w=yr.get(t).defaultShortPrefixId;a.prefix=w,a.iconName=Z(a.prefix,a.iconName)||a.iconName}}return(a.prefix==="fa"||i==="fa")&&(a.prefix=J()||"fas"),a}var io=function(){function e(){Wa(this,e),this.definitions={}}return Ua(e,[{key:"add",value:function(){for(var t=this,a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];var o=r.reduce(this._pullDefinitions,{});Object.keys(o).forEach(function(s){t.definitions[s]=u(u({},t.definitions[s]||{}),o[s]),rt(s,o[s]);var l=vt[$][s];l&&rt(l,o[s]),la()})}},{key:"reset",value:function(){this.definitions={}}},{key:"_pullDefinitions",value:function(t,a){var r=a.prefix&&a.iconName&&a.icon?{0:a}:a;return Object.keys(r).map(function(i){var o=r[i],s=o.prefix,l=o.iconName,f=o.icon,d=f[2];t[s]||(t[s]={}),d.length>0&&d.forEach(function(m){typeof m=="string"&&(t[s][m]=f)}),t[s][l]=f}),t}}])}(),Qt=[],oe={},se={},oo=Object.keys(se);function so(e,n){var t=n.mixoutsTo;return Qt=e,oe={},Object.keys(se).forEach(function(a){oo.indexOf(a)===-1&&delete se[a]}),Qt.forEach(function(a){var r=a.mixout?a.mixout():{};if(Object.keys(r).forEach(function(o){typeof r[o]=="function"&&(t[o]=r[o]),De(r[o])==="object"&&Object.keys(r[o]).forEach(function(s){t[o]||(t[o]={}),t[o][s]=r[o][s]})}),a.hooks){var i=a.hooks();Object.keys(i).forEach(function(o){oe[o]||(oe[o]=[]),oe[o].push(i[o])})}a.provides&&a.provides(se)}),t}function it(e,n){for(var t=arguments.length,a=new Array(t>2?t-2:0),r=2;r<t;r++)a[r-2]=arguments[r];var i=oe[e]||[];return i.forEach(function(o){n=o.apply(null,[n].concat(a))}),n}function te(e){for(var n=arguments.length,t=new Array(n>1?n-1:0),a=1;a<n;a++)t[a-1]=arguments[a];var r=oe[e]||[];r.forEach(function(i){i.apply(null,t)})}function Q(){var e=arguments[0],n=Array.prototype.slice.call(arguments,1);return se[e]?se[e].apply(null,n):void 0}function ot(e){e.prefix==="fa"&&(e.prefix="fas");var n=e.iconName,t=e.prefix||J();if(n)return n=Z(t,n)||n,Vt(ua.definitions,t,n)||Vt(U.styles,t,n)}var ua=new io,lo=function(){b.autoReplaceSvg=!1,b.observeMutations=!1,te("noAuto")},fo={i2svg:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};return G?(te("beforeI2svg",n),Q("pseudoElements2svg",n),Q("i2svg",n)):Promise.reject(new Error("Operation requires a DOM of some kind."))},watch:function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},t=n.autoReplaceSvgRoot;b.autoReplaceSvg===!1&&(b.autoReplaceSvg=!0),b.observeMutations=!0,Bi(function(){uo({autoReplaceSvgRoot:t}),te("watch",n)})}},co={icon:function(n){if(n===null)return null;if(De(n)==="object"&&n.prefix&&n.iconName)return{prefix:n.prefix,iconName:Z(n.prefix,n.iconName)||n.iconName};if(Array.isArray(n)&&n.length===2){var t=n[1].indexOf("fa-")===0?n[1].slice(3):n[1],a=We(n[0]);return{prefix:a,iconName:Z(a,t)||t}}if(typeof n=="string"&&(n.indexOf("".concat(b.cssPrefix,"-"))>-1||n.match(Ti))){var r=ze(n.split(" "),{skipLookups:!0});return{prefix:r.prefix||J(),iconName:Z(r.prefix,r.iconName)||r.iconName}}if(typeof n=="string"){var i=J();return{prefix:i,iconName:Z(i,n)||n}}}},W={noAuto:lo,config:b,dom:fo,parse:co,library:ua,findIconDefinition:ot,toHtml:ye},uo=function(){var n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},t=n.autoReplaceSvgRoot,a=t===void 0?O:t;(Object.keys(U.styles).length>0||b.autoFetchSvg)&&G&&b.autoReplaceSvg&&W.dom.i2svg({node:a})};function Ue(e,n){return Object.defineProperty(e,"abstract",{get:n}),Object.defineProperty(e,"html",{get:function(){return e.abstract.map(function(a){return ye(a)})}}),Object.defineProperty(e,"node",{get:function(){if(G){var a=O.createElement("div");return a.innerHTML=e.html,a.children}}}),e}function mo(e){var n=e.children,t=e.main,a=e.mask,r=e.attributes,i=e.styles,o=e.transform;if(yt(o)&&t.found&&!a.found){var s=t.width,l=t.height,f={x:s/l/2,y:.5};r.style=Re(u(u({},i),{},{"transform-origin":"".concat(f.x+o.x/16,"em ").concat(f.y+o.y/16,"em")}))}return[{tag:"svg",attributes:r,children:n}]}function ho(e){var n=e.prefix,t=e.iconName,a=e.children,r=e.attributes,i=e.symbol,o=i===!0?"".concat(n,"-").concat(b.cssPrefix,"-").concat(t):i;return[{tag:"svg",attributes:{style:"display: none;"},children:[{tag:"symbol",attributes:u(u({},r),{},{id:o}),children:a}]}]}function go(e){var n=["aria-label","aria-labelledby","title","role"];return n.some(function(t){return t in e})}function wt(e){var n=e.icons,t=n.main,a=n.mask,r=e.prefix,i=e.iconName,o=e.transform,s=e.symbol,l=e.maskId,f=e.extra,d=e.watchable,m=d===void 0?!1:d,S=a.found?a:t,x=S.width,T=S.height,w=[b.replacementClass,i?"".concat(b.cssPrefix,"-").concat(i):""].filter(function(M){return f.classes.indexOf(M)===-1}).filter(function(M){return M!==""||!!M}).concat(f.classes).join(" "),I={children:[],attributes:u(u({},f.attributes),{},{"data-prefix":r,"data-icon":i,class:w,role:f.attributes.role||"img",viewBox:"0 0 ".concat(x," ").concat(T)})};!go(f.attributes)&&!f.attributes["aria-hidden"]&&(I.attributes["aria-hidden"]="true"),m&&(I.attributes[ee]="");var k=u(u({},I),{},{prefix:r,iconName:i,main:t,mask:a,maskId:l,transform:o,symbol:s,styles:u({},f.styles)}),F=a.found&&t.found?Q("generateAbstractMask",k)||{children:[],attributes:{}}:Q("generateAbstractIcon",k)||{children:[],attributes:{}},N=F.children,L=F.attributes;return k.children=N,k.attributes=L,s?ho(k):mo(k)}function Zt(e){var n=e.content,t=e.width,a=e.height,r=e.transform,i=e.extra,o=e.watchable,s=o===void 0?!1:o,l=u(u({},i.attributes),{},{class:i.classes.join(" ")});s&&(l[ee]="");var f=u({},i.styles);yt(r)&&(f.transform=Yi({transform:r,width:t,height:a}),f["-webkit-transform"]=f.transform);var d=Re(f);d.length>0&&(l.style=d);var m=[];return m.push({tag:"span",attributes:l,children:[n]}),m}function po(e){var n=e.content,t=e.extra,a=u(u({},t.attributes),{},{class:t.classes.join(" ")}),r=Re(t.styles);r.length>0&&(a.style=r);var i=[];return i.push({tag:"span",attributes:a,children:[n]}),i}var Ve=U.styles;function st(e){var n=e[0],t=e[1],a=e.slice(4),r=je(a,1),i=r[0],o=null;return Array.isArray(i)?o={tag:"g",attributes:{class:"".concat(b.cssPrefix,"-").concat(qe.GROUP)},children:[{tag:"path",attributes:{class:"".concat(b.cssPrefix,"-").concat(qe.SECONDARY),fill:"currentColor",d:i[0]}},{tag:"path",attributes:{class:"".concat(b.cssPrefix,"-").concat(qe.PRIMARY),fill:"currentColor",d:i[1]}}]}:o={tag:"path",attributes:{fill:"currentColor",d:i}},{found:!0,width:n,height:t,icon:o}}var vo={found:!1,width:512,height:512};function bo(e,n){!Kn&&!b.showMissingIcons&&e&&console.error('Icon with name "'.concat(e,'" and prefix "').concat(n,'" is missing.'))}function lt(e,n){var t=n;return n==="fa"&&b.styleDefault!==null&&(n=J()),new Promise(function(a,r){if(t==="fa"){var i=fa(e)||{};e=i.iconName||e,n=i.prefix||n}if(e&&n&&Ve[n]&&Ve[n][e]){var o=Ve[n][e];return a(st(o))}bo(e,n),a(u(u({},vo),{},{icon:b.showMissingIcons&&e?Q("missingIconAbstract")||{}:{}}))})}var en=function(){},ft=b.measurePerformance&&Se&&Se.mark&&Se.measure?Se:{mark:en,measure:en},de='FA "7.2.0"',yo=function(n){return ft.mark("".concat(de," ").concat(n," begins")),function(){return da(n)}},da=function(n){ft.mark("".concat(de," ").concat(n," ends")),ft.measure("".concat(de," ").concat(n),"".concat(de," ").concat(n," begins"),"".concat(de," ").concat(n," ends"))},Et={begin:yo,end:da},Ne=function(){};function tn(e){var n=e.getAttribute?e.getAttribute(ee):null;return typeof n=="string"}function So(e){var n=e.getAttribute?e.getAttribute(gt):null,t=e.getAttribute?e.getAttribute(pt):null;return n&&t}function xo(e){return e&&e.classList&&e.classList.contains&&e.classList.contains(b.replacementClass)}function wo(){if(b.autoReplaceSvg===!0)return Fe.replace;var e=Fe[b.autoReplaceSvg];return e||Fe.replace}function Eo(e){return O.createElementNS("http://www.w3.org/2000/svg",e)}function Ao(e){return O.createElement(e)}function ma(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},t=n.ceFn,a=t===void 0?e.tag==="svg"?Eo:Ao:t;if(typeof e=="string")return O.createTextNode(e);var r=a(e.tag);Object.keys(e.attributes||[]).forEach(function(o){r.setAttribute(o,e.attributes[o])});var i=e.children||[];return i.forEach(function(o){r.appendChild(ma(o,{ceFn:a}))}),r}function Co(e){var n=" ".concat(e.outerHTML," ");return n="".concat(n,"Font Awesome fontawesome.com "),n}var Fe={replace:function(n){var t=n[0];if(t.parentNode)if(n[1].forEach(function(r){t.parentNode.insertBefore(ma(r),t)}),t.getAttribute(ee)===null&&b.keepOriginalSource){var a=O.createComment(Co(t));t.parentNode.replaceChild(a,t)}else t.remove()},nest:function(n){var t=n[0],a=n[1];if(~bt(t).indexOf(b.replacementClass))return Fe.replace(n);var r=new RegExp("".concat(b.cssPrefix,"-.*"));if(delete a[0].attributes.id,a[0].attributes.class){var i=a[0].attributes.class.split(" ").reduce(function(s,l){return l===b.replacementClass||l.match(r)?s.toSvg.push(l):s.toNode.push(l),s},{toNode:[],toSvg:[]});a[0].attributes.class=i.toSvg.join(" "),i.toNode.length===0?t.removeAttribute("class"):t.setAttribute("class",i.toNode.join(" "))}var o=a.map(function(s){return ye(s)}).join(`
`);t.setAttribute(ee,""),t.innerHTML=o}};function nn(e){e()}function ha(e,n){var t=typeof n=="function"?n:Ne;if(e.length===0)t();else{var a=nn;b.mutateApproach===Ii&&(a=X.requestAnimationFrame||nn),a(function(){var r=wo(),i=Et.begin("mutate");e.map(r),i(),t()})}}var At=!1;function ga(){At=!0}function ct(){At=!1}var Me=null;function an(e){if(zt&&b.observeMutations){var n=e.treeCallback,t=n===void 0?Ne:n,a=e.nodeCallback,r=a===void 0?Ne:a,i=e.pseudoElementsCallback,o=i===void 0?Ne:i,s=e.observeMutationsRoot,l=s===void 0?O:s;Me=new zt(function(f){if(!At){var d=J();fe(f).forEach(function(m){if(m.type==="childList"&&m.addedNodes.length>0&&!tn(m.addedNodes[0])&&(b.searchPseudoElements&&o(m.target),t(m.target)),m.type==="attributes"&&m.target.parentNode&&b.searchPseudoElements&&o([m.target],!0),m.type==="attributes"&&tn(m.target)&&~Oi.indexOf(m.attributeName))if(m.attributeName==="class"&&So(m.target)){var S=ze(bt(m.target)),x=S.prefix,T=S.iconName;m.target.setAttribute(gt,x||d),T&&m.target.setAttribute(pt,T)}else xo(m.target)&&r(m.target)})}}),G&&Me.observe(l,{childList:!0,attributes:!0,characterData:!0,subtree:!0})}}function _o(){Me&&Me.disconnect()}function Io(e){var n=e.getAttribute("style"),t=[];return n&&(t=n.split(";").reduce(function(a,r){var i=r.split(":"),o=i[0],s=i.slice(1);return o&&s.length>0&&(a[o]=s.join(":").trim()),a},{})),t}function Po(e){var n=e.getAttribute("data-prefix"),t=e.getAttribute("data-icon"),a=e.innerText!==void 0?e.innerText.trim():"",r=ze(bt(e));return r.prefix||(r.prefix=J()),n&&t&&(r.prefix=n,r.iconName=t),r.iconName&&r.prefix||(r.prefix&&a.length>0&&(r.iconName=Ji(r.prefix,e.innerText)||xt(r.prefix,ta(e.innerText))),!r.iconName&&b.autoFetchSvg&&e.firstChild&&e.firstChild.nodeType===Node.TEXT_NODE&&(r.iconName=e.firstChild.data)),r}function ko(e){var n=fe(e.attributes).reduce(function(t,a){return t.name!=="class"&&t.name!=="style"&&(t[a.name]=a.value),t},{});return n}function To(){return{iconName:null,prefix:null,transform:q,symbol:!1,mask:{iconName:null,prefix:null,rest:[]},maskId:null,extra:{classes:[],styles:{},attributes:{}}}}function rn(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{styleParser:!0},t=Po(e),a=t.iconName,r=t.prefix,i=t.rest,o=ko(e),s=it("parseNodeAttributes",{},e),l=n.styleParser?Io(e):[];return u({iconName:a,prefix:r,transform:q,mask:{iconName:null,prefix:null,rest:[]},maskId:null,symbol:!1,extra:{classes:i,styles:l,attributes:o}},s)}var No=U.styles;function pa(e){var n=b.autoReplaceSvg==="nest"?rn(e,{styleParser:!1}):rn(e);return~n.extra.classes.indexOf(Gn)?Q("generateLayersText",e,n):Q("generateSvgReplacementMutation",e,n)}function Fo(){return[].concat(Y(zn),Y(Un))}function on(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;if(!G)return Promise.resolve();var t=O.documentElement.classList,a=function(m){return t.add("".concat(Ht,"-").concat(m))},r=function(m){return t.remove("".concat(Ht,"-").concat(m))},i=b.autoFetchSvg?Fo():wn.concat(Object.keys(No));i.includes("fa")||i.push("fa");var o=[".".concat(Gn,":not([").concat(ee,"])")].concat(i.map(function(d){return".".concat(d,":not([").concat(ee,"])")})).join(", ");if(o.length===0)return Promise.resolve();var s=[];try{s=fe(e.querySelectorAll(o))}catch{}if(s.length>0)a("pending"),r("complete");else return Promise.resolve();var l=Et.begin("onTree"),f=s.reduce(function(d,m){try{var S=pa(m);S&&d.push(S)}catch(x){Kn||x.name==="MissingIcon"&&console.error(x)}return d},[]);return new Promise(function(d,m){Promise.all(f).then(function(S){ha(S,function(){a("active"),a("complete"),r("pending"),typeof n=="function"&&n(),l(),d()})}).catch(function(S){l(),m(S)})})}function Oo(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;pa(e).then(function(t){t&&ha([t],n)})}function Do(e){return function(n){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=(n||{}).icon?n:ot(n||{}),r=t.mask;return r&&(r=(r||{}).icon?r:ot(r||{})),e(a,u(u({},t),{},{mask:r}))}}var Lo=function(n){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=t.transform,r=a===void 0?q:a,i=t.symbol,o=i===void 0?!1:i,s=t.mask,l=s===void 0?null:s,f=t.maskId,d=f===void 0?null:f,m=t.classes,S=m===void 0?[]:m,x=t.attributes,T=x===void 0?{}:x,w=t.styles,I=w===void 0?{}:w;if(n){var k=n.prefix,F=n.iconName,N=n.icon;return Ue(u({type:"icon"},n),function(){return te("beforeDOMElementCreation",{iconDefinition:n,params:t}),wt({icons:{main:st(N),mask:l?st(l.icon):{found:!1,width:null,height:null,icon:{}}},prefix:k,iconName:F,transform:u(u({},q),r),symbol:o,maskId:d,extra:{attributes:T,styles:I,classes:S}})})}},Mo={mixout:function(){return{icon:Do(Lo)}},hooks:function(){return{mutationObserverCallbacks:function(t){return t.treeCallback=on,t.nodeCallback=Oo,t}}},provides:function(n){n.i2svg=function(t){var a=t.node,r=a===void 0?O:a,i=t.callback,o=i===void 0?function(){}:i;return on(r,o)},n.generateSvgReplacementMutation=function(t,a){var r=a.iconName,i=a.prefix,o=a.transform,s=a.symbol,l=a.mask,f=a.maskId,d=a.extra;return new Promise(function(m,S){Promise.all([lt(r,i),l.iconName?lt(l.iconName,l.prefix):Promise.resolve({found:!1,width:512,height:512,icon:{}})]).then(function(x){var T=je(x,2),w=T[0],I=T[1];m([t,wt({icons:{main:w,mask:I},prefix:i,iconName:r,transform:o,symbol:s,maskId:f,extra:d,watchable:!0})])}).catch(S)})},n.generateAbstractIcon=function(t){var a=t.children,r=t.attributes,i=t.main,o=t.transform,s=t.styles,l=Re(s);l.length>0&&(r.style=l);var f;return yt(o)&&(f=Q("generateAbstractTransformGrouping",{main:i,transform:o,containerWidth:i.width,iconWidth:i.width})),a.push(f||i.icon),{children:a,attributes:r}}}},$o={mixout:function(){return{layer:function(t){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=a.classes,i=r===void 0?[]:r;return Ue({type:"layer"},function(){te("beforeDOMElementCreation",{assembler:t,params:a});var o=[];return t(function(s){Array.isArray(s)?s.map(function(l){o=o.concat(l.abstract)}):o=o.concat(s.abstract)}),[{tag:"span",attributes:{class:["".concat(b.cssPrefix,"-layers")].concat(Y(i)).join(" ")},children:o}]})}}}},jo={mixout:function(){return{counter:function(t){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};a.title;var r=a.classes,i=r===void 0?[]:r,o=a.attributes,s=o===void 0?{}:o,l=a.styles,f=l===void 0?{}:l;return Ue({type:"counter",content:t},function(){return te("beforeDOMElementCreation",{content:t,params:a}),po({content:t.toString(),extra:{attributes:s,styles:f,classes:["".concat(b.cssPrefix,"-layers-counter")].concat(Y(i))}})})}}}},Ro={mixout:function(){return{text:function(t){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=a.transform,i=r===void 0?q:r,o=a.classes,s=o===void 0?[]:o,l=a.attributes,f=l===void 0?{}:l,d=a.styles,m=d===void 0?{}:d;return Ue({type:"text",content:t},function(){return te("beforeDOMElementCreation",{content:t,params:a}),Zt({content:t,transform:u(u({},q),i),extra:{attributes:f,styles:m,classes:["".concat(b.cssPrefix,"-layers-text")].concat(Y(s))}})})}}},provides:function(n){n.generateLayersText=function(t,a){var r=a.transform,i=a.extra,o=null,s=null;if(Sn){var l=parseInt(getComputedStyle(t).fontSize,10),f=t.getBoundingClientRect();o=f.width/l,s=f.height/l}return Promise.resolve([t,Zt({content:t.innerHTML,width:o,height:s,transform:r,extra:i,watchable:!0})])}}},va=new RegExp('"',"ug"),sn=[1105920,1112319],ln=u(u(u(u({},{FontAwesome:{normal:"fas",400:"fas"}}),br),Ci),Ir),ut=Object.keys(ln).reduce(function(e,n){return e[n.toLowerCase()]=ln[n],e},{}),Wo=Object.keys(ut).reduce(function(e,n){var t=ut[n];return e[n]=t[900]||Y(Object.entries(t))[0][1],e},{});function zo(e){var n=e.replace(va,"");return ta(Y(n)[0]||"")}function Uo(e){var n=e.getPropertyValue("font-feature-settings").includes("ss01"),t=e.getPropertyValue("content"),a=t.replace(va,""),r=a.codePointAt(0),i=r>=sn[0]&&r<=sn[1],o=a.length===2?a[0]===a[1]:!1;return i||o||n}function Yo(e,n){var t=e.replace(/^['"]|['"]$/g,"").toLowerCase(),a=parseInt(n),r=isNaN(a)?"normal":a;return(ut[t]||{})[r]||Wo[t]}function fn(e,n){var t="".concat(_i).concat(n.replace(":","-"));return new Promise(function(a,r){if(e.getAttribute(t)!==null)return a();var i=fe(e.children),o=i.filter(function(p){return p.getAttribute(et)===n})[0],s=X.getComputedStyle(e,n),l=s.getPropertyValue("font-family"),f=l.match(Ni),d=s.getPropertyValue("font-weight"),m=s.getPropertyValue("content");if(o&&!f)return e.removeChild(o),a();if(f&&m!=="none"&&m!==""){var S=s.getPropertyValue("content"),x=Yo(l,d),T=zo(S),w=f[0].startsWith("FontAwesome"),I=Uo(s),k=xt(x,T),F=k;if(w){var N=Qi(T);N.iconName&&N.prefix&&(k=N.iconName,x=N.prefix)}if(k&&!I&&(!o||o.getAttribute(gt)!==x||o.getAttribute(pt)!==F)){e.setAttribute(t,F),o&&e.removeChild(o);var L=To(),M=L.extra;M.attributes[et]=n,lt(k,x).then(function(p){var v=wt(u(u({},L),{},{icons:{main:p,mask:ca()},prefix:x,iconName:F,extra:M,watchable:!0})),E=O.createElementNS("http://www.w3.org/2000/svg","svg");n==="::before"?e.insertBefore(E,e.firstChild):e.appendChild(E),E.outerHTML=v.map(function(P){return ye(P)}).join(`
`),e.removeAttribute(t),a()}).catch(r)}else a()}else a()})}function Ho(e){return Promise.all([fn(e,"::before"),fn(e,"::after")])}function qo(e){return e.parentNode!==document.head&&!~Pi.indexOf(e.tagName.toUpperCase())&&!e.getAttribute(et)&&(!e.parentNode||e.parentNode.tagName!=="svg")}var Bo=function(n){return!!n&&Bn.some(function(t){return n.includes(t)})},Ko=function(n){if(!n)return[];var t=new Set,a=n.split(/,(?![^()]*\))/).map(function(l){return l.trim()});a=a.flatMap(function(l){return l.includes("(")?l:l.split(",").map(function(f){return f.trim()})});var r=Te(a),i;try{for(r.s();!(i=r.n()).done;){var o=i.value;if(Bo(o)){var s=Bn.reduce(function(l,f){return l.replace(f,"")},o);s!==""&&s!=="*"&&t.add(s)}}}catch(l){r.e(l)}finally{r.f()}return t};function cn(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1;if(G){var t;if(n)t=e;else if(b.searchPseudoElementsFullScan)t=e.querySelectorAll("*");else{var a=new Set,r=Te(document.styleSheets),i;try{for(r.s();!(i=r.n()).done;){var o=i.value;try{var s=Te(o.cssRules),l;try{for(s.s();!(l=s.n()).done;){var f=l.value,d=Ko(f.selectorText),m=Te(d),S;try{for(m.s();!(S=m.n()).done;){var x=S.value;a.add(x)}}catch(w){m.e(w)}finally{m.f()}}}catch(w){s.e(w)}finally{s.f()}}catch(w){b.searchPseudoElementsWarnings&&console.warn("Font Awesome: cannot parse stylesheet: ".concat(o.href," (").concat(w.message,`)
If it declares any Font Awesome CSS pseudo-elements, they will not be rendered as SVG icons. Add crossorigin="anonymous" to the <link>, enable searchPseudoElementsFullScan for slower but more thorough DOM parsing, or suppress this warning by setting searchPseudoElementsWarnings to false.`))}}}catch(w){r.e(w)}finally{r.f()}if(!a.size)return;var T=Array.from(a).join(", ");try{t=e.querySelectorAll(T)}catch{}}return new Promise(function(w,I){var k=fe(t).filter(qo).map(Ho),F=Et.begin("searchPseudoElements");ga(),Promise.all(k).then(function(){F(),ct(),w()}).catch(function(){F(),ct(),I()})})}}var Vo={hooks:function(){return{mutationObserverCallbacks:function(t){return t.pseudoElementsCallback=cn,t}}},provides:function(n){n.pseudoElements2svg=function(t){var a=t.node,r=a===void 0?O:a;b.searchPseudoElements&&cn(r)}}},un=!1,Go={mixout:function(){return{dom:{unwatch:function(){ga(),un=!0}}}},hooks:function(){return{bootstrap:function(){an(it("mutationObserverCallbacks",{}))},noAuto:function(){_o()},watch:function(t){var a=t.observeMutationsRoot;un?ct():an(it("mutationObserverCallbacks",{observeMutationsRoot:a}))}}}},dn=function(n){var t={size:16,x:0,y:0,flipX:!1,flipY:!1,rotate:0};return n.toLowerCase().split(" ").reduce(function(a,r){var i=r.toLowerCase().split("-"),o=i[0],s=i.slice(1).join("-");if(o&&s==="h")return a.flipX=!0,a;if(o&&s==="v")return a.flipY=!0,a;if(s=parseFloat(s),isNaN(s))return a;switch(o){case"grow":a.size=a.size+s;break;case"shrink":a.size=a.size-s;break;case"left":a.x=a.x-s;break;case"right":a.x=a.x+s;break;case"up":a.y=a.y-s;break;case"down":a.y=a.y+s;break;case"rotate":a.rotate=a.rotate+s;break}return a},t)},Xo={mixout:function(){return{parse:{transform:function(t){return dn(t)}}}},hooks:function(){return{parseNodeAttributes:function(t,a){var r=a.getAttribute("data-fa-transform");return r&&(t.transform=dn(r)),t}}},provides:function(n){n.generateAbstractTransformGrouping=function(t){var a=t.main,r=t.transform,i=t.containerWidth,o=t.iconWidth,s={transform:"translate(".concat(i/2," 256)")},l="translate(".concat(r.x*32,", ").concat(r.y*32,") "),f="scale(".concat(r.size/16*(r.flipX?-1:1),", ").concat(r.size/16*(r.flipY?-1:1),") "),d="rotate(".concat(r.rotate," 0 0)"),m={transform:"".concat(l," ").concat(f," ").concat(d)},S={transform:"translate(".concat(o/2*-1," -256)")},x={outer:s,inner:m,path:S};return{tag:"g",attributes:u({},x.outer),children:[{tag:"g",attributes:u({},x.inner),children:[{tag:a.icon.tag,children:a.icon.children,attributes:u(u({},a.icon.attributes),x.path)}]}]}}}},Ge={x:0,y:0,width:"100%",height:"100%"};function mn(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0;return e.attributes&&(e.attributes.fill||n)&&(e.attributes.fill="black"),e}function Jo(e){return e.tag==="g"?e.children:[e]}var Qo={hooks:function(){return{parseNodeAttributes:function(t,a){var r=a.getAttribute("data-fa-mask"),i=r?ze(r.split(" ").map(function(o){return o.trim()})):ca();return i.prefix||(i.prefix=J()),t.mask=i,t.maskId=a.getAttribute("data-fa-mask-id"),t}}},provides:function(n){n.generateAbstractMask=function(t){var a=t.children,r=t.attributes,i=t.main,o=t.mask,s=t.maskId,l=t.transform,f=i.width,d=i.icon,m=o.width,S=o.icon,x=Ui({transform:l,containerWidth:m,iconWidth:f}),T={tag:"rect",attributes:u(u({},Ge),{},{fill:"white"})},w=d.children?{children:d.children.map(mn)}:{},I={tag:"g",attributes:u({},x.inner),children:[mn(u({tag:d.tag,attributes:u(u({},d.attributes),x.path)},w))]},k={tag:"g",attributes:u({},x.outer),children:[I]},F="mask-".concat(s||Bt()),N="clip-".concat(s||Bt()),L={tag:"mask",attributes:u(u({},Ge),{},{id:F,maskUnits:"userSpaceOnUse",maskContentUnits:"userSpaceOnUse"}),children:[T,k]},M={tag:"defs",children:[{tag:"clipPath",attributes:{id:N},children:Jo(S)},L]};return a.push(M,{tag:"rect",attributes:u({fill:"currentColor","clip-path":"url(#".concat(N,")"),mask:"url(#".concat(F,")")},Ge)}),{children:a,attributes:r}}}},Zo={provides:function(n){var t=!1;X.matchMedia&&(t=X.matchMedia("(prefers-reduced-motion: reduce)").matches),n.missingIconAbstract=function(){var a=[],r={fill:"currentColor"},i={attributeType:"XML",repeatCount:"indefinite",dur:"2s"};a.push({tag:"path",attributes:u(u({},r),{},{d:"M156.5,447.7l-12.6,29.5c-18.7-9.5-35.9-21.2-51.5-34.9l22.7-22.7C127.6,430.5,141.5,440,156.5,447.7z M40.6,272H8.5 c1.4,21.2,5.4,41.7,11.7,61.1L50,321.2C45.1,305.5,41.8,289,40.6,272z M40.6,240c1.4-18.8,5.2-37,11.1-54.1l-29.5-12.6 C14.7,194.3,10,216.7,8.5,240H40.6z M64.3,156.5c7.8-14.9,17.2-28.8,28.1-41.5L69.7,92.3c-13.7,15.6-25.5,32.8-34.9,51.5 L64.3,156.5z M397,419.6c-13.9,12-29.4,22.3-46.1,30.4l11.9,29.8c20.7-9.9,39.8-22.6,56.9-37.6L397,419.6z M115,92.4 c13.9-12,29.4-22.3,46.1-30.4l-11.9-29.8c-20.7,9.9-39.8,22.6-56.8,37.6L115,92.4z M447.7,355.5c-7.8,14.9-17.2,28.8-28.1,41.5 l22.7,22.7c13.7-15.6,25.5-32.9,34.9-51.5L447.7,355.5z M471.4,272c-1.4,18.8-5.2,37-11.1,54.1l29.5,12.6 c7.5-21.1,12.2-43.5,13.6-66.8H471.4z M321.2,462c-15.7,5-32.2,8.2-49.2,9.4v32.1c21.2-1.4,41.7-5.4,61.1-11.7L321.2,462z M240,471.4c-18.8-1.4-37-5.2-54.1-11.1l-12.6,29.5c21.1,7.5,43.5,12.2,66.8,13.6V471.4z M462,190.8c5,15.7,8.2,32.2,9.4,49.2h32.1 c-1.4-21.2-5.4-41.7-11.7-61.1L462,190.8z M92.4,397c-12-13.9-22.3-29.4-30.4-46.1l-29.8,11.9c9.9,20.7,22.6,39.8,37.6,56.9 L92.4,397z M272,40.6c18.8,1.4,36.9,5.2,54.1,11.1l12.6-29.5C317.7,14.7,295.3,10,272,8.5V40.6z M190.8,50 c15.7-5,32.2-8.2,49.2-9.4V8.5c-21.2,1.4-41.7,5.4-61.1,11.7L190.8,50z M442.3,92.3L419.6,115c12,13.9,22.3,29.4,30.5,46.1 l29.8-11.9C470,128.5,457.3,109.4,442.3,92.3z M397,92.4l22.7-22.7c-15.6-13.7-32.8-25.5-51.5-34.9l-12.6,29.5 C370.4,72.1,384.4,81.5,397,92.4z"})});var o=u(u({},i),{},{attributeName:"opacity"}),s={tag:"circle",attributes:u(u({},r),{},{cx:"256",cy:"364",r:"28"}),children:[]};return t||s.children.push({tag:"animate",attributes:u(u({},i),{},{attributeName:"r",values:"28;14;28;28;14;28;"})},{tag:"animate",attributes:u(u({},o),{},{values:"1;0;1;1;0;1;"})}),a.push(s),a.push({tag:"path",attributes:u(u({},r),{},{opacity:"1",d:"M263.7,312h-16c-6.6,0-12-5.4-12-12c0-71,77.4-63.9,77.4-107.8c0-20-17.8-40.2-57.4-40.2c-29.1,0-44.3,9.6-59.2,28.7 c-3.9,5-11.1,6-16.2,2.4l-13.1-9.2c-5.6-3.9-6.9-11.8-2.6-17.2c21.2-27.2,46.4-44.7,91.2-44.7c52.3,0,97.4,29.8,97.4,80.2 c0,67.6-77.4,63.5-77.4,107.8C275.7,306.6,270.3,312,263.7,312z"}),children:t?[]:[{tag:"animate",attributes:u(u({},o),{},{values:"1;0;0;0;0;1;"})}]}),t||a.push({tag:"path",attributes:u(u({},r),{},{opacity:"0",d:"M232.5,134.5l7,168c0.3,6.4,5.6,11.5,12,11.5h9c6.4,0,11.7-5.1,12-11.5l7-168c0.3-6.8-5.2-12.5-12-12.5h-23 C237.7,122,232.2,127.7,232.5,134.5z"}),children:[{tag:"animate",attributes:u(u({},o),{},{values:"0;0;1;1;0;0;"})}]}),{tag:"g",attributes:{class:"missing"},children:a}}}},es={hooks:function(){return{parseNodeAttributes:function(t,a){var r=a.getAttribute("data-fa-symbol"),i=r===null?!1:r===""?!0:r;return t.symbol=i,t}}}},ts=[qi,Mo,$o,jo,Ro,Vo,Go,Xo,Qo,Zo,es];so(ts,{mixoutsTo:W});W.noAuto;W.config;var ns=W.library,as=W.dom;W.parse;W.findIconDefinition;W.toHtml;W.icon;W.layer;W.text;W.counter;/*!
 * Font Awesome Free 7.2.0 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2026 Fonticons, Inc.
 */var rs={prefix:"fas",iconName:"share-from-square",icon:[576,512,[61509,"share-square"],"f14d","M384.5 24l0 72-64 0c-79.5 0-144 64.5-144 144 0 93.4 82.8 134.8 100.6 142.6 2.2 1 4.6 1.4 7.1 1.4l2.5 0c9.8 0 17.8-8 17.8-17.8 0-8.3-5.9-15.5-12.8-20.3-8.9-6.2-19.2-18.2-19.2-40.5 0-45 36.5-81.5 81.5-81.5l30.5 0 0 72c0 9.7 5.8 18.5 14.8 22.2s19.3 1.7 26.2-5.2l136-136c9.4-9.4 9.4-24.6 0-33.9L425.5 7c-6.9-6.9-17.2-8.9-26.2-5.2S384.5 14.3 384.5 24zm-272 72c-44.2 0-80 35.8-80 80l0 256c0 44.2 35.8 80 80 80l256 0c44.2 0 80-35.8 80-80l0-32c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 32c0 8.8-7.2 16-16 16l-256 0c-8.8 0-16-7.2-16-16l0-256c0-8.8 7.2-16 16-16l16 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-16 0z"]},is=rs,os={prefix:"fas",iconName:"plane-departure",icon:[576,512,[128747],"f5b0","M372 143.9L172.7 40.2c-8-4.1-17.3-4.8-25.7-1.7l-41.1 15c-10.3 3.7-13.8 16.4-7.1 25L200.3 206.4 100.1 242.8 40 206.2c-6.2-3.8-13.8-4.5-20.7-2.1L3 210.1c-9.4 3.4-13.4 14.5-8.3 23.1l53.6 91.8c15.6 26.7 48.1 38.4 77.1 27.8l12.9-4.7 0 0 398.4-145c29.1-10.6 44-42.7 33.5-71.8s-42.7-44-71.8-33.5L372 143.9zM32.2 448c-17.7 0-32 14.3-32 32s14.3 32 32 32l512 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-512 0z"]},ss={prefix:"fas",iconName:"sun",icon:[576,512,[9728],"f185","M288-32c8.4 0 16.3 4.4 20.6 11.7L364.1 72.3 468.9 46c8.2-2 16.9 .4 22.8 6.3S500 67 498 75.1l-26.3 104.7 92.7 55.5c7.2 4.3 11.7 12.2 11.7 20.6s-4.4 16.3-11.7 20.6L471.7 332.1 498 436.8c2 8.2-.4 16.9-6.3 22.8S477 468 468.9 466l-104.7-26.3-55.5 92.7c-4.3 7.2-12.2 11.7-20.6 11.7s-16.3-4.4-20.6-11.7L211.9 439.7 107.2 466c-8.2 2-16.8-.4-22.8-6.3S76 445 78 436.8l26.2-104.7-92.6-55.5C4.4 272.2 0 264.4 0 256s4.4-16.3 11.7-20.6L104.3 179.9 78 75.1c-2-8.2 .3-16.8 6.3-22.8S99 44 107.2 46l104.7 26.2 55.5-92.6 1.8-2.6c4.5-5.7 11.4-9.1 18.8-9.1zm0 144a144 144 0 1 0 0 288 144 144 0 1 0 0-288zm0 240a96 96 0 1 1 0-192 96 96 0 1 1 0 192z"]},ls={prefix:"fas",iconName:"gear",icon:[512,512,[9881,"cog"],"f013","M195.1 9.5C198.1-5.3 211.2-16 226.4-16l59.8 0c15.2 0 28.3 10.7 31.3 25.5L332 79.5c14.1 6 27.3 13.7 39.3 22.8l67.8-22.5c14.4-4.8 30.2 1.2 37.8 14.4l29.9 51.8c7.6 13.2 4.9 29.8-6.5 39.9L447 233.3c.9 7.4 1.3 15 1.3 22.7s-.5 15.3-1.3 22.7l53.4 47.5c11.4 10.1 14 26.8 6.5 39.9l-29.9 51.8c-7.6 13.1-23.4 19.2-37.8 14.4l-67.8-22.5c-12.1 9.1-25.3 16.7-39.3 22.8l-14.4 69.9c-3.1 14.9-16.2 25.5-31.3 25.5l-59.8 0c-15.2 0-28.3-10.7-31.3-25.5l-14.4-69.9c-14.1-6-27.2-13.7-39.3-22.8L73.5 432.3c-14.4 4.8-30.2-1.2-37.8-14.4L5.8 366.1c-7.6-13.2-4.9-29.8 6.5-39.9l53.4-47.5c-.9-7.4-1.3-15-1.3-22.7s.5-15.3 1.3-22.7L12.3 185.8c-11.4-10.1-14-26.8-6.5-39.9L35.7 94.1c7.6-13.2 23.4-19.2 37.8-14.4l67.8 22.5c12.1-9.1 25.3-16.7 39.3-22.8L195.1 9.5zM256.3 336a80 80 0 1 0 -.6-160 80 80 0 1 0 .6 160z"]},fs=ls,cs={prefix:"fas",iconName:"moon",icon:[512,512,[127769,9214],"f186","M256 0C114.6 0 0 114.6 0 256S114.6 512 256 512c68.8 0 131.3-27.2 177.3-71.4 7.3-7 9.4-17.9 5.3-27.1s-13.7-14.9-23.8-14.1c-4.9 .4-9.8 .6-14.8 .6-101.6 0-184-82.4-184-184 0-72.1 41.5-134.6 102.1-164.8 9.1-4.5 14.3-14.3 13.1-24.4S322.6 8.5 312.7 6.3C294.4 2.2 275.4 0 256 0z"]},us={prefix:"fas",iconName:"chevron-down",icon:[448,512,[],"f078","M201.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 338.7 54.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z"]},ds={prefix:"fas",iconName:"circle-info",icon:[512,512,["info-circle"],"f05a","M256 512a256 256 0 1 0 0-512 256 256 0 1 0 0 512zM224 160a32 32 0 1 1 64 0 32 32 0 1 1 -64 0zm-8 64l48 0c13.3 0 24 10.7 24 24l0 88 8 0c13.3 0 24 10.7 24 24s-10.7 24-24 24l-80 0c-13.3 0-24-10.7-24-24s10.7-24 24-24l24 0 0-64-24 0c-13.3 0-24-10.7-24-24s10.7-24 24-24z"]},ms=ds;/*!
 * Font Awesome Free 7.2.0 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2026 Fonticons, Inc.
 */var hs={prefix:"fab",iconName:"apple",icon:[384,512,[],"f179","M319.1 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7-55.8 .9-115.1 44.5-115.1 133.2 0 26.2 4.8 53.3 14.4 81.2 12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zM262.5 104.5c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"]};ns.add(ss,cs,fs,us,ms,os,is,hs);as.watch();let pe="iphone",B=null,z=31.5,ie=1.5;function gs(){const e=localStorage.getItem("theme");if(e)document.documentElement.setAttribute("data-bs-theme",e),Oe(e);else{const n=window.matchMedia("(prefers-color-scheme: dark)").matches,t=n?"dark":"light";(window.location.hostname==="localhost"||window.location.hostname==="127.0.0.1")&&(console.log(`System prefers dark mode: ${n}`),console.log(`Setting theme to: ${t}`)),document.documentElement.setAttribute("data-bs-theme",t),Oe(t)}window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change",n=>{if(!localStorage.getItem("theme")){const t=n.matches?"dark":"light";document.documentElement.setAttribute("data-bs-theme",t),Oe(t),(window.location.hostname==="localhost"||window.location.hostname==="127.0.0.1")&&console.log(`System theme changed to: ${t}`)}}),document.getElementById("theme-toggle").addEventListener("click",ps)}function Oe(e){const n=document.querySelector("#theme-toggle i");e==="dark"?n.className="fas fa-moon fs-5":n.className="fas fa-sun fs-5"}function ps(){const n=document.documentElement.getAttribute("data-bs-theme")==="dark"?"light":"dark";document.documentElement.setAttribute("data-bs-theme",n),localStorage.setItem("theme",n),Oe(n)}function Xe(e,n){return e==null?"-":new Intl.NumberFormat("zh-TW",{style:"currency",currency:n,minimumFractionDigits:0,maximumFractionDigits:0}).format(e)}function dt(e){return e==null?"-":`${e>0?"+":""}${e}%`}function ba(e){if(!e)return"-";const n=new Date(e),t=n.getFullYear(),a=String(n.getMonth()+1).padStart(2,"0"),r=String(n.getDate()).padStart(2,"0");return`${t}-${a}-${r}`}function Ct(e){return e?e*(1+ie/100)*z:0}function vs(e){if(!e||e.length===0)return{avg:0,avgWithFee:0,max:0,min:0};const n=e.map(f=>{const d=f.Price_US||0,m=f.Price_TW||0;if(d<=0||m<=0)return 0;const S=d*z;return(m-S)/S*100}).filter(f=>f!==0),t=e.map(f=>{const d=f.Price_US||0,m=f.Price_TW||0;if(d<=0||m<=0)return 0;const S=Ct(d);return(m-S)/S*100}).filter(f=>f!==0);if(n.length===0)return{avg:0,avgWithFee:0,max:0,min:0};const r=n.reduce((f,d)=>f+d,0)/n.length,o=t.reduce((f,d)=>f+d,0)/t.length,s=Math.max(...n),l=Math.min(...n);return{avg:r,avgWithFee:o,max:s,min:l}}async function bs(e){try{const n=await fetch(`data/${e}_data.json`);if(!n.ok)throw new Error(`Failed to load ${e} data: ${n.status}`);const t=await n.json();if(t.metadata&&t.metadata.exchangeRates&&t.metadata.exchangeRates.TWD&&!B){z=t.metadata.exchangeRates.TWD;const a=document.getElementById("exchange-rate");a&&(a.value=z),console.log(`Using exchange rate from data: ${z}`)}if(t.metadata&&t.metadata.lastExchangeRateUpdate){const a=ba(t.metadata.lastExchangeRateUpdate),r=document.querySelector("#exchange-rate + .input-group + .form-text");r&&(r.innerHTML=`Current rate from Cathay Bank (updated: ${a})`)}return t.products.forEach(a=>{const r=a.Price_US||0,i=a.Price_TW||0;if(r>0&&i>0){const o=Ct(r);a.price_difference_with_fee_percent=(i-o)/o*100,a.price_difference_with_fee_percent=parseFloat(a.price_difference_with_fee_percent.toFixed(1)),a.recommended_purchase=a.price_difference_with_fee_percent>0?"US":"TW"}else a.price_difference_with_fee_percent=0,a.recommended_purchase="N/A"}),t}catch(n){return console.error("Failed to load product data:",n),{metadata:{lastUpdated:null,regions:["US","TW"],productType:e,totalProducts:0,exchangeRates:{TWD:z}},products:[]}}}function _t(e){const n=document.querySelector("#products-table tbody"),t=document.querySelector("#products-table thead tr");if(n.innerHTML="",t.innerHTML=`
    <th scope="col">Product</th>
    <th scope="col">US (USD)</th>
    <th scope="col" class="d-none d-md-table-cell">US+Fee (TWD)</th>
    <th scope="col">TW (TWD)</th>
    <th scope="col">Diff</th>
    <th scope="col" class="d-none d-md-table-cell">Rec.</th>
  `,!e||e.length===0){n.innerHTML=`
      <tr>
        <td colspan="6" class="text-center py-3">No product data found</td>
      </tr>
    `;return}e.forEach(a=>{const r=document.createElement("tr"),i=a.Price_US||0,o=a.Price_TW||0,s=Ct(i),l=o>0&&s>0?(o-s)/s*100:0,f=l>0?"price-higher":l<0?"price-lower":"",d=document.createElement("td");if(d.textContent=a.PRODUCT_NAME,pe==="mac"){const N=[];if(a.Chip&&N.push(a.Chip),a.Memory&&N.push(a.Memory),a.Storage&&N.push(a.Storage),a.CPU_Cores&&a.GPU_Cores&&N.push(`${a.CPU_Cores}C CPU / ${a.GPU_Cores}C GPU`),N.length>0){const L=document.createElement("small");L.className="text-muted d-block",L.textContent=N.join(" • "),d.appendChild(L)}}let m="No Data",S="bg-secondary";i>0&&o>0&&(l>2?(m="Buy in US",S="bg-danger"):l<-2?(m="Buy in Taiwan",S="bg-success"):(m="Similar",S="bg-info"));const x=document.createElement("td");x.textContent=Xe(i,"USD");const T=document.createElement("td");T.className="d-none d-md-table-cell",T.textContent=Xe(s,"TWD");const w=document.createElement("td");w.textContent=Xe(o,"TWD");const I=document.createElement("td");I.className=f,I.textContent=dt(l.toFixed(1));const k=document.createElement("td");k.className="d-none d-md-table-cell";const F=document.createElement("span");F.className=`badge ${S}`,F.textContent=m,k.appendChild(F),r.appendChild(d),r.appendChild(x),r.appendChild(T),r.appendChild(w),r.appendChild(I),r.appendChild(k),n.appendChild(r)})}function ya(e){if(!e||!e.products)return;const n=document.getElementById("total-products"),t=document.getElementById("avg-diff"),a=document.getElementById("avg-diff-with-fee"),r=document.getElementById("last-updated");n.textContent=e.products.length;const i=vs(e.products);t.textContent=dt(i.avg.toFixed(1)),t.className=i.avg>0?"card-text display-4 price-higher":"card-text display-4 price-lower",a.textContent=dt(i.avgWithFee.toFixed(1)),a.className=i.avgWithFee>0?"card-text display-4 price-higher":"card-text display-4 price-lower",r.textContent=ba(e.metadata.lastUpdated)}function ys(){const e=document.getElementById("exchange-rate"),n=document.getElementById("card-fee"),t=document.getElementById("settings-changed"),a=localStorage.getItem("price-settings");if(a){const i=JSON.parse(a);z=i.exchangeRate||31.5,ie=i.cardFee||1.5,e.value=z,n.value=ie}e.addEventListener("change",r),n.addEventListener("change",r);function r(){const i=parseFloat(e.value),o=parseFloat(n.value);if(!isNaN(i)&&!isNaN(o)&&i>0&&o>=0){const s=z!==i||ie!==o;z=i,ie=o,localStorage.setItem("price-settings",JSON.stringify({exchangeRate:z,cardFee:ie})),s&&(t.style.display="inline-block",setTimeout(()=>{t.style.display="none"},3e3),B&&(_t(B.products),ya(B)))}}}function Ss(){const e=document.getElementById("product-search");e&&e.addEventListener("input",n=>{const t=n.target.value.toLowerCase();if(!B||!B.products)return;const a=B.products.filter(r=>r.PRODUCT_NAME.toLowerCase().includes(t));_t(a)})}async function Sa(e){pe=e,document.querySelectorAll(".nav-link").forEach(t=>{t.classList.toggle("active",t.dataset.product===e)}),document.getElementById("page-title").textContent=`Apple ${e.toUpperCase()} Price Comparison`,B=await bs(e),ya(B),_t(B.products);const n=document.getElementById("product-search");n&&(n.value="")}function xs(){document.querySelectorAll(".nav-link").forEach(e=>{e.addEventListener("click",n=>{n.preventDefault(),window.location.hash=n.target.dataset.product})}),window.addEventListener("hashchange",()=>{const e=window.location.hash.slice(1)||"iphone";e!==pe&&Sa(e)})}function ws(){const e=/iPad|iPhone|iPod/.test(navigator.userAgent)&&!window.MSStream,n=/^((?!chrome|android).)*safari/i.test(navigator.userAgent);if(e&&n&&!(window.navigator.standalone===!0)&&!localStorage.getItem("ios-add-prompt-shown")){const r=document.getElementById("ios-add-to-home");r&&(r.classList.remove("d-none"),localStorage.setItem("ios-add-prompt-shown",Date.now()),setTimeout(()=>{localStorage.removeItem("ios-add-prompt-shown")},24*60*60*1e3))}}async function Es(){gs(),ys();const e=["iphone","ipad","mac","watch","airpods","tvhome"],n=window.location.hash.slice(1);n&&e.includes(n)&&(pe=n),Ss(),xs(),await Sa(pe),"serviceWorker"in navigator&&navigator.serviceWorker.register("./sw.js").catch(()=>{}),ws()}window.addEventListener("DOMContentLoaded",Es);
