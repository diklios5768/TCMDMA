# 交接文档

## 项目简介

- [中医药数据分析与挖掘平台 XMiner]
- 本项目主要工作是中医临床数据的分析挖掘
  - 工作的主要流程是上传数据->选择算法->设置参数->获得分析结果，分析结果和展示形式是多样化的

## 平台使用

### 技能要求

- 前端
  - NodeJS
    - npm
    - yarn
  - Webpack
  - ES6
  - TypeScript
- 后端
  - Python
  - Git
  - Linux
  - HTTP

### 基础依赖

- 未标注版本的使用最新版即可，但是还是推荐使用 requirements.txt 文件中的版本
- 前端
  - NodeJS15 以上
  - React17
  - Ant Design4 以上
    - Ant Design Pro
    - umi
    - dva
    - AntV
  - webpack5
- 后端
  - 推荐 python3.7 以上
  - flask==2.0
    - flask-sqlalchemy
      - pymysql
      - sqlalchemy==1.3.23
    - flask-login
    - flask-mail
    - flask-cors
    - flask-migrate
  - PDF
    - pdfplumber
    - reportlab
    - fpdf2
  - Excel
    - xlrd
    - openpyxl
  - 算法
    - numpy
    - pandas
    - matplotlib
    - networkx
    - tqdm
    - node2vec==0.4.1
    - gensim==3.8.3
    - efficient-apriori
    - pypinyin
  - 数据库
    - mysql5.7 以上
    - sqlite3 以上

### 使用方法

- 前端
  - 不推荐使用 npm
  - 终端输入 `yarn` 安装环境
  - 安装完成后输入`yarn start`即可运行出网页
- 后端
  - 安装环境
    - 使用 pipenv
      - 先安装 pipenv：`pip install pipenv`
      - 在后端项目文件夹目录下输入：`pipenv install --dev`
    - 或者使用 pip：`pip install -r requirements.txt`
  - 激活虚拟环境
  - 运行：`flask run`或者`python wsgi.py`

## 注意事项

1. 前端目前和后端通信的 http 请求是写死的，需要进行优化
2. 登录和用户管理模块缺失，需要完善添加事情
3. 项目部署，比如使用 gunicorn、docker，建议在后续添加上去
4. 异质关联分析需要重写封装，具体算法参考于婧学姐的论文
5. 生成 PDF 需要修改一下源码，否则标题部分渲染会出现错误
   - 具体是注释掉 fpdf2 模块的 syntax.py 文件中的第 165 行
     - `# appender(create_dictionary_string(obj_dict, open_dict="", close_dict=""))`
6. 请注意 jQuery 的 ajax，原生 fetch API，form 表单，文件提交的区别，这需要调用 request 模块不同的方法，这里经常性的犯错
7. 请务必在编写代码的时候添加异常处理，防止程序出现错误而停止运行
8. 对于 typescript 的警告可以使用 any 类型，不必要强求类型定义

## 后续联系方式

- QQ：1061995104

- 邮箱：yzsxsunhj@126.com

## 文档更新记录

- 2021-11-09
  - 使用毕业论文的交接文档先顶着，后续交接的时候会大更新
