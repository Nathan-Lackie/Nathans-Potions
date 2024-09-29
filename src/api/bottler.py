from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src.utils.liquid import get_liquid, update_liquid
from src.utils.potion import PotionInventory, update_potion

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)


class BottlePlan(BaseModel):
    potion_type: tuple[int, int, int, int]
    quantity: int


@router.post("/deliver/{order_id}")
def post_deliver_bottles(potions_delivered: list[PotionInventory], order_id: int):
    """ """
    print(f"potions delievered: {potions_delivered} order_id: {order_id}")

    for potion in potions_delivered:
        update_liquid(
            tuple(-liquid * potion.quantity for liquid in potion.potion_type)  # type: ignore
        )
        update_potion(potion.potion_type, potion.quantity)

    return "OK"


@router.post("/plan")
def get_bottle_plan() -> list[BottlePlan]:
    """
    Go from barrel to bottle.
    """

    liquid = get_liquid()

    if liquid["green"] >= 100:
        return [
            BottlePlan(
                potion_type=(0, 100, 0, 0),
                quantity=liquid["green"] // 100,
            )
        ]
    else:
        return []


if __name__ == "__main__":
    print(get_bottle_plan())
