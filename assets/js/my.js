$('.open-popup').magnificPopup({
    items: [
      {
        src: 'assets/img/1.jpg',
      },
      {
        src: 'assets/img/2.jpg',
      },
      {
        src: 'assets/img/3.jpg',
      },
      {
        src: 'assets/img/4.jpg',
      },
    ],
    gallery: {
      enabled: true
    },
    type: 'image' // this is a default type
});//@ sourceURL=pen.js</script>

//var cell = document.createElement('div');
//var imgDir = "assets/img/"
//var html = "";
//for (var i = 1; i <= 20; i ++) {
    //var photoPath = imgDir + i + ".jpg";
    //var img = '<a href="#modal" role="button" data-toggle="modal" onclick="replacePhoto(\'' + photoPath + '\')")><img class="candidate-photo" src="' + photoPath + '"/></a>';
    //html += img;
//}
//cell.innerHTML = html;
//$("#candidate-container").append(cell);

function replacePhoto(res) {
    var newCss =  "url('" + res + "')";
    $('#main-photo-container').css('background-image', newCss);
}


//Waterfall effect.
/*  window.onerror = function(){
    location.reload();//如果报错，请它自动刷新。
    }*/
$(function(){
    var random = {};
    random.num = function(min, max){
        return Math.random()*(max-min)+min;
    };
    random.src = function() {
        return "assets/img/" + Math.ceil(Math.random()*20) + ".jpg";
    };
    //容器的CSS表达式，列数，每列的宽度
    var Waterfall = function(expr, col, colWidth){
        //构建整体轮廓
        var container = this.container = $(expr);
        var pw = container.width();//容器的宽
        var gw = (pw - col * colWidth)/(col-1);//列间距离
        this.colWidth = colWidth;
        this.cols = [];
        for(var i = 0; i < col ; i++){//随机生成列
            this.cols[i] = $("<div class='waterfall' />").css({
                position: "absolute",
                top: 0,
                left: (colWidth + gw) * i,
                width: colWidth,
                //backgroundColor: random.hex(),
            }).appendTo(container);
        }
    }
    Waterfall.prototype = {
        //计算出最短的栏栅
        shortestElement:function() {
                            var shortestElement =  this.cols[0];                 
                            for(var i = 1;i < this.cols.length; i++){
                                if(this.cols[i].height() < shortestElement.height()){
                                    shortestElement = this.cols[i];
                                }
                            }
                            return shortestElement;            
                        },
        //添加板块
        addBlocks:function() {
                        for(var i = 0; i < 40; i++){//随机生成40个板砖
                            var src = random.src();
                            var anchor = $("<a href='javascript:;' onclick='replacePhoto(\"" + src + "\")'/>");
                            $("<img class='waterfall_block' src=\"" + src + "\" />").css({
                                margin: 5,
                                width: this.colWidth - 10 ,
                            }).appendTo(anchor);
                            anchor.appendTo( this.shortestElement());
                        }
                    }
    };


    var waterfall = new Waterfall("#candidate-container", 5, 200);
    waterfall.addBlocks();
    $(window).scroll(function(){
        var clientHeight = $(window).height(),
        scrollTop = $(window).scrollTop(),
        scrollHeight = $(document).height();
    if(clientHeight + scrollTop >=  scrollHeight ){
        //waterfall.addBlocks();
        $("<div id='loader'>loading</div>").appendTo(waterfall.shortestElement());
    }
    })
})

