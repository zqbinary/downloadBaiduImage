# -*- coding:utf-8 -*-
import re
import requests
import os
import mysql.connector


def dowmloadPic(html, keyword, goodsId):
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 1
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            continue
        except requests.exceptions.Timeout:
            print "Timeout occurred"
            continue
        except requests.exceptions.TooManyRedirects:
            print("too many Redirect")
            continue
        except requests.exceptions.ChunkedEncodingError:
            print('chunked')
            continue
        except requests:
            print('other')
            continue

        path = '../images/' + goodsId + '-' + keyword
        if not os.path.exists(path):
            os.makedirs(path)

        dir = path + '/' + keyword + '_' + str(i) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1
        if i > 30:
            break


if __name__ == '__main__':
    myDb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="for_goods"
    )

    myCursor = myDb.cursor()

    myCursor.execute("SELECT goods_name,goods_id FROM ecs_goods where goods_id>34 order by goods_id asc")

    myResult = myCursor.fetchall()

    for x in myResult:
        word = x[0].encode('utf-8')
        goodsId = str(x[1])
        print(word)

        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'

        result = requests.get(url)
        dowmloadPic(result.text, word, goodsId)
