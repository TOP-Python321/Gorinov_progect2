from abc import ABC, abstractmethod
from collections.abc import Iterable
from enum import Enum
from numbers import Real
from pathlib import Path
from sys import path
from typing import Type, Self

ROOT_DIR = Path(path[0]).parent.parent.parent


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
            for cls, param in kind[self.mature].params.items()
        }
        self.player_actions: list[Action] = [
            act.__class__(**(act.__dict__ | {'origin': self}))
            for act in kind[self.mature].player_actions
        ]
        self.creature_action: set[Action] = {
            act.__class__(**(act.__dict__ | {'origin': self}))
            for act in kind[self.mature].creature_action
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
        for cls, param in self.kind[self.mature].params.items():
            self.params[cls].min = param.min
            self.params[cls].max = param.max

    def add_creature_age(self, days_val: int):
        self.age += days_val
        print('добавление дней')
        if self.age > self.kind[self.mature].days:
            # без проверки диапазона
            self._grow_up()

    def autosave(self):
        state = State(self.age)
        for param in self.params.values():
            setattr(state, param.__class__.__name__, param.value)
        self.history.append(state)

    def __repr__(self):
        return f"<{self.name}: {'|'.join(f'{p.value:.1f}' for p in self.params.values())}>"

    def __str__(self):
        return f"{self.name}: \n" + '\n'.join(f'{p.name} = {p.value:.1f}' for p in self.params.values())


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


class Action(ABC):
    name: str

    def __init__(
            self,
            timer: int = None,
            image: str | Path = None,
            origin: Creature = None,
            **kwargs
    ):
        self.timer = timer
        self.image = image
        self.origin = origin
        self.state = 'normal'

    @abstractmethod
    def action(self):
        pass


class NoAction:
    __instance: Self = None

    def __new__(cls):
        if cls.__instance is None:
            self = super().__new__(cls)
            self.image = ROOT_DIR / 'data/images/no_action.png'
            self.state = 'disabled'
            self.action = lambda: None
            cls.__instance = self
        return cls.__instance


class Feed(Action):
    name = 'покормить питомца'

    def __init__(
            self,
            amount: int,
            timer: int = None,
            image: str | Path = None,
            origin: Creature = None,
            **kwargs
    ):
        super().__init__(timer, image, origin)
        self.amount = amount

    def action(self):
        self.origin.params[Satiety].value += self.amount
        return f'вы покормили {self.origin.name}'


class Water(Action):
    """Представляет класс описывающий действие - "'напоить питомца'"."""

    name = 'напоить питомца'

    def action(self):
        self.origin.params[Thirst].value -= 1
        return f'вы напоили {self.origin.name}'


class Pet(Action):
    """Описывает действие - "приласкать питомца"."""

    name = 'приласкать питомца'

    def action(self):
        self.origin.params[Mood].value += 1
        return f'вы ласкаете {self.origin.name}'

class PlayPet(Action):
    """Описывает действие - "поиграть с питомцем"."""

    name = 'поиграть с питомцем'

    def action(self):
        self.origin.params[Mood].value += 1
        self.origin.params[Satiety].value -= 2
        self.origin.params[Thirst].value += 2
        if (
                self.origin.params[Mood].value > sum(
                self.origin.params[Mood].range) / 2 and
                self.origin.params[Satiety].value > sum(
                self.origin.params[Satiety].range) / 2
        ):
            self.origin.params[Health].value += 1

        return f'вы играете с {self.origin.name}'


class PlayRope(Action):
    def action(self):
        self.origin.params[Mood].value += 2
        self.origin.params[Satiety].value -= 0.5
        self.origin.params[Thirst].value += 0.5
        return f'{self.origin.name} играет с веревочкой'


class Run(Action):
    def action(self):
        self.origin.params[Mood].value += 2
        self.origin.params[Satiety].value -= 0.5
        self.origin.params[Thirst].value += 0.5
        return f'{self.origin.name} бегает'


class Sleep(Action):
    def action(self) -> str:
        self.origin.params[Satiety].value -= 0.5
        return f'{self.origin.name} спит'


class Miss(Action):
    """Представляет действие питомца - 'скучать'."""

    def action(self) -> str:
        self.origin.params[Mood].value -= 3
        return f'{self.origin.name} скучает'


class Parameter(ABC):
    name: str

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
    name = 'здоровье'

    def update(self):
        hunger = self.origin.params[Satiety]
        thirst = self.origin.params[Thirst]
        critical_thirst = 3 * (sum(thirst.range)) / 4
        critical_hunger = sum(hunger.range) / 4
        if (
            self.origin.params[Satiety].value < critical_hunger or
            self.origin.params[Thirst].value > critical_thirst
        ):
            self.value -= 0.5


class Satiety(Parameter):
    name = 'сытость'
    def update(self):
        self.value -= 1


class Thirst(Parameter):
    """Предcтавляет класс описывающий жажду существа"""
    name = 'жажда'

    def update(self) -> None:
        self.value += 1


class Mood(Parameter):
    """Представляет настроение существа"""
    name = 'настроение'

    def update(self) -> None:
        if self.value < sum(self.origin.params[Mood].range) / 4:
            for action in self.origin.creature_action:
                if action.__class__.__name__ == 'PlayRope' or 'Run':
                    print('!!!action!!!')
                    action.action()
        else:
            self.value -= 1


class MatureOptions:
    def __init__(
            self,
            days: int,
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


AgesParameters = dict[Maturity, MatureOptions] | Iterable[tuple[Maturity, MatureOptions]]


class Kind(dict):
    def __init__(
            self,
            name: str,
            image_path: str | Path,
            ages_parameters: AgesParameters,
    ):
        super().__init__(ages_parameters)
        self.name = name
        self.image = Path(image_path)





