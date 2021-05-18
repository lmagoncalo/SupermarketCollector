import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from product import Product


class MiniPrecoProduct(Product):
    def __init__(self, title_, image_, price_uni_, price_kg_):
        title = str(title_.strip())
        image = str(image_.strip())
        if image[:4] == "data":
            image = None
        price_uni = str(price_uni_.strip())
        pattern = "[()]"
        price_kg = str(price_kg_)
        price_kg = re.sub(pattern, "", price_kg).replace(",", ".").replace("€", "").strip()

        super().__init__(title, image, price_uni, price_kg)

        self.supermarket = "MiniPreco"

    def __str__(self):
        s = "Titulo: " + self.title + "\n"
        if self.image is not None:
            s += "Imagem: " + self.image + "\n"
        s += "Preço unidade: " + self.price_uni + "\n"
        s += "Preço peso: " + self.price_kg + "\n"
        s += "_____________________" + "\n"
        return s

    def get_name(self):
        return self.title

    def get_price_kg(self):
        if any(c.isalpha() for c in self.price_kg):
            return float(self.price_kg.split(" ")[0])
        else:
            float(self.price_kg)


class MiniPrecoScrapper:
    def __init__(self):
        self.BASE_URL = "https://lojaonline.minipreco.pt/search?q={}%3Arelevance"

        self.products = []

    def search(self, keyword):
        count = 0

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        # DRIVER_PATH = "./geckodriver"
        DRIVER_PATH = "./geckodriver_2"
        driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)

        search_url = self.BASE_URL.format(keyword)
        driver.get(search_url)

        grid = driver.find_element_by_class_name('span-16')

        # gridRow
        products = grid.find_elements(By.CLASS_NAME, 'span-3')
        for product in products:
            count += 1

            if count >= 10:
                break

            details_container = product.find_element_by_class_name("productMainLink")

            # Get title
            title_ = details_container.find_element_by_class_name('details')
            title_ = title_.text

            # Get image
            image_ = details_container.find_element_by_class_name("lazy")
            image_ = image_.get_attribute("src")

            # Get price
            price_container = product.find_element_by_class_name("price_container")
            price_uni_ = price_container.find_element_by_class_name("price").text

            price_kg_ = price_container.find_element_by_class_name("pricePerKilogram").text

            self.products.append(MiniPrecoProduct(title_, image_, price_uni_, price_kg_))

        driver.close()
        print(count, "products found.")

    def print_products(self):
        print("Produtos do Mini Preço")
        for p in self.products:
            print(p)
