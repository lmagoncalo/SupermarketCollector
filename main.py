import multiprocessing
import os
from enum import Enum
from multiprocessing import Process
import time

from flask import Flask, render_template
from flask import request

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

    supermarkets = [Supermarket.MINIPRECO,
                    Supermarket.PINGODOCE, Supermarket.INTERMARCHE]

    start = time.time()
    with multiprocessing.Manager() as manager:
        results = manager.list()
        processes = list()
        for index in range(len(supermarkets)):
            p = Process(target=thread_function, args=(supermarkets[index], keyword, results))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

        print(results)

        # Flatten list
        products = [p for sublist in results for p in sublist]

        # To sort the list in place...
        products = sorted(products, key=lambda x: x.price_kg)

        results = list()
        for p in products:
            results.append(p.__dict__)
        end = time.time()
        print(end - start)

    return render_template('web_app.html', results=results)


def search_test(keyword):
    supermarkets = [Supermarket.AUCHAN, Supermarket.MINIPRECO,
                    Supermarket.PINGODOCE, Supermarket.INTERMARCHE]

    start = time.time()
    results = list()
    processes = list()
    for index in range(len(supermarkets)):
        p = Process(target=thread_function, args=(supermarkets[index], keyword, results))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    # Flatten list
    products = [p for sublist in results for p in sublist]

    # To sort the list in place...
    products = sorted(products, key=lambda x: x.price_kg)

    results = list()
    for p in products:
        results.append(p.__dict__)
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
