from pydantic import BaseModel


class CartItemAdd(BaseModel):
    product_id: int
    quantidade: int = 1


class CartItemUpdate(BaseModel):
    cart_item_id: int
    quantidade: int


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    total: float
