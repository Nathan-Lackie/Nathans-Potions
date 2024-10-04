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

    green_potion = utils.get_potion("GREEN_POTION")

    if green_potion.quantity > 0:
        catalog.append(
            CatalogData(
                sku=green_potion.sku,
                name=green_potion.name,
                quantity=1,
                price=green_potion.price,
                potion_type=green_potion.potion_type,
            )
        )

    # TODO: re-add this when order managment works properly
    # for potion in potions:
    #     if len(catalog) >= 6:
    #         break

    #     sku = create_sku(potion.potion_type)
    #     catalog.append(
    #         CatalogData(
    #             sku=sku,
    #             name=sku,
    #             quantity=potion.quantity,
    #             price=50,
    #             potion_type=potion.potion_type,
    #         )
    #     )

    return catalog
