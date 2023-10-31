from itertools import cycle
from pathlib import Path
from sys import path
from tkinter import Tk, PhotoImage, StringVar, messagebox
from tkinter.ttk import Frame, Button, Label
from PIL import ImageTk, Image

# Добавление пути папки проекта в переменную среды PYTHONPATH
ROOT_DIR = Path(path[0]).parent.parent.parent
path.append(str(ROOT_DIR))

from src.tamagotchi.model import *
from src.tamagotchi.app import controller
from data import data


class RootWidget(Tk):
    """"""
    def __init__(self):
        super().__init__()
        self.title('Тамагочи')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width = screen_width // 3
        self.height = screen_height * 3 // 4
        x = screen_width // 2 - self.width // 2
        y = screen_height // 2 - self.height // 2

        self.geometry(f'{self.width}x{self.height}+{x}+{y}')
        # блокировка изменения размера окна
        self.resizable(False, False)

        self.mainframe: Frame = None

    def change_frame(self, new_frame: Frame):
        self.mainframe.destroy()
        self.mainframe = new_frame
        self.mainframe.change_image(new_frame.origin.kind.image)
        self.mainframe.update_creature(new_frame.origin)
        self.after(data.game_hours, lambda: root.mainframe.update_creature_action())
        self.after(data.game_hours * 24, lambda: root.mainframe.origin.add_creature_age(1))
        self.update()


class MainMenu(Frame):
    """"""
    def __init__(self, master: RootWidget, kinds: controller.LoadKinds[model.Kind]):
        super().__init__(master)
        pad = master.width // 100 + 1
        self.grid(
            row=0, column=0,
            padx=pad, pady=pad,
            sticky='nsew',
        )
        columns = 2
        img_size = (master.width - pad*2*(columns+1)) // columns - 10
        self._images: list[PhotoImage] = []
        for i, kind in enumerate(kinds):
            img = PhotoImage(file=kind.image)
            img_width, img_height = img.width(), img.height()
            if img_width != img_size or img_height != img_size:
                img = _resize_image(
                    kind.image,
                    img_size,
                    img_size,
                )
            self._images.append(img)
            row, column = divmod(i, columns)
            btn = Button(
                self,
                image=self._images[i],
                # для теста:
                # command=lambda: master.change_frame(Game(master, yara)),
                # на перспективу:
                command=lambda kid=kind: master.change_frame(Game(master, controller.MainMenu.choose_kind(kid))),
            )
            btn.grid(
                row=row, column=column,
                sticky='nsew',
                padx=pad, pady=pad,
            )


