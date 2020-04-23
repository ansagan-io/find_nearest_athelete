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

def parse_date(date):
    x = date.split("-")
    if len(x[0]) == 4 and len(x[1]) == 2 and len(x[2])==2 and "-" in date and len(date) and type(date) == str :
        return True
    else:
        return False

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Привет! Я запишу твои данные!")
    first_name = input("Введи своё имя: ").capitalize()
    last_name = input("А теперь фамилию: ").capitalize()
    x = input("Выберите ваш пол: 1 Мужской.\n 2 Женский\n")
    gender = "Male" if int(x) == 1 else "Famale" if int(x)==2 else "NULL"
    email = input("Адрес твоей электронной почты: ")
    birthdate = input("Напишите свой день рождения в формате ГГГГ-ММ-ДД(Например: 1996-04-12)")
    height = round(float(input("Напишите свой рост в метрах: ")), 2)

    user = User(
        #Ansaganid=user_id,
        first_name=first_name,
        last_name=last_name,
        gender = gender,
        email=email,
        birthdate = birthdate,
        height = height
    )
    return user

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()

    user = request_data()
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")

if __name__ == "__main__":
    main()