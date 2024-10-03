from pydantic import BaseModel
import sqlalchemy
from src import database as db


class Customer(BaseModel):
    customer_name: str
    character_class: str
    level: int


def set_customers(customers: list[Customer]):
    with db.engine.begin() as connection:
        for customer in customers:
            connection.execute(
                sqlalchemy.text(
                    "INSERT INTO customers (name, character_class, level) VALUES (:name, :character_class, :level) ON CONFLICT DO NOTHING",
                ).bindparams(
                    name=customer.customer_name,
                    character_class=customer.character_class,
                    level=customer.level,
                ),
            )
