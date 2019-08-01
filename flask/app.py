import csv
import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/lotto')
def lotto():
    numbers = random.sample(range(1, 46), 6)
    print(numbers)
    return render_template('lotto.html', numbers=numbers)

@app.route('/lunch')
def lunch():
    menu = ['한식', '중식', '일식', '양식', '인도네시아식', '베트남식', '태국식']
    choice = random.choice(menu)
    return render_template('lunch.html', choice=choice)

@app.route('/opgg')
def opgg():
    return render_template('opgg.html')

@app.route('/search')
def search():
    opgg_url = 'https://www.op.gg/summoner/userName='
    summoner = request.args.get('summoner')
    url = opgg_url + summoner
    res = requests.get(url).text
    print(res)
    soup = BeautifulSoup(res, 'html.parser')
    tier = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank')
    user_tier= tier.text.strip()
    return render_template('search.html', user_tier=user_tier, summoner=summoner)


@app.route('/new')
def new():
    return render_template('new.html')
    
@app.route('/create')
def create():
    product = request.args.get('product')
    category = request.args.get('category')
    replace = request.args.get('replace')
    with open('data.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        info = [product, category, replace]
        writer.writerow(info)
    return render_template('create.html')

@app.route('/nono')
def nono():
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        products = list(reader)
    return render_template('nono.html', products=products)

@app.route('/card')
def card():
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        products = list(reader)
    return render_template('card.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)