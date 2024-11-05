from pydantic import BaseModel
import sqlalchemy
import src.database as db


class Potion(BaseModel):
    sku: str
    name: str
    potion_type: tuple[int, int, int, int]
    price: int
    quantity: int
    desired_quantity: int | None
    show_in_catalog: bool


def reset_potions():
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "DELETE FROM potions",
            ),
        )


def get_potion(sku: str) -> Potion:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """SELECT catalog.sku, name, red, green, blue, dark, price, COALESCE(SUM(update), 0) as quantity, desired_quantity, show_in_catalog FROM catalog
                LEFT JOIN potions ON catalog.sku = potions.sku
                WHERE catalog.sku = :sku
                GROUP BY catalog.sku"""
            ).bindparams(
                sku=sku,
            )
        ).one()

    return Potion(
        sku=result.sku,
        name=result.name,
        potion_type=(result.red, result.green, result.blue, result.dark),
        price=result.price,
        quantity=result.quantity,
        desired_quantity=result.desired_quantity,
        show_in_catalog=result.show_in_catalog,
    )


def get_potions() -> list[Potion]:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """SELECT catalog.sku, name, red, green, blue, dark, price, COALESCE(SUM(update), 0) as quantity, desired_quantity, show_in_catalog FROM catalog
                LEFT JOIN potions ON catalog.sku = potions.sku
                GROUP BY catalog.sku"""
            )
        )

    return [
        Potion(
            sku=potion.sku,
            name=potion.name,
            potion_type=(potion.red, potion.green, potion.blue, potion.dark),
            price=potion.price,
            quantity=potion.quantity,
            desired_quantity=potion.desired_quantity,
            show_in_catalog=potion.show_in_catalog,
        )
        for potion in result
    ]


def get_total_potions() -> int:
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT COALESCE(SUM(update), 0) as quantity FROM potions")
        ).one()

    return result.quantity


def update_potion(sku: str, amount: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO potions (sku, update) VALUES (:sku, :amount)",
            ).bindparams(
                sku=sku,
                amount=amount,
            ),
        )


def update_potion_type(type: tuple[int, int, int, int], amount: int):
    with db.engine.begin() as connection:
        sku = connection.execute(
            sqlalchemy.text(
                "SELECT sku FROM catalog WHERE red = :red AND green = :green AND blue = :blue AND dark = :dark",
            ).bindparams(
                red=type[0],
                green=type[1],
                blue=type[2],
                dark=type[3],
            )
        ).one()

        connection.execute(
            sqlalchemy.text(
                "INSERT INTO potions (sku, update) VALUES (:sku, :amount)",
            ).bindparams(
                sku=sku[0],
                amount=amount,
            ),
        )
