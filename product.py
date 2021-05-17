import json


class Product:
    def __str__(self):
        s = "Titulo: " + self.title + "\n"
        s += "Imagem: " + self.image + "\n"
        s += "Preço unidade: " + self.price_uni + "\n"
        s += "Preço peso: " + str(self.price_kg) + "\n"
        s += "_____________________" + "\n"
        return s

    def __init__(self, title_, image_, price_uni_, price_kg_):
        self.title = title_
        self.image = image_
        self.price_uni = price_uni_
        try:
            self.price_kg = float(price_kg_.split(" ")[0])
        except ValueError:
            print(price_kg_)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
