import os
import unittest

from source.application.file_handler import TargetFileHandler, SourceFileHandler
from source.application.file_merger import TargetFileMerger
from source.model.dto import ReadingInfo, ColumnToRead
from test.test_utils import get_file_source_path


class FileHandler(unittest.TestCase):
    def test_merge(self):
        # given:
        target_file_path = get_file_source_path(os.path.join('file_merger', 'target.xlsx'))
        source_file_path = get_file_source_path(os.path.join('file_merger', 'source.xlsx'))
        reading_info = ReadingInfo(
            id_column_name='ID Позиции Базы',
            columns_for_copy=[
                ColumnToRead('Вид', 'Статус вид'),
                ColumnToRead('Производитель', 'Статус производитель'),
                ColumnToRead('Направление', 'Статус направление'),
                ColumnToRead('Прибор', 'Статус прибор'),
                ColumnToRead('Параметр', 'Статус параметр'),
                ColumnToRead('Артикул', 'Статус артикул')
            ]
        )
        target_file_merger = TargetFileMerger(TargetFileHandler(target_file_path))
        source_file_handler = SourceFileHandler(reading_info, source_file_path)
        source_items = source_file_handler.read_file()
        id_to_source_item = {source_item.id: source_item for source_item in source_items}
        expected_results = {
            "KDA_25_2230903898025000010_0001": {
                "Производитель": "Синтол",
                "Статус производитель": "Нейросеть"
            },
            "ROS_25_2611200472725000032_0012": {
                "Производитель": "Элта",
                "Статус производитель": "Вручную"
            },
            "KDA_25_3231507656825000015_0001": {
                "Производитель": "Элта",
                "Статус производитель": "Вручную"
            },
            "KRY_25_2910206042125000144_0006": {
                "Прибор": "Dirui",
                "Статус прибор": "Вручную"
            },
            "KRY_25_2910206042125000146_0006": {
                "Прибор": "Dirui",
                "Статус прибор": "Вручную"
            },
            "VGG_25_2341450005025000047_0001": {
                "Производитель": "Элта",
                "Статус производитель": "Вручную"
            },
            "KDA_25_2231101050225000415_0001": {
                "Прибор": "ARCHITECT c",
                "Статус прибор": "Вручную"
            },
            "KRY_25_2910600848625000034_0001": {
                "Производитель": "ХЕМА",
                "Статус производитель": "Классификатор"
            },
            "VGG_25_1341006036925000053_0006": {
                "Производитель": "Элта",
                "Статус производитель": "Вручную"
            },
            "ROS_25_2616102736425000023_0009": {
                "Производитель": "Элта",
                "Статус производитель": "Вручную"
            }
        }

        # when:
        result = target_file_merger.merge(reading_info=reading_info, id_to_source_item=id_to_source_item, should_save=False)

        # then:
        self.assertEqual(1478, len(source_items))
        self.assertEqual(1478, len(result))
        for idx, row in result.iterrows():
            idx = row["ID Позиции Базы"]
            if idx in expected_results:
                for expected_result_column_name in expected_results[idx]:
                    self.assertEqual(
                        expected_results[idx][expected_result_column_name],
                        row[expected_result_column_name]
                    )

