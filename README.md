# 项目说明

## 项目目的

* 为中医药数据分析挖掘建立一个可用的，现代化的web平台

## 项目主要功能

* 基本介绍
* 帮助中心
* 有限制的基础功能试用
* 用户中心
    * 登录注册
        * 登录状态管理
    * 项目管理
    * 数据集管理
    * 分析数据管理
        * 在线分析数据查看
        * 完整的分析报告（包括PDF、Excel文件、CSV文件）
    * 能够使用的算法
        * 同质关联分析
        * 骨干网挖掘
        * 社团发现（louvain、cliques、onion_layer）

## 安装虚拟环境

* 请提前装好python3
* 选择 `pipenv` 进行安装
    * 先安装`pipenv`:`pip install pipenv`
    * **根据系统中使用的python版本的不同，请先修改`Pipfile`文件中最后一行python的版本**
    * 使用IDE
        * 设置->项目->python解释器->在三个点点处点击添加->在左边选择使用 pipenv *新建虚拟环境*
        * pipenv会自动选择根目录下的pipenv和pipenv.lock下载需要的库
        * 有的老版本的IDE可能不支持pipenv创建，可以自己安装pipenv在终端使用，或者换用 `virtual environment` 的方法
    * 使用终端
        * 生产环境：`pipenv install`
        * 开发环境：`pipenv install -d`
* 使用 `virtual environment` 进行安装
    * 使用`Pycharm`
        * 设置->项目->python解释器->在三个点点处点击添加->在左边选择使用 virtual environment *新建虚拟环境*
        * 创建之后会自动选择虚拟环境的解释器，之后进入终端执行
            * `pip install -r requiremnets.txt`
            * 或者手动安装包 `pip install flask`
    * 使用终端
        * 需要安装 virtual environment的包
            * `pip install virtualenv`
        * 确定终端进入根目录后，在终端执行`python -m venv venv`
        * 启动和退出虚拟环境
            * 先进入虚拟环境 venv 文件夹（`cd 文件夹名称`）
            * Mac
                * 启动：`source bin/activate`
                * 退出：`deactivate` #这个是全局的命令，任何路径下执行都行
            * Windows
                * 启动：在Scripts文件夹里，使用 `activate` 命令
                * 退出：任意地方使用 `deactivate` 命令
        * 如果后续更换了 `pycharm`
            * 设置->项目->python解释器->在三个点点处点击添加->在左边选择使用`virtual environment`->*添加已经存在的虚拟环境*
