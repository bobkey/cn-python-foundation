# -*- coding: utf-8 -*-

import requests
import expanddouban
import bs4
import csv

#任务1	实现函数getMovieUrl
def getMovieUrl(category, location):
    doubanURL = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,"
    if location == "alllocation":
        url = doubanURL + category
    else:
        url = doubanURL + category + "," + location
    return url

#任务2	通过 URL 获得豆瓣电影页面的 HTML
def getMovies(category,location):
#定义几个列表，用于把解析 HTML 元素放进来
    m = []
    r = []
    l = []
    c = []
    link = []
    pic = []




#得到要打开的 url，输入类型和地区
    searchURL = getMovieUrl(category, location)
    html = expanddouban.getHtml(searchURL)
    soup = bs4.BeautifulSoup(html, "html.parser")

#任务4	通过类型和地区构造URL，并获取对应的HTML。解析 HTML 中的每个电影元素，并构造电影对象列表
    #核心语句，用 soup 找到后再逐一得到各个元素，其中地区和类型是一样的，所以添加了传入的参数
    for i in soup.find_all('a',class_ = 'item'):
        m.append(i.find('span',class_ = 'title').string)
        r.append(i.find('span',class_ = 'rate').string)
        l.append(location)
        c.append(category)
        link.append(i.get('href'))
        pic.append(i.find('img').get('src'))

    return m,r,l,c,link,pic

#任务3	定义电影类，并实现其构造函数
class Movies():
    def __init__(self,name,rate,location,category,info_link,cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def movie_info(self):
        return "{},{},{},{},{},{},".format(self.name,self.rate,self.location,self.category,self.info_link,self.cover_link)

m = Movies("肖恩克的救赎","9.7","美国","剧情","https://movie.douban.com/subject/1292052/","https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg")


#任务5	将电影信息输出到 movies.csv。 包含类别、地区以及对应的电影信息
def writecsv():
    moviename,rates,l,c,links,pic = getMovies("剧情","美国")
    headers = ['电影名', '评分', '地区', '类型', '链接', '图片']
    for i in range(len(moviename)):

        rows = [
            {'电影名':moviename[i], '评分':rates[i], '地区':l[i], '类型':c[i], '链接':links[i], '图片':pic[i]}
        ]

        with open('movies.csv', 'a+', newline='',encoding='utf_8_sig')as ccc:
            f_csv = csv.DictWriter(ccc, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)

writecsv()
#任务6	将电影的统计结果输出到 output.txt。包含你选取的每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少。
#实现得不优雅，写得很繁琐，特别是得到地区列表、统计全部电影
#得到类别、地区的列表
def getLocations():
URL = getMovieUrl("剧情",location="")
html = expanddouban.getHtml(URL)
soup = bs4.BeautifulSoup(html, "html.parser")
items = soup.find_all('ul', 'category')
categories_html = list(items[1].children)
locations_html = list(items[2].children)
# 剔除无关元素，得到地区文本列表
all_location = []
for l in locations_html:
    all_location.append(l.get_text())
all_location.remove("全部地区")
return all_location


all_l = []

for i in all_location:
    a,b,c,d,e,f = getMovies("剧情",i)
    if len(a) == 0:
        continue
    all_l.append("{},{}".format(c[0],len(a)))

#all_l列表内容是["日本,20","美国,15"]，split 得到后面的数字
ranking =sorted(all_l,key=lambda x:int(x.split(",")[1]),reverse=True)
all_m = 0
for i in ranking:
    all_m += int(i.split(",")[1])

r1 = "{:.2f}%".format(int(ranking[0].split(",")[1]) / all_m * 100)
r2 = "{:.2f}%".format(int(ranking[1].split(",")[1]) / all_m * 100)
r3 = "{:.2f}%".format(int(ranking[2].split(",")[1]) / all_m * 100)

print(all_m)
with open("output.txt","w") as f:
    f.write("排名第一的地区是: {}，占比该类型比例是: {}。\n".format(ranking[0].split(",")[0],r1))
    f.write("排名第二的地区是: {}，占比该类型比例是: {}。\n".format(ranking[1].split(",")[0],r2))
    f.write("排名第三的地区是: {}，占比该类型比例是: {}。\n".format(ranking[2].split(",")[0],r3))

