# -*- coding: utf-8 -*-
# Created : 2022/8/5
# author ：sjtuys

import urllib.parse

import pymongo
import requests
import time
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json

num = 0

# qE1 = {'碳排放','温室气体','排放'}
# qE2 = {'污染','废物','废物排放'}
# qE3 = {'水资源','土地多样性','生物多样性','持续性'}
# qE4 = {'环境管理','绿色金融','环境风险','绿色信贷','绿色创新','绿色专利'}
# qE5 = {'环境机遇','可再生','清洁','绿色'}
#
# qS1 = {'员工','福利','雇佣','劳动力','供应链','经营持续性','客户','消费者','信息安全','产品质量','信息泄露'}
# qS2 = {'责任管理','制度安排'}
# qS3 = {'慈善','捐赠','抗疫','就业','税收','贡献','扶贫','共同富裕'}
#
# qG1 = {'股东','治理'}
# qG2 = {'机构设置','机构运作','董监事'}
# qG3 = {'管理层','管理不当'}
# qG4 = {'信息披露','披露'}
# qG5 = {'治理异常','监管处罚','法律诉讼'}
# qG6 = {'财务风险','财务质量'}

queryWord = ['碳排放','温室气体','排放','污染','废物','废物排放','水资源','土地多样性','生物多样性','持续性','环境管理','绿色金融','环境风险','绿色信贷','绿色创新','绿色专利','环境机遇','可再生','清洁','绿色','员工','福利','雇佣','劳动力','供应链','经营持续性','客户','消费者','信息安全','产品质量','信息泄露','责任管理','制度安排','慈善','捐赠','抗疫','就业','税收','贡献','扶贫','共同富裕','股东','治理','机构设置','机构运作','董监事','管理层','管理不当','治理异常','监管处罚','法律诉讼','财务风险','财务质量']

saveIndex = ['.\\E\\气候变化\\','.\\E\\气候变化\\','.\\E\\气候变化\\','.\\E\\污染与废物\\','.\\E\\污染与废物\\','.\\E\\污染与废物\\','.\\E\\自然资源\\','.\\E\\自然资源\\','.\\E\\自然资源\\','.\\E\\自然资源\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境管理\\','.\\E\\环境机遇\\','.\\E\\环境机遇\\','.\\E\\环境机遇\\','.\\E\\环境机遇\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\利益相关方\\','.\\S\\责任管理\\','.\\S\\责任管理\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\S\\社会机遇\\','.\\G\\股东治理\\','.\\G\\股东治理\\','.\\G\\治理结构\\','.\\G\\治理结构\\','.\\G\\治理结构\\','.\\G\\管理层\\','.\\G\\管理层\\','.\\G\\信息披露\\','.\\G\\信息披露\\','.\\G\\公司治理异常\\','.\\G\\公司治理异常\\','.\\G\\公司治理异常\\','.\\G\\管理运营\\','.\\G\\管理运营\\']

