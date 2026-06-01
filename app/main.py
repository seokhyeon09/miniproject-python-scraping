from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

from app.models import mongodb
from app.models.product import ProductModel
from app.product_scraper import NaverProductScraper
import re

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"title": "쇼핑 위시리스트 콜렉터"})


@app.get("/search", response_class=HTMLResponse)
async def read_item(request: Request, q: str):
    keyword = q
    naver_product_scraper = NaverProductScraper()
    products = await naver_product_scraper.search(keyword, 1)

    favorite_products = await mongodb.engine.find(ProductModel, ProductModel.is_favorite == True)
    favorite_links = [product.link for product in favorite_products]

    product_models = []

    for product in products:
        title = remove_html_tags(product["title"])
        
        product_model = ProductModel(
            keyword=keyword,
            title=title,
            image=product.get("image", ""),
            price=int(product.get("lprice", 0) or 0),
            mall_name=product.get("mallName", "") or "null",
            link=product.get("link", ""),
            brand=product.get("brand", "") or product.get("maker", "") or "null",
            category=f"{product.get('category1', '')} > {product.get('category2', '')}".strip(" >") or "null",
        )

        if product_model.link in favorite_links:
            product_model.is_favorite = True

        product_models.append(product_model)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"keyword": q, "products": product_models, "next_url": f"/search?q={q}", "title": f"'{q}' 검색 결과"},
    )


@app.post("/favorites")
async def toggle_favorite(
    request: Request,
    keyword: str = Form(""),
    title: str = Form(...),
    image: str = Form(...),
    price: int = Form(...),
    mall_name: str = Form(...),
    link: str = Form(""),
    brand: str = Form(""),
    category: str = Form(""),
    next_url: str = Form("/"),
):
    favorite_product = await mongodb.engine.find_one(
        ProductModel,
        (ProductModel.link == link)
        & (ProductModel.is_favorite == True),
    )
    if favorite_product:
        await mongodb.engine.delete(favorite_product)
    else:
        product = ProductModel(
            keyword=keyword,
            title=title,
            image=image,
            price=price,
            mall_name=mall_name,
            link=link,
            brand=brand,
            category=category,
            is_favorite=True,
        )
        await mongodb.engine.save(product)

    return RedirectResponse(url=next_url, status_code=303)


@app.get("/favorites", response_class=HTMLResponse)
async def favorites(request: Request):
    products = await mongodb.engine.find(ProductModel, ProductModel.is_favorite == True)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "저장된 위시리스트", "products": products, "next_url": "/favorites"},
    )


@app.on_event("startup")
async def on_app_start():
    print("hello server")
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    print("goodbye server")
    mongodb.close()
