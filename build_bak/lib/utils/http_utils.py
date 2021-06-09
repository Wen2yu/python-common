#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" __module_name__ """

__author__ = 'zhangjiawen'

import numpy as np
import random
import requests
import string
import time
from urllib import parse
from urllib.error import URLError, HTTPError

from .date_utils import now
from factory import get_http_pool, remove_http_pool


api_dict = {
    'random_proxies': 'http://127.0.0.1:1040/proxy/api/random_proxies'
}
suc_ip_list = dict()
proxies_stat = dict()


def update_proxies_stat(scheme, host, ip_str, suc_add=0, empty_add=0, fail_add=0, stat_coef=None):
    global proxies_stat
    key = '%s://%s' % (scheme, host)
    if proxies_stat.get(key) is None:
        proxies_stat[key] = dict()
    if not stat_coef:
        stat_coef = [5, 1, -5]
    else:
        stat_coef = [float(i) for i in stat_coef.split('_')]
    level_add = (np.array([suc_add, empty_add, fail_add]) * np.array(stat_coef + [0] * (3 - len(stat_coef)))).sum()
    if not proxies_stat[key].get(ip_str):
        proxies_stat[key][ip_str] = {'suc': suc_add, 'empty': empty_add, 'fail': fail_add, 'level': level_add}
    else:
        proxies_stat[key][ip_str]['suc'] += suc_add
        proxies_stat[key][ip_str]['empty'] += empty_add
        proxies_stat[key][ip_str]['fail'] += fail_add
        if proxies_stat[key][ip_str]['level'] < 50:
            proxies_stat[key][ip_str]['level'] += level_add
    if proxies_stat[key][ip_str]['level'] < -50:
        proxies_stat[key].pop(ip_str)


def get_ip_list(scheme, host, ip_list=None):
    if ip_list is None:
        ip_list = []
    global proxies_stat
    key = '%s://%s' % (scheme, host)
    if not proxies_stat.get(key, dict()):
        if ip_list:
            pass
        proxies_stat[key] = {
            str(ip): {'suc': 0, 'empty': 0, 'fail': 0, 'level': 0} for ip in ip_list
        }
    return [eval(i[0]) for i in sorted(
        proxies_stat.get(key, dict()).items(),
        key=lambda i: i[1].get('level', 0) + random.random(), reverse=True
    )]


def parse_url(url):
    return parse.urlparse(url)


def get_proxies(protocol=None, retries=5):
    proxies = list()
    idx = 0
    while 1:
        try:
            resp = requests.get(api_dict['random_proxies'], protocol=protocol if protocol else '')
            if resp.ok and resp.text:
                proxies = eval(resp.text)
                break
        except ConnectionError:
            pass
        idx += 1
        if idx >= retries:
            break
    return proxies


def get_proxy_url(proxies, protocol=None, retries=5):
    """
    获取代理url
    :param proxies: 代理列表
    :param protocol: http协议
    :param retries:
    :return:
    """
    result = None
    if proxies is None:
        proxies = get_proxies(protocol, retries=retries)
    if protocol:
        proxies = filter(lambda i: i.get(protocol) and parse_url(i[protocol]).netloc not in ['localhost', '127.0.0.1', '0.0.0.0'], proxies)
    if proxies:
        proxy = random.choice(proxies)
        result = proxy.get(protocol, None)
    return result


def update_http_pool(host, protocol, proxy_url, proxies, **kwargs):
    remove_http_pool(host, protocol=protocol, proxy_url=proxy_url)
    proxy_url = get_proxy_url(proxies, protocol=protocol)
    return get_http_pool(host, protocol=protocol, proxy_url=proxy_url, **kwargs)


def req(url: str, method='GET', protocol=None, proxies=None, params=None, app=None, **kwargs):
    """
    处理http请求
    :param url: 请求链接
    :param method: GET/POST
    :param protocol: 请求协议和代理协议
    :param proxies: 代理列表[{'http': 'http://ip:port', 'https': 'https://ip:port'},...]
    :param params: 请求参数
    :param app: 本次调用来源
    :param kwargs: 链接参数
    :return: 响应文本
    """
    result = None
    if url.find('/%') > 0 and params:
        url = '/'.join([params.get(i[1:], '') if i.startswith("%") else i for i in url.split('/')])
    pr = parse_url(url)
    protocol, host = pr.scheme, pr.netloc
    idx, retries = 0, kwargs.get('retries', 0)
    proxy_url = get_proxy_url(proxies, protocol=protocol)
    pool = get_http_pool(host, protocol=protocol, proxy_url=proxy_url, **kwargs)
    while 1:
        try:
            r = pool.urlopen(method, url, **kwargs)
            if r.status == requests.codes.ok:
                result = r.data.decode()
            else:
                if app:
                    app.logger.info('request to %s with %s through %s failed and the status is %d' % (url, params, proxy_url, r.status))
                if 400 <= r.status < 500:
                    pool = update_http_pool(host, protocol, proxy_url, proxies, **kwargs)
                idx += 1
                if idx < retries:
                    continue
            break
        except Exception as e:
            if app:
                app.logger.info('request to %s with %s through %s occurs exception and the reason is %s' % (url, params, proxy_url, e))
            pool = update_http_pool(host, protocol, proxy_url, proxies, **kwargs)
            idx += 1
            if idx < retries:
                continue
            else:
                break
    return result


