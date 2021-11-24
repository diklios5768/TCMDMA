# 前端开发文档

## 预备知识

- HTML5
- CSS3
- JavaScript(至少掌握 ES5)
- 进阶
  - NodeJS
  - ECMAScript6 及以上
  - TypeScript
  - 三大前端框架 Vue、React、Angular

### 学习参考

- [前端精读](https://github.com/ascoders/weekly)
- [前端流媒体技术](https://github.com/zhw2590582/live-video-study-notes)

## API

### 前后端交互

- AJAX
  - 游览器原生 XMLHttpRequest(XHR)，极力不推荐，除非维护上古页面
  - JQuery:$.ajax()
  - Axios
    - 极力推荐
  - Fetch
    - 游览器原生 fetch 方法(推荐，但是要注意兼容性)
      - 参考[Fetch API](http://www.ruanyifeng.com/blog/2020/12/fetch-tutorial.html)
      - [Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
      - [传统 Ajax 已死，Fetch 永生](https://github.com/camsong/blog/issues/2)
    - NodeJS:Request 库
    - UmiJS
      - [request](https://umijs.org/zh-CN/plugins/plugin-request#%E9%85%8D%E7%BD%AE)
        - 用法基本同 umi-request
        - [umi-request](https://github.com/umijs/umi-request/blob/master/README_zh-CN.md)
      - [useRequest](https://hooks.umijs.org/zh-CN/hooks/async)

#### AJAX 示例

---

- axios 方法的示例

```javascript
const data = {};
const url = "/test";
// GET方法
axios
  .get(url, {
    // 注意：这里不需要转字符串
    params: data,
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
// POST方法
axios
  .post(url, data)
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
```

- fetch 方法的示例

```javascript
// 使用的es7的async和await写法
const data = {};
const url = "/test";
try {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(data),
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
// 可以使用原始的Promise写法
fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json;charset=utf-8",
  },
  body: JSON.stringify(data),
})
  .then((res) => res.json())
  .then((json) => {
    console.log(json);
  })
  .catch((error) => {
    if (error.response) {
      console.log(error.response.status);
    } else {
      console.log(error.message);
    }
  });
```

- jQuery 的 ajax 示例

```javascript
let data = {};
let url = "/test";
// 参考：https://www.cnblogs.com/lvonve/p/11322854.html
// 传统写法
$.ajax({
  url: url,
  type: "POST",
  contentType: "application/json;charset=utf-8",
  dataType: "json",
  data: JSON.stringify(data),
  success: function (result, status) {},
  error: function (error, status) {
    console.log(error);
  },
  complete: function (result, status) {},
});
// 新写法
// 全部都可以写成.then()的形式
$.ajax({})
  .always(function (res) {
    console.log(res);
  })
  .done(function (res) {
    console.log(res);
  })
  .fail(function (error) {
    console.log(error);
  });
```

## 传统网页开发方法：引入 css 和 js 文件

- 框架
  - JQuery
    - [官网](https://jquery.com/)
    - [jQuery 中文](https://www.jquery123.com/)
    - [常用选择器参考](https://www.w3school.com.cn/jquery/jquery_ref_selectors.asp)
    - 常用插件集合网站
      - <http://www.bootstrapmb.com/chajian>
  - BootStrap
    - [英文文档](https://getbootstrap.com/)
  - Vue:前端三大框架只有这个和传统的网页开发方式能够稍微配合一些，其他的都很难弄进来
    - Vue2
      - [官网](https://cn.vuejs.org/)
    - Vue3
      - [官网](https://v3.cn.vuejs.org/)
    - 一些问题
      - 和 jinja2 界定符的冲突，参考：<https://greyli.com/jinja2-and-js-template/>
        - 因为都是使用双大括号`{{}}`，所以要么重载 jinja2，要么重载 vue
        - vue:new 的时候重置`delimiters: ['${', '}$'],`(符号选择自己喜欢的即可)
        - 还有一种解决办法：把 JavaScript 代码都拆出来，单独放到 js 文件中，这样就不经过 jinja2 解析了
        - jinja2
          - 使用 Jinja2 的 raw 标签标记 JavaScript 模板代码
            - `{% raw %}js代码{% endraw %}`
          - 修改 Jinja2 的语法定界符号

```python
from flask import Flask

app = Flask(__name__)

app.jinja_env.block_start_string = '(%'  # 修改块开始符号
app.jinja_env.block_end_string = '%)'  # 修改块结束符号
app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
app.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
app.jinja_env.comment_end_string = '#)'  # 修改注释结束符号
```

- 静态资源设置
  - static_folder 表示静态文件所在路径，默认为 root_dir 下的 static 文件夹
  - static_url_path 的行为比较复杂
    - 如果 static_folder 未被指定（也就是默认值 static），那么 static_url_path 取为 static
    - 如果 static_folder 被指定了，那么 static_url_path 等于 static_folder 的最后一级文件夹名称
    - 手动指定 static_url_path 时，如果 static_url_path 不为空串，url 的路径必须以/开头，如/static，否则相当于 static_url_path=None 的情况，也就是使用 static_folder 的目录名字
    - 手动指定 static_url_path 时，如果 static_url_path 为空串，url 路径不必以/开头
  - static_path 即将废弃，推荐使用 static_path_url
  - `static_folder`是你知道的文件夹位置，`static_url_path`是对外提供的静态资源 url 前缀，修改它可以防止别人知道你的文件夹名称
  - js 和 css 文件在`static/js`、`static/css`文件夹下
  - 其他静态资源文件也建议每个人自己创建对应的文件夹
  - 将静态资源文件替换为相应的 CDN
- 模板
  - 注意 IDE 设置 jinja2 为模板语言，才有相应的提示
  - 已经在 templates/frame 文件夹下创建了一些模板文件，里面已经集成了各对应的框架所需要的基本文件
  - 每个人的网页请在各自的模板文件夹下进行开发

## 现代网页开发方法：使用 nodejs、webpack 等工具进行开发

- 前后端分离
  - flask 只提供 api
  - 前端打包完成后将静态资源文件放到资源文件夹下，并使用 jinja2 语法将他们链接到相应的网页即可
- IDE
  - WebStorm
  - VSCode
  - HBuilderX

## 工具包

- dom 操作
  - jQuery
  - Vue
    - vue2
      - [官网](https://cn.vuejs.org/)
    - vue3
      - [官网](https://v3.cn.vuejs.org/)
  - Knockout
    - [官网](https://knockoutjs.com/)
    - [源码](https://github.com/knockout/knockout)
    - 压缩之后体积接近 70kb，用 gzip 压缩只有 25kb
    - 2 年左右不更新了，vue 更加好用，而且体积也没有大很多
  - riot
- ajax
  - axios
    - [中文文档](http://www.axios-js.com/)
    - [官网](https://github.com/axios/axios)
- 打包
  - webpack
  - Gulp
    - [中文官网](https://www.gulpjs.com.cn/)
  - Snowpack
- 时间处理
  - moment.js
  - 使用 dayjs(moment.js 已经不维护了)
    - [官网](https://day.js.org)
    - [中文文档](https://dayjs.gitee.io/docs/zh-CN/installation/installation)
- 绘图
  - AntV
    - [官网](https://antv.vision/zh)
  - echarts
    - [官网](https://echarts.apache.org/)
  - cytoscape
    - [官网](https://js.cytoscape.org/)
  - d3
    - [官网](https://d3js.org/)
  - google charts
    - [文档](https://developers.google.cn/chart)

### Vue 生态

- vue
  - vuex
  - vue-router
- elements
- vant

### React 生态

- react
  - redux
- antd
  - AHooks.js
  - AntV

### 兼容性问题

- 特性可以通过**[CanIUse](https://caniuse.com/)**查看
- ES6/Vue3：不支持 IE11

## 文档更新记录

- 2021-11-02
  - 初始化文档
- 2021-11-18
  - 增加工具包部分
  - 补充一些包
- 2021-11-20
  - 完善 jQuery 和 fetch 的 ajax 操作示例
- 2021-11-21
  - 修复 jQuery 的 ajax 操作错误，增加更多的示例
  - 完善 axios 和 fetch 的操作方法
- 2021-11-22
  - 增加 Vue 和 React 框架生态部分
