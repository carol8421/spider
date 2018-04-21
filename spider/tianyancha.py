
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import pymysql
from tkinter import messagebox
from tkinter import *
import types
class spider():
    time_start=time.time()
    i=0
    num=34 #类变量，默认爬34个数据
   # firefox_profile=webdriver.FirefoxProfile()
   # firefox_profile.set_preference("permissions.default.stylesheet",2) # 禁用样式表
   # firefox_profile.set_preference("permissions.default.image",2) #禁用图片
   # firefox_profile.set_preference("javascript.enabled",False) #禁用js
    #firefox_profile.update_preferences()  #更新设置
    browse=webdriver.Firefox()  #类变量
    browse.implicitly_wait(120)    #隐式等待120s，当所需要的元素没出现时，作用与全局
    

    # options = Options()
    # options.add_argument('-headless')  # 无头参数
    # browse = Firefox(executable_path='/usr/bin/geckodriver',firefox_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径,river = Firefox(executable_path='geckodriver', firefox_options=options) 
    def open(self,url): 
        try:
            spider.browse.get(url)
        except:
            print("error")
        enterprise_name=spider.browse.find_elements_by_xpath("//div[@class='search_right_item ml10']/div/a")
        return enterprise_name

    def run(self,url):
        list=[]
        q=0
        count=0
        enterprise_name=self.open(url)    #获得页面所有企业的url
        for en in enterprise_name:
            en_url=en.get_attribute("href")   #企业的url
            list.append(en_url)
            q+=1            
       
        for aen in list:
            count+=1
            try:
                spider.browse.get(aen)
                spider.browse.forward()
            except:
                messagebox.showinfo(title='error',message='网速太慢，爬不动了')
                print("网速太慢，爬不动了，休息一会，再重新爬呗")
            
           # time.sleep(1)
            try:
                en_name=spider.browse.find_element_by_xpath("//h1[@class='f18 mt0 mb0 in-block vertival-middle sec-c2']").text#企业的名字
                boss=spider.browse.find_element_by_xpath("//div[@class='human-top']/div[@class='in-block vertical-top pl15']/div/a").text     #企业法人
                address=spider.browse.find_element_by_xpath("//span[@class='in-block overflow-width vertical-top']").text   #地址
                property=spider.browse.find_element_by_xpath("//*[@id='_container_baseInfo']/div/div[2]/table/tbody/tr/td[2]/div[1]/div[2]").text  #企业注册资金
                e_type=spider.browse.find_element_by_xpath("//*[@id='_container_baseInfo']/div/div[3]/table/tbody/tr[2]/td[4]").text   #企业的类型
            except:
                messagebox.showinfo(title='error',message='网速太慢，爬不动了')
                print("网速太慢，爬不动了，休息一会")
            # en_name=str(en_name)
            # boss=str(boss)
            # address=str(address)
            # property=str(property)
            # type=str(type)
            print("企业名称： ",end='')
            print(en_name)
            print("企业法人： ",end='')
            print(boss)
            print("地址： ",end='')
            print(address)
            print("注册资金： ",end='')
            print(property)
            print("公司类型：",end='')
            print(e_type)
            # ewe=type(boss)
            # print(ewe)
            # if type(address) is types.StrType:
            #     print('str')
            spider.i+=1
            try:
                spider.browse.back()
            except:
                messagebox.showinfo(title='error',message='网速太慢，爬不动了')
                print("网速太慢，爬不动了，休息一会，再重新爬呗")
            print(en_name)
            conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='861153',db='enterprise_info',charset='gbk')
            cursor=conn.cursor()
            print("'%s','%s','%s','%s','%s'"%(en_name,boss,address,property,e_type))
        # print(en_name)
        # print("1")
            sql="insert into info (en_name,boss_name,address,property,type) values ('%s','%s','%s','%s','%s')"%(en_name,boss,address,property,e_type)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            # try:
            #     cursor.execute(sql)
            #     conn.commit()                
            # except Exception:
            #     print("数据插入数据库时，发生异常")
            # finally:
            #     cursor.close()
            #     conn.close()
           
            print("爬取第 %s 个数"%spider.i)
            if spider.i==spider.num:
                time_end=time.time()
                t=time_end-spider.time_start
                print("总共用时： %s 秒"%t)
                time.sleep(10)
                messagebox.showinfo(message='爬取数据完成')
                try:
                    spider.browse.close()
                except:
                    print("已完成")
            if count==q:
                nextPageUrl=spider.browse.find_element_by_xpath("//li[@class='pagination-next ng-scope ']/a").get_attribute("href")
                # print("下一页url：%s"%nextPageUrl)
                # spider.browse.close()
                time.sleep(3)
                # self.run(nextPageUrl,num)
                self.run(nextPageUrl)
    def start(self,entry_url,entry_num):
        url=entry_url.get()
        num=entry_num.get()
        print('url :%s   num :%s'%(url,num))
        self.first(url,num)
        
    def first(self,url,num):
        messagebox.showinfo(message='爬取开始')
        spider.num=num
        self.run(url)
  
if __name__=="__main__":
   # url="https://bj.tianyancha.com/search/os1"
    win=Tk()
    win.title("企业数据爬虫")
    win.geometry('260x100+500+200')
    win.iconbitmap('spider.ico')
    win.resizable(0,0)
    Label(win,text="开始url").grid(row=0,column=0)
    var_url=StringVar()
    entry_url=Entry(win,textvariable=var_url)
    entry_url.grid(row=0,column=1)
    Label(win,text="爬取数量").grid(row=1,column=0)
    var_num=StringVar()
    entry_num=Entry(win,textvariable=var_num)
    entry_num.grid(row=1,column=1)
    # url=entry_url.get()
    # num=entry_num.get()
    # print(url)
    # print(num)
    #url='https://bj.tianyancha.com/search/os1/p2'
    #num=40
    sp=spider()
    button=Button(win,text="爬取",command=lambda:sp.start(entry_url,entry_num)).grid(row=2,columnspan=2)
    win.mainloop()
    


       
    
