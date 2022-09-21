from pymongo import MongoClient
from config import MONGO_STR

from models.day import Day
from models.lession import Lession
from models.state import State

client = MongoClient(MONGO_STR)


def load_state() -> State:
    state = State()
    state.days = [
        Day("Понедельник",[
            Lession("1"),
            Lession("2"),
            Lession("3"),
            Lession("4"),
        ]),
        Day("Вторник",[]),
        Day("Среда",[
            Lession("1"),
            Lession("2"),
            Lession("3"),
            Lession("4"),
        ]),
        Day("Четверг",[]),
        Day("Пятника",[])
    ]
    return state

state = load_state()
