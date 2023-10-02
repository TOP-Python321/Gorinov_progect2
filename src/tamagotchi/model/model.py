from abc import ABC, abstractmethod
from enum import Enum
from numbers import Real
from typing import Type
from itertools import chain


class Maturity(Enum):
    CUB = 0
    YOUNG = 1
    ADULT = 2
    OLD = 3


class Creature:
    def __init__(self, kind: 'Kind', name: str):
        self.kind = kind
        self.name = name
        self.age: int = 0
        self.mature: Maturity = Maturity.CUB
        self.params: dict[Type, Parameter] = {
            cls: cls(param.value, param.min, param.max, self)
            for cls, param in kind.value[self.mature].params.items()
        }
        self.player_actions: list[Action] = [
            act.__class__(**(act.__dict__ | {'origin': self}))
            for act in kind.value[self.mature].player_actions
        ]
        self.creature_action: set[Action] = {
            act.__class__(**(act.__dict__ | {'origin': self}))
            for act in kind.value[self.mature].creature_action
        }
        self.history: History = History()

    def update(self):
        for param in self.params.values():
            param.update()

    def _grow_up(self):
        try:
            self.mature = Maturity(self.mature.value + 1)
        except ValueError:
            return
        for cls, param in self.kind.value[self.mature].params.items():
            self.params[cls].min = param.min
            self.params[cls].max = param.max

    def save(self):
        state = State(self.age)
        for param in self.params.values():
            setattr(state, param.__class__.__name__, param.value)
        self.history.append(state)

    def __repr__(self):
        return f"<{self.name}: {'/'.join(f'{p.value:.1f}' for p in self.params.values())}>"


class History(list):
    def get_param_history(self, param_name: str) -> tuple[float, ...]:
        return tuple(
            getattr(state, param_name)
            for state in self
        )


class State:
    """
    Хранитель.
    Атрибуты экземпляра формируются динамически.
    """
    def __init__(self, age: int):
        self.age = age

    def __repr__(self):
        return f"<{'/'.join(f'{v}' for v in self.__dict__.values())}>"


class Parameter(ABC):
    def __init__(
            self,
            value: float,
            min_: float,
            max_: float,
            origin: Creature = None,
    ):
        if min_ <= value <= max_:
            self.__value = value
        else:
            raise ValueError
        self.min = min_
        self.max = max_
        self.origin = origin

    @property
    def range(self):
        return self.min, self.max

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, number: float):
        if isinstance(number, Real):
            if number < self.min:
                self.__value = self.min
            elif self.max < number:
                self.__value = self.max
            else:
                self.__value = number
        else:
            raise TypeError

    @abstractmethod
    def update(self):
        pass


class Health(Parameter):
    def update(self):
        hunger = self.origin.kind.value[self.origin.mature].params[Satiety]
        thirst = self.origin.kind.value[self.origin.mature].params[Thirst]
        critical_thirst = 3 * (sum(thirst.range)) / 4
        critical_hunger = sum(hunger.range) / 4
        if (
            self.origin.params[Satiety].value < critical_hunger or
            self.origin.params[Thirst].value > critical_thirst
        ):
            self.value -= 0.5


class Satiety(Parameter):
    def update(self):
        self.value -= 1


class Thirst(Parameter):
    """Предcтавляет класс описывающий жажду существа"""
    def update(self) -> None:
        self.value += 1


class Mood(Parameter):
    """Представляет настроение существа"""
    def update(self) -> None:
        if self.value < sum(self.origin.kind.value[self.origin.mature].params[Mood].range) / 4:
            for action in self.origin.creature_action:
                if action.__class__.__name__ == 'PlayRope':
                    print('!!!action!!!')
                    action.action()
        else:
            self.value -= 1


class Action(ABC):
    name: str
    
    def __init__(self, timer: int = None, origin: Creature = None):
        self.timer = timer
        self.origin = origin
        
    @abstractmethod
    def action(self):
        pass


class Feed(Action):
    def __init__(self, amount: int, origin: Creature = None, timer: int = 0):
        super().__init__(timer, origin)
        self.amount = amount
        
    def action(self):
        self.origin.params[Satiety].value += self.amount


class Water(Action):
    """Представляет класс описывающий действие - "напоить существо"."""
    def action(self):
        self.origin.params[Thirst].value -= 1


class Pet(Action):
    """Описывает действие - "погладить существо"."""
    def action(self):
        self.origin.params[Mood].value += 1


class PlayRope(Action):
    def action(self):
        self.origin.params[Mood].value += 2
        print('веревочка')


class Sleep(Action):
    def action(self):
        self.origin.params[Satiety].update()
        print('сон')


class KindParameters:
    def __init__(
            self, days: int, 
            *params: Parameter,
            player_actions: list[Action],
            creature_action: set[Action]
        ):
        self.days = days
        self.params: dict[Type, Parameter] = {
            param.__class__: param
            for param in params
        }
        self.player_actions = player_actions
        self.creature_action = creature_action


class Kind(Enum):
    CAT = {
        Maturity.CUB: KindParameters(
            4,
            Health(10, 0, 20),
            Thirst(5, 0, 25),
            Satiety(5, 0, 25),
            Mood(10, 0, 50),
            player_actions=[
                Feed(20),
                Water(),
                Pet()
            ],
            creature_action={
                PlayRope(100),
            }
        ),
        Maturity.YOUNG: KindParameters(
            10,
            Health(0, 0, 50),
            Thirst(0, 0, 30),
            Satiety(0, 0, 30),
            Mood(0, 0, 50),
            player_actions=[
                Feed(25),
                Water(),
                Pet()
            ],
            creature_action={
                PlayRope(100),
                Sleep(120),
            }
        ),
        Maturity.ADULT: KindParameters(
            20,
            Health(0, 0, 45),
            Thirst(0, 0, 25),
            Satiety(0, 0, 25),
            Mood(0, 0, 40),
            player_actions=[
                Feed(20),
                Water(),
                Pet()
            ],
            creature_action={
                PlayRope(180),
                Sleep(60),
            }
        ),
        Maturity.OLD: KindParameters(
            12,
            Health(0, 0, 35),
            Thirst(0, 0, 20),
            Satiety(0, 0, 20),
            Mood(0, 0, 30),
            player_actions=[
                Feed(10),
                Water(),
                Pet()
            ],
            creature_action={
                Sleep(30)
            }
        ),
    }

