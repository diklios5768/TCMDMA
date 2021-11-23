/*
@Date: 2021-11-23 10:56:29
@LastEditTime: 2021-11-23 10:56:34
@LastEditors: diklios
@FilePath: \js\utils\other.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
 */


// 动态引入js
export const injectScript = (src) => {
    const s = document.createElement("script");
    s.type = "text/JavaScript";
    s.async = true;
    s.src = src;
    const t = document.getElementsByTagName("script")[0];
    t.parentNode.insertBefore(s, t);
};