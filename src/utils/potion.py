from pydantic import BaseModel
import sqlalchemy
import src.database as db


class Potion(BaseModel):
    sku: str
    name: str
    potion_type: tuple[int, int, int, int]
    price: int
    quantity: int


def clear_potions():
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE potions SET quantity = 0",
            ),
        )


def get_potion(sku: str) -> Potion:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT sku, name, red, green, blue, dark, price, quantity FROM potions WHERE sku = :sku"
            ).bindparams(
                sku=sku,
            )
        ).first()

    if result is None:
        raise RuntimeError(f"Potion {sku} not found")

    return Potion(
        sku=result[0],
        name=result[1],
        potion_type=tuple(result[2:6]),
        price=result[6],
        quantity=result[7],
    )


def get_potions() -> list[Potion]:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                "SELECT sku, name, red, green, blue, dark, price, quantity FROM potions WHERE quantity > 0"
            )
        )

    return [
        Potion(
            sku=potion[0],
            name=potion[1],
            potion_type=tuple(potion[2:6]),
            price=potion[6],
            quantity=potion[7],
        )
        for potion in result
    ]


def get_total_potions() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT COALESCE(SUM(quantity), 0) FROM potions")
        ).first()

    if result is None:
        raise RuntimeError("Error totalling potion inventory")

    return result[0]


def set_potion(sku: str, amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE potions SET quantity = :amount WHERE sku = :sku",
            ).bindparams(
                sku=sku,
                amount=amount,
            ),
        )


def update_potion(sku: str, amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE potions SET quantity = quantity + :amount WHERE sku = :sku",
            ).bindparams(
                sku=sku,
                amount=amount,
            ),
        )


def update_potion_type(type: tuple[int, int, int, int], amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "UPDATE potions SET quantity = quantity + :amount WHERE red = :red AND green = :green AND blue = :blue AND dark = :dark",
            ).bindparams(
                red=type[0],
                green=type[1],
                blue=type[2],
                dark=type[3],
                amount=amount,
            ),
        )
