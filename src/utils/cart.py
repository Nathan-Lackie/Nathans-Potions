import sqlalchemy
from src import database as db


def add_to_cart(cart_id: int, sku: str, quantity: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO carts (id, potion_sku, quantity) VALUES (:id, :sku, :quantity)"
            ).bindparams(id=cart_id, sku=sku, quantity=quantity)
        )
