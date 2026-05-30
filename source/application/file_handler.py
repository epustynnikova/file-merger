import os

import pandas as pd
from openpyxl import load_workbook
from pyxlsbwriter import XlsbWriter
from spire.xls import Workbook
import re

from source.model.dto import ReadingInfo, SourceItem, StatusEnum, SourceColumnData


class ExcelHandler:
    def __init__(self, input_file_path):
        self.df = None
        self.input_file = InputFile(input_file_path, get_file_type(input_file_path))

    def read_file(self) -> pd.DataFrame:
        self.df = pd.read_excel(self.input_file.path,
                                dtype=str,
                                keep_default_na=False,
                                engine=self.input_file.type.open_lib)
        if self.input_file.type in [FileTypeEnum.XLSX, FileTypeEnum.XLS]:
            self.df.drop(self.df.columns[self.df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
        return self.df

    def save_df(self, file_name=None) -> str:
        if file_name is None:
            return self._save(self.input_file.path)
        else:
            return self._save(file_name, delete_xlsb=False)

    def _save(self, file_name, delete_xlsb=True) -> str:
        if self.input_file.type in [FileTypeEnum.XLSX, FileTypeEnum.XLS]:
            return self._save_xls_xlsx(file_name)
        else:
            return self._save_xlsb(file_name, delete_xlsb)

    def _save_xlsb(self, file_name, delete_xlsb):
        # workbook = Workbook()
        # workbook.LoadFromFile(self.input_file.path)
        # worksheet = workbook.Worksheets[0]
        xslx_file_name = re.sub(r'\.xlsb$', '.xlsx', file_name)
        #
        # for row_idx, row in self.df.iterrows():
        #     excel_row = row_idx + 2
        #     for col_idx, value in enumerate(row):
        #         excel_col = col_idx + 1
        #         cell = worksheet.Range[excel_row, excel_col]
        #         cell.Value = value
        #
        # workbook.SaveToFile(xslx_file_name)
        # workbook.Dispose()
        self.df.to_excel(xslx_file_name, index=False)
        if delete_xlsb:
            os.remove(self.input_file.path)
        return file_name

    def _save_xls_xlsx(self, file_name) -> str:
        wb = load_workbook(self.input_file.path)
        ws = wb.active
        self.df.to_excel(file_name, index=False)
        for r_idx, row in self.df.iterrows():
            excel_row = r_idx + 2  # +2, т.к. pandas: 0 -> строка Excel 2 (если заголовок в строке 1)
            for c_idx, value in enumerate(row):
                excel_col = c_idx + 1
                cell = ws.cell(row=excel_row, column=excel_col)
                cell.value = value  # стиль остаётся прежним
        wb.save(file_name)
        return file_name


class SourceFileHandler(ExcelHandler):
    def __init__(self, reading_info: ReadingInfo, input_file):
        super().__init__(input_file)
        self.reading_info = reading_info

    def read_file(self) -> list[SourceItem]:
        super().read_file()
        source_items = []
        for idx, row in self.df.iterrows():
            id_value = row[self.reading_info.id_column_name]
            columns_values = []
            for reading_column in self.reading_info.columns_for_copy:
                columns_values.append(SourceColumnData(
                    name=reading_column.column_name,
                    value=row[reading_column.column_name],
                    status=StatusEnum.search(row[reading_column.status_name]),
                    status_name=reading_column.status_name
                ))
            source_items.append(SourceItem(
                id=id_value,
                id_name=row[self.reading_info.id_column_name],
                columns=columns_values))
        return source_items


class TargetFileHandler(ExcelHandler):
    def __init__(self, input_file):
        super().__init__(input_file)
