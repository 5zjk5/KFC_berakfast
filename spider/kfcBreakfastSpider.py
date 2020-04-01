import requests
import re
import time
import csv
from fake_useragent import UserAgent


def creat_csv():
    '''
    创建 csv 文件
    '''
    heads = ['name','foods','price','img_url']
    with open('kfc.csv','w',encoding='utf8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(heads)


def get_html(url):
    '''
    请求访问 html
    '''
    headers = {
        'User-Agent' : UserAgent().random,
        'Host' : 'www.4008823823.com.cn',
        'Cookie' : 'ga_uuid=unique-test-e4b1db43-63c2-419d-a530-28946b450684; JSESSIONID=LCeXfYu6fuq3watw1qMbxTzs.vm172-18-0-72; userCookieID=1585529853352722; _jzqa=1.1825587236420480000.1585529855.1585529855.1585529855.1; _jzqx=1.1585529855.1585529855.1.jzqsr=4008823823%2Ecom%2Ecn|jzqct=/kfcios/html/index%2Ehtml.-; _qzja=1.1728462617.1585529854958.1585529854958.1585529854958.1585529854958.1585529854958.0.0.0.1.1; _ga=GA1.3.962546873.1585529856; version=online; memcacheKey=24f45ccf-6423-467a-9ab0-cd7401355eca; yum_remember=5685AFB2-5870-488B-A985-85FD295DC760; WT_FPC=id=276ded99e522bf3d9d81585529852997:lv=1585634149731:ss=1585634144570; KLBRSID=495c673cea27288cca196821357f0360|1585634149|1585634143'
    }
    response = requests.get(url,headers=headers)
    return response


def get_url():
    '''
    获取页面中所有早餐页面的 url
    '''
    url = 'https://www.4008823823.com.cn/kfcios/Html/1rmbBreakfast.html'
    response = get_html(url)
    urls = re.findall('href="(https://www\.4008823823\.com\.cn/kfcios/Html/.*?\.html)"',
                      response.text,re.S)
    return urls[12:23]


def get_info(response):
    '''
    提取早餐信息
    '''
    # 餐名
    titles = re.findall('alt="(.*?)"',response.text,re.S)
    # 食物内容
    foods = re.findall('descCn="(.*?)"',response.text,re.S)
    # 价格
    prices = re.findall('price="(.*?)"',response.text,re.S)
    # 图片链接
    img_urls = re.findall('<img src="(.*?)"',response.text,re.S)

    infos = zip(titles,foods,prices,img_urls)

    return list(infos)


def write_to_csv(infos):
    '''
    把信息保存至 csv
    '''
    with open('kfc.csv','a+',encoding='utf8',newline='') as f:
        writer = csv.writer(f)
        for info in infos:
            writer.writerow(info)


if __name__ == '__main__':
    # 创建 csv
    creat_csv()
    # 获得所有早餐页面 url
    urls = get_url()
    # 提取每个页面的早餐信息
    for url in urls:
        response = get_html(url)
        infos = get_info(response)
        write_to_csv(infos)
       