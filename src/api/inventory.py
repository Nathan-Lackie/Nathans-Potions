from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src.utils.gold import get_gold
from src.utils.liquid import get_total_liquid
from src.utils.potion import get_total_potions

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
        number_of_potions=get_total_potions(),
        ml_in_barrels=get_total_liquid(),
        gold=get_gold(),
    )


# Gets called once a day
@router.post("/plan")
def get_capacity_plan():
    """
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional
    capacity unit costs 1000 gold.
    """

    return {"potion_capacity": 0, "ml_capacity": 0}


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

    return "OK"
