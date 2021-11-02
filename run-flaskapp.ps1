# 不能使用pipenv shell，这会新建一个终端，后面的命令会全部消失
# 注意：Windows下是Scripts不是bin
# -join转的字符串不带空格，鬼知道为什么Out-String没有用
$pipenvPath=(pipenv --venv) -join "";
& "$pipenvPath\Scripts\activate";
python waitress_server.py;