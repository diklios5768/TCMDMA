/*
@Date: 2021-11-23 10:53:05
@LastEditTime: 2021-11-23 11:06:44
@LastEditors: diklios
@FilePath: \js\utils\str.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/

// 去除html标签
export const removeHtmlTag = (str) => {
  return str.replace(/<[^>]+>/g, "");
};

// 获取url参数
export const getQueryString = (name) => {
  const reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
  const search = window.location.search.split("?")[1] || "";
  const r = search.match(reg) || [];
  return r[2];
};

// 获取url查询字符串所有参数
const getQueryArgs = () => {
  let qs = location.search.length > 0 ? location.search.substr(1) : "",
    //保存每一项
    args = {},
    //得到每一项
    items = qs.length ? qs.split("&") : [],
    item = null,
    name = null,
    value = null,
    len = items.length;

  for (let i = 0; i < len; i++) {
    item = items[i].split("=");
    name = decodeURIComponent(item[0]);
    value = decodeURIComponent(item[1]);
    if (name.length) {
      args[name] = value;
    }
  }
  return args;
};

// 追加url参数
export const appendQuery = (url, key, value) => {
  var options = key;
  if (typeof options == "string") {
    options = {};
    options[key] = value;
  }
  options = $.param(options);
  if (url.includes("?")) {
    url += "&" + options;
  } else {
    url += "?" + options;
  }
  return url;
};

// 去除空格,type: 1-所有空格 2-前后空格 3-前空格 4-后空格
export const trim = (str, type) => {
  type = type || 1;
  switch (type) {
    case 1:
      return str.replace(/\s+/g, "");
    case 2:
      return str.replace(/(^\s*)|(\s*$)/g, "");
    case 3:
      return str.replace(/(^\s*)/g, "");
    case 4:
      return str.replace(/(\s*$)/g, "");
    default:
      return str;
  }
};

// 字符转换，type: 1:首字母大写 2：首字母小写 3：大小写转换 4：全部大写 5：全部小写
export const changeCase = (str, type) => {
  type = type || 4;
  switch (type) {
    case 1:
      return str.replace(/\b\w+\b/g, function (word) {
        return (
          word.substring(0, 1).toUpperCase() + word.substring(1).toLowerCase()
        );
      });
    case 2:
      return str.replace(/\b\w+\b/g, function (word) {
        return (
          word.substring(0, 1).toLowerCase() + word.substring(1).toUpperCase()
        );
      });
    case 3:
      return str
        .split("")
        .map(function (word) {
          if (/[a-z]/.test(word)) {
            return word.toUpperCase();
          } else {
            return word.toLowerCase();
          }
        })
        .join("");
    case 4:
      return str.toUpperCase();
    case 5:
      return str.toLowerCase();
    default:
      return str;
  }
};

// 检测密码强度
export const checkPwd = (str) => {
  var Lv = 0;
  if (str.length < 6) {
    return Lv;
  }
  if (/[0-9]/.test(str)) {
    Lv++;
  }
  if (/[a-z]/.test(str)) {
    Lv++;
  }
  if (/[A-Z]/.test(str)) {
    Lv++;
  }
  if (/[\.|-|_]/.test(str)) {
    Lv++;
  }
  return Lv;
};

// 在字符串中插入新字符串
export const insertStr = (source, index, newStr) => {
  var str = source.slice(0, index) + newStr + source.slice(index);
  return str;
};
