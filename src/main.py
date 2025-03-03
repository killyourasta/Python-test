import datetime as dt

from typing import List
from fastapi import FastAPI, HTTPException, Query

from database import (City, Picnic, PicnicRegistration, Session, User)
from external_requests import WeatherAPI
from models import PicnicRegistrationModel, RegisterUserRequest, UserModel

app = FastAPI()


@app.post('/create-city/', summary='Create City', description='Создание города по его названию')
def create_city(city: str = Query(description="Название города", default=None)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = WeatherAPI()
    if not check.check_city_exists(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@app.get('/get-cities/', summary='Get Cities')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    if q:
        cities = Session().query(City).filter(City.name == q)
    else:
        cities = Session().query(City).all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]


@app.get('/users-list/', summary='Get Users')
def users_list(q: List[int] = Query([1, 150],
                                    description='Возрастной диапазон пользователей')):
    """
    Список пользователей
    """
    users = []
    if q:
        return Session().query(User).filter(User.age.between(q[0], q[1])).all()

    users = Session().query(User).all()
    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@app.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.post('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = None, datetime: dt.datetime = None):
    """
    Добавление пикника
    """
    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': Session().query(City).filter(City.id == p.city_id).first().name,
        # Исправлена ошибка (Изменено p.id на city_id)
        'time': p.time,
    }


@app.post('/picnic-register/', summary='Picnic Registration',
          tags=['picnic'], response_model=PicnicRegistrationModel)
def register_to_picnic(user_id: int, picnic_id: int):
    """
    Регистрация пользователя на пикник
    (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
    """
    # TODO: Сделать логику
    pr = PicnicRegistration(user_id=user_id, picnic_id=picnic_id)
    s = Session()
    s.add(pr)
    s.commit()

    return {
        'id': pr.id,
        "user_surname": Session().query(User).filter(User.id == user_id).first().surname,
        "picnic_id": Session().query(Picnic).filter(Picnic.id == picnic_id).first().city_id
    }
