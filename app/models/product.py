from odmantic import Model

class ProductModel(Model):
    keyword: str
    title: str
    image: str
    price: int
    mall_name: str
    link: str
    brand: str = ""
    category: str = ""
    is_favorite: bool = False

    model_config = {
        "collection": "products"
    }
