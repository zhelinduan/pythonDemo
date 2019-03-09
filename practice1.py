import requests
from lxml import etree
import time
import re
#引用正则表达式

url="https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    #refer表明该请求的上一个请求来自哪里
        'Referer':'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=py',
        'Cookie':'_ga=GA1.2.587619178.1542982719; LGUID=20181123221838-abf4ee0e-ef2a-11e8-b8c4-525400f775ce; user_trace_token=20181123221838-ef5a60ce-4f8d-431c-9578-6b476f5675a7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221675d786bd4819-0ab2b7c5952906-35607401-1296000-1675d786bd53cc%22%2C%22%24device_id%22%3A%221675d786bd4819-0ab2b7c5952906-35607401-1296000-1675d786bd53cc%22%7D; JSESSIONID=ABAAABAAAIAACBIADF650A78EE4231894E83F503808316C; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545628905; _gid=GA1.2.239938662.1546480937; index_location_city=%E5%85%A8%E5%9B%BD; SEARCH_ID=ef580eb62d8d44819dbc5e2f0a50dbb4; TG-TRACK-CODE=search_code; LGSID=20190103110125-dbe3d87e-0f03-11e9-bae2-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3Dsug%26fromSearch%3Dtrue%26suginput%3Dpy; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5438213.html; LGRID=20190103110939-023cc649-0f05-11e9-bae7-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546484973'
}
def request_list_page():
    data={
        'first':'false',
        'pn':2,
        'kd':'python'
    }
    for x in range(1,14):
        data['pn']=x
        response=requests.post(url=url,headers=headers,data=data)
        #json方法：如果返回来的是json数据，那么这个方法会自动load的成字典
        result=response.json()
        #获取职位id
        positions=result['content']['positionResult']['result']
        for position in positions:
            positionId=position['positionId']
            position_url='https://www.lagou.com/jobs/%s.html'% positionId
            parse_position_detail(position_url)
            break
        break

def parse_position_detail(url):
    response=requests.get(url,headers=headers)
    text=response.text
    html=etree.HTML(text)
    position_name=html.xpath("//span[@class='name']/text()")[0]
    job_request_spans=html.xpath("//dd[@class='job_request']//span")
    salary_span=job_request_spans[0]
    salary=salary_span.xpath(".//text()")[0].strip()
    city=job_request_spans[1].xpath(".//text()")[0].strip()
    city=re.sub(r"[\s/]","",city)#\s表示空白字符,可能有多个
    work_years=job_request_spans[2].xpath(".//text()")[0].strip()
    work_years = re.sub(r"[\s/]", "", work_years)
    education=job_request_spans[3].xpath(".//text()")[0].strip()
    education=re.sub(r"[\s/]", "", education)
    desc="".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
    #"".join()只获取重要的内容，并将其选出连接起来。
    #.strip()则是去掉多余的空白格
    print(desc)


def main():
    request_list_page()

if __name__ == '__main__':
    main()
