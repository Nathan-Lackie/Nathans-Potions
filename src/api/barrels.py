from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import utils

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)


class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: tuple[int, int, int, int]
    price: int

    quantity: int


class PurchasePlan(BaseModel):
    sku: str
    quantity: int


def search_catalog(wholesale_catalog: list[Barrel], sku: str):
    for barrel in wholesale_catalog:
        if barrel.sku == sku:
            return barrel
    return None


def liquid_in_barrel(barrel: Barrel) -> tuple[int, int, int, int]:
    return tuple(
        liquid * barrel.ml_per_barrel * barrel.quantity for liquid in barrel.potion_type
    )  # type: ignore


@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    """ """
    print(f"barrels delievered: {barrels_delivered} order_id: {order_id}")
    for barrel in barrels_delivered:
        utils.update_liquid(liquid_in_barrel(barrel))
        utils.update_gold(-barrel.price * barrel.quantity)

    return "OK"


# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]) -> list[PurchasePlan]:
    """ """
    print(f"wholesale catalog: {wholesale_catalog}")

    current_green_potions = utils.get_potion("GREEN_POTION").quantity
    current_liquid = utils.get_liquid()["green"]
    current_gold = utils.get_gold()
    current_liquid_capacity = utils.get_liquid_capacity()

    green_barrel = search_catalog(wholesale_catalog, "SMALL_GREEN_BARREL")

    if (
        current_green_potions < 10
        and green_barrel
        and green_barrel.price <= current_gold
        and green_barrel.quantity > 0
        and current_liquid < current_liquid_capacity
    ):
        return [
            PurchasePlan(
                sku="SMALL_GREEN_BARREL",
                quantity=1,
            )
        ]
    else:
        return []
