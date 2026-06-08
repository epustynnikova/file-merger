import asyncio
import logging

import toga
from toga.app import App
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from source.application.process_handler import merge_all

logging.basicConfig(filename=f'excel-file-merger.log',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GuiApplication(toga.App):

    def __init__(self, formal_name, app_id):
        super().__init__(formal_name=formal_name, app_id=app_id)
        self.id_list = None
        self.column_list = None
        self.id_column = None
        self.column_value = None
        self.progress_bar = None
        self.label = None
        self.info_box = None
        self.target_files = None
        self.source_file = None
        self.process_started = False

    async def exit_handler(self, app):
        App.exit(self)

    def startup(self):
        self.source_file = None
        self.target_files = None

        self.main_window = toga.MainWindow()
        self.on_exit = self.exit_handler

        self.info_box = toga.MultilineTextInput(readonly=True, style=Pack(flex=1, margin_top=10), value="")

        self.label = toga.Label("Приложение запущено.", style=Pack(margin_top=10))

        btn_style = Pack(flex=1)

        btn_start = toga.Button(
            "Запустить обработку",
            on_press=self.action_start_script,
            style=btn_style
        )

        btn_app_info = toga.Button(
            "Информация о приложении",
            on_press=self.action_app_info_dialog,
            style=btn_style
        )

        self.progress_bar = toga.ProgressBar(max=100, value=0)

        btn_select_file_source = toga.Button(
            text="Open dialog file",
            on_press=self.select_file_source,
            style=btn_style,
        )

        btn_select_target_files = toga.Button(
            text="Open dialog file",
            on_press=self.select_target_files,
            style=btn_style,
        )

        label1 = toga.Label('Файл-источник:')

        label2 = toga.Label('Список целевых файлов:')

        label3 = toga.Label('Список колонок:')

        label4 = toga.Label('Колонка ID:')

        self.column_value = (
            "Вид,Направление,Производитель,Прибор,Параметр,Артикул,Статус вид,Статус направление,Статус производитель,Статус прибор,Статус параметр,Статус артикул")

        self.column_list = toga.MultilineTextInput(
            value=self.column_value,
            style=Pack(flex=1)
        )

        self.id_column = (
            "ID Позиции Базы")

        self.id_list = toga.MultilineTextInput(
            value=self.id_column,
            style=Pack(flex=1)
        )

        btn_clear_paths = toga.Button(
            text="Очистить",
            on_press=self.clear_paths,
            style=btn_style,
        )

        box = toga.Box(
            style=Pack(flex=1, direction=COLUMN, margin=10),
        )

        def make_row(label_text, widget):
            row = toga.Box(style=Pack(direction=ROW, margin_bottom=10))

            label = toga.Label(
                label_text,
                style=Pack(width=200, margin_right=10)
            )

            row.add(label)
            row.add(widget)

            return row

        box.add(
            make_row(
                label1.text,
                btn_select_file_source
            )
        )

        box.add(
            make_row(
                label2.text,
                btn_select_target_files
            )
        )

        box.add(
            make_row(
                label3.text,
                self.column_list
            )
        )

        box.add(
            make_row(
                label4.text,
                self.id_list
            )
        )

        box.add(self.progress_bar)

        button_row = toga.Box(style=Pack(direction=ROW, margin_top=10))

        button_row.add(btn_start)
        button_row.add(btn_clear_paths)
        box.add(button_row)

        self.main_window.content = box

        self.main_window.show()

        box.add(
            self.info_box,
            self.label,
            btn_app_info
        )

    async def action_start_script(self, widget):
        if not self.process_started:
            if self.source_file is None:
                await self.dialog(toga.InfoDialog("Внимание", "Не выбран файл-источник"))
                self.label.text = "Предупреждение: не выбран файл-источник"
            elif self.target_files is None:
                await self.dialog(toga.InfoDialog("Внимание", "Не выбраны целевые файлы"))
                self.label.text = "Предупреждение: не выбраны целевые файлы"
            else:
                self.column_list.readonly = True
                self.id_list.readonly = True
                column_value = [
                    item.strip()
                    for item in self.column_list.value.split(",")
                    if item.strip()
                ]
                self.label.text = "Запущена обработка"
                self.info_box.value += f"ID колонка: ${self.id_column}\n"
                self.info_box.value += f"Список колонок: ${column_value}\n"
                self.progress_bar.value = 0
                self.process_started = True

                await asyncio.to_thread(
                    merge_all,
                    column_values=column_value,
                    id_column=self.id_column,
                    source_file_path=str(self.source_file),
                    target_files=[str(f) for f in self.target_files],
                    logger=logger,
                    progress_callback=self.update_progress,
                    infobox_callback=self.update_infobox,
                    end_handle_callback=self.end_handle
                )


        else:
            await self.dialog(toga.InfoDialog("Внимание", "Не закончена обработка файла"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    def update_progress(self, value):
        self.loop.call_soon_threadsafe(self._set_progress, value)

    def _set_progress(self, value):
        self.progress_bar.value = value

    def update_infobox(self, text):
        self.loop.call_soon_threadsafe(self._update_infobox, text)

    def _update_infobox(self, text):
        self.info_box.value += text

    def end_handle(self):
        self.loop.call_soon_threadsafe(self._end_handle)

    def _end_handle(self):
        self.label.text = "Закончена обработка файлов"
        self.progress_bar.value = 100
        self.source_file = None
        self.target_files = None
        self.column_list.readonly = False
        self.id_list.readonly = False
        self.process_started = False

    async def select_file_source(self, widget):
        if not self.process_started:
            self.progress_bar.value = 0
            source_file_path = await self.dialog(
                toga.OpenFileDialog(
                    title = "Choose a file",
                    file_types = ["xls", "xlsx", "xlsb"]
                )
            )

            correct_file_types = [".xls", ".xlsx", ".xlsb"]

            if source_file_path is not None:
                if source_file_path.suffix.lower() in correct_file_types:
                    self.source_file = source_file_path
                    self.label.text = f"Выбран исходный файл {self.source_file}\n"
                else:
                    await self.dialog(toga.InfoDialog(
                        "Внимание",
                        "Выберите файл Excel как исходный"))
                    self.label.text = f"Предупреждение: Выберите файл Excel как исходный"
        else:
            await self.dialog(toga.InfoDialog(
                "Внимание",
                "Не закончена обработка файла"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    async def select_target_files(self, widget):
        if not self.process_started:
            self.progress_bar.value = 0
            target_files_paths = await self.dialog(
                toga.OpenFileDialog(
                    title="Choose files",
                    multiple_select=True,
                    file_types=["xls", "xlsx", "xlsb"]
                )
            )

            if target_files_paths is not None:
                correct_file_types = [".xls", ".xlsx", ".xlsb"]
                valid_type_flag = True
                for file_path in target_files_paths:
                    if file_path.suffix.lower() not in correct_file_types:
                        valid_type_flag = False
                if valid_type_flag:
                        self.target_files = target_files_paths

                        target_selected_text = "\n".join(
                            f"Выбран файл для записи: {file_path.name}"
                            for file_path in self.target_files)
                        self.label.text = target_selected_text + "\n"
                else:
                    await self.dialog(toga.InfoDialog(
                        "Внимание",
                        "Выберите только файлы Excel как целевые"))
                    self.label.text = f"Предупреждение: Выберите только файлы Excel как целевые"
        else:
            await self.dialog(toga.InfoDialog(
                "Внимание",
                "Не закончена обработка файлов"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    async def clear_paths(self, widget):
        if not self.process_started:
            self.source_file = None
            self.target_files = None
            self.info_box.value = ""
            self.label.text = "Очищены пути к файлу-источнику и целевым файлам."
        else:
            await self.dialog(toga.InfoDialog(
                "Внимание",
                "Не закончена обработка файлов"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    def exit(self, source_widget):
        App.exit(self)

    async def action_app_info_dialog(self, widget):
        await self.dialog(toga.InfoDialog(
            title="Информация о приложении",
            message="""
            Эта программа объединяет Excel-файлы по выбранным колонкам.
            Текущая версия программы: 0.0.2


            Особенности работы:
            Программа объединяет информацию только из одного файла Excel в несколько файлов Excel при наличии в них указанной пересекающейся колонки.
            Выбор нескольких файлов осуществляется в диалоге выбора файла с зажатой клавишей Ctrl или протягиванием. 
            Все требуемые файлы необходимо выбрать за один раз, в противном случае выбор перезаписывается.
                
            Версия Python 3.13.1 или выше.

            Использованные библиотеки: 
            pyinstaller~=6.15.0
            setuptools~=72.1.0
            numpy~=2.2.3
            pandas~=2.3.1
            toga~=0.5.2
            openpyxl~=3.1.5
            pyxlsb~=1.0.10
            pyxlsbwriter~=0.1.0
            spire.xls~=16.5.0
        """))
        self.label.text = "Была предоставлена информация о приложении"

app = GuiApplication(formal_name="Excel file merger", app_id="file.merger")
app.main_loop()
