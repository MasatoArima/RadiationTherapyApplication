import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
# Selenium
# Scrapy

# データを取得したいページを指定
r = requests.get('https://codezine.jp/article/tag/223')

# 取得データのstatus_codeが200ならアクセス成功
if r.status_code==200:
    print('アクセス成功', type(r))
else :
    print('アクセス失敗')


soup = BeautifulSoup(r.text, 'html.parser')

articles = []

atags = soup.find_all('a')
print('aタグ数：', len(atags))
for atag in atags[:5]:
    print('タイトル', atag.text)
    print('リンク', atag['href'])
print(soup.title)
print(soup.h1)
print(soup.h1.a.img['alt'])

# ループ文でデータを取得していく場合
# for line in text.split('\n'):
#     if '<title>' in line or '<h1>' in line:
#         print(line.strip())



r = requests.get('https://codezine.jp/article/tag/223')
soup = BeautifulSoup(r.text, 'html.parser')

articles = []  # 各記事の情報を格納するリスト

# CSSセレクターで <ul class="catList"><li> を取得
lis = soup.select('ul.catList > li')
for li in lis:
    # 日付の文字列を取得
    day = li.find('div', class_='day').text.strip()
    # 日付をdatetimeに変換
    published = datetime.strptime(day, '%Y/%m/%d')
    h2_tag = li.find('h2')  # h2タグを取得
    title = h2_tag.text  # タイトルを取得
    url = h2_tag.a['href']  # URLを取得
    
    tag_list = li.select('ul.tag > li')  # タグのli要素を取得
    # タグのリストを生成
    tags = [tag.text.strip() for tag in tag_list]
    
    article = {
        'publisthed': published,
        'title': title,
        'url': url,
        'tags': tags
    }
    articles.append(article)

print(articles[:3])

df = pd.DataFrame(articles)

print(df)