# 开发帮助和说明

# !!!请先看完文档再进行开发!!!

# !!!请先看完文档再进行开发!!!

# !!!请先看完文档再进行开发!!!

## 项目目录（必看）

* 注意：由于git不支持空文件夹，可能由于疏忽未在里面创建文件，导致你可能看不到一些文件夹，建议手动创建
* app：flask主文件夹
    * libs：自己定义的资源
    * logs：日志记录文件存放的地方
    * models：数据库相关文件，默认是mysql或者其他关系型数据库
        * design：使用PDMan进行数据库设计的项目文件
        * sqlite：SQLite数据库文件，SQLite数据库以单文件存在的形式
        * export：导出的数据库生成文件或者数据库数据，便于手动备份和迁移
    * static：静态资源文件
    * temp：项目生成的缓存文件存放到这里，定期删除
    * templates：模板文件，使用pycharm请注意右键标记为模板文件夹（旧版或者非专业版可能不会自动识别）
        * frame：根据不同的前端框架写好的模板，不要随便修改
    * users：用户文件存放的位置
    * utils：工具文件，也可以放算法文件
        * 和libs不一样的地方在于提供处理方法，而不是一些资源定义
        * 尽量写成python模块，并在里面写点说明
    * viewModels：调用数据库的一些函数方法
    * views：视图函数
    * `__init__.py`：工厂函数和注册函数
    * `extensions.py`：插件初始化，如果需要分模块多次初始化，则放在utils里面
    * `logging.py`：封装的日志记录器
    * `my_flask.py`：自己封装改写的flask
    * `settings.py`：一些常用的系统配置，如果和某些模块绑定较为紧密则推荐放在模块的同一个文件夹中，以便迁移
* migrations：数据库迁移脚本存放的文件夹
* tests：测试环境和
    * data:测试数据存放的地方
    * models:测试数据库（一般是sqlite3）
    * test.py:常规测试文件
* docs：文档
    * code.md:码对应表
    * development.md:开发的一些帮助、说明和指南
* venv：通过virtual environment创建的虚拟环境，不会上传，但是尽量使用 `venv` 名称
* 启动和配置文件
    * .env：敏感环境配置，不推荐上传到git
    * .flaskenv：flask环境配置，可代替在`app.run()`中进行配置
    * .gitignore：不上传到git的文件或文件夹
    * dockerfile：docker配置文件
    * gunicorn.py:gunicorn配置文件
    * Pipfile,Pipfile.lock：pipenv配置文件
    * README.md:项目说明
    * requirements.txt:无pipenv环境的时候，通过virtual environment创建虚拟环境时需要的配置文件
    * waitress_config.ini:Windows环境下使用waitress的配置文件
    * waitress_server.py:服务器启动文件
    * wsgi.py：程序开发和调试的入口文件，不到万不得已不要修改

## 开发规范

* 导入包顺序：python默认模块->第三方模块->flask框架模块->flask插件模块->自己定义的模块
* 自己定义的模块导入顺序
    * libs->models->viewModels->views
    * utils可能各个地方都会用到，所以不规定顺序
    * 至于单模块，可以看上一级的目录是什么从而决定放置的顺序
* [错误码和请求返回格式](code.md)

## 可能会用到的文档

