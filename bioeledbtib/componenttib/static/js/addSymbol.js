/*!
 * @author: Huang Teng Email: spacewalkerht@163.com
 * @copyright: Huang Teng
 */
symbolTranNodeName = "assembleComponentList";

// 添加表格行
function addRow(c) {
	// alert(c);
	var addTabTbody = document.getElementById("addTable").getElementsByTagName("tbody")[0];// 获得表格
	// backup cell = addTab.cells.length; //table中所有的单元格数
	// backup n = addTab.rows.length;//table 中行数
	// backup cell = cell / n; //table 中的列数
	// 所加行位置	
	if (c == null) {
		n = addTabTbody.rows.length;//table 中行数
	} else {
		var n = c.parentNode.parentNode.rowIndex;//当前行位置，相对于整个table
		//n++;// 在下一行添加,n++是相对于整个table的index时使用。如除去标题行,当前的n即是tbody的行数,n--既是相对于tbody的index，n即是下一行相对于tbody的index
	}
	r = addTabTbody.insertRow(n);// 向table中加入行
	// 添加当前行的每个单元格
	r.insertCell(0).innerHTML = '<button type="button" class="button blue" onclick="delRow(this)" style="width:20px;height:20px;" value="-">-</button>';
	r.insertCell(1).innerHTML = '<button type="button" class="button blue" onclick="addRow(this)" style="width:20px;height:20px;" value="+">+</button>';
	r.insertCell(2).innerHTML = '<input type=\'text\' onblur="terify4Single(this)" title="name" style=\"width:100px;\" value=\"... ...\"/><span class="veritifyMessage" style="display:none; color:#F00;font-size:16px;width:10px;" />';
	r.insertCell(3).innerHTML = '<input type=\'text\' onblur="terify4Single(this)" title="type" style=\"width:100px;\" value=\"ignore\"/><span class="veritifyMessage" style="display:none; color:#F00;font-size:16px;width:10px;" />';
	r.insertCell(4).innerHTML = '<input type=\'text\' onblur="terify4Single(this)" title="direction" style=\"width:100px;\" value=\"0\"/><span class="veritifyMessage" style="display:none; color:#F00;font-size:16px;width:10px;" />';
	r.insertCell(5).innerHTML = '<input type=\'text\' onblur="terify4Single(this)" title="sequence" style=\"width:100px;\" value=\"... ...\"/><span class="veritifyMessage" style="display:none; color:#F00;font-size:16px;width:10px;" />';
	r.insertCell(6).innerHTML = '<input type=\'checkbox\' onblur="terify4Single(this)" title="target gene" style=\"width:20px;\" /><span class="veritifyMessage" style="display:none; color:#F00;font-size:16px;width:10px;" />';
	
	return r;
}

function addRow5Data(c) {
	//console.log(c);
	var dataTab = $("#componentDataTable");// 获得数据表格
	//index
	var nameIndex=0;var parts_typeIndex=0;var directionIndex=0;
	$.each(dataTab.find("th"), function(index,thNode){//遍历th
		if ($(thNode).text() == "name")
			nameIndex=index;
		if ($(thNode).text() == "parts_type")
			parts_typeIndex=index;
		//backup
		//if ($(thNode).text() == "direction")
		//	directionIndex=index;
		if ($(thNode).text() == "sequence")
			sequenceIndex=index;
	});
	//data
	var tr=$(c).parent().parent();//当前行
	//backup不确定是否唯一 var tr=$(c).parents("tr");//当前行
	
	//backup var rowIndex=tr.index();//当前行位置
	//backup var rowIndex=$(c).parent().parent().index();//当前行位置
	//backup var colIndex=$(c).index();//当前列位置
	var name="";var parts_type="";var direction="+";var sequence="";
	$.each(tr.children("td"), function(index,tdNode){//遍历tr
		if (index==nameIndex)
			name=$(tdNode).attr("content");
		if (index==parts_typeIndex)
			parts_type=$(tdNode).text();
		//backup
		//if (index==directionIndex)
		//	direction=tdNode.text();
		if (index==sequenceIndex)
			sequence=$(tdNode).attr("content");
	});
	//添加数据
	r=addRow();
	r5Data=$(r);
	$.each(r5Data.children("td"), function(index,tdNode){//遍历th
		var input=$(tdNode).children();
		if(index==2)
			input.val(name);
		if (index==3)
			input.val(parts_type);
		if (index==4)
			input.val(direction);
		if(index==5)
			input.val(sequence);
	});
	//检查及画图
	terify2add();
	
	return r;
}

