// JavaScript Document

window.onload = function () {
	'use strict';
	// 定义单选框
	var radioDay = document.querySelector('.radioDay');
	var input_date = document.querySelector('.input_date');
	
	// 隐藏日期输入框
	$(".recentDate").click(function(){
		input_date.style.display = 'none';
	});

	// 显示日期类型
	$(".radioPartner").click(function(){//获取radio对象
		radioDay.style.display = 'block';
	});
	
	// 显示日期输入框
	$(".diyDate").click(function(){
		input_date.style.display = 'block';
	});
	
	// 模态框
	var width = $(window).width();
	var height = $(window).height();
	$(function(){
		
		$(".window").css({
			left: (width - $(".window").width()) / 2 + 'px',
			top: '150px'
		});
	});
	
	//弹窗后点击确定模态框消失
	$('#confirm').click(function(){
		$(".modal-sel").hide();
		$(".window").hide();
	});
	
	//弹窗后点击取消模态框消失
	$('#cancel').click(function(){
		$(".modal-sel").hide();
		$(".window").hide();
	});
	
	
	

	// 提交
	$('.button').click(function(){
		// 合作商
		var partner_name = '';
		// 日期类型
		var dateType = '';
		// 日期时间
		var dateTime = '';
		// 输入的cookie值
		var cookie = $('#cookie_text').val();
//		console.log(cookie);
		
		// 判断所选的合作商
		if($('#tmallP').is(':checked')){
			
			partner_name = $('#tmallP').val();
			
		} else if($('#sanyoP').is(':checked')){
			
			partner_name = $('#sanyoP').val();
			
		} else if($('#mideaP').is(':checked')){
			
			partner_name = $('#mideaP').val();
		}
		
		
		// 判断日期类型是否选中
		if($('.recentDate').is(':checked')){

			dateType = $('.recentDate').val();
			
		} else if($('.diyDate').is(':checked')){

			dateType = $('.diyDate').val();
			dateTime = $('#date_time').val();
		}
		
		// post数据
		var data_json = {
			"partner_name": partner_name,
			"dateType": dateType,
			"dateTime": dateTime,
			"cookie": cookie,
		};
		
		
		$.ajax({
			url: '/api/v1_0/spiders', //请求后台地址
			type: 'post', //请求方式
			dataType: 'json', //后台返回数据格式json
			contentType: 'application/json; charset=UTF-8',
			data: JSON.stringify(data_json),
			
			success: function (info) {
			  if (info.status == 0) {
				  	location.href = '/' + info.msg + '.html';
			  } else if (info.status == 4003) {
			        location.href = '/down_file.html';
              } else {
				  	// 错误信息，弹出模态框
					$('.content').html(info.msg);
					$(".modal-sel").show();
					$(".window").show();	  
			  }
			}
			
		});
		
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
};
