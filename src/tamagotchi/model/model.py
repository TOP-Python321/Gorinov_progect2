from abc import ABC, abstractmethod
from collections.abc import Iterable
from enum import Enum
from numbers import Real
from pathlib import Path
from sys import path
from typing import Type, Self

from data import data

ROOT_DIR = Path(path[0]).parent.parent.parent


class Maturity(Enum):
    """Описывает стадии возраста существа."""
    CUB = 0
    YOUNG = 1
    ADULT = 2
    OLD = 3


class Creature:
    """Описывает существо."""
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
        """Обновляет все параметры существа."""
        for param in self.params.values():
            param.update()

    def _grow_up(self) -> None:
        """
        Переключает стадию возраста существа на следующую ступень и заменяет минимальные и максимальные значения
        параметров в соответчтвии ступени возраста.
        """
        try:
            self.mature = Maturity(self.mature.value + 1)
        except ValueError:
            return
        for cls, param in self.kind[self.mature].params.items():
            self.params[cls].min = param.min
            self.params[cls].max = param.max

    def add_creature_age(self, days_val: int) -> None:
        """Увеличивает количество прожитых дней существа."""
        self.age += days_val
        if self.age > self.kind[self.mature].days:
            # без проверки диапазона
            self._grow_up()

    def autosave(self):
        """Сохраняет параметры существа в self.history"""
        state: State = State(self.age)
        for param in self.params.values():
            setattr(state, param.__class__.__name__, param.value)
        self.history.append(state)

    def __repr__(self):
        return f"<{self.name}: {'|'.join(f'{p.value:.1f}' for p in self.params.values())}>"

    def __str__(self):
        return f"{self.name}: \n" + '\n'.join(f'{p.name} = {p.value:.1f}' for p in self.params.values())


class History(list):
    """Представляет класс опекун для State."""
    def get_param_history(self, param_name: str) -> tuple[float, ...]:
        """Возвращает кортеж с параметров 'param_name'"""
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
    """Описывает абстрактный класс действий игрока и питомца."""
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
    """Описывает кнопки в tkinter, для которых не назначены команды активностей игрока."""
    __instance: Self = None

    def __new__(cls):
        if cls.__instance is None:
            self = super().__new__(cls)
            self.image = data.IMAGES_PATH['no_action']
            self.state = 'disabled'
            self.action = lambda: None
            cls.__instance = self
        return cls.__instance


class Feed(Action):
    """Описывает действие - 'покормить питомца'."""
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
        """Пересчитывает параметр Satiety"""
        self.origin.params[Satiety].value += self.amount
        return f'вы покормили {self.origin.name}'


class Water(Action):
    """Представляет класс описывающий действие - 'напоить питомца'."""
    name = 'напоить питомца'

    def action(self):
        """Пересчитывает параметр Thirst"""
        self.origin.params[Thirst].value -= 1
        return f'вы напоили {self.origin.name}'


class Pet(Action):
    """Описывает действие - 'приласкать питомца'."""

    name = 'приласкать питомца'

    def action(self):
        """Пересчитывает параметр Mood"""
        self.origin.params[Mood].value += 1
        return f'вы ласкаете {self.origin.name}'

class PlayPet(Action):
    """Описывает действие - 'поиграть с питомцем'."""
    name = 'поиграть с питомцем'

    def action(self):
        """Пересчитывает параметы существа"""
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
    """Описывает действие  - 'поиграть с веревочкой'."""
    def action(self):
        """Пересчитывает параметы существа"""
        self.origin.params[Mood].value += 2
        self.origin.params[Satiety].value -= 0.5
        self.origin.params[Thirst].value += 0.5
        return f'{self.origin.name} играет с веревочкой'


class Run(Action):
    """Описывает действие  - 'бегать'."""
    def action(self):
        """Пересчитывает параметы существа"""
        self.origin.params[Mood].value += 2
        self.origin.params[Satiety].value -= 0.5
        self.origin.params[Thirst].value += 0.5
        return f'{self.origin.name} бегает'


class Sleep(Action):
    """Описывает действие  - 'спать'."""
    def action(self) -> str:
        """Пересчитывает параметр Satiety"""
        self.origin.params[Satiety].value -= 0.5
        return f'{self.origin.name} спит'


class Miss(Action):
    """Представляет действие питомца - 'скучать'."""

    def action(self) -> str:
        """Пересчитывает параметр Mood"""
        self.origin.params[Mood].value -= 3
        return f'{self.origin.name} скучает'


class Parameter(ABC):
    """Абстактный класс параметров существа."""
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
        """Возвращает минимальное и максимальное значение параметра."""
        return self.min, self.max

    @property
    def value(self) -> float:
        """Возвращает значение параметра."""
        return self.__value

    @value.setter
    def value(self, number: float):
        """Устанавливает значение параметра."""
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
        """обновляет параметры существа."""
        pass


class Health(Parameter):
    """Описывает здоровье существа."""
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
    """Описывает сытость существа."""
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
                    action.action()
        else:
            self.value -= 1


class MatureOptions:
    """Описывает параметры существа в зависимости от возраста."""
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
    """Описывает вид существа."""
    def __init__(
            self,
            name: str,
            image_path: str | Path,
            ages_parameters: AgesParameters,
    ):
        super().__init__(ages_parameters)
        self.name = name
        self.image = Path(image_path)





