from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from product import Product


class IntermarcheProduct(Product):
    def __init__(self, title_, brand_, image_, price_uni_, price_kg_):
        title = brand_ + " " + str(title_.strip())
        image = str(image_.strip())
        if image[:4] == "data":
            image = None
        price_uni = str(price_uni_.strip())
        price_kg = str(price_kg_.replace(",", ".").replace("€", "")).strip()

        super().__init__(title, image, price_uni, price_kg)

        self.supermarket = "Intermarche"

    def __str__(self):
        s = "Titulo: " + self.title + "\n"
        if self.image is not None:
            s += "Imagem: " + self.image + "\n"
        s += "Preço unidade: " + self.price_uni + "\n"
        s += "Preço peso: " + self.price_kg + "\n"
        s += "_____________________" + "\n"
        return s

    def get_price_kg(self):
        if any(c.isalpha() for c in self.price_kg):
            return float(self.price_kg.split(" ")[0])
        else:
            float(self.price_kg)


class IntermarcheScrapper:
    def __init__(self):
        self.BASE_URL = "https://lojaonline.intermarche.pt/44-condeixa-a-nova/produit/recherche?mot={}"

        self.products = []

    def search(self, keyword):
        count = 0

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        DRIVER_PATH = "./geckodriver"
        driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
        search_url = self.BASE_URL.format(keyword)
        driver.get(search_url)

        grid = driver.find_element_by_class_name('content_vignettes')

        # gridRow
        products = grid.find_elements(By.CLASS_NAME, 'vignette_produit_info')
        for product in products:
            count += 1

            if count >= 10:
                break

            details_container = product.find_element_by_class_name("vignette_info")
            # Get brand, title and package weight
            brand_, title_, _ = details_container.text.split("\n")

            # Get image
            image_container = product.find_element_by_class_name("vignette_img")
            image_ = image_container.find_elements_by_tag_name("img")[0].get_attribute("src")

            # Get price
            price_container = product.find_element_by_class_name("vignette_picto_prix")
            prices = price_container.find_elements_by_tag_name("div")[0].text.split("\n")
            if len(prices) == 3:
                _, price_uni_, price_kg_ = prices
            else:
                price_uni_, price_kg_ = prices

            self.products.append(IntermarcheProduct(title_, brand_, image_, price_uni_, price_kg_))

        driver.close()
        print(count, "products found.")

    def print_products(self):
        print("Produtos do Intermarche")
        for p in self.products:
            print(p)
