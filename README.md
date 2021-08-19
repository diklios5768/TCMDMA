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

* 选择 `pipenv` 进行安装
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
            * 设置->项目->python解释器->在三个点点处点击添加->在左边选择使用 virtual environment *添加已经存在的虚拟环境*
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

* 先配置.env环境变量

```dotenv
# 示例，在真实的生产环境中请不要加中文注释，因为pipenv的gbk问题至今未解决
# 存储包含敏感信息的环境变量，不提交到git仓库
SECRET_KEY='35JN7GFaUFNeriObUj93bQpavYWsGPOp6I4BDoe-U6Q'
SECURITY_PASSWORD_SALT='120426439174435924094353414614255850770'
# MySQL数据库URL
# 格式为DATABASE_URL='mysql+pymysql://username:password@host/databasename'
DATABASE_URL='mysql+pymysql://username:password@host/databasename'
REDIS_URL = 'redis://@localhost:6379/0'
# 邮件部分
MAIL_SERVER='smtp.126.com'
# MAIL_PORT=587
MAIL_USERNAME=''
MAIL_PASSWORD=''
MAIL_DEFAULT_SENDER='diklios'
```

* 启动pipenv虚拟环境(千万注意.env文件中不要有中文注释)：`pipenv shell`
* 启动MySQL并初始化
    * 记得需要配置环境变量
        * 提醒：如果密码中含有特殊字符，请手动配置`app/setting.py`文件，使用URL编码进行处理
    * 在终端初始化数据库表：`flask db-init`
    * 初始化表数据：`flask data-init`
* 启动flask
    * 类Unix环境下
        * 先安装gunicorn：`pipenv install gunicorn`
        * 启动：`gunicorn -c gunicorn.py wsgi:wsgi_app`
    * windows环境下
        * 先安装waitress：`pipenv install waitress`
        * 启动：`waitress-serve --listen=*:8000 wsgi:wsgi_app`
        * 永久启动：使用nssm一类的工具
            * 如：`nssm install tcmdma "C:\Users\Administrator\.virtualenvs\TCMDMA-xHTHL4l7\Scripts\python.exe" "C:\Users\Administrator\TCMDMA\waitress_server.py"`
* redis数据库，并配置celery的环境变量（注意是celery的环境变量，在app/utils/celery_handler/config.py中配置）
* celery
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

## 后续优化改进

* 验证码
    * 手机和邮箱验证码
* 手动禁用的token存redis里面，优化token验证机制
* 后续可能使用`apiflask`重新封装一下
* cos对象存储
* 管理员界面，管理员功能
* docker部署
* celery定期清除
    * 验证码，缓存文件，保存的无效token

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