import os
from enum import Enum
from threading import Thread

from flask import Flask, render_template
from flask import request, jsonify

from AuchanScrapper import AuchanScrapper
from ContinenteScrapper import ContinenteScrapper
from IntermarcheScrapper import IntermarcheScrapper
from MiniPrecoScrapper import MiniPrecoScrapper
from PingoDoceScrapper import PingoDoceScrapper


class Supermarket(Enum):
    CONTINENTE = 1
    AUCHAN = 2
    PINGODOCE = 3
    INTERMARCHE = 4
    MINIPRECO = 5


def thread_function(supermarket, keyword, results):
    products = None

    if supermarket == Supermarket.CONTINENTE:
        continente_scrapper = ContinenteScrapper()
        continente_scrapper.search(keyword)
        products = continente_scrapper.products
    elif supermarket == Supermarket.AUCHAN:
        auchan_scrapper = AuchanScrapper()
        auchan_scrapper.search(keyword)
        products = auchan_scrapper.products
    elif supermarket == Supermarket.PINGODOCE:
        pingodoce_scrapper = PingoDoceScrapper()
        pingodoce_scrapper.search(keyword)
        products = pingodoce_scrapper.products
    elif supermarket == Supermarket.INTERMARCHE:
        intermarche_scrapper = IntermarcheScrapper()
        intermarche_scrapper.search(keyword)
        products = intermarche_scrapper.products
    elif supermarket == Supermarket.MINIPRECO:
        minipreco_scrapper = MiniPrecoScrapper()
        minipreco_scrapper.search(keyword)
        products = minipreco_scrapper.products

    results.append(products)


def search_keyword(keyword):
    supermarkets = [Supermarket.CONTINENTE, Supermarket.AUCHAN, Supermarket.PINGODOCE,
                    Supermarket.INTERMARCHE, Supermarket.MINIPRECO]

    threads = list()
    results = list()
    for index in range(len(supermarkets)):
        print(supermarkets[index])
        t = Thread(target=thread_function, args=(supermarkets[index], keyword, results))
        threads.append(t)
        t.start()

    for index, thread in enumerate(threads):
        thread.join()

    # Flatten list
    products = [p for sublist in results for p in sublist]

    # To sort the list in place...
    products = sorted(products, key=lambda x: x.price_kg)

    return products

def obj_dict(obj):
    return obj.__dict__


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    print(keyword)
    products = search_keyword(keyword)
    results = []
    for p in products:
        results.append(p.__dict__)

    # return jsonify(results)
    return render_template('web_app.html', results=results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)


