"""
# name: crawler_taobao
# brief: get taobao comment
# date: 2020.10.29
# author: zxx
"""

import requests
# import beautifulsoup4 as bs
import json
import csv
import re

page_url = []


def get_url(num):
    urlfirst = 'https://rate.tmall.com/list_detail_rate.htm?itemId=629559130014&spuId=1866629792&sellerId=890482188&order=3&currentPage='
    urllast = '&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hv%2FvvLvZpvUvCkvvvvvjiWP2MygjrbPLqOAjljPmPwtjlWn25Wsj1Un2spzj1HdvhvhZ3Em3CdvhHCDr1YZfv1veWARvhvChCvvvm%2BvpvEphE%2FVCpvpbiadvhvmZCm%2F1osvhmIN4OCvvBvpvpZRvhvChCvvvvRvpvhvv2MMg9CvvXmp99hjCuIvpvUphvhlLiZqbTgvpvIphvvvvvvphCvpv9dvvC2FhCvjvUvvhBGphvwv9vvBj1vpCQmvvChNv9Cvh1C5pwvIs%2B3Z0vRYEZc%2Bo3EW5VYyf89nCQSCd2n5FwJ45%2BPYbeaRAHLOvj6LLIt8Zw5mX5ErqO24AHL2f6A%2Be9f4xbEdETQPZ%2B3ZgmBvvhvCyCCvvvvvUOCvvBvppvvdvhvmZCmu1kKvhmfl8QCvvDvprIpL9Cvu%2B7%2BvpvEphULm86vp8QadvhvmZCm41mhvhmSPuQCvvDvpxGp1vCvSwTvvpvWzPA0cefNznsw0T14&needFold=0&_ksTS=1603980078599_4538&callback=jsonp4539'
    for i in range(0, num):
        page_url.append(urlfirst + str(1 + i) + urllast)


def get_info(num):
    name = []
    auctionsku = []
    ratecontent = []
    ratedate = []

    for i in range(num):
        headers = {
            'cookie': 'lid=%E9%9A%8F%E4%BE%BF%E8%B5%B7%E4%B8%AA%E6%B2%A1%E4%BA%BA%E7%94%A8%E8%BF%87%E7%9A%84%E5%90%8D%E5%AD%97; UM_distinctid=1725e492bb58-083a35435ccc5-f7d1d38-1fa400-1725e492bb6cb6; enc=bhUQ0ksKMGckWFnCIWMqNI3D%2F%2BmPI4xUY5ellOIyzpkW9PnMbEpe98P4Ygezhob863AJv64BkSTeF6%2B%2B%2F%2Fn7BA%3D%3D; cna=n1u+FyrnRTICAWf+ROU9uQyD; xlly_s=1; hng=CN%7Czh-CN%7CCNY%7C156; t=50a6e32b924682f2a7ac17b1adeb95e0; tracknick=%5Cu968F%5Cu4FBF%5Cu8D77%5Cu4E2A%5Cu6CA1%5Cu4EBA%5Cu7528%5Cu8FC7%5Cu7684%5Cu540D%5Cu5B57; _tb_token_=aef457b4dbeb; cookie2=17954b2735e26e2454a545d89af09bc0; _m_h5_tk=cc5f68828ebbb19fea3c234541acef77_1603987439653; _m_h5_tk_enc=4a90f61a5cf8d085fe57c53f84672b9a; CNZZDATA1256793290=1233428181-1598313832-https%253A%252F%252Fs.taobao.com%252F%7C1603978823; dnk=%5Cu968F%5Cu4FBF%5Cu8D77%5Cu4E2A%5Cu6CA1%5Cu4EBA%5Cu7528%5Cu8FC7%5Cu7684%5Cu540D%5Cu5B57; uc1=pas=0&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie14=Uoe0bkAe1rYJKg%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVnmS&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false; uc3=vt3=F8dCufJGUbzWpL5ZbCs%3D&id2=UUpkuyHiuejcuw%3D%3D&nk2=qE4gCfs%2BrimSAiUlaTgws9%2BZo%2FhhHg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; uc4=id4=0%40U2guM2YUlERDP9BM%2FoYGfRec1%2FRI&nk4=0%40qnWNzYwx3ImLJOLkwHM3QZ7lrVvtTkH8QlAbRV2W1jgk; _l_g_=Ug%3D%3D; unb=2253071466; lgc=%5Cu968F%5Cu4FBF%5Cu8D77%5Cu4E2A%5Cu6CA1%5Cu4EBA%5Cu7528%5Cu8FC7%5Cu7684%5Cu540D%5Cu5B57; cookie1=AQH3O8H3UdcjciBP%2FgrPKQkQQ%2FtyTeFroSqTwIXogpI%3D; login=true; cookie17=UUpkuyHiuejcuw%3D%3D; _nk_=%5Cu968F%5Cu4FBF%5Cu8D77%5Cu4E2A%5Cu6CA1%5Cu4EBA%5Cu7528%5Cu8FC7%5Cu7684%5Cu540D%5Cu5B57; sgcookie=E100tB8Q2VVV82yfn6ZHhcLf6Xh8c3eWMH%2BuiTKNIMf3xqcgs6OCRPh9QDOGQqygT%2FRQsWCOm8l5Z2u5AcZ9fFfwZw%3D%3D; sg=%E5%AD%9765; csg=e38346d7; cq=ccp%3D0; pnm_cku822=098%23E1hvgvvUvbpvUvCkvvvvvjiWP2MygjrbP2zWsjrCPmPOAjDWRsqO1jibRsdWljlRi9hvCvvv9UUgvpvhvvvvvvvCvvOvCvvvphmUvpvVmvvC9j3Wuvhvmvvv9bI65vbUKvhv8vvvvvCvpvvvvvm2phCv22GvvUnvphvpgvvv96CvpC29vvm2phCvhRvUvpCWCEHxvvauKWjxsLpZaZj9QW2W5CDApn2Wibm0HsCHs4V91Ep7bpPClw03HC3iBXxrlj7JD5HaA42W%2BCy7EcqZa4oQ%2Bull8PolKWVzRvgCvvpvvPMM; tfstk=cqnOBQas5BAgp-yKUVLhc-OwcvhOZiOYOONcDLw9kFddGoIAiKio24ak5-1TvpC..; l=eBEH6VlHqsnyMRTDKOfZnurza779TIRfguPzaNbMiOCPOb5M51oPWZWaHlYHCnGVnsa2R35e4jE9BoLxqy4Fl-EhuzWn9MpTjdTh.; isg=BPn5n0engnKNTVwytnI3D7UvCGXTBu24JJL-CxsuJyCfohg0Y1BiiSbwIKZUGoXw',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'referer': 'https://nike.tmall.com/shop/view_shop.htm?ali_trackid=17_926bd0585d0ac5f102572b1962e8b8e1',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9'
        }

        content = requests.get(page_url[i], headers=headers).text
        dk = re.findall('"displayUserNick":"(.*?)"', content)
        name.extend(dk)
        print(dk)

        auctionsku.extend(re.findall('"auctionSku":"(.*?)"', content))
        ratecontent.extend(re.findall('"rateContent":"(.*?)"', content))
        ratedate.extend(re.findall('"rateDate":"(.*?)"', content))

    for i in range(num):
        text = ','.join((name[i], ratedate[i], auctionsku[i], ratecontent[i])) + '\n'
        with open(r"E:\Content.txt", 'a+', encoding='UTF-8') as file:
            file.write(text + ' ')
            print(i + 1, "写成功")


if __name__ == "__main__":
    page_num = 20
    get_url(page_num)
    get_info(page_num)
