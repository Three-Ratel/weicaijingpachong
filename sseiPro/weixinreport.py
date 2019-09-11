import requests
from lxml import etree

title = '股票提示'
content = '涨幅超过20l'
url = 'http://127.0.0.1:8000/api/v3/wxmonitor/'
page_text = requests.get(url=url,).text
tree = etree.HTML(page_text)
csrfmiddlewaretoken = tree.xpath('/html/body/div/div/div[2]/form/input/@value')[0]
print(csrfmiddlewaretoken)


def weixinapi(title, content):
    requests.post(
        url=url,
        data={
            'title': title,
            'content': content,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }
    )

if __name__ == '__main__':
    weixinapi('dddddd','00023232上涨了5%的幅度,请留意')