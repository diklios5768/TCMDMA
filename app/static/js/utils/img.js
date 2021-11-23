/*
@Date: 2021-11-23 11:12:05
@LastEditTime: 2021-11-23 11:12:13
@LastEditors: diklios
@FilePath: \js\utils\img.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/


//压缩base64方法
function dealImage(base64, w, callback) {
    var newImage = new Image();
    var quality = 0.6; //压缩系数0-1之间
    newImage.src = base64;
    newImage.setAttribute("crossOrigin", 'Anonymous'); //url为外域时需要
    var imgWidth, imgHeight;
    newImage.onload = function () {
        imgWidth = this.width;
        imgHeight = this.height;
        var canvas = document.createElement("canvas");
        var ctx = canvas.getContext("2d");
        if (Math.max(imgWidth, imgHeight) > w) {
            if (imgWidth > imgHeight) {
                canvas.width = w;
                canvas.height = w * imgHeight / imgWidth;
            } else {
                canvas.height = w;
                canvas.width = w * imgWidth / imgHeight;
            }
        } else {
            canvas.width = imgWidth;
            canvas.height = imgHeight;
            quality = 0.6;
        }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
        var base64 = canvas.toDataURL("image/jpeg", quality); //压缩语句
        callback(base64); //必须通过回调函数返回，否则无法及时拿到该值
    }
}