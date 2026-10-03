/* NABIL Autonomous Classroom v13 loader — canonical deployed renderer. */
(function(){'use strict';
function boot(){
  var s=document.createElement('script');
  s.src='/app/static/nabil_classroom_engine_v10.js?v=13';
  s.async=false;
  s.onerror=function(){console.error('NABIL v13 canonical renderer failed to load');};
  document.head.appendChild(s);
}
boot();
})();