* 有可能遇到的问题
    * 安装的时候找不到包或者对应版本
        * 如果未换源的话大概率是网络问题
            * 可以在终端代理后用命令行安装
            * 可以先在根环境下安装之后，在安装虚拟环境的时候会从根环境调用包过来
        * 如果换源之后就确实有可能这个包找不到了，具体可能是撤回或者小版本
            * 建议直接安装最新版或者手动安装一些其他的老版本
            * 然后在requirements.txt文件中删除对应的一行
            * pipenv由于现在未配置，大多数都是默认安装最新的版本
    * 安装失败
        * 先查看pip和setuptools的版本是不是最新的
        * 如果pip是最新的，需要vc++说明是c编译的包，可以装visual studio
            * 如果不想装那么大的visual studio，可以安装windows10的SDK和2015版本的c++生成工具
            * 还不想装，那就去[这个网站](http://www.lfd.uci.edu/~gohlke/pythonlibs/)找对应python和操作系统版本的whl文件手动安装
                * 下载后到对应的文件夹输入命令：`pip install ***.whl`，卸载将`install`改为`uninstall`
        * 还有一种可能是包卸载不干净，最简单方法就是直接删除环境重新创建
            * 老版本的pycharm可能装的pip包比较老，更新的pip后指向不对，但是可以用，建议安装后应该直接删除老版本文件，再次重新执行更新pip的命令
            * 不想操作的建议直接更新最新版本的pycharm
    * 源码编译方法
        * 有一些包不需要vc++，但是也不在pypi官网上发布，就需要自己手动安装
        * 先进入下载下来的包的文件夹：`python setup.py install`

## 项目启动

### 安装数据库（只提供思路，具体百度）

* MySQL
    * Windows
        * 直接下载安装包安装
        * scoop
        * docker+wsl2
    * Linux
        * 根据版本使用相应的包管理工具
        * 尽量不要使用centos（尤其是7之前）了，不支持了
        * 如果实在不会安装使用宝塔面板
* redis
    * Windows
        * 由于官方不支持，所以得用微软提供的windows版本，注意版本号最高是3
        * scoop：同样是Linux版本
        * docker+wsl2：推荐，这个是Linux版本
    * Linux：同装MySQL的方法
* 配置.env环境变量

```dotenv
# 示例，在真实的生产环境中请不要加中文注释，因为pipenv的gbk问题至今未解决
# 存储包含敏感信息的环境变量，不提交到git仓库
# 注意：secret key需要使用特定的方法生成，具体见app/settings文件中的注释
SECRET_KEY='35JN7GFaUFNeriObUj93bQpavYWsGPOp6I4BDoe-U6Q'
CRYPTOGRAPHY_SECRET_KEY='hCfDE7XTwY8DAgkmVT9H8fYdWHXyM_Nqo468OCCU9HY='
SECURITY_PASSWORD_SALT='120426439174435924094353414614255850770'
# MySQL数据库URL
# 格式为 SQLALCHEMY_DATABASE_URI='mysql+pymysql://username:password@host:port/databasename'
SQLALCHEMY_DATABASE_URI='mysql+pymysql://username:password@host:port/databasename'
# redis数据库URL
REDIS_URL = 'redis://@localhost:6379/2'
# 邮件部分
MAIL_SERVER='smtp.126.com'
# MAIL_PORT=587
MAIL_USERNAME=''
MAIL_PASSWORD=''
MAIL_DEFAULT_SENDER='NJUCM MedInfo'
# 配置域名和https
HTTPS=0
HTTP2=0
DOMAIN_NAME='localhost:5000'
```

* 启动pipenv虚拟环境(千万注意.env文件中不要有中文注释)：`pipenv shell`
* 启动MySQL并初始化
    * **记得需要配置环境变量**
        * 提醒：如果密码中含有特殊字符，请手动配置`app/setting.py`文件，使用URL编码进行处理
    * 在终端初始化数据库表：`flask db-init`
    * 初始化表数据：`flask data-init`
        * 输入`p`或者`production`代表生产环境
        * 输入`d`或者`development`代表开发环境
* 启动flask
    * 注意，`Pipfile`中也提供了相应的包，可以根据系统取消相应的注释再重新安装环境
    * 类Unix环境下
        * 先安装gunicorn：`pipenv install gunicorn`
        * 启动：`gunicorn -c gunicorn.py wsgi:wsgi_app`
        * 使用`-D`参数可以以守护进程形式来运行Gunicorn进程，其实就是将这个服务放到后台去运行。
        * 查看端口占用情况：`netstat -ntulp |grep 8000`
        * 删除进程：`kill pid`
    * windows环境下
        * 先安装waitress：`pipenv install waitress`
        * 启动：`waitress-serve --listen=*:8000 wsgi:wsgi_app`
            * 或者`python .\waitress_server.py`(启动之后终端不会有任何提示)
        * 永久启动：使用nssm一类的工具
            * 注意设置一些参数，最重要的项目启动文件夹和开机自启动
            *
          添加服务，如：`nssm install xminer "C:/Users/Administrator/.virtualenvs/TCMDMA-xHTHL4l7/Scripts/python.exe" "waitress_server.py"`
            * 启动服务：`nssm start xminer`
* 启动redis数据库
    * 配置celery的环境变量，在app/utils/celery_handler/config.py中配置，一般来说默认0、1端口即可
    * 配置验证码和token用的环境变量，暂定使用2端口，和celery的端口区分开
* 启动celery
    * 在`app/utils/celery_handler/config.py`中配置环境变量
    * 启动：`celery -A wsgi:celery worker -l INFO`
        * Windows需要使用：`celery -A wsgi:celery worker -l INFO -P threads`

## 版本变动

* v1.0:2021-08-06
    * 使用reportlab完美的完成了PDF的生成，并封装了大量函数和样式
    * 使用token的方式重构了用户登录机制，并支持多种客户端
        * 使用基于WTForms的多种客户端，多种注册登录方式
    * 重构了数据库和相应的调用函数
    * 基于restful API规范重构了项目的api
        * 使用了flask2.0版本的蓝图嵌套机制和http请求方法接口
    * 构建了基于scope的权限管理方式
    * 规范了后端错误返回格式
    * 构建了基于新的登录方式的前端网站，为原本不存在用户功能的网站增加用户级别的功能
    * 增加了gunicorn配置文件，方便部署
    * 重写了表格文件读取和生成的代码加强了整体的功能
    * 使用celery完成异步任务，能够分析并生成报告，发送邮件
    * 增加了新的算法：
        * louvain
        * backboning
        * 最大团
        * 洋葱皮
* v1.1:2021-09-15
    * 优化了平台名称，页脚
    * 优化邮箱发送内容，更改发送邮箱和名称
    * 删除遗留的项目修改弹窗中的无用部分
    * 修改算法名称，增加算法介绍
    * 优化项目卡片展示
    * 修复项目查询功能
    * 改进PDF封面显示和目录标题
    * 增加分享和下载报告的功能
    * 优化新建分析中选择方法展示效果
* v1.2:2021-10-03
    * 修复cliques方法的超出索引问题
    * 修复关联分析默认值太小导致分析太慢的问题
    * 优化快速生成数据库的命令
    * 增加和完善快速导入和更新数据的命令
* v1.3:2021-10-9
    * 优化包导入，去除不必要的包
    * 去除不必要的文件
    * 完善前端页面中项目描述和方法部分超出卡片的问题
    * 完善前端页面中表格显示行序号的问题，并优化说明部分
    * 修复数据集名称不输入但是会跳转的问题
    * 修复方法介绍页面，文字太多导致的卡片高度不一问题
    * 增加帮助页面锚点定位方法
    * 增加默认选择第一个算法
    * 增加全选和取消全选按钮
    * 增加帮助页面的算法参数设置介绍，并修改相应的后端
    * 网络图展示界面方法名称修复
* v1.4:2021-10-16
    * 增加加密和解密字符串工具
    * 增加给用户发邮件验证通过的模板、和验证接口
    * 优化gunicorn配置文件
    * 增加和更新大量管理员页面需要的接口部分
    * 增加停止项目分析接口
    * 增加更改密码接口
    * 增加用户权限等级
    * 增加和优化时间处理工具函数
    * 优化后端表单验证用户名部分逻辑
    * 更新.gitignore文件内容
* v1.5:2021-10-22
    * 登录时返回的用户信息增加是否是管理员
    * 更新权限等级定义和相应的初始化数据库数据函数
    * 优化方法更新函数，兼容新方法的加入
    * 增加链接解析错误提示
    * 数据库基类增加json_remarks字段
    * 增加中文转url编码的工具方法
    * 更改解析加密字符获得文件的方法
    * 增加测试文件夹、测试数据、测试数据库、测试用文件
    * 在app中增加并注册redis数据库
    * 增加验证码功能：生成、发邮件、验证、过期删除
    * 增加注册和验证验证码相应接口
* v1.6:2021-10-23
    * 增加使用redis存储禁用token功能
    * 增加退出登录接口时禁用token的逻辑
    * 增加token验证的时候判断是否被禁用的逻辑
    * 增加了用户token验证时候的账户是否被停用和通过功能，并增加相应错误定义和文档
    * 优化生成初始数据函数中的权限查询和用户通过
    * 完善了通过celery按时清除验证码和禁用token的功能

## 后续优化改进

### 后端优化计划

* 预计v2.0实现
    * 用户注册改为默认活跃、未通过，并修改登录验证机制，没有通过和是否被禁用的账户不能登录
    * 管理员界面，管理员功能：用户管理（仅修改邮箱、密码、通过、删除）、用户数据集管理（仅查看、删除）、项目管理（仅查看、删除）
* celery
    * 停止算法运行
    * 重跑算法（注意删除之前的文件）
    * 超过规定小时的算法自动停止

### 前端优化计划

* 增加邮箱验证码进行验证的功能
* 由于开发失误，可以将getInitState方法进行判断优化，并在组件中使用refresh方法代替现在的一大长段重复代码
* 修改邮箱、手机和密码的功能

### 被搁置的计划（接手的人有兴趣做一下）

* 超级管理员api添加、scope设置和界面
* 手机验证码（暂时不需要，用的话阿里的即可，但是要钱，而且要修改一下验证码的生成、查询、验证方式，区分邮件和手机验证码）
* docker部署
* 使用ASGI
* 单元测试（浩大的工程）
* 前端MockJS测试（因为是前后端一起开发，直接代理就可以了）
* NGINX反向代理和gzip压缩

### 一些想法

* 有空把api里面的sun全部换成tcm
* 增加和定义新的客户端类型
* 处理字符串的部分，即text_handler是否应该放在file_handler中，现在想来应该独立出来，但是调用的地方比较多，不是很想移动位置
* 使用`apiflask`重新封装（也不一定，现在是flask2.0了，不少功能都有了）

## 开发团队介绍

* 南京中医药大学人工智能与信息技术学院医学信息工程专业创新工作室
* 南京中医药大学人工智能与信息技术学院医学信息工程专业17级学生21届毕业生diklios
    * @Contact Email:diklios5768@gmail.com
    * @Github:https://github.com/diklios5768

# 文档更新记录

* 更新时间：2021-07-11
    * 重构了文档结构
    * 拆分了code和development两个文档到docs
    * 增加了开发团队介绍
* 更新时间：2021-07-21
    * 增加了项目功能说明
    * 增加了v1.0版本变动说明
* 更新时间：2021-07-28
    * 增加了celery和部署说明
* 更新时间：2021-07-30
    * 更改了celery启动命令
* 更新时间：2021-08-18
    * 增加了项目目的和算法部分
    * 更新了生产环境启动说明，去除掉了开发版说明
* 更新时间：2021-09-15
    * 增加了v1.1版本更新说明
* 更新时间：2021-10-03
    * 增加了pipenv安装时候的需要注意python版本的提示
* 更新时间：2021-10-22
    * 增加开发文档
    * 增加code文档
    * 增加安装数据库的说明
    * 完善开发计划内容
    * 优化完善v1.5及之前版本的开发内容