// 删除当前行
function delRow(c) {
	// alert(el.id);
	var n = c.parentNode.parentNode.rowIndex;// 当前行数
	var addTab = document.getElementById("addTable");// 获取table
	addTab.deleteRow(n);
	//检查及画图
	terify2add();
}

// 验证信息输入是否合法
function terifyNoNull(objText) {
	// alert(objText.value);
	// 信息不能为空
	with (objText) {
		if (value == null || value == "") {
			objText.parentNode.children[1].style.display = "block";
			objText.parentNode.children[1].innerHTML = "*required";
			return false;
		} else {
			objText.parentNode.children[1].style.display = "none";
			return true;
		}
	}
}
function terifyNum(objText) {
	// 信息必须为数字
	with (objText) {
		if (isNaN(value)) {
			objText.parentNode.children[1].style.display = "block";
			objText.parentNode.children[1].innerHTML = "*only number";
			return false;
		} else {
			objText.parentNode.children[1].style.display = "none";
			return true;
		}
	}
}
function terifyArrow(objText) {
	// 信息必须为 箭头
	with (objText) {
		if (value != "-->") {
			objText.parentNode.children[1].style.display = "block";
			objText.parentNode.children[1].innerHTML = "*only -->";
			return false;
		} else {
			objText.parentNode.children[1].style.display = "none";
			return true;
		}
	}
}
function terifyNoNull5Num(objText) {
	// 信息不能为空
	if (terifyNoNull(objText)) {
		if (terifyNum(objText)) {
			return true;
		}
	}
	return false;
}
function terifyNoNull5Arrow(objText) {
	// 信息不能为空
	if (terifyNoNull(objText)) {
		if (terifyArrow(objText)) {
			return true;
		}
	}
	return false;
}

// 清空node
function removeChildren(node) {
	while (node.hasChildNodes()) // 当node下还存在子节点时 循环继续
	{
		node.removeChild(node.firstChild);
	}
}

//检查单个数据
function terify4Single(objText) {
	document.getElementById("addForm").style.display = "none";
	terifyNoNull(objText)
}
// 检查并生成DataTable对象
function terify2add() {
	// 判断数据是否可以写入标志，false为可以写入，true为不可以写入
	var flag = false;
	// 获取table
	var addTab = document.getElementById("addTable");
	var memberList = new Array();
	var componentList = new Array();
	// 循环行
	var isContinue = true;
	for (var i = 1; i < addTab.rows.length; i++) {
		// 第0行为标题行，所以i=1，跳过第一行
		var cells = addTab.rows[i].cells;
		for (var j = 2; j < cells.length; j++) {
			// 第0,1列为按钮，所以i=2，跳过第0,1列
			var valueNode = cells[j].childNodes[0];
			// format check
			if (!(terifyNoNull(valueNode))) {
				//bakcup document.getElementById("addForm").style.display = "none";
				isContinue = false;
			}
		}
		// add reactioin
		// var reaction=valueNode.value+"\t"+reactantsNode.value+"
		// "+arrowNode.value+"
		// "+productsNode.value+"\t"+lowerBoundNode.value+"\t"+upperBoundNode.value+"\t"+objectNode.value;
		memberList.push(cells[2].childNodes[0].value);// name
		
		componentList.push({
			"name" : cells[2].childNodes[0].value.trim(),
			"eleType" : cells[3].childNodes[0].value.trim(),
			"direction" : cells[4].childNodes[0].value.trim(),
			"sequence" : cells[5].childNodes[0].value.replace(/[\s]/g, "").toUpperCase(),
			"isTarget" : cells[6].childNodes[0].checked,
		});
	}
	if (!isContinue) {
		document.getElementById("addForm").style.display = "none";
		return;
	}
	// show
	// backup show8word("show8Word",memberList);
	show8Pic(componentList, "show8Pic");

	// hidden input for submit
	submit8Input(JSON.stringify(componentList), "addForm");
	// console.log(typeof componentList);
	// console.log(typeof JSON.stringify(componentList));
}
// input for submit
function submit8Input(valueString, submitFormId) {
	// submitFormNode->symbolTranNode
	var symbolTranNode = document.createElement("input");
	symbolTranNode.type = "hidden";// hidden
	symbolTranNode.name = symbolTranNodeName;
	symbolTranNode.value = valueString;
	var submitFormNode = document.getElementById(submitFormId);
	submitFormNode.appendChild(symbolTranNode);
	submitFormNode.style.display = "block";
}

