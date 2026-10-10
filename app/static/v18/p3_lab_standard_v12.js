(function(global){
'use strict';
const STANDARD={
id:'NABIL_P3_SMART_LAB_STANDARD_V12',visual_language:'MATCH_MATH_GOLDEN_CARD',
supported_languages:{en:{ui:'en',speech:'en-US',dir:'ltr',label:'EN'},ar:{ui:'ar',speech:'ar-LB',dir:'rtl',label:'AR'},fr:{ui:'fr',speech:'fr-FR',dir:'ltr',label:'FR'}},
teacher:{typewriter:{title_ms:90,line_ms:65,text_ms:34,pause_after_line_ms:420,pause_after_step_ms:1200},speech:{rate:0.72,pitch:1,volume:1},sequence:['WRITE','SAY','POINT','HIGHLIGHT','ANIMATE','VERIFY','LOCK_RESULT'],final_reference_card:true,final_result_hidden_until_last_step:true},
presentation:{colors:{background:'#031025',card:'#082447',panel:'#071c35',board:'#04172c',border:'#1f5c91',cyan:'#25d8ff',gold:'#ffd35a',green:'#52e6a4',red:'#ff6178',violet:'#b98cff',text:'#f7fbff',muted:'#9fc4e5'},cards_match_math:true,left_results_progressive:true,current_step_gold:true,verified_result_green:true},
families:{mathematics:['function','algebra','geometry','analytic-geometry','vectors','sequences','probability','statistics','trigonometry','complex','matrices'],physics:['mechanics','dc-circuit','ohm-law','optics','waves','projectile','rc'],chemistry:['reaction','precipitation','ionic','molecular-structure','stoichiometry'],biology:['cell','heart-circulation','organ-system','process-diagram']},
contract:{full_lab_ui_from_start:true,final_answer_hidden:true,progressive_reveal:true,synchronized_voice_board_visual:true,restart_exact:true,p1_p2_untouched:true}
};
const api={STANDARD,getLanguage(code){return STANDARD.supported_languages[code]||STANDARD.supported_languages.en;}};
if(typeof module!=='undefined'&&module.exports)module.exports=api;global.NabilP3LabStandardV12=api;
})(typeof window!=='undefined'?window:globalThis);
