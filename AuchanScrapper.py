import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from product import Product


class AuchanProduct(Product):
    def __init__(self, title_, brand_, image_, price_uni_, price_kg_):
        if brand_ is None:
            brand = ""
        else:
            brand = str(brand_.strip())
        title = brand + " " + str(title_.strip())
        image = str(image_.strip())
        price_uni = str(price_uni_.strip())
        price_kg = str(price_kg_.replace(",", ".").replace("€", "")).strip()

        super().__init__(title, image, price_uni, price_kg)

        self.supermarket = "Auchan"

    def __str__(self):
        s = "Titulo: " + self.title + "\n"
        s += "Imagem: " + self.image + "\n"
        s += "Preço unidade: " + self.price_uni + "\n"
        s += "Preço peso: " + self.price_kg + "\n"
        s += "_____________________" + "\n"
        return s

    def get_name(self):
        return self.title + " " + self.brand

    def get_price_kg(self):
        if any(c.isalpha() for c in self.price_kg):
            # TODO - Returns None when the price is already clean
            return float(self.price_kg.split(" ")[0])
        else:
            float(self.price_kg)


class AuchanScrapper:
    def __init__(self):
        self.BASE_URL = "https://www.auchan.pt/Frontoffice/search/{}"

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

        grid = driver.find_element_by_id('divDataList')

        # gridRow
        products = grid.find_elements(By.CLASS_NAME, 'product-item')
        for product in products:
            count += 1

            if count >= 10:
                break

            details_container = product.find_element_by_class_name("product-item-header")

            # Get title
            title_ = details_container.find_elements_by_tag_name('h3')
            title_ = title_[0].text

            # Get type
            type_ = details_container.find_element_by_class_name("product-item-brand")
            type_ = type_.text

            # Get image
            image_ = product.find_element_by_class_name("product-item-image")
            image_ = image_.get_attribute("src")

            # Get price
            price_container = product.find_element_by_class_name("product-item-price")
            price_uni_ = price_container.text

            price_container = product.find_element_by_class_name("product-item-actions-column")
            price_kg_ = price_container.text.split("/")[0]

            self.products.append(AuchanProduct(title_, type_, image_, price_uni_, price_kg_))

        driver.close()
        print(count, "products found.")

    def print_products(self):
        print("Produtos do Auchan")
        for p in self.products:
            print(p)
