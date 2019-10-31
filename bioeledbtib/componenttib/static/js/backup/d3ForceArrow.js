function forceArrow(dataSet,svgParentId){
	var width = 660;
	var height = 450;
	var svg = d3.select("#"+svgParentId).append("svg:svg")
				.attr("id", ("svg-"+svgParentId))
				.attr("width", width)
				.attr("height", height);
	//var padding={left:30,right:30,top:20,bottom:20};

	//dataSet
	if(dataSet==""){
		return;
		//alert("空串");
	}
	var nodes = {};
	var typeKindString=new Array();
	dataSet.forEach(function(link) {
		typeKindString.push(link.type);
		link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
		link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
	});

	//layout
	var force = d3.layout.force()
		.nodes(d3.values(nodes))
		.links(dataSet)
		.size([width, height])
		.linkDistance(60)
		.charge(-300)
		//.on("tick", tick)
		.start();

	svg.append("svg:defs").attr("id","marker_Defs-"+svgParentId)
		.selectAll("marker")
		.data(typeKindString.unique())
		.enter().append("svg:marker")
		.attr("id", String)
		.attr("viewBox", "0 -5 10 10")
		.attr("refX", 15)
		.attr("refY", -1.5)
		.attr("markerWidth", 6)
		.attr("markerHeight", 6)
		.attr("orient", "auto")
		.append("svg:path")
		.attr("d", "M0,-5L10,0L0,5");

	var path = svg.append("svg:g").selectAll("path")
		.data(force.links())
		.enter().append("svg:path")
		.attr("class", function(d) { return "link " + d.type; })
		.attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

	/*var circle_GaussianBlur=svg.append("svg:defs").append("svg:filter").attr("id","circle_GaussianBlur")
		.append("svg:feGaussianBlur")
		.attr("in","SourceGraphic")
		.attr("stdDeviation",2);*/
	var radial_Defs=svg.append("svg:defs").attr("id","radial_Defs-"+svgParentId)
	var circle_radialGradient1 = radial_Defs.append("radialGradient")
		.attr("id",("circle_radialGradient1-"+svgParentId))
		.attr("cx","50%")
		.attr("cy","50%")
		.attr("r","30%")
		.attr("fx","50%")
		.attr("fy","50%");
	circle_radialGradient1.append("stop")
		.attr("offset","0%")
		.style("stop-color","rgb(255,255,255)");
	circle_radialGradient1.append("stop")
		.attr("offset","100%")
		.style("stop-color","Green");
	var circle_radialGradient2 = radial_Defs.append("radialGradient")
		.attr("id",("circle_radialGradient2-"+svgParentId))
		.attr("cx","50%")
		.attr("cy","50%")
		.attr("r","30%")
		.attr("fx","50%")
		.attr("fy","50%");
	circle_radialGradient2.append("stop")
		.attr("offset","0%")
		.style("stop-color","rgb(255,255,255)");
	circle_radialGradient2.append("stop")
		.attr("offset","100%")
		.style("stop-color","LimeGreen");
	var circle = svg.append("svg:g").selectAll("circle")
		.data(force.nodes())
		.enter().append("svg:circle")
		.attr("r", 10)
		.style("fill","url(#"+circle_radialGradient1.attr("id")+")")
		.call(force.drag);
	circle.on("mousedown",function(d,i){
			d3.select(this)
		        .transition()
		        .duration(50)
		    	.style("fill","url(#"+circle_radialGradient2.attr("id")+")");
		})
		.on("dblclick",function(d,i){
			if(d.name.indexOf("b")==0){
				//基因Id
				window.open("http://www.ibiodesign.net/ecoin/search/gene?geneEcoId="+d.name);
			}else{
				//代谢物
				window.open("http://www.ibiodesign.net/ecoin/search/metabolite?metaName="+d.name);
			}
			//window.location.href = "http://www.ourd3js.com/";
		})
		.on("mouseup",function(d,i){
		    d3.select(this)
		        .transition()
		        .duration(50)
		    	.style("fill","url(#"+circle_radialGradient1.attr("id")+")");
		})

	var text = svg.append("svg:g").selectAll("text")
		.data(force.nodes())
		.enter().append("svg:text")
	    .attr("dx", 15)
	    .attr("dy", 5)
	    .text(function(d){
	       return d.name;
	    });
	text.attr("fill","rgb(72,72,72)")
		.on("mouseover",function(d,i){
			//console.log(d3.event);
		    d3.select(this)
		        .attr("fill","rgb(0,0,0)");
		})
		.on("click",function(d,i){
			//console.log(d);
			//console.log(d.name);
			//console.log(d.name.indexOf("b"));
			if(d.name.indexOf("b")==0){
				//基因Id
				window.open("http://www.ibiodesign.net/ecoin/search/interaction?substanceSymbol="+d.name+"&substanceType=gene");
			}else{
				//代谢物
				window.open("http://www.ibiodesign.net/ecoin/search/interaction?substanceSymbol="+d.name+"&substanceType=meta");
			}
			//window.location.href = "http://www.ourd3js.com/";
		})
		.on("mouseout",function(d,i){
		    d3.select(this)
		        .transition()
		        .duration(500)
		        .attr("fill","rgb(72,72,72)");
		})

	force.on("tick", function(){
		//Msource.x,source.yArr00,1target.x,target.y
		path.attr("d", function(d) {
		var dx = d.target.x - d.source.x,
		    dy = d.target.y - d.source.y,
		    dr = Math.sqrt(dx * dx + dy * dy);
		return "M" + d.source.x + "," 
		+ d.source.y + "A" + dr + "," 
		+ dr + " 0 0,1 " + d.target.x + "," 
		+ d.target.y;
		});
		circle.attr("cx",function(d){ return d.x; })
			.attr("cy",function(d){ return d.y; });
		text.attr("transform", function(d) {
		    return "translate(" + d.x + "," + d.y + ")";
		 });
	});
}


Array.prototype.unique = function(){
	//数组去重
	var n = {},r=[]; //n为hash表，r为临时数组
	for(var i = 0; i < this.length; i++) //遍历当前数组
	{
		if (!n[this[i]]) //如果hash表中没有当前项
		{
			n[this[i]] = true; //存入hash表
			r.push(this[i]); //把当前数组的当前项push到临时数组里面
		}
	}
	return r;
}
