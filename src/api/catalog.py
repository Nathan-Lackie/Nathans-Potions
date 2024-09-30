from fastapi import APIRouter
from pydantic import BaseModel

from src.utils.potion import get_potions

router = APIRouter()


class CatalogData(BaseModel):
    sku: str
    name: str
    quantity: int
    price: int
    potion_type: tuple[int, int, int, int]


def create_sku(potion_type: tuple[int, int, int, int]):
    return f"POTION_{'_'.join([str(liquid) for liquid in potion_type])}"


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    print("Catalog requested")

    catalog: list[CatalogData] = []

    potions = get_potions()

    if len(potions) > 0:
        catalog.append(
            CatalogData(
                sku=create_sku((0, 100, 0, 0)),
                name="Green Potion",
                quantity=1,
                price=50,
                potion_type=(0, 100, 0, 0),
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
