XMiner
==============================================

------------------------------------------------------------------------

## 项目目的

* 为中医药数据分析挖掘建立一个可用的，现代化的web平台

## 项目主要功能

* 基本介绍
* 帮助中心
* 有限制的基础功能试用
* 用户中心
    * 登录注册
        * 注册采用验证码的形式
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

## 项目启动

### 安装虚拟环境
--------------

* 请提前装好python3
* 选择 `pipenv` 进行安装
    * 先安装`pipenv`:`pip install pipenv`
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
        * 创建之后会自动选择虚拟环境的解释器，之后进入终端，进入`dependency`文件夹
            * 直接安装提供的环境：`pip install -r requiremnets.txt`
            * 或者手动安装包 `pip install flask`
    * 使用终端
        * 安装 virtual environment的包（python3.4以下）
            * `pip install virtualenv`
            * python3.4以上自带虚拟环境包，不需要安装，跳过这一步
        * 确定终端进入根目录后，在终端执行`python -m venv venv`
        * 启动和退出虚拟环境
            * 先进入虚拟环境 venv 文件夹（`cd 文件夹名称`）
            * Mac
                * 启动：`source bin/activate`
                * 退出：`deactivate` #这个是全局的命令，任何路径下执行都行
            * Windows
                * 启动：在Scripts文件夹里，使用 `activate` 命令
                * 退出：任意地方使用 `deactivate` 命令
        * 剩下的安装方法同`pycharm`
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

### 安装数据库（只提供思路，具体百度）
------------------------------

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
RATELIMIT_STORAGE_URL='redis://@localhost:6379/3'
CACHE_REDIS_URL='redis://@localhost:6379/4'
# 邮件部分
MAIL_SERVER='smtp.126.com'
# MAIL_PORT=587
MAIL_USERNAME=''
MAIL_PASSWORD=''
MAIL_DEFAULT_SENDER='NJUCM MedInfo'
ADMIN_MAIL=''
HTTP2=0
# 配置域名
DOMAIN_NAME='localhost:5000'
```

* 启动pipenv虚拟环境(千万注意.env文件中不要有中文注释)：`pipenv shell`
    * 这是一个比较方便的方法，因为可能后续有很多命令都要在这个新shell下执行，可以一劳永逸
    * 如果只需要执行一次命令，可以考虑使用`pipenv run 命令`
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
            * 如果有HTTPS:`gunicorn --certfile=<证书文件> --keyfile=<证书密钥文件> -c gunicorn.py wsgi:wsgi_app`
            * 使用`-D`参数可以以守护进程形式来运行Gunicorn进程，其实就是将这个服务放到后台去运行。
        * 查看端口占用情况：`netstat -ntulp |grep 8000`
        * 删除进程：`kill pid`
    * windows环境下
        * 先安装waitress：`pipenv install waitress`
        * 启动：`waitress-serve --listen=*:8000 wsgi:wsgi_app`
            * 或者`python waitress_server.py`(启动之后终端不会有任何提示)
            * 或者`.\run-flaskapp.ps1`
                * 注意：powershell脚本并不能用于nssm安装服务，因为没有加载任何环境变量（除非自己手动设置，但是非常麻烦），所以连python都不会载入进去
        * 永久启动：使用nssm一类的工具
            * 管理员模式启动终端
            * 进入到项目文件夹
            * 添加服务
                * `nssm install xminer "虚拟环境的python路径" ".\waitress_server.py"`
            * 设置参数
                * 设置启动文件夹：`nssm set xminer AppDirectory 绝对路径`
                * 设置开机自启动：`nssm set xminer Start SERVICE_AUTO_START`
                * 设置日志路径：`nssm set xminer AppStdout "...\nssm-log\service.log"`
                * 设置错误日志路径：`nssm set xminer AppStderr "...\nssm-log\service-error.log"`
                    * 日志文件一定要存在
                    * 路径是具体的绝对路径
            * 设置环境变量
                * `nssm set xminer AppEnvironmentExtra 变量名=变量值`
                * 由于一个一个设置环境变量比较麻烦，所以在`wsgi.py`和`app/settings.py`中手动进行了环境变量的载入
                    * 在`app/settings.py`中再次设置是celery的原因
                    * 实际上这个方法不够优雅，导致settings没法分模块，但暂时没找到更完美的解决办法
            * 启动服务：`nssm start xminer`
* 启动redis数据库
    * 配置celery的环境变量，在app/utils/celery_handler/config.py中配置，一般来说默认0、1端口即可
    * 配置验证码和token用的环境变量，暂定使用2端口，和celery的端口区分开
* 启动celery
    * 在`app/utils/celery_handler/config.py`中配置环境变量
    * 启动：`celery -A wsgi:celery worker -l INFO -n xminer_worker`
        * Windows需要使用：`celery -A wsgi:celery worker -l INFO -n xminer_worker -P threads`
        * 似乎`-P gevent`或者`-P eventlet`也能启动，未测试运行效果
    * 最好也添加为服务在后台运行

## 开发

### 开发团队介绍
--------------

* 南京中医药大学人工智能与信息技术学院医学信息工程专业创新工作室
* 南京中医药大学人工智能与信息技术学院医学信息工程专业17级学生21届毕业生diklios
    * @Contact Email:diklios5768@gmail.com
    * @Github:https://github.com/diklios5768

### 开发文档
------------

* [简体中文](docs/index.md)