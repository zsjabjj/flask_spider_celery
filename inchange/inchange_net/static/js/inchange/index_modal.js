// JavaScript Document
//模态框弹出的位置
	var width = $(window).width();
	var height = $(window).height();
	$(function(){
		'use strict';
		$(".window").css({
			left: (width - $(".window").width()) / 2 + 'px',
			top: '150px'
		});
	});
	
	//点击显示模态框弹窗
	$(document).on('click','#button',function(){
		'use strict';
		$(".modal-sel").show();
		$(".window").show();
	});
	
	//弹窗后点击确认后ajax传值
	$(document).on('click','#confirm',function(){
		'use strict';
		$(".modal-sel").hide();
		$(".window").hide();
	});
	
	//弹窗后点击取消模态框消失
	$(document).on('click','#cancel',function(){
		'use strict';
		$(".modal-sel").hide();
		$(".window").hide();
	});