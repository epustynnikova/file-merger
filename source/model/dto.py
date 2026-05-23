from dataclasses import dataclass
from enum import Enum


@dataclass(eq=True, order=True, unsafe_hash=True)
class ReadingInfo:
    id_column_name: str
    columns_for_copy: list[ColumnToRead]


@dataclass(eq=True, order=True, unsafe_hash=True)
class ColumnToRead:
    column_name: str
    status_name: str


@dataclass(eq=True, order=True, unsafe_hash=True)
class SourceItem:
    id: str
    id_name: str
    columns: list[SourceColumnData]


@dataclass(eq=True, order=True, unsafe_hash=True)
class SourceColumnData:
    name: str
    value: str
    status_name: str
    status: StatusEnum


class StatusEnum(Enum):
    CONTRACT = ('Контракт', 1)
    MANUAL = ('Вручную', 2)
    AROUND = ('Примерно', 3)
    SCROLLING = ('Скроллинг', 3)
    ALT_BASE = ('Альтбаза', 3)
    CLASSIFICATOR = ('Классификатор', 4)
    NEURAL = ('Нейросеть', 4)
    CLASSIFICATOR_AND_NEURAL = ('Классификатор и нейросеть', 4)
    EMPTY = ('', 5)

    def __init__(self, str_value, rate):
        self.str_value = str_value
        self.rate = rate

    @staticmethod
    def search(value_from_xls: str) -> StatusEnum:
        for item in StatusEnum:
            if item.str_value == value_from_xls:
                return item
        return StatusEnum.EMPTY

    def need_to_refresh(self, target):
        if self.rate <= 3:
            return self.rate <= target.rate
        return self.rate < target.rate
