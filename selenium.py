#使用selenium来访问拉勾网，模拟浏览器去访问，浏览器无法识别，可以更好的访问
#Selenium是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。而对于爬虫来说，使用Selenium操控浏览器来爬取网上的数据那么肯定是爬虫中的杀手武器。
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LagouSpider(object):
     dirver_path=r"/usr/local/bin/chromedriver"
     def __init__(self):
         self.driver=webdriver.Chrome(executable_path=LagouSpider.dirver_path)
         self.url="https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=py"
         self.positions=[]

     def run(self):
         self.driver.get(self.url)
         #获取多个页面，自动跳转到下一页，知道在next_btn的属性有"pager_next_disabled"退出循环
         while True:
             #用page_source可以获取到整个页面的内容信息，包括ajax部分
             source = self.driver.page_source
             WebDriverWait(driver=self.driver,timeout=10).until(
                 EC.presence_of_element_located((By.XPATH,"//div[@class='pager_container']/span[last()]"))
             )#需要等待
             self.parse_list_page(source)
             next_btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
             # if判断条件表明：如果访问的该页是最后一页则不用点击，如果不是最后一页可以进行点击
             if "pager_next_disabled" in next_btn.get_attribute("class"):
                break
             else:
                next_btn.click()
             #time.sleep是为了防止出现过于频繁的操作而被防止
             time.sleep(1)
#获取每一页里所有的具体职位信息
     def parse_list_page(self,source):
         html=etree.HTML(source)
         links=html.xpath("//a[@class='position_link']/@href")
         for link in links:
             self.request_detail_page(link)
             time.sleep(1)
#获取每一页的详细页面
     def request_detail_page(self,url):
         #self.driver.get(url)#会将原来的页面刷新掉
        #在新的窗口打开新的详细页
         self.driver.execute_script("window.open('%s')"%url)
         self.driver.switch_to.window(self.driver.window_handles[1])
         #webdriverwait()等待出现的是标签而不是文本内容，若判断条件是文本内容，则该循环不会终止
         WebDriverWait(driver=self.driver,timeout=10).until(
             EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']/span[@class='name']"))
         )
         source=self.driver.page_source
         self.parse_detail_page(source)
         #关闭当前的详情页
         self.driver.close()
         #继续切换回职位列表页
         self.driver.switch_to.window(self.driver.window_handles[0])

     def parse_detail_page(self,source):
         html = etree.HTML(source)
         position_name = html.xpath("//span[@class='name']//text()")[0]
         job_request_spans = html.xpath("//dd[@class='job_request']//span")
         salary_span = job_request_spans[0]
         salary = salary_span.xpath(".//text()")[0].strip()
         city = job_request_spans[1].xpath(".//text()")[0].strip()
         city = re.sub(r"[\s/]", "", city)  # \s表示空白字符,可能有多个
         work_years = job_request_spans[2].xpath(".//text()")[0].strip()
         work_years = re.sub(r"[\s/]", "", work_years)
         education = job_request_spans[3].xpath(".//text()")[0].strip()
         education = re.sub(r"[\s/]", "", education)
         desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
         position={
             'name':position_name,
             'salary':salary_span,
             'city':city,
             'work_years':work_years,
             'education':education,
             'desc':desc
         }
         self.positions.append(position)
         print(position)
         print("="*55)

if __name__ == '__main__':
    spider=LagouSpider()
    spider.run()