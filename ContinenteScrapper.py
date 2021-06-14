from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from product import Product


class ContinentProduct(Product):
    def __init__(self, title_, brand_, image_, price_uni_, price_kg_):
        title = str(brand_.strip()) + " " + str(title_.strip())
        image = str(image_.strip())
        price_uni = str(price_uni_.strip())
        price_kg = str(price_kg_.replace(",", ".").replace("€", "")).strip()

        super().__init__(title, image, price_uni, price_kg)

        self.supermarket = "Continente"

    def __str__(self):
        s = "Titulo: " + self.title + "\n"
        s += "Imagem: " + self.image + "\n"
        s += "Preço unidade: " + self.price_uni + "\n"
        s += "Preço peso: " + self.price_kg + "\n"
        s += "_____________________" + "\n"
        return s


class ContinenteScrapper:
    def __init__(self):
        self.BASE_URL = "https://www.continente.pt/stores/continente/pt-pt/public/Pages/searchResults.aspx?k={}"

        self.products = []

    def search(self, keyword):
        count = 0

        options = Options()
        # options.add_argument("--window-size=1920,1200")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")

        DRIVER_PATH = "./geckodriver"
        driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)

        search_url = self.BASE_URL.format(keyword)
        driver.get(search_url)

        grid = driver.find_element_by_class_name('gridRow')

        # gridRow
        products = grid.find_elements(By.CLASS_NAME, 'productItem')
        for product in products:
            count += 1

            if count >= 10:
                break

            details_container = product.find_element_by_class_name("containerDescription")

            # Get title
            title_ = details_container.find_element_by_class_name("title")
            title_ = title_.text

            # Get type
            brand_ = details_container.find_element_by_class_name("type")
            brand_ = brand_.text

            # Get image
            image_container = driver.find_element_by_class_name('lazy')
            image_ = image_container.get_attribute("src")

            # Get price
            price_container = product.find_element_by_class_name("containerPrice")
            price_uni_ = price_container.find_element_by_class_name("priceFirstRow")
            price_uni_ = price_uni_.text
            price_kg_ = price_container.find_element_by_class_name("priceSecondRow")
            price_kg_ = price_kg_.text

            self.products.append(ContinentProduct(title_, brand_, image_, price_uni_, price_kg_))

        driver.quit()
        print(self.products[0].supermarket, " - ", count, "products found.")

    def print_products(self):
        print("Produtos do Continente")
        for p in self.products:
            print(p)
