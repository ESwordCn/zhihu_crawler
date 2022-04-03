import glob
import json
import os

import html2epub
import requests
from bs4 import BeautifulSoup

get_soup = lambda web_url:BeautifulSoup(requests.get(web_url).text, 'html.parser')

def make_ebup(dir=None,book_name ='zhihu',content="知乎盐选爬取"):
    epub = html2epub.Epub(content)
    if not dir:dir = r"zhihu\*.html"
    for html_file in glob.glob(dir):
        chapter = html2epub.create_chapter_from_file(html_file,title=os.path.split(html_file)[1][:-5])
        epub.add_chapter(chapter)
        print(f'已添加{html_file}')

    epub.create_epub('')


def get_web_content(web_url):
    soup = get_soup(web_url)
    content = soup.find('section',id="output_wrapper_id")
    title = soup.find('h3',attrs={'class':"post-title entry-title"})
    return str(title) + str(content)

def get_article_list(web_url,json_file_name = 'zhihu_article_list.json'):
    if os.path.exists(json_file_name):
        with open(json_file_name,'r') as fp:
            return json.load(fp)

    soup = get_soup(web_url)
    result_set = soup.find('tbody').find_all('a')
    article_list = {result.text:result['href'] for result in result_set}

    with open(json_file_name,'w') as fp:
        json.dump(article_list,fp)

    return article_list

if __name__ == '__main__':
    
    web_url = 'https://www.zhihuban.ml/2021/12/navigation.html'
    article_list = get_article_list(web_url)

    for title in article_list.keys():
        content = get_web_content(article_list[title])   #.replace('\u200b','') 等价于 encoding='utf-8'
        with open(f'zhihu\{title}.html', 'w' ,encoding='utf-8') as f:
            f.write(content)
            print(f'已爬取：{title}')
    make_ebup(r"zhihu\*.html") #制作电子书 epub

