import scrapy
from scrapy.selector import Selector
import json
from math import ceil 

#extract()是返回一个数组list，里面保含多个string字符，能使爬取的网页转换为list数据
companyf=open('compInfor.txt','w',encoding='utf-8')#将company存到该文件，编码格式是utf-8
companyid_f=open('companyid_f.txt','w',encoding='utf-8')
jobf=open('jobInfor.txt','w',encoding='utf-8')

class CompanySpider(scrapy.Spider):
    name = 'company'
    allowed_domains = ['51job.com']
    #start_urls = ['http://51job.com/'],这个网址只是51job的网址，但是它里面有几百万个公司的信息，所以会报错,format-字符串格式化
    start_urls = ['https://jobs.51job.com/all/co{}.html'.format(i) for i in (3228,150997,601830,1243257,1265851,2049136,2557268,2619421,3805962,3101056,54832720)]#爬取的范围
    #如果想爬取指定的，就将range(1,11)改为[1]
    def getCompany(self,selector):
        xpaths=[('//*[@id="hidCOID"]/@value','compID'),
                ('/html/body/div[2]/div[3]/div[2]/div/h1/@title','compName'),
                ('/html/body/div[2]/div[3]/div[2]/div/img/@src','compLogo'),
                ('/html/body/div[2]/div[3]/div[2]/div/p/@title','c_o'),#公司性质、规模、行业
                ('/html/body/div[2]/div[3]/div[3]/div[2]/div/p/text()','compAdd'),
                ('/html/body/div[2]/div[3]/div[3]/div[2]/div/p[2]/span[2]','compWeb'),
                ('/html/body/div[2]/div[3]/div[3]/div[1]/div/div/div[1]/div','compDesc'),
                ('//*[@id="hidTotal"]/@value','c_pub_jobcount')]
        company_date={}
        for x,key in xpaths:
        #x代表xpath,key代表值，即键值对里的值
            try:
                if key=='compWeb':
                        company_date[key]=selector.xpath(x).xpath('string(.)').extract()[0]
                elif key=='compAdd':
                        company_date[key]=selector.xpath(x).extract()[1]
                    #有些地址之前还有一个'公司地址'的标签，但这并不是我们想要提取的信息，我们需要的是后面那个，故用下标1.
                else:
                        company_date[key]=selector.xpath(x).extract()[0]
                #try-except抛出异常
            except Exception as err:
                print(err.args)
                company_date[key]='-'
        return company_date
    
    '''提取所有岗位数据'''
    def getworks(self,selector,compID,prefix='//*[@id="joblistdata"]'):
        jobs=[]
        try:
            len1=len(selector.xpath(prefix+'//div[.]/p/a/@title').extract())#len求长度
            for i in range(1,len1+1):
                job_date=selector.xpath(prefix+'//div[{}]'.format(i)).xpath('string(.)').extract()
                #这里也是先定位在取数据
                jobID=selector.xpath(prefix+'//div[{}]/p/a/@href'.format(i)).extract()[0]
                jobID1=jobID.split('/')[-1].split('.html')[0]#分割，再次从右边分割，在从html分割，第一个
                job=job_date[0].split('\n')[1:]
                #jobName1=selector.xpath('//*[@id="joblistdata"]/div[2]/p/a').xpath('string(.)').extract()
                # print(work_date[0].split('\n'))
                # print('\n')
                # print(work_date)
                job_w={'jobID':jobID1,
                       'compID':compID,
                       'jobName':job[0],
                       'jobExper_Edu_Num':job[1],
                       'jobcCity':job[2],
                       'jobSalsry':job[3],
                       'jobNum':job[4].strip()}#strip()是去掉后面的空格和换行
                jobs.append(job_w)#将work_w字典加入到jobs中
        except Exception as err:
            print(err.args)#可写可不写
            print('-')
        
        return jobs
    
    #解析下一页数据
    def nextjob(self,response):
        selector = Selector(text=response.text)
        '''提取岗位数据(pageno)'''
        compID=response.url.split('/co')[-1].replace('.html','')#提取岗位id
        jobs=self.getworks(selector,compID,prefix='')#prefix前缀改成空
        for job in jobs:
            jobstr=json.dumps(job,ensure_ascii=False)+'\n'
            jobf.write(jobstr)
            print(jobstr)
        print(len(jobs))
            
    def parse(self, response):#response是返回的数据
        selector = Selector(text=response.text)
        
        company=self.getCompany(selector)#字典数据转换为字符串
        companystr=json.dumps(company,ensure_ascii=False)+'\n'#True可以让不是字符串的转为ascii
        print(companystr)
        #保存到本地txt文本中
        companyf.write(companystr )
        companyid_f.write(company['compID']+'\n')
        
        #提取岗位数据
        jobs=self.getworks(selector,company['compID'])
        for job in jobs:
            jobstr=json.dumps(job,ensure_ascii=False)+'\n'
            jobf.write(jobstr)
            #print(workstr)
        print(len(jobs))
        
        #岗位数大于20才可以，一页20
        url=response.url#url就是地址
        totalPage=ceil(int(company['c_pub_jobcount'])/20)#发布总页数,发布总个数,ceil()就是如ceil(38/20)=2,即只要有余数就向上加一
        #formdata参数
        for pageno in range(2,totalPage+1):
            formdata={'pageno':str(pageno),#页数
                       'jobarea':str(company['c_pub_jobcount']), 
                       'funtype':'',
                       'salary':''}
            yield scrapy.FormRequest(url,formdata=formdata,#yield能使这个语句被添加到start_urls,
                                   callback=self.nextjob)
    
   # 'https://jobs.51job.com/all/co123056.html'.split('/co')[-1].replace('.html','')
  