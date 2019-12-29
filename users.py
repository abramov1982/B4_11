from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = ("sqlite:///sochi_athletes.sqlite3")
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения
    регистрационных данных пользователей
    """
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы,
    если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def email_check(email):
    """
    Ввод почтового адреса с проверкой корректности ввода
    """
    if (email.count("@") == 1) and ("." in email[email.find("@"):]):
        return True
    return False
        

def gender_check(gender):
    """
    Ввод пола с проверкой корректности ввода
    """
    if (gender == "male") or (gender == "female"):
        return True
    return False
        

def birthdate_check(birthdate):
    try:
        datetime.strptime(birthdate, '%d-%m-%Y').date()
        return True
    except:
        return False
        
def height_check(height):
    """
    Проверка корректности ввода роста в см.
    """
    if len(height) >= 2:
        if (height[1] == ".") and (len(height) <= 4):
            try:
                height = float(height)
                return True
            except:
                return False
    return False
    


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    print("Привет! Я запишу твои данные!")
    
    first_name = input("Введи своё имя: ")
    
    last_name = input("А теперь фамилию: ")
    
    gender = input("Введите свой пол (male / female): ")
    while not gender_check(gender):
        gender = input("Введите пол в верном формате (male / female): ")
    
    email = input("Введите свою электронную почту: ")
    while not email_check(email):
        email = input("Введите корректный адрес электронной почты: ")
    
    birthdate = input("Дата Вашего рождения в формате (DD-MM-YYYY): ")
    while not birthdate_check(birthdate):
        birthdate = input("Введите дату в корректном формате (DD-MM-YYYY): ")
    
    height = input('Введите ваш рост в формате "М.см": ')
    while not height_check(height):
        height = input('Введите ваш рост в корректном формате "М.см": ')
    
    user = User(first_name=first_name, 
                last_name=last_name, 
                gender=gender,
                email=email,
                birthdate=birthdate,
                height=height
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
    
if __name__ == "__main__":
    main()