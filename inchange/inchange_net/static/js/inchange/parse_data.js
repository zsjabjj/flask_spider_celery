// JavaScript Document
function parseData(Datas){
	'use strict';

//	获得合作商
	for(var p in Datas.Data){
		if(Datas.Data){	
			//	ps为各个合作商名
			var ps = Datas.Data[p];

			//	获得年目录
			for(var y in Datas[ps]){
				if(Datas[ps]){
					//	ys为各个年目录名
					var ys = Datas[ps][y];

					addYears(Datas, ps, y);
					//	获得月目录
					for(var m in Datas[ys]){
						if(Datas[ys]){
							//	ms为各个月目录名
							var ms = Datas[ys][m];

							addMonths(Datas, ys, m);
							//	获得日目录
							for(var d in Datas[ms]){
								if(Datas[ms]){
									//	ds为各个日目录
									var ds = Datas[ms][d];

									addDays(Datas, ms, d);
									// 获得文件
									for(var f in Datas[ds]){
										if(Datas[ds]){
											// fs各个文件
											var fs = Datas[ds][f];
											var file_path = Datas.dir_path + '/' + ps + '/' + ys + '/' + ms + '/' + ds + '/' + fs;
											addFiles(ds, fs, file_path);
										}  // fs各个文件
									}  // 获得文件
								}  // ds为各个日目录
							}  // 获得日目录
						}  // ms为各个月目录名
					}  // 获得月目录
				}  // ys为各个年目录名			
			}  // 获得年目录
		}  // ps为各个合作商名
		
	}  // 获得合作商
}

//添加年目录
function addYears(datas, add_part, add_year){
	'use strict';
	
	var $li = $('<li><input type="checkbox" id=' + datas[add_part][add_year] + '><label for=' + datas[add_part][add_year] + '>' + datas[add_part][add_year] + '</label><ul class="pure-tree ' + datas[add_part][add_year] + '"></ul></li>');
	
	$li.appendTo($('.' + add_part));
}

//添加月目录
function addMonths(datas, add_year, add_month){
	'use strict';
	var $li = $('<li><input type="checkbox" id=' + datas[add_year][add_month] + '><label for=' + datas[add_year][add_month] + '>' + datas[add_year][add_month] + '</label><ul class="pure-tree ' + datas[add_year][add_month] + '"></ul></li>');
	
	$li.appendTo($('.' + add_year));
}

//添加日目录
function addDays(datas, add_month, add_day){
	'use strict';
	var $li = $('<li><input type="checkbox" id=' + datas[add_month][add_day] + '><label for=' + datas[add_month][add_day] + '>' + datas[add_month][add_day] + '</label><ul class="pure-tree ' + datas[add_month][add_day] + '"></ul></li>');
	
	$li.appendTo($('.' + add_month));
}

//添加文件
function addFiles(add_day, add_file, add_path){
	'use strict';

	var $li = $('<li class="pure-tree_link"><a href="' + add_path + '" download>' + add_file + '</a></li>');
	
	$li.appendTo($('.' + add_day));
}


