from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Acme Retail Inventory Management System",
    description="Inventory Management REST API",
    version="1.0.0",
    docs_url="/doc",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ---------------------------------------------------------
# Data models
# ---------------------------------------------------------

class Product(BaseModel):
    sku: str
    name: str
    quantity: int = 0
    price: Optional[float] = None


class StockUpdate(BaseModel):
    quantity: int


# ---------------------------------------------------------
# Temporary in-memory database
# ---------------------------------------------------------

products: dict[str, dict] = {}


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/", summary="Root")
def root():
    return {
        "service": "inventory-management-system",
        "version": "1.0.0",
        "status": "running",
    }


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "ok",
    }


# ---------------------------------------------------------
# Get all products
# ---------------------------------------------------------

@app.get("/products", summary="Get Products")
def get_products():
    return list(products.values())


# ---------------------------------------------------------
# Create product
# ---------------------------------------------------------

@app.post("/products", summary="Create Product")
def create_product(product: Product):

    if product.sku in products:
        raise HTTPException(
            status_code=409,
            detail="Product already exists",
        )

    products[product.sku] = product.model_dump()

    return products[product.sku]


# ---------------------------------------------------------
# Search products
# Important: keep this endpoint before /products/{sku}
# ---------------------------------------------------------

@app.get("/products/search", summary="Search Products")
def search_products(q: str):

    query = q.lower()

    return [
        product
        for product in products.values()
        if query in product["name"].lower()
        or query in product["sku"].lower()
    ]


# ---------------------------------------------------------
# Low-stock products
# ---------------------------------------------------------

@app.get(
    "/products/low-stock",
    summary="Get Low Stock Products",
)
def get_low_stock_products(threshold: int = 5):

    return [
        product
        for product in products.values()
        if 0 < product["quantity"] <= threshold
    ]


# ---------------------------------------------------------
# Out-of-stock products
# ---------------------------------------------------------

@app.get(
    "/products/out-of-stock",
    summary="Get Out Of Stock Products",
)
def get_out_of_stock_products():

    return [
        product
        for product in products.values()
        if product["quantity"] == 0
    ]


# ---------------------------------------------------------
# Stock IN
# ---------------------------------------------------------

@app.post(
    "/products/{sku}/stock/in",
    summary="Stock In",
)
def stock_in(sku: str, stock: StockUpdate):

    if sku not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if stock.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero",
        )

    products[sku]["quantity"] += stock.quantity

    return {
        "message": "Stock added successfully",
        "product": products[sku],
    }


# ---------------------------------------------------------
# Stock OUT
# ---------------------------------------------------------

@app.post(
    "/products/{sku}/stock/out",
    summary="Stock Out",
)
def stock_out(sku: str, stock: StockUpdate):

    if sku not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if stock.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero",
        )

    current_quantity = products[sku]["quantity"]

    if stock.quantity > current_quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock",
        )

    products[sku]["quantity"] -= stock.quantity

    return {
        "message": "Stock removed successfully",
        "product": products[sku],
    }


# ---------------------------------------------------------
# Product status
# ---------------------------------------------------------

@app.get(
    "/products/{sku}/status",
    summary="Get Product Status",
)
def get_product_status(sku: str):

    if sku not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    quantity = products[sku]["quantity"]

    if quantity == 0:
        status = "out-of-stock"

    elif quantity <= 5:
        status = "low-stock"

    else:
        status = "in-stock"

    return {
        "sku": sku,
        "quantity": quantity,
        "status": status,
    }


# ---------------------------------------------------------
# Get individual product
# ---------------------------------------------------------

@app.get(
    "/products/{sku}",
    summary="Get Product",
)
def get_product(sku: str):

    if sku not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return products[sku]


# ---------------------------------------------------------
# Update product
# ---------------------------------------------------------

@app.put(
    "/products/{sku}",
    summary="Update Product",
)
def update_product(
    sku: str,
    product: Product,
):

    if sku not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    updated_product = product.model_dump()

    # URL SKU remains authoritative
    updated_product["sku"] = sku

    products[sku] = updated_product

    return products[sku]


# ---------------------------------------------------------
# Delete product
# ---------------------------------------------------------

@app.delete(
    "/products/{sku}",
    summary="Delete Product",
)
def delete_product(sku: str):

    if sku not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    deleted_product = products.pop(sku)

    return {
        "message": "Product deleted successfully",
        "product": deleted_product,
    }