/*!
 * @author: Huang Teng
 */
function triggerShow5Hide(effectedSymbolString,triggerObj){
	var effectedObj=document.querySelector(effectedSymbolString)
	if (effectedObj.style.display=="none"){
		//show
		effectedObj.style.display="inline-block";
		//effectedObj.style.display="inline";
		triggerObj.innerHTML="Hide";
		triggerObj.value="Hide";
	}else{
		//hide
		effectedObj.style.display="none";
		triggerObj.innerHTML="Show";
		triggerObj.value="Show";
		//svg.parentNode.removeChild(svg);//backup
	}
}

function textShow5Truncate(text,intLen,triggerObj){
	var strContent=text; 
	var strTemp=""; 
	while(strContent.length>intLen){ 
		strTemp+=strContent.substr(0,intLen)+"<br/>"; 
		strContent=strContent.substr(intLen,strContent.length); 
	} 
	strTemp+=strContent; 
	triggerObj.innerHTML=strTemp; 
}
function textShow5Truncate(intLen,triggerObj){
	var strContent=triggerObj.getAttribute("content");
	//console.log(triggerObj.onmouseover)
	var strTemp=""; 
	while(strContent.length>intLen){ 
		strTemp+=strContent.substr(0,intLen)+"<br/>"; 
		strContent=strContent.substr(intLen,strContent.length); 
	} 
	strTemp+=strContent; 
	triggerObj.innerHTML=strTemp; 
}