class Xueqiuspider:
    def __init__(self):
        #An example of the start _url:https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol=SH600519&hl=0&source=all&sort=time&page=1&q=%E7%A2%B3%E6%8E%92%E6%94%BE&type=11
        self.start_url = 'https://xueqiu.com/stock/cata/stocklist.json?page={page}&size=90&order=desc&orderby=percent&type=11%2C12&_={real_time}'  # 股票列表网
        #每页爬取90个股票代码
        a = time.time()
        real_time = str(a).replace('.', '')[0:-1]
        '''访问雪球股票评论时的时间参数，不加也可以正常返回，但是为了保险还是加上时间参数'''

        self.headers = {
            "Host": "xueqiu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
            "Referer": "https://xueqiu.com/hq",
            "Cookie": 'device_id=2ac5f4e2dbe4ef69cfa8fd2625c5f44c; s=dw11sw4w35; bid=03cc3ef57f4fbbcbfc0acda517a52431_l59jgqqh; __utma=1.1437834222.1657108248.1657108248.1657108248.1; __utmz=1.1657108248.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_is_login=1; u=1776094685; xq_a_token=90c85b0bc5c24f4b065d6f93f6b211e194eba394; xqat=90c85b0bc5c24f4b065d6f93f6b211e194eba394; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjE3NzYwOTQ2ODUsImlzcyI6InVjIiwiZXhwIjoxNjYxMDc0NDE1LCJjdG0iOjE2NTg0ODI0MTU5NzcsImNpZCI6ImQ5ZDBuNEFadXAifQ.aFBoIut1VOZg0R7p56TCKonvl0soY0Y1LrOiNkcYJR75pv-BTh7XMWY1reu7Wb-x6QW1qmPOtFoa9pOS1RpQGDAJMR3jhYQP4jpl1pZFmabJwSkak3IFBoqnL0E_yD0_pQB-nkavhDcTiN8ykg3ruXYOYotc5qSbGPaVCQo6pyRBuzi1xmmyLJjOuto7NnL2LoT-sh0H6voRkK1hQ5Wze2TzZn3s5a0TPn8SdlA_Idk0ADTp9kggsJDRdjkadecnhhoRPSUVa7TBp4M_Z_nMBcZmMsAEpQhFEAPVTTplQKzgGu-bAQi4dBsYgsZL2dJ-mbKwnw4WQyeGgvLrG6_2kg; xq_r_token=3f9455acf1faf81fecd98f975f59a5f0daf50727; Hm_lvt_1db88642e346389874251b5a1eded6e3=1657170073,1658218587,1659446255,1659519589; acw_tc=2760827916595864793066940ec59266af007a7f2a5b3506597f0decfd91fd; is_overseas=0',
        }

    def parse(self):
        # for i in range(100):#在全站爬虫中爬取评论数据时取消本行代码注释，将下一行注释
        for i in range(1):#在Demo中只爬取90个股票代码
            a = time.time()
            real_time = str(a).replace('.', '')[0:-1]
            response = requests.get(self.start_url.format(page=str(i+1),real_time=real_time), headers=self.headers, verify=False)
            count_all = response.json()['count']['count']
            if i * 90 < count_all:
                time.sleep(5)
                response = requests.get(self.start_url.format(page=str(i+1),real_time=real_time), headers=self.headers, verify=False)
                res_list = response.json()['stocks']
                yield res_list
            else:
                break

    def parse_all_url(self, res):
        symbol = res['symbol']
        count = 100
        for p in range(53):
            q = urllib.parse.quote(queryWord[p])
            #An example of the detail_url:https://xueqiu.com/query/v1/symbol/search/status.json?count=10&comment=0&symbol=SH600519&hl=0&source=all&sort=time&page=1&q=%E7%BB%BF%E8%89%B2%E9%87%91%E8%9E%8D&type=11
            for i in range(100):
                detail_url = "https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={}&hl=0&source=user&sort=time&page={}&q={}&type=11".format(
                    symbol, i + 1,q)
                print(detail_url)

                #try:
                content_list, count = self.parse_comment_url(detail_url,p,symbol)
                time.sleep(random.random())
                # 不设置delay爬到三万条数据时IP会被封掉，因此设置一个随机数delay
                if count == 0:
                    break
                #except Exception as e:
                    # print("Error:", e)
                    # time.sleep(0.5)
                    # content_list = self.parse_comment_url(detail_url,p,symbol)
                    # time.sleep(0.5)
                self.save_file(content_list)

    def parse_comment_url(self, url, p,symbol):
        response = requests.get(url, headers=self.headers, verify=False)
        res_list = response.json()['list']
        count = response.json()['count']

        content_list = []
        for res in res_list:
            global num
            num += 1
            item = {}
            item['num'] = num
            item['url'] = 'https://xueqiu.com' + str(res['target'])
            item['股票代码'] = symbol
            item['关键词'] = queryWord[p]
            item['comment_id'] = res['id']
            item['comment_title'] = res['title']
            item["from:"] = url
            #item['comment_text'] = res['text']
            #An example of the detail pages:https://xueqiu.com/6639666687/177799719
            content_list.append(item)
            res['url'] = item['url']
            fileName = saveIndex[p]+symbol+'ID'+str(item['comment_id'])+'.json'
            with open(fileName, 'a') as f:
                f.write(str(res).encode("gbk", 'ignore').decode("gbk", "ignore"))
                f.write("\n")
        return content_list, count

    def save_file(self, content_list):
        for content in content_list:
            with open('sum.json', 'a') as f:
                f.write(str(content).encode("gbk", 'ignore').decode("gbk", "ignore"))
                f.write("\n")

    def run(self):
        for res_list in self.parse():
            for res in res_list:
                self.parse_all_url(res)


if __name__ == '__main__':
    xueqiu = Xueqiuspider()
    xueqiu.run()