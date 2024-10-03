from fastapi import APIRouter, Depends
from src.api import auth
from src import utils

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.post("/reset")
def reset():
    """
    Reset the game state. Gold goes to 100, all potions are removed from
    inventory, and all barrels are removed from inventory. Carts are all reset.
    """
    utils.set_gold(100)

    utils.clear_potions()

    utils.set_liquid((0, 0, 0, 0))

    return "OK"
