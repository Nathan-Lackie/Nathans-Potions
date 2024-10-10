from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import utils
from src.utils.potion import Potion


router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)


class PotionInventory(BaseModel):
    potion_type: tuple[int, int, int, int]
    quantity: int


class BottlePlan(BaseModel):
    potion_type: tuple[int, int, int, int]
    quantity: int


@router.post("/deliver/{order_id}")
def post_deliver_bottles(potions_delivered: list[PotionInventory], order_id: int):
    """ """
    print(f"potions delievered: {potions_delivered} order_id: {order_id}")

    for potion in potions_delivered:
        utils.update_liquid(
            tuple(-liquid * potion.quantity for liquid in potion.potion_type)  # type: ignore
        )
        utils.update_potion_type(potion.potion_type, potion.quantity)

    return "OK"


def add_potion_to_plan(
    bottle_plan: list[BottlePlan], potion_type: tuple[int, int, int, int]
):
    for plan in bottle_plan:
        if plan.potion_type == potion_type:
            plan.quantity += 1
            return

    bottle_plan.append(BottlePlan(potion_type=potion_type, quantity=1))


def can_afford_potion(potion: Potion, current_liquid: tuple[int, int, int, int]):
    for i in range(4):
        if current_liquid[i] < potion.potion_type[i]:
            return False

    return True


@router.post("/plan")
def get_bottle_plan() -> list[BottlePlan]:
    """
    Go from barrel to bottle.
    """

    liquid: tuple[int, int, int, int] = utils.get_liquid_tuple()
    potions = utils.get_potions()
    total_potions = sum([potion.quantity for potion in potions])
    capacity = utils.get_potion_capacity()

    potions.sort(key=lambda potion: potion.quantity)

    bottle_plan: list[BottlePlan] = []

    # We want to ensure potions are bottled evenly
    # We do this by always adding quantity to the smallest element in the potion list, while keeping it sorted
    # If we don't have enough liquid for a potion type, or we've reached the desired quantity for that potion type, we remove it from the list
    # We continue this until either the potion list is empty, or we run out of potion capacity
    i = 0
    while len(potions) > 0 and total_potions < capacity:
        desired_quantity = potions[i].desired_quantity
        reached_desired_quantity = (
            desired_quantity is not None and potions[i].quantity >= desired_quantity
        )

        # If we can't afford a potion, or we've reached the desired quantity, remove it from the list
        if not can_afford_potion(potions[i], liquid) or reached_desired_quantity:
            potions.pop(i)
            i = max(0, i - 1)
        # Navigate to the smallest element in the list
        elif i != 0 and potions[i - 1].quantity < potions[i].quantity:
            i -= 1
        elif i != len(potions) - 1 and potions[i].quantity >= potions[i + 1].quantity:
            i += 1
        # Add to the potion plan
        else:
            add_potion_to_plan(bottle_plan, potions[i].potion_type)
            potions[i].quantity += 1
            total_potions += 1
            liquid = tuple([liquid[j] - potions[i].potion_type[j] for j in range(4)])  # type: ignore

    return bottle_plan


if __name__ == "__main__":
    print(get_bottle_plan())
