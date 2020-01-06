# Импорт модулей
import datetime
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Путь до базы (предполагается что база лежит в каталоге из которого испольняется скрипт)

DB_PATH = ("sqlite:///sochi_athletes.sqlite3")
Base = declarative_base()


# Создание фабрики сессий

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

engine = sa.create_engine(DB_PATH)
Sessions = sessionmaker(engine)
session = Sessions()


# Создание экземпляра класса для получения данных из базы

class Athelete(Base):
        """
        Инициация полей необходимых для получения из базы
        """
        __tablename__ = "athelete"
        id = sa.Column(sa.Integer, primary_key=True)
        age = sa.Column(sa.Integer)
        birthdate = sa.Column(sa.Text)
        gender = sa.Column(sa.Text)
        height = sa.Column(sa.REAL)
        weight = sa.Column(sa.Integer)
        gold_medals = sa.Column(sa.Integer)
        silver_medals = sa.Column(sa.Integer)
        bronze_medals = sa.Column(sa.Integer)
        total_medals = sa.Column(sa.Integer)
        sport = sa.Column(sa.Text)
        country = sa.Column(sa.Text)


# Функция конвертирования даты в число

def date_convert(birthdate_string):
    parts = birthdate_string.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return (date)


# Функция поиска ближайшего по возрасту спортсмена

def search_birthdate(birthdate, search_id):
    result_birthdate_min = []
    result_birthdate_max = []
    result_birthdate = []
    request_birthdate_min = session.query(func.max(Athelete.birthdate), Athelete.id)\
                                        .filter(
                                                Athelete.birthdate <= birthdate, 
                                                Athelete.id != search_id
                                                )
                                        
    request_birthdate_max = session.query(func.min(Athelete.birthdate), Athelete.id)\
                                        .filter(
                                                Athelete.birthdate >= birthdate,
                                                Athelete.id != search_id
                                                )
    for i in request_birthdate_min:
        try:
            result_birthdate_min.append(date_convert(i[0]))
            result_birthdate_min.append(i[1])
        except:
            result_birthdate_min.append(None)
    
    for i in request_birthdate_max:
        try:
            result_birthdate_max.append(date_convert(i[0]))
            result_birthdate_max.append(i[1])
        except:
            result_birthdate_max.append(None)
    
    if result_birthdate_max[0] is None:
        result_birthdate = result_birthdate_min
    elif result_birthdate_min[0] is None:
        result_birthdate = result_birthdate_max
    else:
        if (birthdate - result_birthdate_max[0]) <= (result_birthdate_min[0] - birthdate):
            result_birthdate = result_birthdate_max
        else:
            result_birthdate = result_birthdate_min
    print("id ближайшего по дате рождения атлета - {}, дата его рождения {}.".format(result_birthdate[1],
                                                                            result_birthdate[0]
                                                                            ))


# Функция поиска ближайшего по росту спортсмена    

def search_height(height, search_id):
    result_height_min = []
    result_height_max = []
    result_height = []
    request_height_min = session.query(func.max(Athelete.height), Athelete.id)\
                                        .filter(
                                                Athelete.height <= height, 
                                                Athelete.id != search_id
                                                )
                                        
    request_height_max = session.query(func.min(Athelete.height), Athelete.id)\
                                        .filter(
                                                Athelete.height >= height,
                                                Athelete.id != search_id
                                                )
    for i in request_height_min:
        result_height_min.append(i[0])
        result_height_min.append(i[1])
    for i in request_height_max:
        result_height_max.append(i[0])
        result_height_max.append(i[1])
    if result_height_max[0] is None:
        result_height = result_height_min
    elif result_height_min[0] is None:
        result_height = result_height_max
    else:
        if (height - result_height_max[0]) <= (result_height_min[0] - height):
            result_height = result_height_max
        else:
            result_height = result_height_min
    print("id ближайшего по росту атлета - {}, его рост {} м.".format(result_height[1],
                                                                      result_height[0]
                                                                      ))
   

#Фунция запуска скрипта

def main():
    query_id = input('Введите id спортсмена: ')
    etalon = session.query(Athelete).get(query_id)
    if etalon is None:
        print("Спортсмена с таким id нет в базе")
        return
    else:
        etalon_height = etalon.height
        etalon_birthdate = etalon.birthdate
        print("Рост спортсмена с id " + query_id + " составляет " + str(etalon_height))
        search_height(etalon_height, query_id)
        print("Дата рождения спортсмена с id " + query_id + " - " +  str(etalon_birthdate))
        search_birthdate(date_convert(etalon_birthdate), query_id)
    
    
if __name__ == "__main__":
    main()