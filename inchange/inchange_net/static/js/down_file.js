// JavaScript Document
$(document).ready(function(){
 
	"use strict";
	var partner = $('#part').html();
	console.log(partner);
	if('猫超' === partner){
		$('.tmall').show();
	} else if('三洋' === partner){
		$('.sanyo').show();
	} else if('美的' === partner){
		$('.midea').show();
	}
	// 页面加载获取文件列表
	$.ajax({
		url: '/index/getFiles', //请求后台地址
		type: 'get', //请求方式
		dataType: 'json', //后台返回数据格式json
		success: function (info) {
			// 数据分析处理
			parseData(info.fileList);
		}

	});
	
	//配置
	var config = {
		vx: 4, //小球x轴速度,正为右，负为左
		vy: 4, //小球y轴速度
		height: 2, //小球高宽，其实为正方形，所以不宜太大
		width: 2,
		count: 200, //点个数
		color: "121, 162, 185", //点颜色
		stroke: "130,255,255", //线条颜色
		dist: 6000, //点吸附距离
		e_dist: 20000, //鼠标吸附加速距离
		max_conn: 10 //点到点最大连接数
	};

	//调用
	CanvasParticle(config);
	
});
