#! /usr/bin/python
# -*- coding:UTF-8 -*-

from urllib import request
import re
import pymysql


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
                            + u'导演:\s(.*?)\s.*?<br>'
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
            print('成功写入文件，共有%d条记录...' % len(self.movieList))
        except Exception as e:
            print(e)
        finally:
            file.close()

    def upload(self):
        db = pymysql.connect("localhost", "root", "love1125", "PythonTest", charset='utf8')
        cursor = db.cursor()

        insertStr = "INSERT INTO doubanTop250(rank, name, alias, director," \
                    "showYear, makeCountry, movieType, movieScore, scoreNum, shortFilm)" \
                    "VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', %f, %d, '%s')"

        try:
            for movie in self.movieList:
                insertSQL = insertStr % (int(movie[0]), str(movie[1]), str(movie[2]), str(movie[3]),
                                         str(movie[4]), str(movie[5]), str(movie[6]), float(movie[7]),
                                         int(movie[8]), str(movie[9]))
                cursor.execute(insertSQL)
            db.commit()
            print('成功上传至数据库...')
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.close()

    def main(self):
        print('开始抓取豆瓣电影TOP250...')
        self.get_page_info()
        print('成功获取豆瓣电影TOP250...')
        print('开始写入文件...')
        self.write_page()
        print('开始上传至数据库...')
        self.upload()


douban = MovieTop()
douban.main()