"""Add OTP records with various scenarios

Revision ID: 082450edab94
Revises: 54ad50b71c68
Create Date: 2025-12-17 16:00:00.000000

"""
from typing import Sequence, Union
import uuid
import random
from datetime import datetime, timedelta

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '082450edab94'
down_revision: Union[str, None] = '54ad50b71c68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def generate_phone() -> str:
    """Генерирует российский номер телефона"""
    codes = ['900', '901', '902', '903', '904', '905', '906', '907', '908', '909',
             '910', '911', '912', '913', '914', '915', '916', '917', '918', '919',
             '920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
             '950', '951', '952', '953', '960', '961', '962', '963', '964', '965',
             '966', '967', '968', '969', '977', '978', '980', '981', '982', '983',
             '984', '985', '986', '987', '988', '989', '991', '992', '993', '999']
    code = random.choice(codes)
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f'+7{code}{number}'


def upgrade() -> None:
    connection = op.get_bind()
    
    now = datetime.now()
    otp_records = []
    
    # 1. Нормальные запросы - успешно использованные коды (50 шт)
    for i in range(50):
        phone = generate_phone()
        created_at = now - timedelta(days=random.randint(1, 30), 
                                     hours=random.randint(0, 23),
                                     minutes=random.randint(0, 59))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': True
        })
    
    # 2. Неиспользованные коды - истекшие (30 шт)
    for i in range(30):
        phone = generate_phone()
        created_at = now - timedelta(days=random.randint(1, 7),
                                     hours=random.randint(0, 23))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': False
        })
    
    # 3. Подозрительно: много запросов с одного номера (брутфорс)
    bruteforce_phone = '+79991234567'
    for i in range(20):
        created_at = now - timedelta(minutes=random.randint(1, 30))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': bruteforce_phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': False
        })
    
    # 4. Подозрительно: запросы в ночное время (2-5 утра)
    for i in range(15):
        phone = generate_phone()
        night_hour = random.randint(2, 5)
        created_at = now.replace(hour=night_hour, minute=random.randint(0, 59)) - timedelta(days=random.randint(0, 5))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': random.choice([True, False])
        })
    
    # 5. Подозрительно: последовательные номера телефонов (перебор)
    base_number = '+7999000'
    for i in range(10):
        phone = f'{base_number}{str(i).zfill(4)}'
        created_at = now - timedelta(hours=random.randint(1, 3))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': False
        })
    
    # 6. Подозрительно: один код запрашивается много раз (повтор)
    suspicious_phone = '+79998887766'
    same_code = 1234
    for i in range(8):
        created_at = now - timedelta(minutes=i * 2)
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': suspicious_phone,
            'code': same_code,
            'created_at': created_at,
            'is_used': False
        })
    
    # 7. Подозрительно: очень старые неиспользованные коды
    for i in range(10):
        phone = generate_phone()
        created_at = now - timedelta(days=random.randint(60, 180))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': False
        })
    
    # 8. Свежие активные коды (ожидают использования)
    for i in range(10):
        phone = generate_phone()
        created_at = now - timedelta(minutes=random.randint(1, 5))
        otp_records.append({
            'id': str(uuid.uuid4()),
            'phone_number': phone,
            'code': random.randint(1000, 9999),
            'created_at': created_at,
            'is_used': False
        })
    
    # Вставляем все записи
    for otp in otp_records:
        connection.execute(
            sa.text("""
                INSERT INTO one_time_passwords (id, phone_number, code, created_at, is_used)
                VALUES (:id, :phone_number, :code, :created_at, :is_used)
            """),
            otp
        )
    
    connection.commit()


def downgrade() -> None:
    op.execute("DELETE FROM one_time_passwords")
