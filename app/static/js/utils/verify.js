/*
@Date: 2021-11-23 10:14:44
@LastEditTime: 2021-11-23 10:56:54
@LastEditors: diklios
@FilePath: \js\utils\verify.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/

// 验证邮箱
export const isEmail = (s) => {
    return /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(
        s
    );
};

// 验证手机电话号码
export const isMobilePhone = (s) => {
    return /^1[0-9]{10}$/.test(s);
};

// 验证电话号码
export const isPhone = (s) => {
    return /^([0-9]{3,4}-)?[0-9]{7,8}$/.test(s);
};

// 验证URL地址
export const isURL = (s) => {
    return /^http[s]?:\/\/.*/.test(s);
};

// 是否是字符串
export const isString = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "String";
};

// 是否是数字
export const isNumber = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Number";
};

// 是否是boolean
export const isBoolean = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Boolean";
};

// 是否是函数

export const isFunction = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Function";
};
// 是否为null
export const isNull = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Null";
};

// 是否是undefined
export const isUndefined = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Undefined";
};

// 是否是对象
export const isObj = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Object";
};

// 是否是数组
export const isArray = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Array";
};

// 是否是时间类型
export const isDate = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Date";
};

// 是否正则
export const isRegExp = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "RegExp";
};

// 是否是错误对象
export const isError = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Error";
};

// 是否是Symbol函数
export const isSymbol = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Symbol";
};

// 是否是Promise对象
export const isPromise = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Promise";
};

// 是否是Set对象
export const isSet = (o) => {
    return Object.prototype.toString.call(o).slice(8, -1) === "Set";
};

// 判断类型集合
export const checkStr = (str, type) => {
    switch (type) {
        case "phone": //手机号码
            return /^1[3|4|5|6|7|8|9][0-9]{9}$/.test(str);
        case "tel": //座机
            return /^(0\d{2,3}-\d{7,8})(-\d{1,4})?$/.test(str);
        case "card": //身份证
            return /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(str);
        case "pwd": //密码以字母开头，长度在6~18之间，只能包含字母、数字和下划线
            return /^[a-zA-Z]\w{5,17}$/.test(str);
        case "postal": //邮政编码
            return /[1-9]\d{5}(?!\d)/.test(str);
        case "QQ": //QQ号
            return /^[1-9][0-9]{4,9}$/.test(str);
        case "email": //邮箱
            return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(str);
        case "money": //金额(小数点2位)
            return /^\d*(?:\.\d{0,2})?$/.test(str);
        case "URL": //网址
            return /(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/.test(
                str
            );
        case "IP": //IP
            return /((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))/.test(
                str
            );
        case "date": //日期时间
            return (
                /^(\d{4})\-(\d{2})\-(\d{2}) (\d{2})(?:\:\d{2}|:(\d{2}):(\d{2}))$/.test(
                    str
                ) || /^(\d{4})\-(\d{2})\-(\d{2})$/.test(str)
            );
        case "number": //数字
            return /^[0-9]$/.test(str);
        case "english": //英文
            return /^[a-zA-Z]+$/.test(str);
        case "chinese": //中文
            return /^[\\u4E00-\\u9FA5]+$/.test(str);
        case "lower": //小写
            return /^[a-z]+$/.test(str);
        case "upper": //大写
            return /^[A-Z]+$/.test(str);
        case "HTML": //HTML标记
            return /<("[^"]*"|'[^']*'|[^'">])*>/.test(str);
        default:
            return true;
    }
};

// 严格的身份证校验
export const isCardID = (sId) => {
    if (!/(^\d{15}$)|(^\d{17}(\d|X|x)$)/.test(sId)) {
        console.log("你输入的身份证长度或格式错误");
        return false;
    }
    //身份证城市
    var aCity = {
        11: "北京",
        12: "天津",
        13: "河北",
        14: "山西",
        15: "内蒙古",
        21: "辽宁",
        22: "吉林",
        23: "黑龙江",
        31: "上海",
        32: "江苏",
        33: "浙江",
        34: "安徽",
        35: "福建",
        36: "江西",
        37: "山东",
        41: "河南",
        42: "湖北",
        43: "湖南",
        44: "广东",
        45: "广西",
        46: "海南",
        50: "重庆",
        51: "四川",
        52: "贵州",
        53: "云南",
        54: "西藏",
        61: "陕西",
        62: "甘肃",
        63: "青海",
        64: "宁夏",
        65: "新疆",
        71: "台湾",
        81: "香港",
        82: "澳门",
        91: "国外",
    };
    if (!aCity[parseInt(sId.substr(0, 2))]) {
        console.log("你的身份证地区非法");
        return false;
    }

    // 出生日期验证
    var sBirthday = (
            sId.substr(6, 4) +
            "-" +
            Number(sId.substr(10, 2)) +
            "-" +
            Number(sId.substr(12, 2))
        ).replace(/-/g, "/"),
        d = new Date(sBirthday);
    if (
        sBirthday !=
        d.getFullYear() + "/" + (d.getMonth() + 1) + "/" + d.getDate()
    ) {
        console.log("身份证上的出生日期非法");
        return false;
    }

    // 身份证号码校验
    var sum = 0,
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2],
        codes = "10X98765432";
    for (var i = 0; i < sId.length - 1; i++) {
        sum += sId[i] * weights[i];
    }
    var last = codes[sum % 11]; //计算出来的最后一位身份证号码
    if (sId[sId.length - 1] != last) {
        console.log("你输入的身份证号非法");
        return false;
    }

    return true;
};

// 游览器判断
export const ua = navigator.userAgent.toLowerCase();

// 是否是微信浏览器
export const isWeiXin = () => {
    return ua.match(/microMessenger/i) == "micromessenger";
};

// 是否是移动端
export const isDeviceMobile = () => {
    return /android|webos|iphone|ipod|balckberry/i.test(ua);
};

// 是否是QQ浏览器
export const isQQBrowser = () => {
    return !!ua.match(/mqqbrowser|qzone|qqbrowser|qbwebviewtype/i);
};

// 是否是爬虫
export const isSpider = () => {
    return /adsbot|googlebot|bingbot|msnbot|yandexbot|baidubot|robot|careerbot|seznambot|bot|baiduspider|jikespider|symantecspider|scannerlwebcrawler|crawler|360spider|sosospider|sogou web sprider|sogou orion spider/.test(
        ua
    );
};

// 是否ios
export const isIos = () => {
    var u = navigator.userAgent;
    if (u.indexOf("Android") > -1 || u.indexOf("Linux") > -1) {
        //安卓手机
        return false;
    } else if (u.indexOf("iPhone") > -1) {
        //苹果手机
        return true;
    } else if (u.indexOf("iPad") > -1) {
        //iPad
        return false;
    } else if (u.indexOf("Windows Phone") > -1) {
        //winphone手机
        return false;
    } else {
        return false;
    }
};

// 是否为PC端
export const isPC = () => {
    var userAgentInfo = navigator.userAgent;
    var Agents = [
        "Android",
        "iPhone",
        "SymbianOS",
        "Windows Phone",
        "iPad",
        "iPod",
    ];
    var flag = true;
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = false;
            break;
        }
    }
    return flag;
};