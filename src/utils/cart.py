from pydantic import BaseModel
import sqlalchemy
from src import database as db, utils


class CartItem(BaseModel):
    sku: str
    price: int
    quantity: int


class CardCheckout(BaseModel):
    potions: int
    gold: int


def add_to_cart(cart_id: int, sku: str, quantity: int):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO carts (id, potion_sku, quantity) VALUES (:id, :sku, :quantity)"
            ).bindparams(id=cart_id, sku=sku, quantity=quantity)
        )


def get_contents(cart_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """SELECT sku, potions.price, carts.quantity FROM potions
                JOIN carts ON carts.potion_sku = potions.sku
                WHERE carts.id = :id"""
            ).bindparams(id=cart_id)
        )

    return [CartItem(sku=item[0], price=item[1], quantity=item[2]) for item in result]


def checkout_cart(cart_id: int):
    cart_items = get_contents(cart_id)

    total_price = 0
    total_quantity = 0
    for item in cart_items:
        total_price += item.quantity * item.price
        total_quantity += item.quantity
        utils.update_potion(item.sku, -item.quantity)

    utils.update_gold(total_price)

    return CardCheckout(potions=total_quantity, gold=total_price)
