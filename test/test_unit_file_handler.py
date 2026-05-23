import os
import time
import unittest

import pandas as pd

from source.application.file_handler import XLSAndXLSXHandler, SourceFileHandler
from source.model.dto import ReadingInfo, ColumnToRead, StatusEnum
from test.test_utils import get_file_source_path


class FileHandler(unittest.TestCase):
    def test_read(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsx'))
        handler = XLSAndXLSXHandler(file_path)

        # when:
        read_df = handler.read_file()

        # then:
        self.assertEqual(10, len(read_df))

    def test_write(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsx'))
        handler = XLSAndXLSXHandler(file_path)
        df = handler.read_file()
        saved_file_name = str(time.time()) + "_test.xlsx"

        # when:
        start_letter = ord('a')
        for i in range(len(df)):
            df.loc[i, 'a'] = chr(start_letter + i)

        # then:
        handler.save_df(saved_file_name)
        df = pd.read_excel(saved_file_name, dtype=str, keep_default_na=False, engine='openpyxl')
        self.assertEqual(10, len(df))
        self.assertEqual('a', df.loc[0, 'a'])
        self.assertEqual('j', df.loc[9, 'a'])

        os.remove(saved_file_name)

    def test_read_source(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsx'))
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
        handler = SourceFileHandler(reading_info, file_path)
        exprected_values = {
            'SVE_25_1666001346225000006_0005': {
                'Вид': [StatusEnum.NEURAL, 'Расходные материалы'],
                'Производитель': [StatusEnum.CLASSIFICATOR, 'Bio-Rad'],
                'Направление': [StatusEnum.NEURAL, 'Аллергодиагностика'],
                'Прибор': [StatusEnum.EMPTY, ''],
                'Параметр': [StatusEnum.EMPTY, ''],
                'Артикул': [StatusEnum.EMPTY, '']
        },
            'KEM_25_54206009501250000590000_0022': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Вектор-Бест'],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.CLASSIFICATOR, 'BioSystems BA 400'],
                'Параметр': [StatusEnum.MANUAL, 'ГЛИКОЗИЛИРОВАННЫЙ ГЕМОГЛОБИН'],
                'Артикул': [StatusEnum.CLASSIFICATOR, 'вектор_9520']
            },
            'KEM_25_54206009501250000590000_0024': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Вектор-Бест'],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.CLASSIFICATOR, 'BioSystems BA 400'],
                'Параметр': [StatusEnum.MANUAL, 'КАЛИБРАТОР ГЛИКОЗИЛИРОВАННОГО ГЕМОГЛОБИНА'],
                'Артикул': [StatusEnum.MANUAL, '9522']
            },
            'KEM_25_54206009501250000590000_0025': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Вектор-Бест'],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.CLASSIFICATOR, 'BioSystems BA 400'],
                'Параметр': [StatusEnum.MANUAL, 'КОНТРОЛЬ ГЛИКОЗИЛИРОВАННОГО ГЕМОГЛОБИНА'],
                'Артикул': [StatusEnum.MANUAL, '9588']
            },
            'KEM_25_54206009501250000590000_0023': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Вектор-Бест'],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.CLASSIFICATOR, 'BioSystems BA 400'],
                'Параметр': [StatusEnum.MANUAL, 'ГЛИКОЗИЛИРОВАННЫЙ ГЕМОГЛОБИН'],
                'Артикул': [StatusEnum.CLASSIFICATOR, '9590']
            },
            'SPE_25_2780701521625000535_0019': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Mindray'],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.MANUAL, 'Mindray BS'],
                'Параметр': [StatusEnum.MANUAL, 'КОНТРОЛЬ ГЛИКОЗИЛИРОВАННОГО ГЕМОГЛОБИНА'],
                'Артикул': [StatusEnum.EMPTY, '']
            },
            'KEM_25_54234002473250000120000_0049': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.EMPTY, ''],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.EMPTY, ''],
                'Параметр': [StatusEnum.MANUAL, 'ГЛИКОЗИЛИРОВАННЫЙ ГЕМОГЛОБИН'],
                'Артикул': [StatusEnum.EMPTY, '']
            },
            'SVE_25_56601001930250002250000_0008': {
                'Вид': [StatusEnum.NEURAL, 'Расходные материалы'],
                'Производитель': [StatusEnum.EMPTY, ''],
                'Направление': [StatusEnum.CLASSIFICATOR_AND_NEURAL, 'Биохимия'],
                'Прибор': [StatusEnum.EMPTY, ''],
                'Параметр': [StatusEnum.EMPTY, ''],
                'Артикул': [StatusEnum.EMPTY, '']
            },
            'KEM_25_54218010999250005600000_0005': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Roche'],
                'Направление': [StatusEnum.AROUND, 'Биохимия'],
                'Прибор': [StatusEnum.CLASSIFICATOR, 'Cobas c'],
                'Параметр': [StatusEnum.MANUAL, 'КАЛИБРАТОР ГЛИКОЗИЛИРОВАННОГО ГЕМОГЛОБИНА'],
                'Артикул': [StatusEnum.CLASSIFICATOR, '4528417190']
            },
            'ORE_25_85612014915250000110000_0037': {
                'Вид': [StatusEnum.MANUAL, 'Реагенты'],
                'Производитель': [StatusEnum.MANUAL, 'Roche'],
                'Направление': [StatusEnum.MANUAL, 'Биохимия'],
                'Прибор': [StatusEnum.CLASSIFICATOR, 'Cobas c 502'],
                'Параметр': [StatusEnum.MANUAL, 'ГЛИКОЗИЛИРОВАННЫЙ ГЕМОГЛОБИН'],
                'Артикул': [StatusEnum.CLASSIFICATOR, '5336163190']
            }
        }


        # when:
        items = handler.read_file()

        # then:
        self.assertEqual(10, len(items))
        for item in items:
            expected_value_for_item = exprected_values[item.id]
            for column in item.columns:
                self.assertEqual(
                    expected_value_for_item[column.name][0],
                    column.status
                )
                self.assertEqual(
                    expected_value_for_item[column.name][1],
                    column.value
                )
            
