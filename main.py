import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, render_template
import pymongo
from pyecharts.charts import Line#折线图所导入的包
from pyecharts.charts import Bar#柱状图所导入的包
from pyecharts.charts import Grid
from pyecharts.charts import EffectScatter#散点图所导入的包
from pyecharts.charts import Page, WordCloud
from pyecharts.globals import SymbolType
from pyecharts import options as opts

app = Flask(__name__)

def create():
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    mongoClient.list.booklist.drop()
    mongoClient.list.musiclist.drop()
    mongoClient.list.movielist.drop()
    mongoClient.close()
create()

#当当图书畅销榜

def insert1(value):
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    list = mongoClient.list
    try:
        list.booklist.insert_one({"bookname": value[0], "author": value[1], "price": value[2]})
    except:
        print("插入数据失败")
    mongoClient.close()

def findprint1():
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    list = mongoClient.list
    try:
        res = list.booklist.find()
        '''for i in res:
            print(i)'''
        return res
    except:
        print("输出数据失败")
        return 0
    mongoClient.close()


pertern1 = re.compile(
    r'<div class="name"><a.*?title="(.*?)">.*?</a>.*?<div class="publisher_info">.*?<a.*?>(.*?)</a>.*?<span class="price_n">(.*?)</span>',
    re.S)

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
url1 = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-1'
res1 = requests.get(url1,headers=headers)
res1.status_code
res1.encoding
res1.apparent_encoding
res1.encoding = res1.apparent_encoding
#print(res1.text)
soup1 = BeautifulSoup(res1.text, 'html.parser')
data1 = soup1.find_all('ul', attrs={'class': 'bang_list clearfix bang_list_mode'})

data1 = str(data1)
#print(data1)
item1 = re.findall(pertern1, data1)

for i1 in item1:
    #print(i1)
    insert1(i1)

#酷狗音乐TOP500
def insert2(value):
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    list = mongoClient.list
    try:
        list.musiclist.insert_one({"number": value[0],"singer": value[1], "song": value[2], "time": value[3]})
    except:
        print("插入数据失败")
    mongoClient.close()

def findprint2():
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    list = mongoClient.list
    try:
        res = list.musiclist.find()
        '''for i in res:
            print(i)'''
        return res
    except:
        print("输出数据失败")
        return 0
    mongoClient.close()



pertern2 = re.compile(
    r'<li class="" data-index="(.*?)" title="(.*?) - (.*?)\">.*?<span class="pc_temp_time">\n*\t*(.*?)\n*\t*</span>',
    re.S)

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
url2 = 'https://www.kugou.com/yy/rank/home/1-8888.html?from=rank'
res2 = requests.get(url2)
res2.status_code
res2.encoding
res2.apparent_encoding
res2.encoding = res2.apparent_encoding
#print(res2.text)
soup2 = BeautifulSoup(res2.text, 'html.parser')
data2 = soup2.find(attrs={'class':'pc_temp_songlist'})

data2 = str(data2)
#print(data2)
item2 = re.findall(pertern2, data2)

for i2 in item2:
    #print(i2)
    insert2(i2)

#爱奇艺VIP热播榜
def insert3(value):
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    list = mongoClient.list
    try:
        list.movielist.insert_one({"score": value[0]+value[1],"moviename": value[2], "des": value[3]})
    except:
        print("插入数据失败")
    mongoClient.close()

def findprint3():
    mongoClient = pymongo.MongoClient(host="localhost", port=27017)
    list = mongoClient.list
    try:
        res = list.movielist.find()
        '''for i in res:
            print(i)'''
        return res
    except:
        print("输出数据失败")
        return 0
    mongoClient.close()


pertern3 = re.compile(
    r'<li.*?<strong class="num">(.*?)</strong>(.*?)\n.*?</span>.*?<a.*?>(.*?)</a>.*?<p class="site-piclist_info_describe">(.*?)</p>',
    re.S)

url3 = 'https://vip.iqiyi.com/hot.html?cid=1'
res3 = requests.get(url3)
res3.status_code
res3.encoding
res3.apparent_encoding
res3.encoding = res3.apparent_encoding
#print(res3.text)
soup3 = BeautifulSoup(res3.text, 'html.parser')
data3 = soup3.find_all('ul', attrs={'class': 'site-piclist'})

data3 = str(data3)
#print(data3)
item3 = re.findall(pertern3, data3)

for i3 in item3:
    #print(i3)
    insert3(i3)

a1=findprint1()
d1=[]
x1=[]
y1=[]
num = 0
for ii1 in a1:
    d1.append(ii1)
for j1 in d1:
    x1.append(j1['bookname'])
    y1.append(j1['price'][1:])
    print(j1)
for ix3 in x1:
    print(ix3)
for iy3 in y1:
    print(iy3)
def line2():
    line = (
        Line()#实例化Line
        .add_xaxis(x1)#加入X轴数据
        .add_yaxis("图书价格", y1)#加入Y轴数据
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-图书价格"))#全局设置项
    )
    return line
line2().render('E:\\university\\python\\ENJOYTIME\\templates\\bookprice.html')#保存图片为HTML网页

a2=findprint2()
d2=[]
x2=[]
y2=[]
for ii2 in a2:
    d2.append(ii2)
for j2 in d2:
    x2.append(j2['song']+' '+j2['singer'])
    y2.append(j2['time'].replace(':', '.'))
    print(j2)
for ix3 in x2:
    print(ix3)
for iy3 in y2:
    print(iy3)

def effectScatter1():
    effectScatter = (
        EffectScatter()#实例化Line
        .add_xaxis(x2)#加入X轴数据
        .add_yaxis("歌曲时长(m.s)",y2 )#加入Y轴数据
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-歌曲时长"))
    )
    return effectScatter
effectScatter1().render('E:\\university\\python\\ENJOYTIME\\templates\\musictime.html')#保存图片为HTML网页

a3=findprint3()
d3=[]
x3=[]
y3=[]
for ii3 in a3:
    d3.append(ii3)
for j3 in d3:
    x3.append(j3['moviename'])
    y3.append(j3['score'])
    #print(j3)
for ix3 in x3:
    print(ix3)
for iy3 in y3:
    print(iy3)

def line1():
    line = (
        Line()#实例化Line
        .add_xaxis(x3)#加入X轴数据
        .add_yaxis("电影得分",y3 )#加入Y轴数据
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-电影得分"))
    )
    return line
line1().render('E:\\university\\python\\ENJOYTIME\\templates\\moviescore.html')#保存图片为HTML网页

@app.route('/book')
def book():
    return render_template('booklist.html', data=d1)

@app.route('/music')
def music():
    return render_template('musiclist.html', data=d2)

@app.route('/movie')
def movie():
    return render_template('movielist.html', data=d3)


@app.route('/bookprice')
def bookprice():
    return render_template('bookprice.html')


@app.route('/moviescore')
def moviescore():
    return render_template('moviescore.html')

@app.route('/musictime')
def musictime():
    return render_template('musictime.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)