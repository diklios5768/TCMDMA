/* 
@Date: 2021-11-23 10:38:54
@LastEditTime: 2021-11-23 10:38:55
@LastEditors: diklios
@FilePath: \js\utils\math.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/

// el是否包含某个class
export const hasClass = (el, className) => {
    let reg = new RegExp("(^|\\s)" + className + "(\\s|$)");
    return reg.test(el.className);
};

// el添加某个class
export const addClass = (el, className) => {
    if (hasClass(el, className)) {
        return;
    }
    let newClass = el.className.split(" ");
    newClass.push(className);
    el.className = newClass.join(" ");
};

// el去除某个class
export const removeClass = (el, className) => {
    if (!hasClass(el, className)) {
        return;
    }
    let reg = new RegExp("(^|\\s)" + className + "(\\s|$)", "g");
    el.className = el.className.replace(reg, " ");
};