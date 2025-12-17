"""Add 150 orders with order_products

Revision ID: 54ad50b71c68
Revises: 9ed9d9dcf4b2
Create Date: 2025-12-17 15:45:00.000000

"""
from typing import Sequence, Union
import uuid
import random
from datetime import datetime, timedelta
from decimal import Decimal

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54ad50b71c68'
down_revision: Union[str, None] = '9ed9d9dcf4b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    
    # Получаем пользователей
    result = connection.execute(sa.text("SELECT id FROM users"))
    users = [row[0] for row in result]
    
    if not users:
        print("Warning: No users found. Skipping order creation.")
        return
    
    # Получаем заказчиков с их user_id
    result = connection.execute(sa.text("SELECT id, user_id FROM customers"))
    customers = [(row[0], row[1]) for row in result]
    
    if not customers:
        print("Warning: No customers found. Skipping order creation.")
        return
    
    # Получаем продукты с их user_id и ценой
    result = connection.execute(sa.text("SELECT id, user_id, price FROM products"))
    products = [(row[0], row[1], row[2]) for row in result]
    
    if not products:
        print("Warning: No products found. Skipping order creation.")
        return
    
    # Группируем заказчиков и продукты по user_id
    customers_by_user = {}
    for customer_id, user_id in customers:
        if user_id not in customers_by_user:
            customers_by_user[user_id] = []
        customers_by_user[user_id].append(customer_id)
    
    products_by_user = {}
    for product_id, user_id, price in products:
        if user_id not in products_by_user:
            products_by_user[user_id] = []
        products_by_user[user_id].append((product_id, price))
    
    # Пользователи, у которых есть и заказчики, и продукты
    valid_users = [u for u in users if u in customers_by_user and u in products_by_user]
    
    if not valid_users:
        print("Warning: No users with both customers and products. Skipping order creation.")
        return
    
    # Создаем 150 заказов
    # Получаем текущий максимальный номер заказа для каждого пользователя
    result = connection.execute(sa.text("SELECT user_id, COALESCE(MAX(number), 0) FROM orders GROUP BY user_id"))
    existing_max_numbers = {row[0]: row[1] for row in result}
    
    # Счетчик номеров заказов для каждого пользователя (начинаем с max+1)
    order_numbers_by_user = {u: existing_max_numbers.get(u, 0) + 1 for u in valid_users}
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(150):
        user_id = random.choice(valid_users)
        customer_id = random.choice(customers_by_user[user_id])
        order_id = str(uuid.uuid4())
        
        # Получаем и увеличиваем номер заказа для этого пользователя
        order_number = order_numbers_by_user[user_id]
        order_numbers_by_user[user_id] += 1
        
        # Случайная дата за последний год
        created_at = base_date + timedelta(days=random.randint(0, 365), 
                                           hours=random.randint(8, 20),
                                           minutes=random.randint(0, 59))
        
        # Создаем заказ
        connection.execute(
            sa.text("""
                INSERT INTO orders (id, number, created_at, customer_id, user_id)
                VALUES (:id, :number, :created_at, :customer_id, :user_id)
            """),
            {
                'id': order_id,
                'number': order_number,
                'created_at': created_at,
                'customer_id': customer_id,
                'user_id': user_id
            }
        )
        
        # Добавляем от 1 до 5 позиций в заказ
        user_products = products_by_user[user_id]
        num_items = random.randint(1, min(5, len(user_products)))
        selected_products = random.sample(user_products, num_items)
        
        for product_id, product_price in selected_products:
            order_product_id = str(uuid.uuid4())
            quantity = random.randint(1, 10)
            # Цена может отличаться от текущей (скидка или наценка ±10%)
            price_modifier = random.uniform(0.9, 1.1)
            price = Decimal(str(round(float(product_price) * price_modifier, -2)))
            if price < 100:
                price = Decimal('100')
            
            connection.execute(
                sa.text("""
                    INSERT INTO order_products (id, quantity, price, order_id, product_id)
                    VALUES (:id, :quantity, :price, :order_id, :product_id)
                """),
                {
                    'id': order_product_id,
                    'quantity': quantity,
                    'price': price,
                    'order_id': order_id,
                    'product_id': product_id
                }
            )
        
    connection.commit()


def downgrade() -> None:
    op.execute("DELETE FROM order_products")
    op.execute("DELETE FROM orders")
