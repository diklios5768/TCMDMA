/*
@Date: 2021-11-23 11:04:05
@LastEditTime: 2021-11-23 11:04:29
@LastEditors: diklios
@FilePath: \js\utils\func.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/

// 函数节流器
export const debounce = (fn, time, interval = 200) => {
    if (time - (window.debounceTimestamp || 0) > interval) {
        fn && fn();
        window.debounceTimestamp = time;
    }
}