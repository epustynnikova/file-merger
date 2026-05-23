import pandas as pd

from source.model.dto import ReadingInfo, SourceItem, StatusEnum, SourceColumn


class XLSAndXLSXHandler:
    def __init__(self, input_file_path):
        self.df = None
        self.input_file_path = input_file_path

    def read_file(self) -> pd.DataFrame:
        self.df = pd.read_excel(self.input_file_path, dtype=str, keep_default_na=False, engine='openpyxl')
        self.df.drop(self.df.columns[self.df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
        return self.df

    def save_df(self, file_name=None) -> str:
        if file_name is None:
            self.df.to_excel(self.input_file_path, index=False)
            return self.input_file_path
        else:
            self.df.to_excel(file_name, index=False)
            return file_name


class SourceFileHandler(XLSAndXLSXHandler):
    def __init__(self, reading_info: ReadingInfo, input_file_path):
        super().__init__(input_file_path)
        self.reading_info = reading_info

    def read_file(self) -> list[SourceItem]:
        super().read_file()
        source_items = []
        for idx, row in self.df.iterrows():
            id_value = row[self.reading_info.id_column_name]
            columns_values = []
            for reading_column in self.reading_info.columns_for_copy:
                columns_values.append(SourceColumn(
                    name=reading_column.column_name,
                    value=row[reading_column.column_name],
                    status=StatusEnum.search(row[reading_column.status_name]),
                ))
            source_items.append(SourceItem(id_value, columns_values))
        return source_items


class TargetFileHandler(XLSAndXLSXHandler):
    def __init__(self, input_file_path):
        super().__init__(input_file_path)


