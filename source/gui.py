import logging
from asyncio import sleep

import toga
from toga.app import App
from toga.constants import COLUMN
from toga.style import Pack

logging.basicConfig(filename=f'file-merger.log',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GuiApplication(toga.App):

    def __init__(self, formal_name, app_id):
        super().__init__(formal_name=formal_name, app_id=app_id)

        # variables
        self.file_name = ''

        # objects
        self.label = toga.Label("Приложение запущено.", style=Pack(margin_top=20))
        self.progress_bar = toga.ProgressBar(max=100, value=0)

    async def exit_handler(self, app):
        App.exit(self)

    def startup(self):
        self.main_window = toga.MainWindow()
        self.on_exit = self.exit_handler


        btn_style = Pack(flex=1)

        btn_start = toga.Button(
            "Запустить обработку",
            on_press=self.action_start_script,
            style=btn_style
        )

        box = toga.Box(
            children=[
                self.progress_bar,
                btn_start,
                self.label
            ],
            style=Pack(flex=1, direction=COLUMN, margin=10),
        )

        self.main_window.content = box

        self.main_window.show()

    async def action_start_script(self, widget):
        if self.progress_bar.value in [0, 100]:
            self.progress_bar.value = 0
            for i in range(0, 100):
                await sleep(1)
                self.progress_bar.value = i
                print(i)
            self.label.text = f"Закончена обработка файла"
            self.progress_bar.value = 100
        else:
            await self.dialog(toga.InfoDialog("Внимание", f"Не закончена обработка файла"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    def exit(self):
        App.exit(self)


app = GuiApplication(formal_name="Мержим файлы", app_id="file.merger")
app.main_loop()