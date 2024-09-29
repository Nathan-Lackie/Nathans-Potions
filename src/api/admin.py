from fastapi import APIRouter, Depends
from src.api import auth
from src.utils.gold import set_gold
from src.utils.liquid import set_liquid
from src.utils.potion import clear_potions

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
    set_gold(100)

    clear_potions()

    set_liquid((0, 0, 0, 0))

    return "OK"
