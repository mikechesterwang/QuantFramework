import abc
from enum import Enum


class Type(Enum):
    LONG = 1
    SHORT = -1


class Position:

    def __init__(self, type: Type, cost: float = 0, amount: float = 0):
        self._type = type
        self._cost = cost
        self._amount = amount

    def add(self, cost: float, amount: float):
        assert cost > 0 and amount > 0
        total_amount = self._amount + amount
        self._cost = (self._cost * self._amount + cost * amount) / total_amount
        self._amount = total_amount

    def close(self, cost: float, amount: float):
        assert cost > 0 and amount >= self._amount
        earnings = (cost - self._cost) * self._type * amount
        self._amount = self._amount - amount
        return earnings

    def close_all(self, cost):
        return self.close(cost, self._amount)

class CryptoBroker:

    def __init__(self, money=1_000_000, leverage=1, transaction_cost=0):
        self._money = money
        self._leverage = leverage
        self._transaction_cost = transaction_cost
        self._long_position = {}
        self._short_position = {}

    def open(self, key: str, type: Type):
        if type == Type.LONG:
            self._long_position[key] = Position(type, 0, 0)
        else:
            self._short_position[key] = Position(type, 0, 0)

    def long(self, cost: float, amount: float):
        assert cost > 0 and amount > 0
        remaining = self._money - cost * amount
        self._long_position.add(cost, amount)