// show by word
function show8word(memberList, showNodeId) {
	// showNode->pNode->textNode->待展示的内容
	// showNode
	var showNode = document.getElementById(showNodeId);
	removeChildren(showNode);// 清空showNode
	// 待展示的内容
	var symbolShow = "";
	for (j = 0; j < memberList.length; j++) {
		symbolShow = symbolShow + memberList[j] + "\t";
	}
	// textNode
	var textNode = document.createTextNode(symbolShow);
	// pNode
	var pNode = document.createElement("p");
	pNode.appendChild(textNode);
	// showNode
	showNode.appendChild(pNode);
}
// show by pic
var legendButtonList = [ {
	"text" : "ignore",
	"eleType" : "ignore",
	"direction" : null
}, {
	"text" : "promoter",
	"eleType" : "promoter",
	"direction" : "right"
}, {
	"text" : "terminator",
	"eleType" : "terminator",
	"direction" : "right"
}, {
	"text" : "replication origin",
	"eleType" : "replication origin",
	"direction" : "right"
}, {
	"text" : "selection marker",
	"eleType" : "selection marker",
	"direction" : "right"
} ];
var eleType_colorDic = {
	"ignore" : "#FFFFFF",
	"promoter" : "#00FF00",
	//"promoter function module" : "#009900",
	"terminator" : "#FF6600",
	//"terminator function module" : "#FF0000",
	"replication origin" : "#00FFFF",
	//"replication origin function module" : "#0099FF",
	"selection marker" : "#CC66FF",
	//"selection marker function module" : "#CC00FF"
};
var directionDic = {
	"+" : "right",
	"-" : "left",
	"0" : null
}
function constructShowButtonNode(text, eleType, direction) {
	// console.log(text);
	// var colorDic={"Dark
	// Blue":"primary","Yellow":"warning","Green":"success","Light
	// Blue":"info","White":"default","Red":"danger"}
	var showButtonNode = document.createElement("button");// button
	// type
	showButtonNode.setAttribute("type", "button");
	// text
	showButtonNode.appendChild(document.createTextNode(text));
	// class
	var classString = "btn btn-sm";
	if (direction != null) {
		classString += " btn-arrow-" + direction;
	}
	showButtonNode.setAttribute("class", classString);
	// style
	showButtonNode.setAttribute("style", "margin:10px 16px;border:solid gray 1px;background-color: "+eleType_colorDic[eleType]+";");
	return showButtonNode;
}

function show8Pic(componentList, showNodeId) {
	// showNode->div->待展示的内容
	// console.log(typeof componentList);
	// showNode
	var showNode = document.getElementById(showNodeId);
	removeChildren(showNode);// 清空showNode
	// legend div
	var legendDivNode = document.createElement("div");
	legendDivNode.appendChild(document.createElement("span").appendChild(
			document.createTextNode("Legend:")));// legend title
	for ( var i in legendButtonList) {
		// legendButton
		legendButton = legendButtonList[i];
		// button
		var legendButtonNode = constructShowButtonNode("... ...",
				legendButton["eleType"], legendButton["direction"]);
		legendButtonNode.setAttribute("style", legendButtonNode
				.getAttribute("style")
				+ "width:50px;border:solid gray 1px;");// 固定长度
		legendDivNode.appendChild(legendButtonNode);
		// text
		legendDivNode.appendChild(document.createElement("span").appendChild(
				document.createTextNode(legendButton["text"] + " ")));
	}
	showNode.appendChild(legendDivNode);
	// content div
	var contentDivNode = document.createElement("div");
	for (var j = 0; j < componentList.length; j++) {
		component = componentList[j];
		contentDivNode.appendChild(constructShowButtonNode(component["name"],
				component["eleType"], directionDic[component["direction"]]));// 待展示的内容
	}
	showNode.appendChild(contentDivNode);
}

