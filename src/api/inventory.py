from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import utils

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(auth.get_api_key)],
)


class Inventory(BaseModel):
    number_of_potions: int
    ml_in_barrels: int
    gold: int


@router.get("/audit")
def get_inventory():
    """ """

    return Inventory(
        number_of_potions=utils.get_total_potions(),
        ml_in_barrels=utils.get_total_liquid(),
        gold=utils.get_gold(),
    )


# Gets called once a day
@router.post("/plan")
def get_capacity_plan():
    """
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional
    capacity unit costs 1000 gold.
    """
    current_gold = utils.get_gold()
    current_liquid_capacity = utils.get_liquid_capacity()
    current_potion_capacity = utils.get_potion_capacity()

    cant_afford_capacity = current_gold // 4 <= 1000
    have_full_capacity = current_potion_capacity >= 4 and current_liquid_capacity >= 4

    if cant_afford_capacity or have_full_capacity:
        return {"potion_capacity": 0, "ml_capacity": 0}

    if current_potion_capacity < current_liquid_capacity:
        return {"potion_capacity": 1, "ml_capacity": 0}
    else:
        return {"potion_capacity": 0, "ml_capacity": 1}


class CapacityPurchase(BaseModel):
    potion_capacity: int
    ml_capacity: int


# Gets called once a day
@router.post("/deliver/{order_id}")
def deliver_capacity_plan(capacity_purchase: CapacityPurchase, order_id: int):
    """
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional
    capacity unit costs 1000 gold.
    """

    utils.update_gold(
        -1000 * (capacity_purchase.ml_capacity + capacity_purchase.potion_capacity)
    )
    utils.update_liquid_capacity(capacity_purchase.ml_capacity)
    utils.update_potion_capacity(capacity_purchase.potion_capacity)

    return "OK"
