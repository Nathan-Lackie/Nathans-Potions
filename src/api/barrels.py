from typing import Literal
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


def potion_from_color(color: Literal["red", "green", "blue", "dark"]):
    if color == "red":
        return (1, 0, 0, 0)

    if color == "green":
        return (0, 1, 0, 0)

    if color == "blue":
        return (0, 0, 1, 0)

    if color == "dark":
        return (0, 0, 0, 1)

    raise RuntimeError(f"Invalid color: {color}")


def find_greatest_barrel(
    wholesale_catalog: list[Barrel],
    potion_type: tuple[int, int, int, int],
    capacity: int,
    current_gold: int,
):
    greatest_barrel = None

    for barrel in wholesale_catalog:
        if (
            barrel.potion_type != potion_type
            or barrel.ml_per_barrel > capacity
            or barrel.price > current_gold
        ):
            continue

        if (
            greatest_barrel is None
            or barrel.ml_per_barrel > greatest_barrel.ml_per_barrel
        ):
            greatest_barrel = barrel

    return greatest_barrel


# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]) -> list[PurchasePlan]:
    """ """
    print(f"wholesale catalog: {wholesale_catalog}")

    current_liquid = utils.get_liquid()
    current_gold = utils.get_gold()
    current_liquid_capacity = utils.get_liquid_capacity() // 4

    purchase_plan: list[PurchasePlan] = []

    for color in current_liquid:
        if current_liquid[color] == 0:
            greatest_barrel = find_greatest_barrel(
                wholesale_catalog,
                potion_from_color(color),
                current_liquid_capacity,
                current_gold,
            )

            if greatest_barrel is not None:
                purchase_plan.append(PurchasePlan(sku=greatest_barrel.sku, quantity=1))
                current_gold -= greatest_barrel.price

    return purchase_plan
