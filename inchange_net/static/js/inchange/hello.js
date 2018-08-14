$(document).ready(function () {

    // 获取详情页面要展示的房屋编号
    // var queryData = decodeQuery();
    // var houseId = queryData["id"];

    // 获取该房屋的详细信息
    $.get("/api/v1_0/dailys", function (resp) {
        if (resp.status == 0) {
            if (resp.files) {
                for (var i in resp.files) {
                    var file = resp.files[i];
                    var $li = $("<li><a href='api/v1_0/download/" + file + "'>" + file + "</a>(下载请点文件，<a href='/api/v1_0/delete/" + file + "'>删除请点我</a>)</li>");

                    $li.appendTo($('.swiper-wrapper'));
                }
            }
            // $(".col-xs-6").html(template("file-list-tmpl", {files: resp.files}));

            // // resp.user_id为访问页面用户,resp.data.user_id为房东
            // if (resp.data.user_id != resp.data.house.user_id) {
            //     $(".book-house").attr("href", "/booking.html?hid="+resp.data.house.hid);
            //     $(".book-house").show();
            // }
            //     var mySwiper = new Swiper ('.col-xs-6', {
            //         loop: true,
            //         autoplay: 2000,
            //         autoplayDisableOnInteraction: false,
            //         pagination: '.swiper-pagination',
            //         paginationType: 'fraction'
            //     });
            // }
        }
    })
});