def req_get(url, params=None, header=None, ip_list=None, **kw):
    kw.update({'url': url, 'params': params, 'headers': header, 'ip_list': ip_list})
    return handle_except(handle_get_req, **kw)


def handle_get_req(**kw):
    return requests.get(kw.pop('url'), kw.pop('params'), headers=kw.pop('headers', None), proxies=kw.pop('proxies'), **kw)


def req_post(url: str, data=None, header=None, ip_list=None, **kw):
    kw.update({'url': url, 'headers': header, 'ip_list': ip_list})
    if data:
        data_obj = eval(data)
        if data_obj.get('id') and data_obj.get('code'):
            kw['json'] = data
    return handle_except(handle_post_req, **kw)


def handle_post_req(**kw):
    return requests.post(**kw)


def req_put(url: str, data=None, header=None, ip_list=None, **kw):
    kw.update({'url': url, 'headers': header, 'ip_list': ip_list})
    return handle_except(handle_put_req, **kw)


def handle_put_req(**kw):
    return requests.put(**kw)


def handle_except(handle, **kw):
    global suc_ip_list
    app = kw.pop('app', None)
    result, err_ip_list = {"req_code": -1}, []
    if not kw.get('url'):
        return result
    if not kw.get('timeout'):
        kw['timeout'] = 6
    max_err_ip = kw.pop('max_err_ip', 5)
    try:
        index, i = 0, 0
        pr = parse_url(kw['url'])
        scheme, host = pr.scheme, pr.netloc
        ip_list = get_ip_list(scheme, host, kw.pop('ip_list', []))
        stat_coef = kw.pop('stat_coef', None)
        while i < len(ip_list):
            sub_ip_list = ip_list[i:i + 5]
            random.shuffle(sub_ip_list)
            for ip in sub_ip_list:
                i += 5
                try:
                    if 0 < max_err_ip <= index:
                        i = len(ip_list)
                        break
                    if ip:
                        kw['proxies'] = ip
                    elif len(ip_list) >= 1 and ip_list[0] and max_err_ip < 0:
                        continue
                    else:
                        kw.pop('proxies', None)
                    if kw.get('headers') and kw.get('handle_header_method'):
                        kw['headers'] = kw.pop('handle_header_method')(kw['headers'])
                    r = handle(**kw)
                    if app:
                        app.logger.info('%s  %s  %d %d %d %s' % (
                            kw.get('url', ''), kw.get('proxies'), index,
                            proxies_stat.get('%s://%s' % (scheme, host), dict()).get(str(ip), dict).get('level', 0),
                            r.status_code, kw.get('params')
                        ))
                    if 200 <= r.status_code < 300:
                        result["req_code"] = 0
                        result["data"] = r.content
                        result.pop("err_msg", None)
                        update_proxies_stat(scheme, host, str(ip), suc_add=1, stat_coef=stat_coef)
                        break
                    else:
                        if r.content:
                            result["req_code"] = 0
                            result["data"] = r.content
                            result.pop("err_msg", None)
                            update_proxies_stat(scheme, host, str(ip), suc_add=1, stat_coef=stat_coef)
                            break
                        result["req_code"] = -98
                        result["err_msg"] = '请求返回不成功: %d %s' % (r.status_code, kw.get('url', ''))
                        update_proxies_stat(scheme, host, str(ip), fail_add=1, stat_coef=stat_coef)
                except Exception as ip_e:
                    update_proxies_stat(scheme, host, str(ip), fail_add=2, stat_coef=stat_coef)
                    result["req_code"] = -1
                    result["err_msg"] = ip_e
                    # print(ip_e)
                finally:
                    index += 1
                    if result["req_code"] == 0:
                        i = len(ip_list)
                    # time.sleep(random.choice(range(3, 10)))
    except HTTPError as h_e:
        result["req_code"] = -2
        result["err_msg"] = h_e.reason
    except URLError as u_e:
        result["req_code"] = -3
        result["err_msg"] = u_e.reason
    except Exception as e:
        result["req_code"] = -99
        result["err_msg"] = e
    finally:
        if err_ip_list:
            result['err_ip_list'] = err_ip_list
    if result["req_code"] == 0:
        if app:
            app.logger.info(result)
        else:
            print({k: str(v, 'utf-8') if type(v) == bytes else v for k, v in result.items()})
    return result
