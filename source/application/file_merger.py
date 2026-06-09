from source.application.file_handler import TargetFileHandler
from source.model.dto import SourceItem, ReadingInfo, search


class TargetFileMerger:
    def __init__(self, file_handler: TargetFileHandler):
        self.file_handler = file_handler

    def merge(self,
              reading_info: ReadingInfo,
              id_to_source_item: dict[str, SourceItem],
              should_save=True,
              saved_file_path=None):
        df = self.file_handler.read_file()
        for idx, row in df.iterrows():
            id_value = row[reading_info.id_column_name]
            if id_value in id_to_source_item:
                for source_column in id_to_source_item[id_value].columns:
                    source_status = source_column.status
                    source_value = source_column.value
                    target_status = search(row[source_column.status_name])
                    target_value = row[source_column.name]
                    if source_status.need_to_refresh(target_status) and source_value != target_value:
                        print(
                            f'idx: {id_value}, {source_column.name}, source: {source_status, source_value}, target: {target_status, target_value}')
                        df.loc[idx, source_column.name] = source_value
                        df.loc[idx, source_column.status_name] = source_status.str_value
        if should_save:
            self.file_handler.save_df(saved_file_path)
        return df
