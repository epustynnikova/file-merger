import logging
from asyncio import sleep

import toga
from toga.app import App
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from source.application.file_handler import SourceFileHandler, TargetFileHandler
from source.application.file_merger import TargetFileMerger
from source.model.dto import ColumnToRead, ReadingInfo

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

    async def exit_handler(self, app):
        App.exit(self)

    def startup(self):
        self.source_file = None
        self.target_files = None

        self.main_window = toga.MainWindow()
        self.on_exit = self.exit_handler

        self.info_box = toga.MultilineTextInput(readonly=True, style=Pack(flex=1, margin_top=10), value = "")

        self.label = toga.Label("Приложение запущено.", style=Pack(margin_top=10))

        btn_style = Pack(flex=1)

        btn_start = toga.Button(
            "Запустить обработку",
            on_press=self.action_start_script,
            style=btn_style
        )

        btn_app_info = toga.Button(
            "Информация о приложении", style=btn_style
        )

        self.progress_bar = toga.ProgressBar(max=100, value=0)

        btn_select_file_source = toga.Button(
            text = "Open dialog file",
            on_press = self.select_file_source,
            style = btn_style,
        )

        btn_select_target_files = toga.Button(
            text = "Open dialog file",
            on_press = self.select_target_files,
            style = btn_style,
        )

        label1 = toga.Label('Файл-источник:')

        label2 = toga.Label('Список целевых файлов:')

        label3 = toga.Label('Список колонок:')

        label4 = toga.Label('Колонка ID:')

        self.column_value = ("Вид,Направление,Производитель,Прибор,Параметр,Артикул,Статус вид,Статус направление,Статус прибор,Статус параметр,Статус артикул")

        self.column_list = toga.MultilineTextInput(
            value = self.column_value,
            style=Pack(flex=1)
        )

        self.id_column = (
            "ID Позиции Базы")

        self.id_list = toga.MultilineTextInput(
            value = self.id_column,
            style=Pack(flex=1)
        )

        btn_clear_paths = toga.Button(
            text = "Очистить",
            on_press = self.clear_paths,
            style = btn_style,
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
        if self.progress_bar.value in [0, 100]:
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

                center = len(column_value) // 2
                columns = []
                for i in range(center + 1):
                    columns.append(ColumnToRead(column_value[i], column_value[i+center]))
                reading_info = ReadingInfo(
                    id_column_name=self.id_column,
                    columns_for_copy=columns,
                )
                logger.info(f"Parsed reading info: {reading_info}")
                source_handler = SourceFileHandler(reading_info, str(self.source_file))
                id_to_source_item = {source_item.id: source_item for source_item in source_handler.read_file()}
                logger.info(f"Read {len(id_to_source_item.values())} source items")
                logger.info(f"IDs: {len(id_to_source_item.keys())}")
                files_count = 0
                for file in self.target_files:
                    try:
                        logger.info(f"Processing file: {file}")
                        target_file_path = str(file)
                        file_merger = TargetFileMerger(TargetFileHandler(target_file_path))
                        logger.info(f"Read file: {file}")
                        file_merger.merge(reading_info, id_to_source_item)
                        self.info_box.value += f"Обработан файл: {target_file_path}\n"
                        logger.info(f"Finished processing file: {file}")
                        files_count += 1
                    except Exception as ex:
                        self.info_box.value += f"В процессе обработки файла {target_file_path} произошла ошибка\n"
                        logger.info(f"Finished processing file: {file} with exception: {ex}")
                    self.progress_bar.value = round(100 * (files_count / len(self.target_files)))
                    logger.info(f"From {len(self.target_files)} files handled {files_count} files, percentage: {self.progress_bar.value}%")
                self.label.text = "Закончена обработка файлов"
                self.progress_bar.value = 100
                self.column_list.readonly = False
                self.id_list.readonly = False
        else:
            await self.dialog(toga.InfoDialog("Внимание", "Не закончена обработка файла"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    async def select_file_source(self, widget):
        if self.progress_bar.value in [0, 100]:
            source_file_path = await self.dialog(
                toga.OpenFileDialog("Choose a file")
            )

            if source_file_path is not None:
                self.source_file = source_file_path
                self.label.text = f"Выбран исходный файл {self.source_file}\n"
        else:
            await self.dialog(toga.InfoDialog(
                "Внимание",
                "Не закончена обработка файла"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    async def select_target_files(self, widget):
        if self.progress_bar.value in [0, 100]:
            target_files_paths = await self.dialog(
                toga.OpenFileDialog(
                    title="Choose files",
                    multiple_select=True,
                )
            )

            if target_files_paths is not None:
                self.target_files = target_files_paths

                target_selected_text = "\n".join(
                    f"Выбран файл для записи: {file_path.name}"
                    for file_path in self.target_files)
                self.label.text = target_selected_text + "\n"
        else:
            await self.dialog(toga.InfoDialog(
                "Внимание",
                "Не закончена обработка файлов"))
            self.label.text = "Предупреждение: не закончена обработка предыдущего файла"

    async def clear_paths(self, widget):
        if self.progress_bar.value in [0, 100]:
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


app = GuiApplication(formal_name="Excel file merger", app_id="file.merger")
app.main_loop()
