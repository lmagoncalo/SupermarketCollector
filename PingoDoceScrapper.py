from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from product import Product


class PingoDoceProduct(Product):
    def __init__(self, title_, image_, price_uni_, price_kg_):
        title = str(title_.strip())
        if image_ is not None:
            image = str(image_.strip())
        else:
            image = None
        price_uni = str(price_uni_.strip())
        price_kg = str(price_kg_.replace(",", ".").replace("€", "")).strip()

        super().__init__(title, image, price_uni, price_kg)

        self.supermarket = "PingoDoce"

    def __str__(self):
        s = "Titulo: " + self.title + "\n"
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


class PingoDoceScrapper:
    def __init__(self):
        self.BASE_URL = "https://mercadao.pt/store/pingo-doce/search?queries={}"

        self.products = []

    def search(self, keyword):
        count = 0

        options = Options()
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")

        DRIVER_PATH = "./geckodriver_linux"
        driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
        search_url = self.BASE_URL.format(keyword)
        driver.get(search_url)

        grid = driver.find_element_by_class_name('_3zhFFG0Bu9061elHI8VCq3')

        # gridRow
        products = grid.find_elements(By.CLASS_NAME, 'P9eg53AkHYfXRP7gt5njS')
        for product in products:
            count += 1

            if count >= 10:
                break

            details_container = product.find_element_by_class_name("product-details")

            # Get title
            title_ = details_container.find_element_by_class_name('pdo-heading-s')
            title_ = title_.text

            # Get image
            image_ = product.find_element_by_class_name("pdo-block")
            image_ = image_.get_attribute("src")

            # Get price
            price_container = product.find_element_by_class_name("bottom-info")
            price_uni_ = price_container.find_element_by_class_name("detail-price").text

            weight_description = price_container.find_element_by_class_name("pdo-block").text
            _, price_kg_ = weight_description.split("|")

            self.products.append(PingoDoceProduct(title_, image_, price_uni_, price_kg_))

        driver.close()
        print(self.products[0].supermarket, " - ", count, "products found.")

    def print_products(self):
        print("Produtos do Pingo Doce")
        for p in self.products:
            print(p)