class Game(Frame):
    """"""
    def __init__(self, master: RootWidget, origin: model.Creature):
        super().__init__(master)
        self.origin = origin
        self.cycl_creat_act = self.cycle_creature_action(self.origin.creature_action)
        pad = (master.width // 100 + 1) * 2
        ipad = pad // 4
        self.grid(
            row=0, column=0,
            sticky='nsew',
            padx=pad, pady=pad,
        )
        self._screen_size = master.width - pad * 2
        self._actions_height = (master.height - self._screen_size - pad*4) // 3
        self._text_height = self._actions_height * 2
        self.rowconfigure(0, minsize=self._text_height)
        self.rowconfigure(1, minsize=self._screen_size)
        self.rowconfigure(2, minsize=self._actions_height)
        self.columnconfigure(0, minsize=self._screen_size)

        text_panel = Frame(self)
        text_panel.grid(
            row=0, column=0,
            sticky='nsew',
            pady=(0, pad),
        )
        text_panel.rowconfigure(0, minsize=self._text_height)
        text_panel.columnconfigure(0, minsize=self._screen_size//7*5)
        text_panel.columnconfigure(1, minsize=self._screen_size//7*2)

        self.message = StringVar(self, '')
        Label(
            text_panel,
            textvariable=self.message,
            wraplength=self._screen_size//7*5,
            font=('Arial Narrow', 16, 'italic'),
            anchor='nw',
            justify='left',
            # background='#ccc',
        ).grid(
            row=0, column=0,
            sticky='nsew',
            ipadx=ipad, ipady=ipad,
        )

        self.params = StringVar(self, '')
        Label(
            text_panel,
            textvariable=self.params,
            wraplength=self._screen_size//7*2,
            font=('Consolas', 10, 'bold'),
            anchor='ne',
            justify='right',
            # background='#ddd',
        ).grid(
            row=0, column=1,
            sticky='nsew',
            ipadx=ipad, ipady=ipad,
        )

        self._image: PhotoImage = None
        self.screen = Label(self)
        self.screen.grid(
            row=1, column=0,
            sticky='nsew',
            pady=(0, pad),
        )

        self.create_buttons(origin)

    def create_buttons(self, origin: model.Creature):
        buttons_panel = Frame(self)
        buttons_panel.grid(
            row=2, column=0,
            sticky='nsew',
        )
        buttons = 6
        self.actions: list[Button] = []
        self._buttons_images: list[PhotoImage] = []
        paddings = ((self._screen_size - self._actions_height*6)//(buttons-1),)*(buttons-1) + (0,)
        img_size = self._actions_height - 10
        for i, pad in enumerate(paddings):
            try:
                action = origin.player_actions[i]
            except IndexError:
                action = NoAction()
            img = PhotoImage(file=action.image)
            img_width, img_height = img.width(), img.height()
            if img_width != img_size or img_height != img_size:
                img = _resize_image(
                    action.image,
                    img_size,
                    img_size,
                )
            self._buttons_images.append(img)
            btn = Button(
                buttons_panel,
                image=self._buttons_images[-1],
                state=action.state,
                # необходимо добавить параметр в lambda-функцию, чтобы каждая из создаваемых в цикле функций обращалась к соответствующему экземпляру action
                # иначе, функции обращаются к action только во время вызова, а не в момент создания
                # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result

                # lambda вызывает функцию которая обновляет change_message() и change_params()
                command=lambda act=action: self.to_button_action(act)
            )
            btn.grid(
                row=0, column=i,
                sticky='nsew',
                padx=(0, pad),
            )
            self.actions.append(btn)

    def change_message(self, text: str) -> None:
        self.message.set(text)
        self.update_idletasks()

    def change_params(self, text: str) -> None:
        self.params.set(text)
        self.update_idletasks()

    def to_button_action(self, action):
        """Обновляет текстовые поля состояния питомца и параметры питомца."""
        self.change_message(action.action())
        self.change_params(str(self.origin))

    def change_image(self, img_path: str | Path) -> None:
        self._image = PhotoImage(file=img_path)
        img_width, img_height = self._image.width(), self._image.height()
        if img_width != self._screen_size or img_height != self._screen_size:
            self._image = _resize_image(
                img_path,
                self._screen_size,
                self._screen_size,
            )
        self.screen.configure(image=self._image)
        self.update_idletasks()

    # сделать привязку к игровому дню
    def update_creature(self, origin: model.Creature):
        origin.update()
        self.change_params(str(origin))
        self.after(data.game_hours, lambda: self.update_creature(origin))
        self.update()

    def cycle_creature_action(self, iter_action):
        for action in cycle(iter_action):
            yield action

    def update_creature_action(self):
        action = next(self.cycl_creat_act)
        print(action)
        self.change_image(action.image)
        for to_action in self.origin.creature_action:
            if to_action == action:
                print(action.__class__.__name__)
                self.change_message(action.action())

        self.after(action.timer * 1000, lambda: self.update_creature_action())
        self.update()

def _resize_image(
        image_path,
        new_width: int,
        new_height: int
) -> PhotoImage:
    img = Image.open(image_path)
    img = img.resize((new_width, new_height))
    return ImageTk.PhotoImage(img)

    # resized_image = PhotoImage(width=new_width, height=new_height)
    # for x in range(new_width):
    #     for y in range(new_height):
    #         x_old = x * old_width // new_width
    #         y_old = y * old_height // new_height
    #         rgb = '#{:02x}{:02x}{:02x}'.format(*image.get(x_old, y_old))
    #         resized_image.put(rgb, (x, y))
    # return resized_image


if __name__ == '__main__':
    root = RootWidget()
    frame = Game(root, controller.App().creature) if controller.App.is_live() else MainMenu(root, controller.LoadKinds(*controller.LoadKinds.generate()))
    root.mainframe = frame

    if not isinstance(root.mainframe, MainMenu):
        root.mainframe.change_image(frame.origin.kind.image)
        root.mainframe.change_message('Питомец рад вас видеть.')
        root.mainframe.update_creature(frame.origin)
        # через игровой час запускается активность питомца
        root.after(data.game_hours, lambda: root.mainframe.update_creature_action())
        # прибавление прожитого дня питомцу
        root.after(data.game_hours * 24, lambda: root.mainframe.origin.add_creature_age(1))

    def on_closing():
        # сохранение перед выходом из игры
        root.mainframe.origin.autosave()
        controller.LoadCreature.save(root.mainframe.origin)
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


