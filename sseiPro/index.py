import requests
import json
#from sseiPro.weixinreport import weixinapi


# url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=1992&season=1'
from weixinreport import weixinapi

url = 'http://api.money.126.net/data/feed/0000001,0600684,UD_SHAZ,UD_SHAD,UD_SHAP,money.api?callback=_ntes_quote_callback95356349'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Cookie': 'UM_distinctid=16cbea6f0d7b-0af3a5e5640507-6353160-ff000-16cbea6f0d931b; _ntes_nnid=03360db13a04b3b3238be6a3559aadff,1566566709940; vinfo_n_f_l_n3=4a3ed6f35b3a2116.1.0.1566566709987.0.1566566828711; vjuids=-a5e0e64c8.16cff6cf2b0.0.a88d61b579fe8; _ntes_nuid=03360db13a04b3b3238be6a3559aadff; vjlast=1567653426.1567857015.13'
    # 'Cookie'':'UM_distinctid=16cbea6f0d7b-0af3a5e5640507-6353160-ff000-16cbea6f0d931b; _ntes_nnid=03360db13a04b3b3238be6a3559aadff,1566566709940; vjuids=-a5e0e64c8.16cff6cf2b0.0.a88d61b579fe8; _ntes_nuid=03360db13a04b3b3238be6a3559aadff; vjlast=1567653426.1567857015.13; ne_analysis_trace_id=1567861883820; s_n_f_l_n3=4a3ed6f35b3a21161567861883828; vinfo_n_f_l_n3=4a3ed6f35b3a2116.1.1.1566566709987.1566566828711.1567862082945'
}
params = {
    'year': '1992',
    'season': '1',
    'callback': '_ntes_quote_callback95356349'select本质上是通过设置或者检查存放fd标志位的数据结构来进行下一步处理。
这样所带来的缺点是：

1
单个进程可监视的fd数量被限制

2
需要维护一个用来存放大量fd的数据结构，这样会使得用户空间和内核空间在传递该结构时复制开销大

3
对socket进行扫描时是线性扫描

poll本质上和select没有区别，它将用户传入的数组拷贝到内核空间，然后查询每个fd对应的设备状态，如果设备就绪则在设备等待队列中加入一项并继续遍历，

如果遍历完所有fd后没有发现就绪设备，则挂起当前进程，直到设备就绪或者主动超时，被唤醒后它又要再次遍历fd。这个过程经历了多次无谓的遍历。

它没有最大连接数的限制，原因是它是基于链表来存储的，但是同样有一个缺点：大量的fd的数组被整体复制于用户态和内核地址空间之间，而不管这样的复制是不是有意义。

poll还有一个特点是“水平触发”，如果报告了fd后，没有被处理，那么下次poll时会再次报告该fd。

epoll支持水平触发和边缘触发，最大的特点在于边缘触发，它只告诉进程哪些fd刚刚变为就需态，并且只会通知一次。

在前面说到的复制问题上，epoll使用mmap减少复制开销。

还有一个特点是，epoll使用“事件”的就绪通知方式，通过epoll_ctl注册fd，一旦该fd就绪，内核就会采用类似callback的回调机制来激活该fd，
epoll_wait便可以收到通知

}
s_list = [0]
while True:
    session = requests.Session()
    page_text = session.get(url=url, params=params, headers=headers)
    rest = page_text.text.split('(', maxsplit=1)[1].rsplit(')', maxsplit=1)[0]

    rest = json.loads(rest)

    code = '0000001'
    szzs = rest[code].get('price')
    percent = rest[code].get('percent')
    updown = rest[code].get('updown')
    open = rest[code].get('open')
    yestclose = rest[code].get('yestclose')
    high = rest[code].get('high')
    low = rest[code].get('low')


    while szzs != s_list[0]:
        s_list.pop()
        if szzs < 2883.68:
            weixinapi('上证指数', '上证指数低于2883.68')
            weixinapi('上证指数', '上证指数为{}'.format(szzs, ))
        if szzs > 3000.00:
            weixinapi('上证指数', '上证指数高于3000.00')
            weixinapi('上证指数', '上证指数为{}'.format(szzs, ))
        if updown > 8:
            weixinapi('涨额', '涨额超过8')
        if updown < -5:
            weixinapi('跌额', '跌额超过5')
        if percent > 0.0025:
            weixinapi('涨幅', '涨幅超过1/4')
        if percent < -0.0025:
            weixinapi('跌幅', '跌幅超过1/4')

        s_list.append(szzs)
        print(szzs, s_list[0])



