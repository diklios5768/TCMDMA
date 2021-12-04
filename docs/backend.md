# 后端开发文档和帮助

## !!!请先看完文档再进行开发

## 预备知识

- python3.6 以上的基础知识
- flask1.0 以上

## 项目目录（必看）

- 注意：由于 git 不支持空文件夹，可能由于疏忽未在里面创建文件，导致你可能看不到一些文件夹，建议手动创建
- app：flask 主文件夹
  - libs：自己定义的资源
  - logs：日志记录文件存放的地方
  - models：数据库相关文件，默认是 mysql 或者其他关系型数据库
    - design：使用 PDMan 进行数据库设计的项目文件
    - sqlite：SQLite 数据库文件，SQLite 数据库以单文件存在的形式
    - export：导出的数据库生成文件或者数据库数据，便于手动备份和迁移
  - static：静态资源文件
  - temp：项目生成的缓存文件存放到这里，定期删除
  - templates：模板文件，使用 pycharm 请注意右键标记为模板文件夹（旧版或者非专业版可能不会自动识别）
    - frame：根据不同的前端框架写好的模板，不要随便修改
  - users：用户文件存放的位置
  - utils：工具文件，也可以放算法文件
    - 和 libs 不一样的地方在于提供处理方法，而不是一些资源定义
    - 尽量写成 python 模块，并在里面写点说明
  - viewModels：调用数据库的一些函数方法
  - views：视图函数
  - `__init__.py`：工厂函数和注册函数
  - `extensions.py`：插件初始化，如果需要分模块多次初始化，则放在 utils 里面
  - `logging.py`：封装的日志记录器
  - `my_flask.py`：自己封装改写的 flask
  - `settings.py`：一些常用的系统配置，如果和某些模块绑定较为紧密则推荐放在模块的同一个文件夹中，以便迁移
- migrations：数据库迁移脚本存放的文件夹
- tests：测试环境和
  - data:测试数据存放的地方
  - models:测试数据库（一般是 sqlite3）
  - test.py:常规测试文件
- docs：文档
- dependency：依赖文件夹
  - pipenv 由于认为父文件夹为虚拟环境文件夹，会自动创建，其他都是先创建虚拟环境的，故不能移过来，而且常用的就是这个，不需要移动
  - requirements.txt：无 pipenv 环境的时候，通过 virtual environment 创建虚拟环境时需要的配置文件
- venv/.venv：通过 virtual environment 创建的虚拟环境，不会上传，但是尽量使用 `venv` 名称
- server-log：服务器运行日志
- 启动和配置文件
  - .env：敏感环境配置，不推荐上传到 git
  - .flaskenv：flask 环境配置，可代替在`app.run()`中进行配置
  - .gitignore：不上传到 git 的文件或文件夹
  - dockerfile：docker 配置文件
  - gunicorn.py:gunicorn 配置文件
  - Pipfile,Pipfile.lock：pipenv 配置文件
  - README.md:项目说明
  - waitress_config.ini:Windows 环境下使用 waitress 的配置文件
  - waitress_server.py:服务器启动文件
  - wsgi.py：程序开发和调试的入口文件，不到万不得已不要修改

## 开发规范

- 导入包顺序：python 默认模块->第三方模块->flask 框架模块->flask 插件模块->自己定义的模块
- 自己定义的模块导入顺序
  - libs->models->viewModels->views
  - utils 可能各个地方都会用到，所以不规定顺序
  - 至于单模块，可以看上一级的目录是什么从而决定放置的顺序
- [错误码和请求返回格式](code.md)

## 可能会用到的文档

