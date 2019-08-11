$(document).ready(function() {
    Date.prototype.Format = function (fmt) {
      var o = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "H+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
      };
      if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
      for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
      return fmt;
    }

    var myDate = new Date().Format("yyyy/MM/dd");
    var myDateTime = new Date().Format("yyyy/MM/dd HH:mm:ss");
    var myTime = new Date().Format("HH:mm:ss");

    $("input.date-auto").focus(function(){
        if($(this).val()==''){
            $(this).val(myDate);
        }
    });

    $("input.datetime-auto").focus(function(){
        if($(this).val()==''){
            $(this).val(myDateTime);
        }
    });

    $("input.time-auto").focus(function(){
        if($(this).val()==''){
            $(this).val(myTime);
        }
    });
});