/*
@Date: 2021-11-23 10:57:29
@LastEditTime: 2021-11-23 11:02:26
@LastEditors: diklios
@FilePath: \js\utils\array.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
 */

// 合并数组且不重复
export const mergeArray = (arr1, arr2) => {
    let _arr = [];
    for (let i = 0; i < arr1.length; i++) {
        _arr.push(arr1[i]);
    }
    for (let i = 0; i < arr2.length; i++) {
        let flag = true;
        for (let j = 0; j < arr1.length; j++) {
            if (arr2[i] === arr1[j]) {
                flag = false;
                break;
            }
        }
        if (flag) {
            _arr.push(arr2[i]);
        }
    }
    return _arr;
};

// 数组转置
export const array_transform=(arr)=> {
    var arr1 = [];
    var arr2 = [];
    var arr_col = arr[0].length;
    var arr_row = arr.length;
    for (var i = 0; i < arr_col; i++) {
        for (var j = 0; j < arr_row; j++) {
            if (arr[j].length != arr_col) {
                return {
                    code: false,
                    msg: "column not same"
                };
            } else {
                arr1.push(arr[j][i]);
            }
        }
        arr2.push(arr1);
        arr1 = [];
    }
    return {
        code: true,
        msg: arr2
    };
}

// 判断一个元素是否在数组中
export const contains = (arr, val) => {
    return arr.indexOf(val) != -1 ? true : false;
}

// 数组排序，{type} 1：从小到大 2：从大到小 3：随机
export const sort = (arr, type = 1) => {
    return arr.sort((a, b) => {
        switch (type) {
            case 1:
                return a - b;
            case 2:
                return b - a;
            case 3:
                return Math.random() - 0.5;
            default:
                return arr;
        }
    })
}

// 数组去重
export const unique = (arr) => {
    if (Array.hasOwnProperty('from')) {
        return Array.from(new Set(arr));
    } else {
        var n = {}, r = [];
        for (var i = 0; i < arr.length; i++) {
            if (!n[arr[i]]) {
                n[arr[i]] = true;
                r.push(arr[i]);
            }
        }
        return r;
    }
}

// 求两个集合的并集
export const union = (a, b) => {
    var newArr = a.concat(b);
    return this.unique(newArr);
}

// 求两个集合的交集
export const intersect = (a, b) => {
    var _this = this;
    a = this.unique(a);
    return this.map(a, function (o) {
        return _this.contains(b, o) ? o : null;
    });
}

// 删除其中一个元素
export const remove = (arr, ele) => {
    var index = arr.indexOf(ele);
    if (index > -1) {
        arr.splice(index, 1);
    }
    return arr;
}

// 将类数组转换为数组
export const formArray = (ary) => {
    var arr = [];
    if (Array.isArray(ary)) {
        arr = ary;
    } else {
        arr = Array.prototype.slice.call(ary);
    };
    return arr;
}

// 最大值
export const max = (arr) => {
    return Math.max.apply(null, arr);
}

// 最小值
export const min = (arr) => {
    return Math.min.apply(null, arr);
}
// 求和
export const sum = (arr) => {
    return arr.reduce((pre, cur) => {
        return pre + cur
    })
}

// 平均值
export const average = (arr) => {
    return this.sum(arr) / arr.length
}

