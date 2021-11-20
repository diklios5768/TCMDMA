# 前端开发文档

## 预备知识

* HTML5
* CSS3
* JavaScript(至少掌握 ES5)
* 进阶
    * NodeJS
    * ECMAScript6及以上
    * TypeScript
    * 三大前端框架Vue、React、Angular

## API

### 前后端交互

* ajax
    * 游览器原生XMLHttpRequest(XHR)，极力不推荐，除非维护上古页面
    * jQuery:$.ajax()
    * Axios
        * 极力推荐
    * fetch
        * 游览器原生fetch方法(推荐，但是要注意兼容性)
            * 参考[Fetch API](http://www.ruanyifeng.com/blog/2020/12/fetch-tutorial.html)
            * [Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
            * [传统 Ajax 已死，Fetch 永生](https://github.com/camsong/blog/issues/2)
        * NodeJS:Request库
        * UmiJS
            * [request](https://umijs.org/zh-CN/plugins/plugin-request#%E9%85%8D%E7%BD%AE)
                * 用法基本同umi-request
                * [umi-request](https://github.com/umijs/umi-request/blob/master/README_zh-CN.md)
            * [useRequest](https://hooks.umijs.org/zh-CN/hooks/async)

### 示例

* fetch方法的示例

```javascript
// 使用的es7的async和await写法，也可以使用原始的Promise写法
const data = {};
const url = '/test';
try {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify(data)
    });

    const json = await response.json();
    console.log(json);
} catch (error) {
    console.log(error);
    if (error.response) {
        console.log(error.response.status);
    } else {
        console.log(error.message);
    }
}

```

* jQuery的ajax示例

```javascript
let data = {};
let url = '/test';
$.ajax({
    url: url,
    type: 'POST',
    contentType: "application/json;charset=utf-8",
    dataType: 'json',
    data: JSON.stringify(data),
    done: function (result, status) {

    }, fail: function (error, status) {
        console.log(error);
    }, complete: function (result, status) {

    }
});

```

## 传统网页开发方法：引入css和js文件

* 文档
    * [jQuery中文](https://www.jquery123.com/)
    * [bootstrap](https://getbootstrap.com/)
* 静态资源设置
    * static_folder表示静态文件所在路径，默认为root_dir下的static文件夹
    * static_url_path的行为比较复杂
        * 如果static_folder未被指定（也就是默认值static），那么static_url_path取为static
        * 如果static_folder被指定了，那么static_url_path等于static_folder的最后一级文件夹名称
        *
      手动指定static_url_path时，如果static_url_path不为空串，url的路径必须以/开头，如/static，否则相当于static_url_path=None的情况，也就是使用static_folder的目录名字
        * 手动指定static_url_path时，如果static_url_path为空串，url路径不必以/开头
    * static_path即将废弃，推荐使用static_path_url
    * `static_folder`是你知道的文件夹位置，`static_url_path`是对外提供的静态资源url前缀，修改它可以防止别人知道你的文件夹名称
    * js和css文件在`static/js`、`static/css`文件夹下
    * 其他静态资源文件也建议每个人自己创建对应的文件夹
    * 将静态资源文件替换为相应的CDN
* 模板
    * 注意IDE设置jinja2为模板语言，才有相应的提示
    * 已经在templates/frame文件夹下创建了一些模板文件，里面已经集成了各对应的框架所需要的基本文件
    * 每个人的网页请在各自的模板文件夹下进行开发

## 现代网页开发方法：使用nodejs、webpack等工具进行开发

* 具体开发方法因为内容太多就不赘述了，只是推荐使用webstorm、vscode、HBuilderX等IDE辅助开发，前后端分离，flask只提供api
* 打包完成后将静态资源文件放到自己的资源文件夹下

## 工具包

* dom操作
    * jQuery
    * Vue
    * Knockout
    * riot
    *
* ajax
    * axios
        * [中文文档](http://www.axios-js.com/)
        * [官网](https://github.com/axios/axios)
* 打包
    * webpack
    * Gulp
        * [中文官网](https://www.gulpjs.com.cn/)
    * Snowpack
* 时间处理
    * moment.js
    * 使用dayjs(moment.js已经不维护了)
        * [官网](https://day.js.org)
        * [中文文档](https://dayjs.gitee.io/docs/zh-CN/installation/installation)

* 绘图
    * AntV
        * [官网](https://antv.vision/zh)
    * echarts
        * [官网](https://echarts.apache.org/)
    * cytoscape
        * [官网](https://js.cytoscape.org/)
    * d3
        * [官网](https://d3js.org/)
    * google charts
        * [文档](https://developers.google.cn/chart)

# 文档更新记录

* 2021-11-02
    * 初始化文档
* 2021-11-18
    * 补充一些包
* 2021-11-20
    * 完善jQuery和fetch的ajax操作示例