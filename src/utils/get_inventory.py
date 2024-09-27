from pydantic import BaseModel
import sqlalchemy
from src import database as db


class Inventory(BaseModel):
    num_green_potions: int
    num_green_ml: int
    gold: int


def get_inventory_db():
    with db.engine.begin() as connection:
        result = (
            connection.execute(sqlalchemy.text("SELECT * FROM global_inventory"))
            .mappings()
            .first()
        )

        if result is None:
            raise Exception("Global inventory table is empty!")

        return Inventory(
            num_green_potions=result["num_green_potions"],
            num_green_ml=result["num_green_ml"],
            gold=result["gold"],
        )
