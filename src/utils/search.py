from datetime import datetime
from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
import sqlalchemy
from src import database as db


class Order(BaseModel):
    id: int
    customer: str
    item: str
    quantity: int
    gold: int
    time: datetime


class SearchResult(BaseModel):
    has_next_page: bool
    orders: List[Order]


def search_orders(
    page: int,
    customer: str,
    name: str,
    order: str,
    direction: str,
):
    if order not in ["customer", "item", "gold", "timestamp"]:
        raise HTTPException(400, "Invalid order column")

    if direction not in ["ASC", "DESC"]:
        raise HTTPException(400, "Invalid order direction")

    with db.engine.begin() as connection:
        items = (
            connection.execute(
                sqlalchemy.text(
                    f"""SELECT carts.id, customers.name as customer, catalog.name as item, carts.quantity as quantity, price * quantity as gold, timestamp as time FROM carts
                JOIN visits ON carts.visit_id = visits.id
                JOIN customers ON visits.customer_id = customers.id
                JOIN catalog ON carts.potion_sku = catalog.sku
                WHERE position(lower(:customer) IN lower(customers.name)) > 0 AND position(lower(:name) IN lower(catalog.name)) > 0
                ORDER BY {order} {direction}
                LIMIT 6
                OFFSET :page * 5"""
                ).bindparams(
                    customer=customer,
                    name=name,
                    page=page - 1,
                )
            )
            .mappings()
            .all()
        )

        has_next_page = len(items) > 5

        return SearchResult(
            has_next_page=has_next_page,
            orders=[Order(**item) for item in items[:5]],
        )
