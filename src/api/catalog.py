from typing import Tuple
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CatalogData(BaseModel):
    sku: str
    name: str
    quantity: int
    price: int
    potion_type: Tuple[int, int, int, int]


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    return [
        CatalogData(
            sku="RED_POTION_0",
            name="red potion",
            quantity=1,
            price=50,
            potion_type=(100, 0, 0, 0),
        )
    ]
