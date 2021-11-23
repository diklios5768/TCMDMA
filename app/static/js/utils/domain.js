/*
@Date: 2021-11-23 11:11:39
@LastEditTime: 2021-11-23 11:12:24
@LastEditors: diklios
@FilePath: \js\utils\domain.js
@Description: 
@License: MIT
@Author: diklios
@Contact Email: diklios5768@gmail.com
@Github: https://github.com/diklios5768
@Blog: 
@Motto: All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
*/


window.location.protocol + "//" + window.location.host; //   返回https://mp.csdn.net
window.location.host; //返回url 的主机部分，例如：mp.csdn.net
window.location.hostname; //返回mp.csdn.net
window.location.href; //返回整个url字符串(在浏览器中就是完整的地址栏)
window.location.pathname; //返回/a/index.php或者/index.php
window.location.protocol; //返回url 的协议部分，例如： http:，ftp:，maito:等等。
window.location.port //url 的端口部分，如果采用默认的80端口，那么返回值并不是默认的80而是空字符
