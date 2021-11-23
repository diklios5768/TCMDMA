/* 
@Date: 2021-11-23 10:38:54
@LastEditTime: 2021-11-23 11:10:52
@LastEditors: diklios
@FilePath: \js\utils\window.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/

// 获取滚动的坐标
export const getScrollPosition = (el = window) => ({
    x: el.pageXOffset !== undefined ? el.pageXOffset : el.scrollLeft,
    y: el.pageYOffset !== undefined ? el.pageYOffset : el.scrollTop,
});

// 滚动到顶部
export const scrollToTop = () => {
    const c = document.documentElement.scrollTop || document.body.scrollTop;
    if (c > 0) {
        window.requestAnimationFrame(scrollToTop);
        window.scrollTo(0, c - c / 8);
    }
};


// el是否在视口范围内
export const elementIsVisibleInViewport = (el, partiallyVisible = false) => {
    const { top, left, bottom, right } = el.getBoundingClientRect();
    const { innerHeight, innerWidth } = window;
    return partiallyVisible
        ? ((top > 0 && top < innerHeight) ||
            (bottom > 0 && bottom < innerHeight)) &&
        ((left > 0 && left < innerWidth) || (right > 0 && right < innerWidth))
        : top >= 0 && left >= 0 && bottom <= innerHeight && right <= innerWidth;
};

// 拦截粘贴板
export const copyTextToClipboard = (value) => {
    var textArea = document.createElement("textarea");
    textArea.style.background = "transparent";
    textArea.value = value;
    document.body.appendChild(textArea);
    textArea.select();
    try {
        var successful = document.execCommand("copy");
    } catch (err) {
        console.log("Oops, unable to copy");
    }
    document.body.removeChild(textArea);
};