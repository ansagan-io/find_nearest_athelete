import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)

class Atheletes(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

engine = sa.create_engine(DB_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
users = session.query(User).all()
atheletes = session.query(Atheletes).all()
user_ids = []

for user in users:
    user_ids.append(user.id)

def date_convert(birthday):
    x = birthday.split("-")
    a = (int(x[0])-1900)*365
    b = (int(x[1]))*round((365/12))
    days = int(x[2])+a+b

    return days

athelete_height_dict = {}
athelete_birth_dict = {}

def find_nearest(given_value, a_list):

    delta = float()
    found = float()
    for num in a_list:
        if num != None:
            felta = float(num) - float(given_value)
            if delta == 0:
                delta = float(abs(felta))
                found = num
            elif float(abs(felta)) < delta:
                delta = float(abs(felta))
                found = num
            else:
                pass
    return found

def find(user_height, user_birthdate):
    for athelete in atheletes:
        athelete_height_dict[athelete.name] = athelete.height
        athelete_birth_dict[athelete.name] = date_convert(athelete.birthdate)
    near_ath_name_by_height = float()
    near_ath_name_by_birth = float()
    for key, value in athelete_height_dict.items():
        if value == find_nearest(user_height, list(athelete_height_dict.values())):
            near_ath_name_by_height = key
    for key, value in athelete_birth_dict.items():
        if value == find_nearest(user_birthdate, list(athelete_birth_dict.values())):
            near_ath_name_by_birth = key
    print_text = f"Атлет ближащий по росту - {near_ath_name_by_height},\nАтлет ближащий по дня рождения - {near_ath_name_by_birth}"
    return print_text

def main():
    user_all = len(users)
    user_id = int()
    if user_all == 1:
        user_id = int(input("В базе данных только один пользователь. Введите цифру один: "))
    elif user_all <= 4 and user_all != 1:
        user_id = int(input(f"В базе данных всего {user_all} пользователя. Введите id пользователя: "))
    elif user_all >= 5 and user_all != 1:
        user_id = int(input(f"В базе данных {user_all} пользователей. Введите id пользователя: "))
    
    if user_id in user_ids:
        for user in users:
            if user_id == user.id:
                user_height = user.height
                user_birthdate = date_convert(user.birthdate) 
                users_cnt = find(user_height, user_birthdate)
                print(users_cnt)
    else:
        print("Нет пользователя с таким ID")
    
if __name__ == "__main__":
    main()
