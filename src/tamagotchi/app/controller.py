from datetime import datetime as dt
from fractions import Fraction as frac
from json import dumps as jdumps, loads as jloads
from pathlib import Path
from sys import path


from src.tamagotchi.model import model


ROOT_DIR = Path(path[0]).parent.parent.parent


class App:
    def __init__(self):
        # self.creature: model.Creature = LoadCreature.load() if self._is_live() else MainMenu.choose_kind()
        if self.is_live():
            self.creature: model.Creature = LoadCreature.load()

    @staticmethod
    def is_live() -> bool:
        return LoadCreature.default_path.is_file()


class LoadCreature:
    default_path: str | Path = ROOT_DIR / 'data/creature.save'
    game_days_to_real_hours: frac = frac(1, 2)

    @classmethod
    def save(cls, creature: model.Creature):
        data = {
            'timestamp': dt.now().timestamp(),
            'kind': creature.kind.name,
            'name': creature.name,
            'age': creature.age,
            'maturity': creature.mature.value,
            'params': creature.history[-1].__dict__
        }
        data = jdumps(data, ensure_ascii=False)
        cls.default_path.write_text(data, encoding='utf-8')

    # @classmethod
    # def load(cls) -> model.Creature:
    #     data = cls.default_path.read_text(encoding='utf-8')
    #     data = jloads(data)
    #     kind = None
    #     for elem in LoadKinds(*LoadKinds.generate()):
    #         if elem.name == data['kind']:
    #             kind = elem
    #
    #     creature = model.Creature(kind, data['name'])
    #     creature.age = data['age']
    #     creature.mature = model.Maturity(data['maturity'])
    #     for k, v in data['params'].items():
    #         for elem in creature.params.keys():
    #             if elem.__name__ == k:
    #                 creature.params[elem].value = v
    #     return creature
    @classmethod
    def load(cls) -> model.Creature:
        data = cls.default_path.read_text(encoding='utf-8')
        data = jloads(data)
        kind = None
        for elem in LoadKinds(*LoadKinds.generate()):
            if elem.name == data['kind']:
                kind = elem

        state = model.State(data['age'])
        for param, val in data['params'].items():
            if param != 'age':
                setattr(state, param, val)

        state = cls.__params_evolution(state)
        creature = model.Creature(kind, data['name'])
        creature.age = state.age
        # доработать возможное изменение model.Maturity
        creature.mature = model.Maturity(data['maturity'])
        for k, v in state.__dict__.items():
            for elem in creature.params.keys():
                if elem.__name__ == k:
                    creature.params[elem].value = v
        return creature

    @classmethod
    def __params_evolution(cls, saved_state: model.State, hours: float = 0) -> model.State:
        """Пересчитывает параметры существа в соответствии с мат.моделью имитации жизни при закрытом приложении (ТЗ п.3в)."""
        game_day = hours*cls.game_days_to_real_hours
        ...
        return saved_state


class MainMenu:
    @staticmethod
    def start():
        """Запускает GUI с фреймом главного меню."""

    @staticmethod
    def choose_kind(chosen_kind: model.Kind) -> model.Creature:
        # надо передать имя питомца
        """Создаёт питомца на основе выбранного пользователем вида."""
        return model.Creature(chosen_kind, '')


class LoadKinds(list):
    # default_path: str | Path = ROOT_DIR / 'data/kinds.save'

    def __init__(self, *kinds: model.Kind):
        super().__init__(kinds)

    @classmethod
    def read_file(cls):
        pass

    @staticmethod
    def generate():
        from src.tamagotchi.utils import cat_kind, dog_kind
        return cat_kind, dog_kind
