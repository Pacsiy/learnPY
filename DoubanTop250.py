#! /usr/bin/python
# -*- coding:UTF-8 -*-

from urllib import request
import re


class MovieTop(object):
    def __init__(self):
        self.start = 0
        self.param = '&filter'
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                       "Chrome/65.0.3325.146 Safari/537.36"}
        self.movieList = []
        self.filePath = './DoubanTop250.txt'

    def get_page(self):
        try:
            url = 'https://movie.douban.com/top250?start=' + str(self.start) + '&filter='
            myRequest = request.Request(url, headers=self.headers)
            response = request.urlopen(myRequest)
            page = response.read().decode('utf-8')
            print('正在获取第' + str((self.start+25)//25) + '页数据...')
            self.start += 25
            return page
        except request.URLError as e:
            if hasattr(e, 'reason'):
                print('获取失败，失败原因：', e.reason)

    def get_page_info(self):
        patern = re.compile(u'<div.*?class="item">.*?'
                            + u'<div.*?class="pic">.*?'
                            + u'<em.*?class="">(.*?)</em>.*?'
                            + u'<div.*?class="info">.*?'
                            + u'<span.*?class="title">(.*?)</span>.*?'
                            + u'<span.*?class="other">(.*?)</span>.*?'
                            + u'<div.*?class="bd">.*?'
                            + u'<p.*?class="">.*?'
                            + u'导演:(.*?)&nbsp;&nbsp;&nbsp;.*?<br>'
                            + u'(.*?)&nbsp;/&nbsp;'
                            + u'(.*?)&nbsp;/&nbsp;(.*?)</p>.*?'
                            + u'<div.*?class="star">.*?'
                            + u'<span.*?class="rating_num".*?property="v:average">'
                            + u'(.*?)</span>.*?'
                            + u'<span>(.*?)人评价</span>.*?'
                            + u'<span.*?class="inq">(.*?)</span>'
                            , re.S)

        while self.start <= 225:
            page = self.get_page()
            movies = re.findall(patern, page)
            for movie in movies:
                self.movieList.append([movie[0],
                                       movie[1],
                                       movie[2].lstrip('&nbsp;/&nbsp;'),
                                       movie[3],
                                       movie[4].lstrip(),
                                       movie[5],
                                       movie[6].rstrip(),
                                       movie[7],
                                       movie[8],
                                       movie[9]])

    def write_page(self):
        print('开始写入文件...')
        file = open(self.filePath, 'w', encoding='utf-8')
        try:
            for movie in self.movieList:
                file.write('电影排名：' + movie[0] + '\n')
                file.write('电影名称：' + movie[1] + '\n')
                file.write('电影别名：' + movie[2] + '\n')
                file.write('导演：' + movie[3] + '\n')
                file.write('上映年份：' + movie[4] + '\n')
                file.write('制作国家/地区：' + movie[5] + '\n')
                file.write('电影类别：' + movie[6] + '\n')
                file.write('评分：' + movie[7] + '\n')
                file.write('参评人数：' + movie[8] + '\n')
                file.write('简短影评：' + movie[9] + '\n')
                file.write('\n')
            print('成功写入文件...')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def main(self):
        print('开始抓取豆瓣电影TOP250...')
        self.get_page_info()
        self.write_page()
        print('成功获取豆瓣电影TOP250...')


douban = MovieTop()
douban.main()