// 检查并生成DataTable对象
function CheckReaRow() {
	// 判断数据是否可以写入标志，false为可以写入，true为不可以写入
	var flag = false;
	// 获取table
	var addTab = document.getElementById("addTable");
	var reactionList = new Array();
	// 循环行
	for (i = 1; i < addTab.rows.length; i++) {
		// 第一行为标题行，所以i=1，跳过第一行
		var cells = addTab.rows[i].cells;

		var nameNode = cells[0].childNodes[0];
		var reactantsNode = cells[1].childNodes[0];
		var arrowNode = cells[2].childNodes[0];
		var productsNode = cells[3].childNodes[0];
		var lowerBoundNode = cells[4].childNodes[0];
		var upperBoundNode = cells[5].childNodes[0];
		var objectNode = cells[6].childNodes[0];
		// format check
		var isContinue = true;
		if (!(terifyNoNull(nameNode) && terifyNoNull5Arrow(arrowNode)
				&& terifyNoNull5Num(lowerBoundNode)
				&& terifyNoNull5Num(upperBoundNode) && terifyNoNull5Num(objectNode))) {
			document.getElementById("addForm").style.display = "none";
			isContinue = false;
		} else {
			if (lowerBoundNode.value > upperBoundNode.value) {
				document.getElementById("addForm").style.display = "none";
				lowerBoundNode.parentNode.children[1].style.display = "block";
				lowerBoundNode.parentNode.children[1].innerHTML = "*bigger?";
				upperBoundNode.parentNode.children[1].style.display = "block";
				upperBoundNode.parentNode.children[1].innerHTML = "*smaller?";
				isContinue = false;
			} else {
				lowerBoundNode.parentNode.children[1].style.display = "none";
				upperBoundNode.parentNode.children[1].style.display = "none";
			}
			if (!(objectNode.value == 0.0 || objectNode.value == 1.0)) {
				document.getElementById("addForm").style.display = "none";
				objectNode.parentNode.children[1].style.display = "block";
				objectNode.parentNode.children[1].innerHTML = "*0.0 or 1.0";
				isContinue = false;
			} else {
				objectNode.parentNode.children[1].style.display = "none";
			}
		}
		if (!(terifyNoNull(reactantsNode) || terifyNoNull(productsNode))) {
			document.getElementById("addForm").style.display = "none";
			reactantsNode.parentNode.children[1].style.display = "block";
			reactantsNode.parentNode.children[1].innerHTML = "*both null?";
			productsNode.parentNode.children[1].style.display = "block";
			productsNode.parentNode.children[1].innerHTML = "*both null?";
			isContinue = false;
		} else {
			reactantsNode.parentNode.children[1].style.display = "none";
			productsNode.parentNode.children[1].style.display = "none";
		}
		if (!isContinue) {
			return;
		}
		// add reactioin
		// var reaction=nameNode.value+"\t"+reactantsNode.value+"
		// "+arrowNode.value+"
		// "+productsNode.value+"\t"+lowerBoundNode.value+"\t"+upperBoundNode.value+"\t"+objectNode.value;
		var memberList = new Array();
		memberList.push(nameNode.value);
		memberList.push(reactantsNode.value);
		memberList.push(arrowNode.value);
		memberList.push(productsNode.value);
		memberList.push(lowerBoundNode.value);
		memberList.push(upperBoundNode.value);
		memberList.push(objectNode.value);
		reactionList.push(memberList);
	}
	// addReaShowNode
	var addReaShowNode = document.getElementById("addReaShow");
	while (addReaShowNode.hasChildNodes()) // 当div下还存在子节点时 循环继续
	{
		addReaShowNode.removeChild(addReaShowNode.firstChild);
	}
	// addReaShowTable
	var addReaShowTabNode = document.createElement("table");
	addReaShowTabNode.id = "addReaShowTable";
	addReaShowTabNode.className = "gridtable";
	// thead
	var thead4showTabNode = document.createElement("thead");
	thead4showTabNode.innerHTML = "<tr><th>reaction name</th><th>reactants</th><th>--></th><th>products</th><th>lower bound</th><th>upper bound</th><th>object</th></tr>";
	addReaShowTabNode.appendChild(thead4showTabNode);
	// tbody
	var tbody4showTabNode = document.createElement("tbody");
	for (i = 0; i < reactionList.length; i++) {
		var memberList = reactionList[i];
		var tr4showTabNode = document.createElement("tr");
		// var reaction="\t";
		for (j = 0; j < memberList.length; j++) {
			var td4showTabNode = document.createElement("td");
			var memberNode = document.createTextNode(memberList[j]);
			// reaction=reaction+(memberList[j]+"\t");
			td4showTabNode.appendChild(memberNode);
			tr4showTabNode.appendChild(td4showTabNode);
		}
		// var pNode=document.createElement("p");
		// var showRowNode=document.createTextNode(reaction);
		// pNode.appendChild(showRowNode);
		// addReaShowNode.appendChild(pNode);
		tbody4showTabNode.appendChild(tr4showTabNode);
	}
	addReaShowTabNode.appendChild(tbody4showTabNode);
	addReaShowNode.appendChild(addReaShowTabNode);

	document.getElementById("addForm").style.display = "block";
}

//backup
function delBlank(str){
	return str.replace(/[\s]/g, "")
//	str = str.replace(/<\/?[^>]*>/g,''); //去除HTML tag
//	str = str.replace(/[ | ]*\n/g,'\n'); //去除行尾空白
//	str = str.replace(/\n[\s| | ]*\r/g,'\n'); //去除多余空行
//	str=str.replace(/ /ig,'');//去掉 
//	str=str.replace(/^[\s　]+|[\s　]+$/g, "");//去掉全角半角空格
//	str=str.replace(/[\r\n]/g,"");//去掉回车换行
}