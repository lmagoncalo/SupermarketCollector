from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from config import GOOGLE_CHROME_PATH, CHROMEDRIVER_PATH
from product import Product


class AuchanProduct(Product):
    def __init__(self, title_, image_, price_uni_, price_kg_):
        title = str(title_.strip())
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
        return self.title


class AuchanScrapper:
    def __init__(self):
        self.BASE_URL = "https://www.auchan.pt/Frontoffice/search/{}"

        self.products = []

    def search(self, keyword):
        count = 0

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.binary_location = GOOGLE_CHROME_PATH

        driver = webdriver.Chrome(options=options, executable_path=CHROMEDRIVER_PATH)

        search_url = self.BASE_URL.format(keyword)
        driver.get(search_url)

        grid = driver.find_element_by_class_name('justify-content-start')

        # gridRow
        products = grid.find_elements(By.CLASS_NAME, 'product')
        for product in products:
            count += 1

            if count >= 10:
                break

            details_container = product.find_element_by_class_name("product-tile")

            # Get title
            title_ = details_container.find_element_by_class_name('auc-product-tile__name')
            title_ = title_.text

            # Get image
            image_ = details_container.find_element_by_class_name("image-container").find_element_by_class_name("tile-image")
            image_ = image_.get_attribute("src")

            # Get price
            price_uni = product.find_element_by_class_name("auc-product-tile__prices")
            price_uni_ = price_uni.text.split("\n")[-1]

            price_kg = product.find_element_by_class_name("auc-product-tile__measures")
            price_kg_ = price_kg.text

            self.products.append(AuchanProduct(title_, image_, price_uni_, price_kg_))

        driver.close()
        print(self.products[0].supermarket, " - ", count, "products found.")

    def print_products(self):
        print("Produtos do Auchan")
        for p in self.products:
            print(p)
