from fastapi import APIRouter
from pydantic import BaseModel
from src import utils

router = APIRouter()


class CatalogData(BaseModel):
    sku: str
    name: str
    quantity: int
    price: int
    potion_type: tuple[int, int, int, int]


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    print("Catalog requested")

    catalog: list[CatalogData] = []

    potions = utils.get_potions()

    for potion in potions:
        if len(catalog) >= 6:
            break

        if potion.quantity == 0:
            continue

        catalog.append(
            CatalogData(
                sku=potion.sku,
                name=potion.name,
                quantity=potion.quantity,
                price=potion.price,
                potion_type=potion.potion_type,
            )
        )

    return catalog
