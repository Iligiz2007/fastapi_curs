from fastapi import APIRouter
from app.schemas import Product as ProductSchemas,ProductCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.db_depends import get_db
from app.models import Product as ProductModel,Category as CategoryModel
# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/",response_model=list[ProductSchemas],status_code=status.HTTP_200_OK)
async def get_all_products(db:Session = Depends(get_db)):
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    products = db.scalars(stmt).all()

    return products


@router.post("/",response_model=ProductSchemas,status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate,db:Session = Depends(get_db)):
    stmt = select(CategoryModel).where(CategoryModel.id == product.category_id,CategoryModel.is_active == True)
    result = db.scalars(stmt).first()
    if result is None:
            raise HTTPException(status_code=400, detail="Category not found or inactive")
    
    data = product.model_dump()
    data["is_active"] = True
    db_product = ProductModel(**data)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
    


@router.get("/category/{category_id}",response_model=list[ProductSchemas],status_code=status.HTTP_200_OK)
async def get_products_by_category(category_id: int,db:Session = Depends(get_db)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    stmt = select(ProductModel).where(ProductModel.category_id == category_id,ProductModel.is_active == True)
    products = db.scalars(stmt).all()
    if products is None:
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    return products


@router.get("/{product_id}",response_model= ProductSchemas,status_code=status.HTTP_200_OK)
async def get_product(product_id: int,db:Session = Depends(get_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,ProductModel.is_active == True)
    product = db.scalars(stmt).first()
    if product is None:
        raise HTTPException(status_code=400, detail="Product not found or inactive")
    if product.category_id is None:
        raise HTTPException(status_code=400, detail="Category not found or inactive")

    return product


@router.put("/{product_id}",response_model= ProductSchemas,status_code=status.HTTP_200_OK)
async def update_product(product_id: int,product:ProductCreate,db:Session = Depends(get_db)):
    """
    Обновляет товар по его ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,ProductModel.is_active == True)
    db_product = db.scalars(stmt).first()
    if db_product is None:
            raise HTTPException(status_code=400, detail="Product not found or inactive")
    if db_product.category_id is None:
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    db.execute(update(CategoryModel).where(CategoryModel.id== product_id).values(**product))
    
    return {"message": f"Товар {product_id} обновлён (заглушка)"}


@router.delete("/{product_id}",status_code = status.HTTP_200_OK)
async def delete_product(product_id: int,db:Session = Depends(get_db)):
    """
    Удаляет товар по его ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,ProductModel.is_active == True)
    db_product = db.scalars(stmt).first()
    if db_product is None:
            raise HTTPException(status_code=400, detail="Product not found or inactive")
    if db_product.category_id is None:
        raise HTTPException(status_code=400, detail="Category not found or inactive")
    return {"message": f"Товар {product_id} удалён (заглушка)"}