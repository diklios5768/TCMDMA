/*
@Date: 2021-11-23 10:55:30
@LastEditTime: 2021-11-23 10:55:50
@LastEditors: diklios
@FilePath: \js\utils\download.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
 */


// 根据url地址下载
export const download = (url) => {
    var isChrome = navigator.userAgent.toLowerCase().indexOf("chrome") > -1;
    var isSafari = navigator.userAgent.toLowerCase().indexOf("safari") > -1;
    if (isChrome || isSafari) {
        var link = document.createElement("a");
        link.href = url;
        if (link.download !== undefined) {
            var fileName = url.substring(url.lastIndexOf("/") + 1, url.length);
            link.download = fileName;
        }
        if (document.createEvent) {
            var e = document.createEvent("MouseEvents");
            e.initEvent("click", true, true);
            link.dispatchEvent(e);
            return true;
        }
    }
    if (url.indexOf("?") === -1) {
        url += "?download";
    }
    window.open(url, "_self");
    return true;
};