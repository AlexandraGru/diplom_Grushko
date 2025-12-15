"""Add 100 users with Russian phone numbers

Revision ID: dbf17d2f10c7
Revises: 04c701a89a47
Create Date: 2025-12-15 18:34:50.403993

"""
from typing import Sequence, Union
import uuid
import random

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbf17d2f10c7'
down_revision: Union[str, None] = '04c701a89a47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Русские имена для генерации данных
SURNAMES = [
    'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Соколов',
    'Лебедев', 'Козлов', 'Новиков', 'Морозов', 'Петров', 'Волков', 'Соловьев',
    'Васильев', 'Зайцев', 'Павлов', 'Семенов', 'Голубев', 'Виноградов',
    'Богданов', 'Воробьев', 'Федоров', 'Михайлов', 'Орлов', 'Филиппов',
    'Марков', 'Новиков', 'Морозов', 'Волков', 'Алексеев', 'Лебедев',
    'Семенов', 'Егоров', 'Павлов', 'Козлов', 'Степанов', 'Николаев',
    'Орлов', 'Андреев', 'Макаров', 'Никитин', 'Захаров', 'Зайцев',
    'Соловьев', 'Борисов', 'Яковлев', 'Григорьев', 'Романов', 'Воробьев'
]

NAMES = [
    'Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей', 'Алексей', 'Артем',
    'Илья', 'Кирилл', 'Михаил', 'Никита', 'Матвей', 'Роман', 'Егор',
    'Арсений', 'Иван', 'Денис', 'Евгений', 'Тимофей', 'Владислав',
    'Игорь', 'Владимир', 'Павел', 'Руслан', 'Марк', 'Лев', 'Дмитрий',
    'Антон', 'Николай', 'Данил', 'Олег', 'Вадим', 'Игорь', 'Степан',
    'Юрий', 'Борис', 'Ярослав', 'Эдуард', 'Валерий', 'Григорий',
    'Мария', 'Анна', 'Виктория', 'Екатерина', 'Наталья', 'Марина',
    'Ольга', 'Елена', 'Светлана', 'Татьяна', 'Ирина', 'Юлия', 'Анастасия',
    'Дарья', 'Евгения', 'Ксения', 'Алина', 'Валерия', 'Полина', 'Вероника',
    'Александра', 'Кристина', 'София', 'Диана', 'Арина', 'Милана', 'Алиса'
]

PATRONYMICS = [
    'Александрович', 'Дмитриевич', 'Максимович', 'Сергеевич', 'Андреевич',
    'Алексеевич', 'Артемович', 'Ильич', 'Кириллович', 'Михайлович',
    'Никитич', 'Матвеевич', 'Романович', 'Егорович', 'Арсеньевич',
    'Иванович', 'Денисович', 'Евгеньевич', 'Тимофеевич', 'Владиславович',
    'Александровна', 'Дмитриевна', 'Максимовна', 'Сергеевна', 'Андреевна',
    'Алексеевна', 'Артемовна', 'Ильинична', 'Кирилловна', 'Михайловна',
    'Никитична', 'Матвеевна', 'Романовна', 'Егоровна', 'Арсеньевна',
    'Ивановна', 'Денисовна', 'Евгеньевна', 'Тимофеевна', 'Владиславовна'
]


def generate_phone_number() -> str:
    """Генерирует российский номер телефона +7XXXXXXXXXX"""
    # Российские коды операторов (первые 3 цифры после +7)
    operator_codes = ['900', '901', '902', '903', '904', '905', '906', '907', 
                      '908', '909', '910', '911', '912', '913', '914', '915',
                      '916', '917', '918', '919', '920', '921', '922', '923',
                      '924', '925', '926', '927', '928', '929', '930', '931',
                      '932', '933', '934', '936', '937', '938', '939', '950',
                      '951', '952', '953', '954', '955', '956', '957', '958',
                      '959', '960', '961', '962', '963', '964', '965', '966',
                      '967', '968', '969', '977', '978', '980', '981', '982',
                      '983', '984', '985', '986', '987', '988', '989', '991',
                      '992', '993', '994', '995', '996', '997', '999']
    code = random.choice(operator_codes)
    # Остальные 7 цифр
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f'+7{code}{number}'


def generate_inn() -> str:
    """Генерирует ИНН (12 цифр для физических лиц)"""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])


def upgrade() -> None:
    # Создаем список из 100 пользователей
    users_data = []
    used_phones = set()
    used_inns = set()
    
    for i in range(100):
        # Генерируем уникальные телефон и ИНН
        while True:
            phone = generate_phone_number()
            if phone not in used_phones:
                used_phones.add(phone)
                break
        
        while True:
            inn = generate_inn()
            if inn not in used_inns:
                used_inns.add(inn)
                break
        
        user_id = str(uuid.uuid4())
        surname = random.choice(SURNAMES)
        name = random.choice(NAMES)
        patronymic = random.choice(PATRONYMICS) if random.random() > 0.1 else None  # 90% с отчеством
        
        users_data.append({
            'id': user_id,
            'surname': surname,
            'name': name,
            'patronymic': patronymic,
            'phone_number': phone,
            'inn': inn,
            'role': 'user'
        })
    
    # Вставляем данные через op.get_bind()
    connection = op.get_bind()
    
    for user in users_data:
        if user['patronymic']:
            connection.execute(
                sa.text("""
                    INSERT INTO users (id, surname, name, patronymic, phone_number, inn, role)
                    VALUES (:id, :surname, :name, :patronymic, :phone_number, :inn, :role)
                """),
                {
                    'id': user['id'],
                    'surname': user['surname'],
                    'name': user['name'],
                    'patronymic': user['patronymic'],
                    'phone_number': user['phone_number'],
                    'inn': user['inn'],
                    'role': user['role']
                }
            )
        else:
            connection.execute(
                sa.text("""
                    INSERT INTO users (id, surname, name, phone_number, inn, role)
                    VALUES (:id, :surname, :name, :phone_number, :inn, :role)
                """),
                {
                    'id': user['id'],
                    'surname': user['surname'],
                    'name': user['name'],
                    'phone_number': user['phone_number'],
                    'inn': user['inn'],
                    'role': user['role']
                }
            )
    
    connection.commit()


def downgrade() -> None:
    # Удаляем всех пользователей, созданных этой миграцией
    # Удаляем пользователей с российскими номерами (+7...)
    op.execute("DELETE FROM users WHERE phone_number LIKE '+7%'")

