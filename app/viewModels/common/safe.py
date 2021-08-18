from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for


def is_safe_url(target):
    ref_url = urlparse(request.host_url)  # 获取程序内的主机url
    test_url = urlparse(urljoin(request.host_url, target))  # 将目标URl转换为绝对路径
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc  # 验证是否属于内部url


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
