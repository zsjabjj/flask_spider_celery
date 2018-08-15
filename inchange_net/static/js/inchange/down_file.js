// JavaScript Document


$(document).ready(function () {

    "use strict";
    // var partner = $('#part').html();
    // console.log(partner);
    // if('猫超' === partner){
    // 	$('.tmall').show();
    // } else if('三洋' === partner){
    // 	$('.sanyo').show();
    // } else if('美的' === partner){
    // 	$('.midea').show();
    // }
    // 页面加载获取文件列表
    $.ajax({
        url: '/api/v1_0/getFiles', //请求后台地址
        type: 'post', //请求方式
        dataType: 'json', //后台返回数据格式json
        success: function (info) {
            if ('猫超' === info.part) {
                // console.log(info.part);
                $('.tmall').show();
            } else if ('三洋' === info.part) {
                // console.log(info.part);
                $('.sanyo').show();
            } else if ('美的' === info.part) {
                // console.log(info.part);
                $('.midea').show();
            }
            // console.log('get start');
            // console.log(info.fileList);
            // 数据分析处理
            parseData(info.fileList, info.part);
            // console.log('get end');
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

function parseData(Datas, part) {
    'use strict';
    var dir_path = Datas.dir_path + '/datas/Data/';
//	获得合作商
    for (var p in Datas.Data) {
        if (Datas.Data) {
            //	ps为各个合作商名
            var ps = Datas.Data[p];
            // console.log(ps);
            //	获得年目录
            for (var y in Datas[ps]) {
                if (Datas[ps]) {
                    //	ys为各个年目录名
                    var ys = Datas[ps][y];
                    // console.log(ys);
                    addYears(Datas, ps, y);
                    //	获得月目录
                    for (var m in Datas[ys]) {
                        if (Datas[ys]) {
                            //	ms为各个月目录名
                            var ms = Datas[ys][m];
                            // console.log(ms);
                            addMonths(Datas, ys, m);
                            //	获得日目录
                            for (var d in Datas[ms]) {
                                if (Datas[ms]) {
                                    // console.log(ds);
                                    if ('美的' === part) {
                                        var mideas = Datas[ms][d];
                                        var file_path = dir_path + ps + '/' + ys + '/' + ms + '/' + mideas;
                                        console.log(file_path);
                                        console.log(Datas.dir_path);

                                        addDays(ms, mideas, file_path, part);
                                    } else {
                                        //	ds为各个日目录
                                        var ds = Datas[ms][d];
                                        addDays(Datas, ms, d, part);
                                    }

                                    // 获得文件
                                    for (var f in Datas[ds]) {
                                        if (Datas[ds]) {
                                            // fs各个文件
                                            var fs = Datas[ds][f];
                                            var file_path = dir_path + ps + '/' + ys + '/' + ms + '/' + ds + '/' + fs;
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
function addYears(datas, add_part, add_year) {
    'use strict';

    var $li = $('<li><input type="checkbox" id=' + datas[add_part][add_year] + '><label for=' + datas[add_part][add_year] + '>' + datas[add_part][add_year] + '</label><ul class="pure-tree ' + datas[add_part][add_year] + '"></ul></li>');

    $li.appendTo($('.' + add_part));
}

//添加月目录
function addMonths(datas, add_year, add_month) {
    'use strict';
    var $li = $('<li><input type="checkbox" id=' + datas[add_year][add_month] + '><label for=' + datas[add_year][add_month] + '>' + datas[add_year][add_month] + '</label><ul class="pure-tree ' + datas[add_year][add_month] + '"></ul></li>');

    $li.appendTo($('.' + add_year));
}

//添加日目录
function addDays(datas, add_month, add_day, part) {
    'use strict';
    if ('美的' === part) {
        var $li = $('<li class="pure-tree_link"><a href="/api/v1_0/downloads' + add_day + '" download>' + add_month + '</a></li>');

        $li.appendTo($('.' + datas));
    } else {
        var $li = $('<li><input type="checkbox" id=' + datas[add_month][add_day] + '><label for=' + datas[add_month][add_day] + '>' + datas[add_month][add_day] + '</label><ul class="pure-tree ' + datas[add_month][add_day] + '"></ul></li>');

        $li.appendTo($('.' + add_month));
    }

}

//添加文件
function addFiles(add_day, add_file, add_path) {
    'use strict';

    var $li = $('<li class="pure-tree_link"><a href="/api/v1_0/downloads' + add_path + '" download>' + add_file + '</a></li>');

    $li.appendTo($('.' + add_day));
}