- flask
  - [官方英文文档](https://flask.palletsprojects.com/en/2.0.x/)
  - [中文文档](http://docs.jinkan.org/docs/flask/)
  - [flask 扩展推荐](https://www.fullstackpython.com/flask-extensions-plug-ins-related-libraries.html)
- [A4](https://baike.baidu.com/item/A4%E7%BA%B8)
  - 常规页边距：上下 2.54cm，左右 3.18cm
- HTTP 请求头
  - [参考](https://www.cnblogs.com/10000miles/p/9220503.html)
- 别人的项目参考：<https://github.com/karec/cookiecutter-flask-restful>

## pycharm 指北

- 准备
  - 建议去官网注册账号后使用学校教育邮箱白嫖正版
  - 建议使用 jetbrains toolbox 进行安装
  - 建议每个 IDE 都打开 jetbrains 官方同步插件

## Python 包管理

- pipenv：推荐使用，更加现代化，后续所有的安装包的方法都是此方法，如果使用的是传统的方法，记得把`pipenv`更改为`pip`
  - `pipenv install 包名`
  - 更新所有包：`pipenv update`
  - [官网](https://github.com/pypa/pipenv)
  - [文档](https://pipenv.pypa.io/en/latest/)
    - 最好学习一下高级用法
  - [**巨坑，用了额外的索引会导致 lock 的时候非常慢，一般来说项目再大几分钟就好了**](https://github.com/pypa/pipenv/issues/2730#issuecomment-423599283)
- virtual environment
  - 请注意先激活了虚拟环境
  - `pip install 包名`
- 使用 IDE
  - 在设置中，选择解释器，添加新的包
- 导出包
  - 原生方法
    - 导出生产环境包：`pip freeze > requirements.txt`
    - 导出开发环境包：`pip freeze > requirements-dev.txt`
  - 使用`pipreqs`:这个不像 freeze 那样会导出一大堆的包
    - 安装：`pipenv install pipreqs`
    - 导出：`pipreqs ./ --encoding=utf8`
      - 默认导出的文件名就是`requirements.txt`
  - 使用`pipenv`：推荐，导出的方法多种多样
    - 导出生产环境包：`pipenv lock -r > requirements-pipenv.txt`
    - 导出包含开发环境的包：`pipenv lock -r --dev > requirements-pipenv-dev.txt`
    - 只导出开发环境的包：`pipenv lock -r --dev-only > requirements-pipenv-dev-only.txt`
- 问题
  - 如果报错说找不到包，可以在终端进行代理，或者换源
  - 安装失败，注意看是不是要安装 vc++14，我倾向于直接装一个 visual studio 的 c++环境，操作起来很简单，下载安装即可
  - 虚拟环境像是本机环境，注意有可能是之前安装过虚拟环境，没有删除干净又创建了新的虚拟环境，导致路径错误，需要手动更改文件内容，或者重新拉项目安装虚拟环境

## 后端开发

- 使用`pylint`进行代码风格的修正
- 可以安装 `watchdog` 重载器,以获得更优秀性能的重载，且无需任何额外的配置
  - `pipenv install watchdog --dev`
- 已经安装了 `Flask-Cors` 并进行配置以解决跨域问题，但是目前是全局跨域，后续可能会改为对某一批函数进行跨域处理
- 使用`Flask-SOCKETIO`配合前端使用`socketio`
  - `pipenv install flask-socketio`
- `views`文件夹下，每个人的路由已经分出来并注册到了 app 里面
- 如果要独自开发自己的后端，可以参考`app/__init__.py`下的工厂函数和`app/settings.py`环境设置函数
  - `app/__init__py`中的工厂函数部分一定要仔细了解一下，都是 flask 的进阶操作

### Git 相关使用

- 直接克隆项目：`git clone 仓库的链接`
- 请在下载项目完毕后单独新开一个分支，在自己的分支上进行开发
- git 相关使用可以参考

  - [30 天精通 Git 版本控管](https://github.com/doggy8088/Learn-Git-in-30-days)
  - [阮一峰的 git 教程](https://www.liaoxuefeng.com/wiki/896043488029600)
  - git 提交规范参考：[git commit 规范指南](https://www.jianshu.com/p/201bd81e7dc9?utm_source=oschina-app)

- .gitignore 说明
  - `app/logs`和`app/users`是提交到代码仓库的时候需要移除的，但不是迁移的时候需要移除的

### 调试

- 建议使用`pysnooper`
  - `pipenv install pysnooper --dev`
- `Flask-Failsafe`
  - <https://github.com/mgood/flask-failsafe>
- google 的`Cyberbrain`
  - [介绍](https://mp.weixin.qq.com/s/7kfX3SmTjP89yo4PA4S54Q)
- `Flask-debugtoolbar`

### 数据库开发

- SQL 类型数据库
  - 设计
    - 在`app/models/design`文件夹下可以创建自己设计的数据库
    - Chiner(原 PDMan)
      - [源码](https://gitee.com/robergroup/chiner)
    - [NocoDB](https://github.com/nocodb/nocodb)
  - 查看和管理
    - Navicat
      - 自带的 ER 图非常方便
    - Datagrip
    - DBeaver
  - 数据库导出
    - 最好设计先行，只有实在没有用办法的时候才通过工具导出
    - [mysql_markdown](https://github.com/alicfeng/mysql_markdown)
  - 开发
    - 使用`Flask-SQLAlchemy`
      - [Flask-SQLAlchemy 官方英文文档](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
      - [Flask-SQLAlchemy 中文文档](http://www.pythondoc.com/flask-sqlalchemy/)
      - `pipenv install flask-sqlalchemy`
      - 在`models/__init__.py`文件中给出了创建、删除、重新生成数据库的示例
      - 创建自己的数据库时可以直接继承`models`文件夹下公用的数据库类
      - 在`models`文件夹下每个人创建自己的数据库文件夹
      - 级联:<https://docs.sqlalchemy.org/en/14/orm/cascades.html>
        - 级联删除：<https://esmithy.net/2020/06/20/sqlalchemy-cascade-delete/>
          - 设置 ForeignKey 的`ondelete="CASCADE"`和模型 relationship 中的`passive_deletes=True`
          - 模型的关系中设置`cascade="all, delete-orphan"`
            - ON DELETE 方法更加高效
            - ON DELETE 是在多的一边进行设置，而 delete 和 delete-orphan 是在一的那边进行设置
    - 使用原生的`SQLAlchemy`
      - [SQLAlchemy 官方英文文档](https://www.sqlalchemy.org/) 、[或者更详细的](https://docs.sqlalchemy.org/en/14/)
      - [SQLAlchemy 中文文档](https://www.osgeo.cn/sqlalchemy/)
      - 创建 session(会话)
        - 可以使用原生的方法
          - [参考](https://www.cnblogs.com/ChangAn223/p/11277468.html)
        - 也可以使用`Flask-SQLAlchemy-Session`
          - [文档](https://flask-sqlalchemy-session.readthedocs.io/en/latest/)
    - 使用`sqlalchemy-utils`
      - 提供了大量的字段类型和工具函数
      - [官网](https://github.com/kvesteri/sqlalchemy-utils)
      - [文档](https://sqlalchemy-utils.readthedocs.io/en/latest/installation.html)
    - 其他一些 API 和 Swagger 的库也附带数据库功能，具体参考对应部分文档
  - 数据库迁移:
    - `pipenv install flask-migrate`
    - 当已经是生产环境的时候，建议纳入版本控制
    - 如果是开发环境直接全部清除和生产测试数据即可，不需要使用这个库
    - 使用
      - 命令：`flask db`，使用`flask db --help`查看
      - 生成迁移环境（一个项目只需要生成一次）：`flask db init`
      - 生成迁移脚本：`flask db migrate -m "迁移备注信息"`
      - 更新数据库：`flask db upgrade`
      - 撤回更新：`flask db downgrade`
  - 生成假数据：faker
    - `pipenv install faker --dev`
      - [faker 能够生成的数据类型](https://www.jianshu.com/p/6bd6869631d9)
    - 在每个数据库类下面写对应的 fake 函数
  - 问题
    - create_all()创建数据
      - 执行成功刷新数据库却没有变化，请重新断开连接，再重新连接数据库看看
      - create_all()方法被调用时正是通过这个属性来获取表信息。因此，当我们调用 create_all()
        前，需要确保模型类被声明创建。如果模型类存储在单独的模块中，不导入该模块就不会执行其中的代码，模型类便不会被创建，进而便无法注册表信息到 db.Model.metadata.tables 中，所以这时需要导入相应的模块。
      - 一般情况下，我们不用关心这个问题。在单脚本的 Flask 程序中自不必说，在使用包组织的 Flask 程序中，创建程序实例时必然需要导入视图函数所在的模块，或是蓝本所在的模块，而这些模块会导入模型类。
    - 如果使用 MySQL 需要安装`pymysql`或者`cymysql`驱动，并在配置文件中加上相应字段
- redis 数据库
  - 客户端驱动
    - 常用：`pipenv install redis`
      - [官网](https://github.com/redis/redis-py)
      - [文档](https://redis-py.readthedocs.io/en/stable/)
      - 参考：<https://www.cnblogs.com/amou/p/9227139.html>
    - 测试：`pipenv install mockredispy`
      - [官网](https://github.com/locationlabs/mockredis)
  - flask 扩展
    - flask-redis
      - 这个库比较基础，但足够了
      - 安装：`pipenv install flask-redis`
      - [官网](https://github.com/underyx/flask-redis)
    - Flask-And-Redis
    - 安装：`pipenv install Flask-And-Redis`
    - [官网](https://github.com/playpauseandstop/Flask-And-Redis)
    - [文档](https://flask-and-redis.readthedocs.io/en/latest/)
- 其他数据库
  - Flask-MongoEngine
  - Flask-Peewee
  - PonyORM

### 用户-角色-权限-分组-安全管理

- 总览
  - 用户和角色存放于数据库，一个用户可以有多个角色，一个角色也对应了很多用户，所以是多对多的关系
  - 权限则和角色绑定，以配置文件的形式，将内容写在 app/libs/scope.py 文件中
    - 因为权限无法存放于数据库中，权限只是访问 api 的权限，但是角色可以放到数据库中
  - 用户状态
    - 注册
    - 未验证
    - 活跃
    - 删除
- 使用`flask-login`
  - `pipenv install flask-login`
  - [文档](http://www.pythondoc.com/flask-login/)
  - [英文文档](https://flask-login.readthedocs.io/en/latest/)
  - 注意数据库中避免使用`user_id`,`remember_token`
  - 配合`flask-wtf`一起使用会更加方便
  - 但是只能用于网页，使用的是基于 session 的 cookies
- 用户 id 处理
  - 使用`hashids`
    - 安装：`pipenv install hashids`
    - [github 地址](https://github.com/davidaurelio/hashids-python)
    - [官网](https://hashids.org/python/)
- JWT
  - 存储位置参考：<https://stormpath.com/blog/where-to-store-your-jwts-cookies-vs-html5-web-storage>
  - flask_jwt_extended
    - [官网](https://github.com/vimalloc/flask-jwt-extended)
    - [文档](https://flask-jwt-extended.readthedocs.io/en/stable/)
    - 参考
      - <https://www.jianshu.com/p/10d0da01244c>
      - <https://blog.csdn.net/djstavaV/article/details/112261875>
  - Flask-Security-Too
    - 注意，老版本的 flask-security 已经不维护了，不推荐使用
    - [官网](https://github.com/Flask-Middleware/flask-security)
    - [文档](https://flask-security-too.readthedocs.io/en/stable/)
    - 安装：`pipenv install -U Flask-Security-Too`
    - 简介
      - 可以代替相当多的插件，如 Flask-Login,Flask-Mail,Flask-Principal,Flask-WTF,itsdangerous,passlib,PyQRCode
      - 支持的数据库
        - Flask-SQLAlchemy
        - Flask-MongoEngine
        - Peewee Flask utils
        - PonyORM
  - flask-praetorian
    - [文档](https://flask-praetorian.readthedocs.io/en/latest/)
  - flask-httpauth
    - 比较基础的 token 验证方案，也比较足够了
    - [示例](https://www.cnblogs.com/se7enjean/p/12470502.html)
  - <https://www.jianshu.com/p/0d14ae8f081c>
- 使用 OAuth 服务进行认证
  - 使用`flask-OAuth`
- 使用 OpenID 服务进行认证
  - 使用`flask-OpenID`

### 权限管理控制

- 权限管理一定是基于用户角色的，用户角色的划分是根据需求决定的
- 但是不同项目架构中的管理方法是有区别的
  - 可以使用基于`Flask-Security-Too`的权限验证方法（自己写也可以实现，就是需要加一个 permission 模型或者在 role 模型里面加上一个 permission 字段），但是会在每个函数前面加上装饰器
  - 个人现在使用 scope 权限作用域的方法，把 api 写进配置文件，只要模块分的够好，写的代码就会少很多

### API

- 前置知识
  - HTTP 协议
  - WSGI
  - ASGI
    - [参考](https://blog.csdn.net/weixin_43064185/article/details/108614935)
- 测试工具
  - ApiPost
  - Postman
  - 前端：mockjs
- API 设计
  - RestfulAPI 规范
    - 开发规范
      - 有 API 版本号
      - 通过 HTTP 请求的不同方法访问和修改资源
      - 只使用 JSON 格式传输数据
    - flask-restful
      - [文档](https://flask-restful.readthedocs.io/en/latest/)
    - 其他参考：
      - [put、post、patch 的区别](https://www.cnblogs.com/shuchengyi/p/11139273.html)
    - 注意：但是严格的 restful API 是有缺陷的，所以也没必要严格使用这套方法
  - GraphQL
    - [GraphQL 官网](https://graphql.cn/)
      - `pipenv install graphene`
    - [flask-graphql](https://github.com/graphql-python/flask-graphql)
      - `pipenv install flask-graphql`
    - [graphene-sqlalchemy](https://github.com/graphql-python/graphene-sqlalchemy/)
      - `pipenv install graphene-sqlalchemy`
    - 教程：<https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/>
  - 自定义
- API 限制
  - 使用`flask-limiter`
    - 安装：`pipenv install Flask-Limiter`
    - [文档](https://flask-limiter.readthedocs.io/en/stable/)
    - 限制
      - 格式
        - "100 per day"、"20 per hour"、"5 per minute"、"1 per second"
        - "100/day"、"20/hour"、"5/minute"、"1/second"
      - 速率限制可以设置全局配置，针对所有接口进行限制
      - 也可以通过装饰器进行局部限制
      - 对于不想限制的接口，可以通过装饰器@limiter.exempt 进行解除限制
    - limiter 装饰器
      - @limiter.exempt：解除限制
      - @limiter.limit
        - limit_value:可以是字符串，也可以是一个获得字符串的函数（从 app.config 中加载）
        - key_func:据什么进行限制，flask_limiter.util 提供了两种方式
          - flask_limiter.util.get_ipaddr()：使用 X-Forwarded-For 标头中的最后一个 IP 地址，否则回退到请求的 remote_address 。
          - flask_limiter.util.get_remote_address()：使用请求的 remote_address
            - 注意：在真实开发中，大部分项目都配置了 Nginx，如果直接使用 get_remote_address，获取到的是 Nginx 服务器的地址，相当于来自该 Nginx
              服务器的所有请求会被当做同一个 IP 访问，所以项目中一般都是自定义 key_func
          - X-Forwarded-For：一般是每一个非透明代理转发请求时会将上游服务器的 ip 地址追加到 X-Forwarded-For 的后面，使用英文逗号分割； _
            X-Real-IP：一般是最后一级代理将上游 ip 地址添加到该头中；_ X-Forwarded-For 是多个 ip 地址，而 X-Real-IP
            是一个；如果只有一层代理，这两个头的值就是一样的
        - exempt_when=callable:当满足给定条件时，可以免除限制
          - 也可以使用 Limiter.request_filter 实现
        - deduct_when:断某些情况不计入使用频率的次数
        - error_message：自定义错误信息
      - 共享限制：创建一个 limiter.shared_limit 对象
        - 命名共享限制：通过相同的 shared_limit 对象进行装饰。
        - 动态共享限制：将可调用对象作为范围传递，该函数的返回值将用作范围。注意，callable 具有一个参数：表示请求端点的字符串。
        - 与单个 limiter 一样可以叠加多个 share_limiter 装饰器
        - 可接受 key_function 参数
        - 也可结束动态的策略配置函数， 与 limiter 一致
      - @limiter.request_filter：符合条件的屏蔽策略
    - 速度限制策略
      - Flask-Limiter 内置了三种不同的速率限制策略
        - Fixed Window
        - Fixed Window with Elastic Expiry
        - Moving Window
    - 参考
      - <https://www.cnblogs.com/Du704/p/13281032.html>
      - <https://blog.csdn.net/zuozuochong/article/details/88365970>
- swagger：基于 RESTful API 的文档集成工具
  - [官网](https://swagger.io/)
  - [Swagger UI](https://swagger.io/tools/swagger-ui/)
  - Flask-RESTPlus:flask-restful 框架的一个加强版
    - 两年多不维护了，新的 fork 是 Flask RESTX
    - [官网](https://github.com/noirbizarre/flask-restplus)
    - [文档](https://flask-restplus.readthedocs.io/en/stable/swagger.html)
  - Flask RESTX
    - [官网](https://github.com/python-restx/flask-restx)
    - [文档](https://flask-restx.readthedocs.io/en/latest/)
    - 虽然这两个效果不错，但是问题在于他们使用的是基于类的视图，对于代码改动较大
  - Flasgger
    - 非常棒的插件，支持视图级别的文档撰写，也支持类，还支持参数验证（注意，非表单验证，不一样的）
    - 安装：`pipenv install flasgger`
    - [官网](https://github.com/flasgger/flasgger)
    -
- 后端获取回传值的方法

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

### 表单

- 使用基础的`wtforms`
  - `pipenv install wtforms`
  - [官网](https://github.com/wtforms/wtforms)
  - [文档](https://wtforms.readthedocs.io/)
- 使用`flask-WTF`
  - `pipenv install flask-wtf`
  - [文档](http://www.pythondoc.com/flask-wtf/)
  - [参考](https://www.cnblogs.com/cwp-bg/p/9714741.html)
- 使用`webargs`
  - 增强版 flask-wtf，不仅仅是表单，连 HTTP 的各个参数也能校验
    - Flasgger 只能方便的校验 query 和 body 的参数
    - 其他的校验虽然可以自己写，但不简便
  - 安装：`pipenv install webargs`
  - [官网](https://github.com/marshmallow-code/webargs)
  - [文档](https://webargs.readthedocs.io/en/latest/)

### 后台管理

- `flask-admin`
  - 类似 Django 的 xadmin 插件，提供快速简单的后台管理功能
  - [官网](https://github.com/flask-admin/flask-admin)
  - [文档](https://flask-admin.readthedocs.io/en/latest/)
  - [参考]
    - <https://www.jianshu.com/p/aef7bbdf74fa>
    - <https://segmentfault.com/a/1190000013073352>
- `Flask App Builder`
  - 基于 Flask 实现的一个用于快速构建 Web 后台管理系统的简单的框架
  - [官网](https://github.com/dpgaspar/Flask-AppBuilder)
  - [文档](https://flask-appbuilder.readthedocs.io/en/latest/)

### 本地化日期和时间

- 目的：为了让不同时区的用户看到的都是各自时区的实际时间，而不是服务器所在地的时间
- 服务器级别
  - datetime 使用 utcnow()方法
    - UTC（世界标准时间）
    - 有一天我们想把服务器迁移到不同时区的地方，那么所有数据库中的时间戳必须修改成当地的正确时间在服务器重启之前。
    - 但是这还有一个更重要的问题。对于不同时区的用户很难清楚知道 blog 的发布时间因为他们看到的是在 PST 时区的时间。他们需要提前知道服务器的时区是 PST
      才能做出适当的调整。显然，这不是一个好的选择，这是为什么开始使用我们的数据库的时候，我们决定我们总是以 UTC 时区存储时间戳。
  - 使用时间戳，而不是 datetime
    - 使用 int 类型，而不是 timestamp 类型
      - 因为 timestamp 类型继承 datetime，只是范围不同
      - 数据库也不一定支持改时区设置
      - 即使数据库支持，迁移的时候数据库还需要设置，对应到前端还是需要处理
      - python 内置处理 datetime 序列化是转为一个字符串，和 sqlalchemy 本身的 datetime 类型还不一样，所以统一使用 int 即可
- 前端
  - 使用`flask-moment`
    - `pipenv install flask-moment`
    - [官网](https://flask-moment.readthedocs.io/en/latest/)
    - [参考](https://www.cnblogs.com/franknihao/p/7374964.html)
    - **注意：前后端分离的话不需要使用这个插件**

### 邮件

- `Flask-Mail`
  - 安装：`pipenv install flask-mail`
  - [官网](https://pythonhosted.org/Flask-Mail/)
  - 2014 年之后项目不再维护，建议使用`Flask-Mailman`
- `Flask-Mailman`
  - [官网](https://github.com/waynerv/flask-mailman)
  - [文档](https://www.waynerv.com/flask-mailman/)
  - 安装：`pipenv install Flask-Mailman`
- 使用`sendgrid`提供邮箱服务
  - `pipenv install sendgrid`
  - [sendgrid 官网](https://sendgrid.com/)
  - 现在的 sendgrid 似乎不能免费使用了，换 126 或者 163 邮箱吧

### 手机验证码

- 用阿里云的服务

### 异步任务队列

- 使用`celery`
  - `pipenv install celery`
  - [官网](https://github.com/celery/celery)
  - [celery 中文文档](https://www.celerycn.io)
  - [英文文档](https://docs.celeryproject.org/en/stable/)
  - 使用
    - 配置：参考：<https://docs.celeryproject.org/en/stable/userguide/configuration.html>
      - 目前 celery 同时支持大写和小写的变量配置，但是以后会只剩下小写的，所以尽量使用小写的配置名称
      - 由于 celery 实际上和 flask 并不是一个服务，所以暂时配置文件不放在一起写
    - 启动 worker：`celery -A app.utils.celery_handler.celery(这里填写的是相对于项目文件夹的celery位置) worker -l INFO`
      - 一般启动路径为`模块（即有__init__.py的文件夹）路径.celery变量名称` 或者 `python文件路径:celery变量名称`
      - 如果遇到任务不执行，一般来说是 Windows 的问题
        - 参数的最后面添加`--pool=solo`:`celery -A app.utils.celery_handler.celery worker -l INFO --pool=solo`
        - 或者`-P threads`:`celery -A app.utils.celery_handler.celery worker -l INFO -P threads`
      - 如果不需要使用 flask 的上下文，那么只需要配置并启动 celery 所在的模块即可，如果需要使用，那么参考`wsgi.py`中 celery 的实现方法
    - [辅助插件：Flask-Celery-Tools](https://github.com/Salamek/Flask-Celery-Tools)
      - 注意：这个插件暂时并不能支持最新的 flask 和 celery，只能用于老版本，而且也不是很推荐用老方法了
    - 简单使用参考
      - 一些参数：<https://www.cnblogs.com/weiweivip666/p/13966300.html>
      - <https://zhuanlan.zhihu.com/p/82761922>
      - <https://www.cnblogs.com/qiu-hua/p/12705478.html>
      - <https://www.cnblogs.com/wanghong1994/p/12144548.html>
- 使用`rq`

  - 简介
    - 比 celery 更加简单的异步工具
    - 需要系统有 fork()功能，所以 Windows 用不了
  - 安装
    - `pipenv install rq`
    - 或者`pipenv install Flask-RQ2`，方便和 flask 集成
  - 使用
    - [rq 官方文档](https://python-rq.org/docs/)
    - [github 地址](https://github.com/rq/rq)
    - [flask-rq2 官网](https://github.com/rq/Flask-RQ2)
    - [Flask-RQ2 文档](https://flask-rq2.readthedocs.io/en/latest/)
  - 问题参考
    - <https://www.crifan.com/flask_rq2_redis_background_process_not_work/>

- 使用`Huey`

### 多进程和多线程（如果使用了任务队列，可以不再使用这些技术）

- [参考](https://segmentfault.com/a/1190000007495352)

### 脚本

- 使用`flask-script`
  - [文档](https://flask-script.readthedocs.io/en/latest/)

### 缓存

- 使用`Flask-Cache`:太老了，很多年不更新了，不推荐使用
  - 安装：`pipenv install Flask-Cache`
  - [官网](https://github.com/thadeusb/flask-cache)
  - [文档](https://pythonhosted.org/Flask-Cache/)
  - 使用 Memoization 甚至能够缓存相同参数的函数
    - 如果函数不接受参数的话，cached() 和 memoize() 两者的作用是一样的
  - 具体的删除方法见官方文档
  - 参考：<https://blog.csdn.net/qq_41134008/article/details/105698861>
- 使用`flask-caching`:fork 老版本的 flask-cache
  - 安装：`pipenv install flask-caching`
  - [官网](https://github.com/pallets-eco/flask-caching)
  - [文档](https://flask-caching.readthedocs.io/en/latest/)

### 字符处理

- 处理 Unicode
  - 使用`unidecode`
    - 安装：`pipenv install unidecode`
    - 此包将 unicode 编码转为 iASCII 编码，可以实现中文转为拼音
- 处理中文
  - 使用`pypinyin`
    - 安装：`pipenv install pypinyin`
- 加密
  - 使用`Flask-Bcrypt`
    - [官网](https://github.com/maxcountryman/flask-bcrypt)
    - [文档](https://flask-bcrypt.readthedocs.io/en/latest/)
    - 安装：`pipenv install Flask-Bcrypt`
    - 但是问题在于这个库很久没有提交到 pypi 上了
  - 使用`Bcrypt-Flask`
    - [官网](https://github.com/mahenzon/flask-bcrypt)
    - 安装：`pipenv install Bcrypt-Flask`
    - 有人把 Flask-Bcrypt 的最新版提交了上来

### 全文搜索

- 使用`flask-whooshee`
  - 安装：`pipenv install flask-whooshee`
  - [官网](https://github.com/bkabrda/flask-whooshee)
  - [文档](https://flask-whooshee.readthedocs.io/en/latest/)
- 以下两个比较老了，不更新了，不推荐使用
  - `flask-whooshalchemy`
  - `Flask-WhooshAlchemyPlus`

### 文件处理

- send_file 和 send_from_directory
  - 通常情况下，使用 send_from_directory 可以保证文件的安全性，他会检查文件是否在指定的文件夹中，因为文件夹是你指定的，所以你相信这个文件夹是可以被访问的
  - send_file 是基础用法，send_from_directory 检查完成后调用的就是这个方法
  - send_file 可以发送保存在内存中的文件，而 send_from_directory 并不可以
    - `send_file(memory_file, attachment_filename='multiple_file_example.zip', as_attachment=True)`
    - flask2.1.0 之后，参数名称发生了变化，同理调用 send_from_directory 的时候参数名称也要注意改变一下
      - attachment_filename -> download_name
      - cache_timeout -> max_age
      - add_etags -> etag
- 表格文件处理：参考`app/utils/file_handler`

#### PDF 处理

- 生成
  - 原生
    - 推荐使用 reportlab
      - 安装：`pipenv install reportlab`
    - 较好的代替 fpdf2
    - 其他库都是比较老的，不是很推荐使用了
  - docx 转 PDF
  - html,markdown 转 PDF
- 读取
  - PyPDF2
  - PyPDF3

### 单元测试

- 使用`pytest`
  - `pipenv install pytest`
  - 函数测试
    - 从命令行进入测试文件所在目录，pytest 会在该目录中寻找以 test 开头的文件
    - 找到测试文件，进入测试文件中寻找以 test\_开头的函数并执行
    - 测试函数以断言 assert 结尾
  - 类测试
    - 测试类所在的文件以 test\_开头
    - 测试类以 Test 开头，并且不能带有**init**方法
    - 类中测试函数以 test\_开头
    - 测试函数以 assert 断言结尾
  - 参考：<https://flask.palletsprojects.com/en/2.0.x/testing/>
- 使用`pytest-flask`
  - 安装：`pipenv install pytest-flask`
  - [官网](https://github.com/pytest-dev/pytest-flask)
  - [文档](https://pytest-flask.readthedocs.io/en/latest/)
- 使用`Flask-Testing`
  - 安装:`pipenv install Flask-Testing`
  - [官网](https://github.com/jarus/flask-testing)
  - [文档](https://pythonhosted.org/Flask-Testing/)

### 国际化

- 使用[flask-babel](http://www.pythondoc.com/flask-babel/)
  - `pipenv install flask-babel`

## 算法

- 测试
  - jupyterlab
    - 安装：`pip install jupyterlab`
  - 网页版
    - 推荐使用`deepnote`或者`Datalore`，不需要 gpu 的时候更方便
    - 百度飞桨
- 必备库
  - numpy
    - 安装：`pipenv install numpy`
    - [官网](https://numpy.org/)
    - [英文文档](https://numpy.org/doc/stable/)
    - [中文文档](https://www.numpy.org.cn/)
  - pandas
    - 安装：`pipenv install pandas`
    - [官网](https://pandas.pydata.org/)
- 绘图和图像处理
  - matplotlib
    - `pipenv install matplotlib --dev`
    - [中文文档](https://www.matplotlib.org.cn/)
    - [英文文档](https://matplotlib.org/)
  - Graphviz
    - `pipenv install pygraphviz`
    - [文档](http://www.graphviz.org/documentation/)
  - opencv
    - `pipenv install opencv-python`
- 人工智能
  - scipy
    - `pipenv install scipy`
  - pytorch
    - 安装：`pipenv install pytorch torchvision torchaudio cpuonly -c pytorch`
      - 更详细的安装见：<https://pytorch.org/get-started/locally/>
    - [官网](https://pytorch.org/)
    - [中文文档](https://pytorch-cn.readthedocs.io/zh/latest/)
  - TensorFlow
    - `pipenv install tensorflow`
    - [官网](https://www.tensorflow.org/)
- 复杂网络
  - networkx
    - `pipenv install networkx`
    - [官网](https://networkx.org/)
    - [文档](https://www.osgeo.cn/networkx/)

## 运维

### 快速启动脚本

- flask

```shell
# run-flaskapp.sh
. $(pipenv --venv)/bin/activate;
gunicorn -c gunicorn.py wsgi:wsgi_ap -D;
```

```powershell
# run-flaskapp.ps1
# 不能使用pipenv shell，这会新建一个终端，后面的命令会全部消失
# 注意：Windows下是Scripts不是bin
# -join转的字符串不带空格，鬼知道为什么Out-String没有用
$pipenvPath = (pipenv --venv) -join "";
& "$pipenvPath\Scripts\activate";
python waitress_server.py;
```

- celery

```shell
# run-celeryapp.sh
. $(pipenv --venv)/bin/activate;
celery -A wsgi:celery worker -l INFO;
```

```powershell
# run-celeryapp.ps1
$pipenvPath = (pipenv --venv) -join "";
& "$pipenvPath\Scripts\activate";
celery -A wsgi:celery worker -l INFO -P threads;
```

### 部署

- 注意：推荐在 Linux 环境下进行部署，能够减少很多问题
- 参考
  - <http://docs.jinkan.org/docs/flask/deploying/wsgi-standalone.html>
  - <https://www.jianshu.com/p/260f18aa5462>
- 使用 uwsgi 作为 web 服务器
  - 注意：uWSGI 和 Gunicorn 一样都是不支持 Windows 的
  - 安装：`pipenv install uwsgi`

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

- 使用 Gunicorn 作为 web 服务器
  - 首先注意：gunicorn 是在类 Unix 环境下使用的，Windows 下不好使用，可以使用 waitress 代替
    - 有一种解决办法，但是还未测试过：<https://blog.csdn.net/wowotuo/article/details/98526685>
  - [官网](https://gunicorn.org/)
  - 详细配置参考
    - <https://www.jianshu.com/p/69e75fc3e08e>
    - <https://www.jianshu.com/p/260f18aa5462>
  - 安装：`pipenv install gunicorn`
  - 使用
    - 简单使用：在虚拟环境启动的情况下，输入`guncorn --bind 0.0.0.0:8000 wsgi:app`
    - 带有证书：`gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:8000 hello:app`
    - 使用`gunicorn.py`配置文件：`gunicorn -c gunicorn配置文件(需要加后缀) wsgi路径(不要要后缀)`
- 使用 waitress
  - [官网]()
  - [英文文档](https://docs.pylonsproject.org/projects/waitress/en/latest/)
  - 使用
    - 简单使用:`waitress-serve --listen=*:8000 wsgi:flask_app`
      - 配置参考：<https://www.cnblogs.com/zyl007/p/14746543.html>
    - 使用启动文件：`python waitress_server.py`
    - 使用配置文件:<https://docs.pylonsproject.org/projects/pastedeploy/en/latest/>
- 使用 Tornado
  - 可以在 Windows 环境下使用
  - 参考：<https://segmentfault.com/a/1190000018117085>
- Zappa
  - 安装：`pipenv install zappa`
  - 官网：
  - 使用参考：<https://mp.weixin.qq.com/s/Yfg163FzIY4kZpeTKoU05w>
    - zappa init
    - 在`zappa_settings.json`中修改基本配置
    - 启动服务：`zappa deploy dev`
- docker
  - 配置`dockerfile`
- Nginx
  - [官网](http://nginx.org/en/docs/)
  - 配置文件参考
    - <https://www.jianshu.com/p/7d79cd1b1301>
    - <https://www.runoob.com/w3cnote/nginx-setup-intro.html>
    - <https://www.jianshu.com/p/aed6b5204225>
    - <https://www.cnblogs.com/sdadx/p/10360208.html>

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

- windows 下作为服务：使用 nssm、winsw 之类的工具

### HTTPS

- [参考](https://juejin.cn/post/6844903665677893640)
- 临时证书
  - 安装依赖项：`pip install pyopenssl`
  - 将`ssl_context ='adhoc'`添加到程序的 `app.run()` 调用中
- 自签名证书
  - 生成自签名证书：`openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
  - 使用这个新的自签名证书：`app.run(ssl_context=('cert.pem', 'key.pem'))`
- 使用真实的证书
  - 免费 CA：<https://letsencrypt.org/>
  - 腾讯云
  - 阿里云
- `flask-sslify`:因为长时间不维护已经不推荐使用
- 直接使用 NGINX 代理即可简单实现

### 域名

- 腾讯云
- 阿里云

### 日志记录

- 使用 logging 模块配合 flask 自带的 app.logger 即可，详细参考 register 中的 logger 模块
- 一般来说错误信息是要发邮件的

### 持续集成(CI)

- Jenkins
- Gitlab-CI 和 Gitlab-runner

## 注意事项

- flask2.0 开始支持异步，蓝图嵌套，快捷路由器装饰等功能，尽量使用新版本，详见：<https://zhuanlan.zhihu.com/p/371659808>
- 使用 pycharm 右键文件夹，可以选择清除 python 编译文件快速清除.pyc 文件（但是不能清除**pycache**文件夹）
  - Linux & MacOS & WSL:`find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`

# 补充

## 其他通用型框架

### Django

- Python 的另一个主流框架
  - 杀手锏功能是后台管理

### Tornado

### web2py

### Bottle

### CherryPy

### Pyramid

### Sanic

## 二次框架

### Eve

- 简介
  - 基于 Flask
  - 官网：<https://github.com/pyeve/eve>

### Connexion

- 简介
  - 基于 Flask
  - 官网：<https://github.com/zalando/connexion>

### APIFlask

- 简介
  - 这是一个基于 flask 的高阶版框架，可以从 flask 几乎无缝迁移
  - 官网：<https://apiflask.com>

### FastAPI

- **_首先必须明确，Flask 和 FastAPI 是不好对比的，具体参考：<https://greyli.com/flask-fastapi/>_**
- 简介
  - 基于`Starlette`
  - 官网：<https://fastapi.tiangolo.com/>
  - 源码：<https://github.com/tiangolo/fastapi>

## 文档更新记录

- 2021-07-11
  - 重构了整个文档结构，增加了大量参考链接
- 2021-07-21
  - 微调了文档的结构
  - 添加了 http 状态码和 restful api 相关的内容
- 2021-07-23
  - 增加了测试部分
  - 完善了项目文档结构说明
  - 注意事项中添加了清除 python 缓存的方法
- 2021-07-28
  - 修改了 celery 的说明使用部分
  - 更新了网页开发资源和模板文件说明
- 2021-07-30
  - 更改了 celery 需要 flask 上下文变量的使用说明
- 2021-08-17
  - 增加了 uwsgi、gunicorn 和 nginx 的内容
- 2021-10-22
  - 完善了项目结构说明
- 2021-11-02
  - 增加 HTTPS 和 api 限制相关的内容
  - 拆分出前端开发文档
- 2021-11-06
  - 增加文档集成的内容
  - 整体修补了一些内容
- 2021-11-16
  - 新开持续集成内容
- 2021-11-18
  - 添加部分 pipenv 内容
- 2021-11-23
  - 添加补充部分，主要是其他框架
