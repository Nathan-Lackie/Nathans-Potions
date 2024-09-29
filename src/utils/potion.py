from pydantic import BaseModel
import sqlalchemy
import src.database as db


class PotionInventory(BaseModel):
    potion_type: tuple[int, int, int, int]
    quantity: int


def check_potion(potion: tuple[int, int, int, int]):
    if sum(potion) != 100:
        raise RuntimeError("Invalid potion: " + str(potion))


def clear_potions():
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE potion_inventory SET quantity = 0",
            ),
        )


def get_potion(potion_type: tuple[int, int, int, int]) -> int:
    check_potion(potion_type)

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT quantity FROM potion_inventory WHERE red = :red AND green = :green AND blue = :blue AND dark = :dark"
            ).bindparams(
                red=potion_type[0],
                green=potion_type[1],
                blue=potion_type[2],
                dark=potion_type[3],
            )
        ).first()

    if result is None:
        return 0

    return result[0]


def get_potions():
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT red, green, blue, dark, quantity FROM potion_inventory WHERE quantity > 0"
            )
        )

    return [
        PotionInventory(potion_type=tuple(potion[0:4]), quantity=potion[4])
        for potion in result
    ]


def set_potion(potion_type: tuple[int, int, int, int], amount: int):
    check_potion(potion_type)

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """INSERT INTO potion_inventory (red, green, blue, dark, quantity)
                VALUES (:red, :green, :blue, :dark, :amount)
                ON CONFLICT (red, green, blue, dark) DO UPDATE SET quantity = :amount""",
            ).bindparams(
                red=potion_type[0],
                green=potion_type[1],
                blue=potion_type[2],
                dark=potion_type[3],
                amount=amount,
            ),
        )


def update_potion(potion_type: tuple[int, int, int, int], amount: int):
    check_potion(potion_type)

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """INSERT INTO potion_inventory (red, green, blue, dark, quantity)
                VALUES (:red, :green, :blue, :dark, :amount)
                ON CONFLICT (red, green, blue, dark) DO UPDATE SET quantity = potion_inventory.quantity + :amount""",
            ).bindparams(
                red=potion_type[0],
                green=potion_type[1],
                blue=potion_type[2],
                dark=potion_type[3],
                amount=amount,
            ),
        )
