import json
import os
from dataclasses import dataclass, asdict
from typing import List


@dataclass(eq=True, order=True, unsafe_hash=True)
class ReadingInfoValues:
    idColumnName: str
    columnsList: list[str]


@dataclass(eq=True, order=True, unsafe_hash=True)
class ReadingInfoValues:
    id_column_name: str
    columns_list: List[str]

    def get_columns_list_as_str(self) -> str:
        return ", ".join(self.columns_list)

    def set_columns_list_from_str(self, values: str) -> None:
        self.columns_list = [i.strip() for i in values.split(",")]


def read_properties(file_path: str = "properties.json") -> ReadingInfoValues:
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ReadingInfoValues(**data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка разбора JSON в {file_path}: {e}")
        except TypeError as e:
            raise TypeError(f"Несоответствие полей JSON и dataclass: {e}")
    else:
        values = ReadingInfoValues(
            id_column_name="ID Позиции Базы",
            columns_list=[
                "Вид",
                "Направление",
                "Производитель",
                "Прибор",
                "Параметр",
                "Артикул",
                "Статус вид",
                "Статус направление",
                "Статус производитель",
                "Статус прибор",
                "Статус параметр",
                "Статус артикул"
            ])
        write_properties(values, file_path)
        return values


def write_properties(obj: ReadingInfoValues, file_path: str = "properties.json") -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(asdict(obj), f, ensure_ascii=False, indent=2)