* flask
    * [官方英文文档](https://flask.palletsprojects.com/en/2.0.x/)
    * [中文文档](http://docs.jinkan.org/docs/flask/)
    * [flask扩展推荐](https://www.fullstackpython.com/flask-extensions-plug-ins-related-libraries.html)
* apiFlask
    * [官网](https://apiflask.com/)
* [A4](https://baike.baidu.com/item/A4%E7%BA%B8)
    * 常规页边距：上下2.54cm，左右3.18cm
* HTTP请求头
    * [参考](https://www.cnblogs.com/10000miles/p/9220503.html)
* 别人的项目参考：https://github.com/karec/cookiecutter-flask-restful

## pycharm指北

* 准备
    * 建议去官网注册账号后使用学校教育邮箱白嫖正版
    * 建议使用jetbrains toolbox进行安装
    * 建议每个IDE都打开jetbrains 官方同步插件

## Python包管理

* pipenv：推荐使用，更加现代化，后续所有的安装包的方法都是此方法，如果使用的是传统的方法，记得把`pipenv`更改为`pip`
    * `pipenv install 包名`
    * 更新所有包：`pipenv update`
* virtual environment
    * 请注意先激活了虚拟环境
    * `pip install 包名`
* 使用IDE
    * 在设置中，选择解释器，添加新的包
* 导出包
    * `pip freeze > requirements.txt`
* 问题
    * 如果报错说找不到包，可以在终端进行代理，或者换源
    * 虚拟环境像是本机环境，注意有可能是之前安装过虚拟环境，没有删除干净又创建了新的虚拟环境，需要手动更改文件内容，或者重新拉项目安装虚拟环境

## 后端开发

* 使用`pylint`进行代码风格的修正
* 可以安装 `watchdog` 重载器,以获得更优秀性能的重载，且无需任何额外的配置
    * `pipenv install watchdog --dev`
* 已经安装了 `Flask-Cors` 并进行配置以解决跨域问题，但是目前是全局跨域，后续可能会改为对某一批函数进行跨域处理
* 使用`Flask-SOCKETIO`配合前端使用`socketio`
    * `pipenv install flask-socketio`
* `views`文件夹下，每个人的路由已经分出来并注册到了app里面
* 如果要独自开发自己的后端，可以参考`app/__init__.py`下的工厂函数和`app/settings.py`环境设置函数
    * `app/__init__py`中的工厂函数部分一定要仔细了解一下，都是flask的进阶操作

### Git 相关使用

* 直接克隆项目：`git clone git@129.211.88.58:diklios/databaseAPI.git`
* 请在下载项目完毕后单独新开一个分支，在自己的分支上进行开发
* git相关使用可以参考[阮一峰的git教程](https://www.liaoxuefeng.com/wiki/896043488029600)
* git提交规范参考：[git commit 规范指南 - 简书 (jianshu.com)](https://www.jianshu.com/p/201bd81e7dc9?utm_source=oschina-app)

### 调试

* 建议使用`pysnooper`
    * `pipenv install pysnooper --dev`
* `Flask-Failsafe`
    * https://github.com/mgood/flask-failsafe
* google的`Cyberbrain`
    * [介绍](https://mp.weixin.qq.com/s/7kfX3SmTjP89yo4PA4S54Q)
* `Flask-debugtoolbar`
    *

### 数据库开发

* 设计使用PDMan，在`app/models/design`文件夹下可以创建自己设计的
* 使用`Flask-SQLAlchemy` 进行开发
    * [Flask-SQLAlchemy官方英文文档](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
    * [Flask-SQLAlchemy中文文档](http://www.pythondoc.com/flask-sqlalchemy/)
    * `pipenv install flask-sqlalchemy`
        * 在`models/__init__.py`文件中给出了创建、删除、重新生成数据库的示例
        * 创建自己的数据库时可以直接继承`models`文件夹下公用的数据库类
        * 在`models`文件夹下每个人创建自己的数据库文件夹
    * 级联:https://docs.sqlalchemy.org/en/14/orm/cascades.html
        * 级联删除：https://esmithy.net/2020/06/20/sqlalchemy-cascade-delete/
            * 设置ForeignKey的`ondelete="CASCADE"`和模型relationship中的`passive_deletes=True`
            * 模型的关系中设置`cascade="all, delete-orphan"`
                * ON DELETE方法更加高效
                * ON DELETE是在多的一边进行设置，而delete和delete-orphan是在一的那边进行设置
* 使用原生的`SQLAlchemy`
    * [SQLAlchemy官方英文文档](https://www.sqlalchemy.org/) 、[或者更详细的](https://docs.sqlalchemy.org/en/14/)
    * [SQLAlchemy中文文档](https://www.osgeo.cn/sqlalchemy/)
    * 创建session(会话)
        * 可以使用原生的方法
            * [参考](https://www.cnblogs.com/ChangAn223/p/11277468.html)
        * 也可以使用`Flask-SQLAlchemy-Session`
            * [文档](https://flask-sqlalchemy-session.readthedocs.io/en/latest/)
* 数据库迁移:
    * `pipenv install flask-migrate`
    * 当已经是生产环境的时候，建议纳入版本控制
    * 如果是开发环境直接全部清除和生产测试数据即可，不需要使用这个库
    * 使用
        * 命令：`flask db`，使用`flask db --help`查看
        * 生成迁移环境（一个项目只需要生成一次）：`flask db init`
        * 生成迁移脚本：`flask db migrate -m "迁移备注信息"`
        * 更新数据库：`flask db upgrade`
        * 撤回更新：`flask db downgrade`
* 数据库生成假数据:faker
    * `pipenv install faker --dev`
        * [faker能够生成的数据类型](https://www.jianshu.com/p/6bd6869631d9)
    * 在每个数据库类下面写对应的fake函数
* redis数据库
    * 客户端包
        * 一般：`pipenv install redis`
            * [官网](https://github.com/redis/redis-py)
            * [文档](https://redis-py.readthedocs.io/en/stable/)
            * 参考：https://www.cnblogs.com/amou/p/9227139.html
        * 测试：`pipenv install mockredispy`
            * [官网](https://github.com/locationlabs/mockredis)
    * `pipenv install flask-redis`
        * [官网](https://github.com/underyx/flask-redis)
        * 这个库比较基础
    * `pipenv install Flask-And-Redis`
        * [官网](https://github.com/playpauseandstop/Flask-And-Redis)
        * [文档](https://flask-and-redis.readthedocs.io/en/latest/)
* 其他
    * Flask-MongoEngine
    * Flask-Peewee
    * PonyORM
* 问题
    * create_all()创建数据
        * 执行成功刷新数据库却没有变化，请重新断开连接，再重新连接数据库看看
        * create_all()方法被调用时正是通过这个属性来获取表信息。因此，当我们调用create_all()
          前，需要确保模型类被声明创建。如果模型类存储在单独的模块中，不导入该模块就不会执行其中的代码，模型类便不会被创建，进而便无法注册表信息到db.Model.metadata.tables中，所以这时需要导入相应的模块。
        * 一般情况下，我们不用关心这个问题。在单脚本的Flask程序中自不必说，在使用包组织的Flask程序中，创建程序实例时必然需要导入视图函数所在的模块，或是蓝本所在的模块，而这些模块会导入模型类。
    * 如果使用MySQL需要安装`pymysql`或者`cymysql`驱动，并在配置文件中加上相应字段

### 用户-角色-权限-分组-安全管理

* 总览
    * 用户和角色存放于数据库，一个用户可以有多个角色，一个角色也对应了很多用户，所以是多对多的关系
    * 权限则和角色绑定，以配置文件的形式，将内容写在app/libs/scope.py文件中
        * 因为权限无法存放于数据库中，权限只是访问api的权限，但是角色可以放到数据库中
    * 用户状态
        * 注册
        * 未验证
        * 活跃
        * 删除
* 使用`flask-login`
    * `pipenv install flask-login`
    * [文档](http://www.pythondoc.com/flask-login/)
    * [英文文档](https://flask-login.readthedocs.io/en/latest/)
    * 注意数据库中避免使用`user_id`,`remember_token`
    * 配合`flask-wtf`一起使用会更加方便
    * 但是只能用于网页，使用的是基于session的cookies
* 用户id处理
    * 使用`hashids`
        * 安装：`pipenv install hashids`
        * [github地址](https://github.com/davidaurelio/hashids-python)
        * [官网](https://hashids.org/python/)
* JWT
    * 存储位置参考：https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage
    * flask_jwt_extended
        * [官网](https://github.com/vimalloc/flask-jwt-extended)
        * [文档](https://flask-jwt-extended.readthedocs.io/en/stable/)
        * 参考
            * https://www.jianshu.com/p/10d0da01244c
            * https://blog.csdn.net/djstavaV/article/details/112261875
    * Flask-Security-Too
        * [官网](https://github.com/Flask-Middleware/flask-security)
        * [文档](https://flask-security-too.readthedocs.io/en/stable/)
        * 安装：`pipenv install -U Flask-Security-Too`
        * 简介
            * 可以代替相当多的插件，如Flask-Login,Flask-Mail,Flask-Principal,Flask-WTF,itsdangerous,passlib,PyQRCode
            * 支持的数据库
                * Flask-SQLAlchemy
                * Flask-MongoEngine
                * Peewee Flask utils
                * PonyORM
    * flask-praetorian
        * [文档](https://flask-praetorian.readthedocs.io/en/latest/)
    * flask-httpauth
        * 比较基础的token验证方案
        * [示例](https://www.cnblogs.com/se7enjean/p/12470502.html)
    * https://www.jianshu.com/p/0d14ae8f081c
* 使用OAuth服务进行认证
    * 使用`flask-OAuth`
* 使用OpenID服务进行认证
    * 使用`flask-OpenID`

### 权限管理控制

* 权限管理一定是基于用户角色的，用户角色的划分是根据需求决定的
* 但是不同项目架构中的管理方法是有区别的
    * 可以使用基于`Flask-Security-Too`的权限验证方法（自己写也可以实现，就是需要加一个permission模型或者在role模型里面加上一个permission字段），但是会在每个函数前面加上装饰器
    * 个人推荐使用scope权限作用域的方法，把api写进配置文件，只要模块分的够好，写的代码就会少很多

### API

* 前置知识
    * HTTP协议
    * WSGI
    * ASGI
        * [参考](https://blog.csdn.net/weixin_43064185/article/details/108614935)
* 测试工具
    * ApiPost
    * 或者Postman
    * 前端：mockjs
* API设计
    * RestFul API
        * 开发规范
            * 有api版本号
            * 通过HTTP请求的各项方法访问和修改资源
            * 只使用JSON格式传输数据
        * 其他参考：
            * [put、post、patch的区别](https://www.cnblogs.com/shuchengyi/p/11139273.html)
        * flask-restful：https://flask-restful.readthedocs.io/en/latest/
        * 注意：但是严格的restful API是有缺陷的，所以也没必要严格使用这套方法
    * GraphQL
        * [GraphQL 官网](https://graphql.cn/)
            * `pipenv install graphene`
        * [flask-graphql](https://github.com/graphql-python/flask-graphql)
            * `pipenv install flask-graphql`
        * [graphene-sqlalchemy](https://github.com/graphql-python/graphene-sqlalchemy/)
            * `pipenv install graphene-sqlalchemy`
    * 自定义
* 前后端交互
    * ajax
        * 游览器原生XMLHttpRequest(XHR)
        * jQuery:$.ajax()
        * Axios:axios.put()
    * fetch
        * 游览器原生fetch方法(推荐)
            * 参考[Fetch API](http://www.ruanyifeng.com/blog/2020/12/fetch-tutorial.html)
            * [Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
            * [传统 Ajax 已死，Fetch 永生](https://github.com/camsong/blog/issues/2)
        * NodeJS:Request库
        * UmiJS
            * [request](https://umijs.org/zh-CN/plugins/plugin-request#%E9%85%8D%E7%BD%AE)
                * 用法基本同umi-request
                * [umi-request](https://github.com/umijs/umi-request/blob/master/README_zh-CN.md)
            * [useRequest](https://hooks.umijs.org/zh-CN/hooks/async)
* fetch方法的示例

```javascript
const data = {'type': 'random', 'count': 2};
const response = await fetch('http://127.0.0.1:5000/sun/api/find_project', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8',
    },
    body: JSON.stringify(data)
});

const json = await response.json();
console.log(json);
```

* jQuery的ajax示例

```javascript
let data = {};
let url = '';
$.ajax({
    url: url,
    data: data,
    type: 'POST',
    success: function (data) {

    }, error: function (e) {

    }, complete: function (data) {

    }

})

```

* 后端获取回传值的方法

```python
from flask import request

# 使用fetch()指定post方法传回来的数据
data = request.json
# json就是调用的get_json()方法
data2 = request.get_json()
# 使用jQuery的ajax
data3 = request.get_json('data')
# 使用url查询字符串
data4 = request.args.to_dict()
```

### 后台管理

* `flask-admin`
    * 这个插件只适合小型应用的开发，如果使用前后端分离技术，则不适用
    * [github地址](https://flask-admin.readthedocs.io/en/latest/)
    * [参考](https://www.jianshu.com/p/aef7bbdf74fa)

### 本地化日期和时间

* 目的：为了让不同时区的用户看到的都是各自时区的实际时间，而不是服务器所在地的时间
* 服务器级别
    * datetime使用utcnow()方法
        * UTC（世界标准时间）
        * 有一天我们想把服务器迁移到不同时区的地方，那么所有数据库中的时间戳必须修改成当地的正确时间在服务器重启之前。
        * 但是这还有一个更重要的问题。对于不同时区的用户很难清楚知道 blog 的发布时间因为他们看到的是在 PST 时区的时间。他们需要提前知道服务器的时区是 PST
          才能做出适当的调整。显然，这不是一个好的选择，这是为什么开始使用我们的数据库的时候，我们决定我们总是以 UTC 时区存储时间戳。
    * 使用时间戳，而不是datetime
        * 使用int类型，而不是timestamp类型
            * 因为timestamp类型继承datetime，只是范围不同
            * 数据库也不一定支持改时区设置
            * 即使数据库支持，迁移的时候数据库还需要设置，对应到前端还是需要处理
            * python内置处理datetime序列化是转为一个字符串，和sqlalchemy本身的datetime类型还不一样，所以统一使用int即可
* 前端
    * 使用`flask-moment`
        * `pipenv install flask-moment`
        * [官网](https://flask-moment.readthedocs.io/en/latest/)
        * [参考](https://www.cnblogs.com/franknihao/p/7374964.html)
        * 前后端分离的话无法使用
    * 使用dayjs(moment.js已经不维护了)
        * [官网](https://day.js.org)
        * [中文文档](https://dayjs.gitee.io/docs/zh-CN/installation/installation)

### 邮件

* `pipenv install flask-mail`
    * [flask-mail官网](https://pythonhosted.org/Flask-Mail/)
* `pipenv install sendgrid`
    * [sendgrid官网](https://sendgrid.com/)

### 表单

* 使用`flask-WTF`
    * `pipenv install flask-wtf`、`pipenv install wtforms`、`pipenv install email_validator`
    * [文档](http://www.pythondoc.com/flask-wtf/)
    * [参考](https://www.cnblogs.com/cwp-bg/p/9714741.html)
* 使用`webargs`
    * 增强版flask-wtf

### 异步任务队列

* 使用`celery`
    * `pipenv install celery`
    * [官网](https://github.com/celery/celery)
    * [celery中文文档](https://www.celerycn.io)
    * [英文文档](https://docs.celeryproject.org/en/stable/)
    * 使用
        * 配置：参考：https://docs.celeryproject.org/en/stable/userguide/configuration.html
            * 目前celery同时支持大写和小写的变量配置，但是以后会只剩下小写的，所以尽量使用小写的配置名称
            * 由于celery实际上和flask并不是一个服务，所以暂时配置文件不放在一起写
        * 启动worker：`celery -A app.utils.celery_handler.celery(这里填写的是相对于项目文件夹的celery位置) worker -l INFO`
            * 一般启动路径为`模块（即有__init__.py的文件夹）路径.celery变量名称` 或者 `python文件路径:celery变量名称`
            * 如果遇到任务不执行，一般来说是Windows的问题
                * 参数的最后面添加`--pool=solo`:`celery -A app.utils.celery_handler.celery worker -l INFO --pool=solo`
                * 或者`-P threads`:`celery -A app.utils.celery_handler.celery worker -l INFO -P threads`
            * 如果不需要使用flask的上下文，那么只需要配置并启动celery所在的模块即可，如果需要使用，那么参考`wsgi.py`中celery的实现方法
        * [辅助插件：Flask-Celery-Tools](https://github.com/Salamek/Flask-Celery-Tools)
            * 注意：这个插件暂时并不能支持最新的flask和celery，只能用于老版本，而且也不是很推荐用老方法了
        * 简单使用参考
            * 一些参数：https://www.cnblogs.com/weiweivip666/p/13966300.html
            * https://zhuanlan.zhihu.com/p/82761922
            * https://www.cnblogs.com/qiu-hua/p/12705478.html
            * https://www.cnblogs.com/wanghong1994/p/12144548.html
* 使用`rq`
    * 简介
        * 比celery更加简单的异步工具
        * 需要系统有fork()功能，所以Windows用不了
    * 安装
        * `pipenv install rq`
        * 或者`pipenv install Flask-RQ2`，方便和flask集成
    * 使用
        * [rq官方文档](https://python-rq.org/docs/)
        * [github地址](https://github.com/rq/rq)
        * [flask-rq2官网](https://github.com/rq/Flask-RQ2)
        * [Flask-RQ2文档](https://flask-rq2.readthedocs.io/en/latest/)
    * 问题参考
        * https://www.crifan.com/flask_rq2_redis_background_process_not_work/

* 使用`Huey`

### 多进程和多线程（如果使用了任务队列，可以不再使用这些技术）

* [参考](https://segmentfault.com/a/1190000007495352)

### 脚本

* 使用`flask-script`
    * [文档](https://flask-script.readthedocs.io/en/latest/)

### 缓存

* 使用`Flask-Cache`
    * [文档](https://pythonhosted.org/Flask-Cache/)

### 字符处理

* 处理Unicode
    * 使用`unidecode`
        * 安装：`pipenv install unidecode`
        * 此包将unicode编码转为iASCII编码，可以实现中文转为拼音
* 处理中文
    * 使用`pypinyin`
        * 安装：`pipenv install pypinyin`
* 加密
    * 使用`Flask-Bcrypt`
        * [文档](https://flask-bcrypt.readthedocs.io/en/latest/)

### 全文搜索

* 使用`flask-whooshee`
    * 安装：`pipenv install flask-whooshee`
* 搭配`flask-whooshalchemy`
    *

### 文件处理

* send_file 和 send_from_directory
    * 通常情况下，使用send_from_directory可以保证文件的安全性，他会检查文件是否在指定的文件夹中，因为文件夹是你指定的，所以你相信这个文件夹是可以被访问的
    * send_file是基础用法，send_from_directory检查完成后调用的就是这个方法
    * send_file可以发送保存在内存中的文件，而send_from_directory并不可以
        * `send_file(memory_file, attachment_filename='multiple_file_example.zip', as_attachment=True)`
        * flask2.1.0之后，参数名称发生了变化，同理调用send_from_directory的时候参数名称也要注意改变一下
            * attachment_filename -> download_name
            * cache_timeout -> max_age
            * add_etags -> etag
* 表格文件处理：参考`app/utils/file_handler`

#### PDF处理

* 生成
    * 原生
        * 推荐使用reportlab
            * 安装：`pipenv install reportlab`
        * 较好的代替fpdf2
        * 其他库都是比较老的，不是很推荐使用了
    * docx转PDF
    * html,markdown转PDF
* 读取
    * PyPDF2
    * PyPDF3

### 单元测试

* 使用`pytest`
    * `pipenv install pytest`
    * 函数测试
        * 从命令行进入测试文件所在目录，pytest会在该目录中寻找以test开头的文件
        * 找到测试文件，进入测试文件中寻找以test_开头的函数并执行
        * 测试函数以断言assert结尾
    * 类测试
        * 测试类所在的文件以test_开头
        * 测试类以Test开头，并且不能带有__init__方法
        * 类中测试函数以test_开头
        * 测试函数以assert断言结尾
    * 参考：https://flask.palletsprojects.com/en/2.0.x/testing/
* 使用`pytest-flask`
    * 安装：`pipenv install pytest-flask`
    * [官网](https://github.com/pytest-dev/pytest-flask)
    * [文档](https://pytest-flask.readthedocs.io/en/latest/)
* 使用`Flask-Testing`
    * 安装:`pipenv install Flask-Testing`
    * [官网](https://github.com/jarus/flask-testing)
    * [文档](https://pythonhosted.org/Flask-Testing/)

## 前端开发

### 传统网页开发方法：引入css和js文件

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

### 现代网页开发方法：使用nodejs、webpack等工具进行开发

* 具体开发方法因为内容太多就不赘述了，只是推荐使用webstorm辅助开发，前后端分离，flask只提供api
* 打包完成后将静态资源文件放到自己的资源文件夹下

### 国际化

* 使用[flask-babel](http://www.pythondoc.com/flask-babel/)
    * `pipenv install flask-babel`

## 算法

* 测试
    * jupyterlab
        * 安装：`pip install jupyterlab`
    * 网页版
        * 推荐使用`deepnote`或者`Datalore`，不需要gpu的时候更方便
        * 百度飞桨
* 必备库
    * numpy
    * pandas
        * [官网](https://pandas.pydata.org/)
* 绘图和图像处理
    * matplotlib
        * `pipenv install matplotlib --dev`
        * [中文文档](https://www.matplotlib.org.cn/)
        * [英文文档](https://matplotlib.org/)
    * Graphviz
        * `pipenv install pygraphviz`
        * [文档](http://www.graphviz.org/documentation/)
    * opencv
        * `pipenv install opencv-python`
* 人工智能
    * scipy
    * pytorch
    * TensorFlow
        * `pipenv install tensorflow`
        * [官网](https://www.tensorflow.org/)
* 复杂网络
    * networkx
        * `pipenv install networkx`
        * [官网](https://networkx.org/)
        * [文档](https://www.osgeo.cn/networkx/)

## 运维

### 部署

* 注意：推荐在Linux环境下进行部署，能够减少很多问题
* 参考
    * http://docs.jinkan.org/docs/flask/deploying/wsgi-standalone.html
    * https://www.jianshu.com/p/260f18aa5462
* 使用uwsgi作为web服务器
    * 注意：uWSGI和Gunicorn一样都是不支持Windows的
    * 安装：`pipenv install uwsgi`

```ini
# 配置示例
[uwsgi]
# uwsgi 启动时所使用的地址与端口,也可以使用.sock文件的方式
socket = 127.0.0.1:5000
# 指向网站目录
chdir = /home/moco/www/myflask
# python 启动程序文件
wsgi-file = manage.py
# python 程序内用以启动的 application 变量名
callable = app
# 处理器数
processes = 1
# 线程数
threads = 1
#状态检测地址
stats = 127.0.0.1:5001
#项目flask日志文件
logto = /home/moco/www/myflask/log.log
```

* 使用Gunicorn作为web服务器
    * 首先注意：gunicorn是在类Unix环境下使用的，Windows下不好使用，可以使用waitress代替
        * 有一种解决办法，但是还未测试过：https://blog.csdn.net/wowotuo/article/details/98526685
    * [官网](https://gunicorn.org/)
    * 详细配置参考
        * https://www.jianshu.com/p/69e75fc3e08e
        * https://www.jianshu.com/p/260f18aa5462
    * 安装：`pipenv install gunicorn`
    * 使用
        * 简单使用：在虚拟环境启动的情况下，输入`guncorn --bind 0.0.0.0:8000 wsgi:app`
        * 带有证书：`gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:8000 hello:app`
        * 使用`gunicorn.py`配置文件：`gunicorn -c gunicorn配置文件(需要加后缀) wsgi路径(不要要后缀)`
* 使用waitress
    * [官网]()
    * [英文文档](https://docs.pylonsproject.org/projects/waitress/en/latest/)
    * 使用
        * 简单使用:`waitress-serve --listen=*:8000 wsgi:flask_app`
            * 配置参考：https://www.cnblogs.com/zyl007/p/14746543.html
        * 使用启动文件：`python waitress_server.py`
        * 使用配置文件:https://docs.pylonsproject.org/projects/pastedeploy/en/latest/
* 使用Tornado
    * 可以在Windows环境下使用
    * 参考：https://segmentfault.com/a/1190000018117085
* Zappa
    * 安装：`pipenv install zappa`
    * 官网：
    * 使用参考：https://mp.weixin.qq.com/s/Yfg163FzIY4kZpeTKoU05w
        * zappa init
        * 在`zappa_settings.json`中修改基本配置
        * 启动服务：`zappa deploy dev`
* docker
    * 配置`dockerfile`
* Nginx
    * [官网](http://nginx.org/en/docs/)
    * 配置文件参考
        * https://www.jianshu.com/p/7d79cd1b1301
        * https://www.runoob.com/w3cnote/nginx-setup-intro.html
        * https://www.jianshu.com/p/aed6b5204225
        * https://www.cnblogs.com/sdadx/p/10360208.html

```text
# 负载均衡
upstream testserver {
    server 127.0.0.1:5000;
    # server 127.0.0.1:5001;
    # server 127.0.0.1:5002;
    # ...
    # 可加入多个，由 nginx 负责负载均衡
}
server {
    listen 80;
    # 这里填写你自己的域名(或者ip)
    server_name www.rookiefly.me;
    charset utf-8;
    location / {
    proxy_pass http://testserver;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass_header Set-Cookie;
    }
}
```

```text
# 不做负载均衡
server {
    listen 80;
    server_name  139.224.130.2xx;
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

* windows下作为服务：使用nssm、winsw之类的工具

### HTTPS

* [参考](https://juejin.cn/post/6844903665677893640)
* 临时证书
    * 安装依赖项：`pip install pyopenssl`
    * 将`ssl_context ='adhoc'`添加到程序的 `app.run()` 调用中
* 自签名证书
    * 生成自签名证书：`openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
    * 使用这个新的自签名证书：`app.run(ssl_context=('cert.pem', 'key.pem'))`
* 使用真实的证书
    * 免费CA：https://letsencrypt.org/
    * 腾讯云
    * 阿里云

### 域名

* 腾讯云
* 阿里云

### 日志记录

* 使用logging模块配合flask自带的app.logger即可

## 注意事项

* flask2.0开始支持异步，蓝图嵌套，快捷路由器装饰等功能，尽量使用新版本，详见：https://zhuanlan.zhihu.com/p/371659808
* 使用pycharm右键文件夹，可以选择清除python编译文件快速清除.pyc文件（但是不能清除__pycache__文件夹）
    * Linux & MacOS & WSL:`find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`

# 文档更新记录

* 更新时间：2021-07-11
    * 重构了整个文档结构，增加了大量参考链接
* 更新时间：2021-07-21
    * 微调了文档的结构
    * 添加了http状态码和restful api相关的内容
* 更新时间：2021-07-23
    * 增加了测试部分
    * 完善了项目文档结构说明
    * 注意事项中添加了清除python缓存的方法
* 更新时间：2021-07-28
    * 修改了celery的说明使用部分
    * 更新了网页开发资源和模板文件说明
* 更新时间：2021-07-30
    * 更改了celery 需要flask上下文变量的使用说明
* 更新时间：2021-08-17
    * 增加了uwsgi、gunicorn和nginx的内容
* 更新时间：2021-10-22
    * 完善了项目结构说明