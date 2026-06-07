import os
import time
import unittest

import pandas as pd

from source.application.file_handler import ExcelHandler, SourceFileHandler
from source.model.dto import ReadingInfo, ColumnToRead, StatusEnum
from test.test_utils import get_file_source_path


class FileHandler(unittest.TestCase):
    def test_read_xsl(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsx'))
        handler = ExcelHandler(file_path)

        # when:
        read_df = handler.read_file()

        # then:
        self.assertEqual(10, len(read_df))

    def test_read_xslb(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsb'))
        handler = ExcelHandler(file_path)

        # when:
        read_df = handler.read_file()

        # then:
        self.assertEqual(40, len(read_df))

    def test_write_xlsx(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsx'))
        handler = ExcelHandler(file_path)
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

    def test_write_xlsb(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsb'))
        handler = ExcelHandler(file_path)
        df = handler.read_file()
        saved_file_name = str(time.time()) + "_test.xlsb"
        real_saved_file_name = saved_file_name.replace(".xlsb", ".xlsx")

        # when:
        start_letter = 1
        for i in range(len(df)):
            df.loc[i, 'a'] = start_letter + i

        # then:
        handler.save_df(saved_file_name)
        self.assertTrue(os.path.exists(real_saved_file_name))

        os.remove(real_saved_file_name)

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
                'Артикул': [StatusEnum.CLASSIFICATOR, 4528417190]
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

    def test_read_source_xlsb(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', 'source.xlsb'))
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
        expected_values = {
            'н0000001': {'Вид': [StatusEnum.EMPTY, '_wow'],
                         'Производитель': [StatusEnum.EMPTY, '_wow'],
                         'Направление': [StatusEnum.EMPTY, '_wow'],
                         'Прибор': [StatusEnum.EMPTY, '_wow'],
                         'Параметр': [StatusEnum.EMPTY, '_wow'],
                         'Артикул': [StatusEnum.EMPTY, '_wow']},
            'н0000002': {'Вид': [StatusEnum.NEURAL, '_wow'],
                         'Производитель': [StatusEnum.NEURAL, '_wow'],
                         'Направление': [StatusEnum.NEURAL, '_wow'],
                         'Прибор': [StatusEnum.NEURAL, '_wow'],
                         'Параметр': [StatusEnum.NEURAL, '_wow'],
                         'Артикул': [StatusEnum.NEURAL, '_wow']},
            'н0000003': {'Вид': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR, '_wow']},
            'н0000004': {'Вид': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow']},
            'н0000005': {'Вид': [StatusEnum.AROUND, '_wow'],
                         'Производитель': [StatusEnum.AROUND, '_wow'],
                         'Направление': [StatusEnum.AROUND, '_wow'],
                         'Прибор': [StatusEnum.AROUND, '_wow'],
                         'Параметр': [StatusEnum.AROUND, '_wow'],
                         'Артикул': [StatusEnum.AROUND, '_wow']},
            'н0000006': {'Вид': [StatusEnum.SCROLLING, '_wow'],
                         'Производитель': [StatusEnum.SCROLLING, '_wow'],
                         'Направление': [StatusEnum.SCROLLING, '_wow'],
                         'Прибор': [StatusEnum.SCROLLING, '_wow'],
                         'Параметр': [StatusEnum.SCROLLING, '_wow'],
                         'Артикул': [StatusEnum.SCROLLING, '_wow']},
            'н0000007': {'Вид': [StatusEnum.MANUAL, '_wow'],
                         'Производитель': [StatusEnum.MANUAL, '_wow'],
                         'Направление': [StatusEnum.MANUAL, '_wow'],
                         'Прибор': [StatusEnum.MANUAL, '_wow'],
                         'Параметр': [StatusEnum.MANUAL, '_wow'],
                         'Артикул': [StatusEnum.MANUAL, '_wow']},
            'н0000008': {'Вид': [StatusEnum.CONTRACT, '_wow'],
                         'Производитель': [StatusEnum.CONTRACT, '_wow'],
                         'Направление': [StatusEnum.CONTRACT, '_wow'],
                         'Прибор': [StatusEnum.CONTRACT, '_wow'],
                         'Параметр': [StatusEnum.CONTRACT, '_wow'],
                         'Артикул': [StatusEnum.CONTRACT, '_wow']},
            'н0000009': {'Вид': [StatusEnum.EMPTY, '_wow'],
                         'Производитель': [StatusEnum.EMPTY, '_wow'],
                         'Направление': [StatusEnum.EMPTY, '_wow'],
                         'Прибор': [StatusEnum.EMPTY, '_wow'],
                         'Параметр': [StatusEnum.EMPTY, '_wow'],
                         'Артикул': [StatusEnum.EMPTY, '_wow']},
            'н0000010': {'Вид': [StatusEnum.NEURAL, '_wow'],
                         'Производитель': [StatusEnum.NEURAL, '_wow'],
                         'Направление': [StatusEnum.NEURAL, '_wow'],
                         'Прибор': [StatusEnum.NEURAL, '_wow'],
                         'Параметр': [StatusEnum.NEURAL, '_wow'],
                         'Артикул': [StatusEnum.NEURAL, '_wow']},
            'н0000011': {'Вид': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR, '_wow']},
            'н0000012': {'Вид': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow']},
            'н0000013': {'Вид': [StatusEnum.AROUND, '_wow'],
                         'Производитель': [StatusEnum.AROUND, '_wow'],
                         'Направление': [StatusEnum.AROUND, '_wow'],
                         'Прибор': [StatusEnum.AROUND, '_wow'],
                         'Параметр': [StatusEnum.AROUND, '_wow'],
                         'Артикул': [StatusEnum.AROUND, '_wow']},
            'н0000014': {'Вид': [StatusEnum.SCROLLING, '_wow'],
                         'Производитель': [StatusEnum.SCROLLING, '_wow'],
                         'Направление': [StatusEnum.SCROLLING, '_wow'],
                         'Прибор': [StatusEnum.SCROLLING, '_wow'],
                         'Параметр': [StatusEnum.SCROLLING, '_wow'],
                         'Артикул': [StatusEnum.SCROLLING, '_wow']},
            'н0000015': {'Вид': [StatusEnum.MANUAL, '_wow'],
                         'Производитель': [StatusEnum.MANUAL, '_wow'],
                         'Направление': [StatusEnum.MANUAL, '_wow'],
                         'Прибор': [StatusEnum.MANUAL, '_wow'],
                         'Параметр': [StatusEnum.MANUAL, '_wow'],
                         'Артикул': [StatusEnum.MANUAL, '_wow']},
            'н0000016': {'Вид': [StatusEnum.CONTRACT, '_wow'],
                         'Производитель': [StatusEnum.CONTRACT, '_wow'],
                         'Направление': [StatusEnum.CONTRACT, '_wow'],
                         'Прибор': [StatusEnum.CONTRACT, '_wow'],
                         'Параметр': [StatusEnum.CONTRACT, '_wow'],
                         'Артикул': [StatusEnum.CONTRACT, '_wow']},
            'н0000017': {'Вид': [StatusEnum.EMPTY, '_wow'],
                         'Производитель': [StatusEnum.EMPTY, '_wow'],
                         'Направление': [StatusEnum.EMPTY, '_wow'],
                         'Прибор': [StatusEnum.EMPTY, '_wow'],
                         'Параметр': [StatusEnum.EMPTY, '_wow'],
                         'Артикул': [StatusEnum.EMPTY, '_wow']},
            'н0000018': {'Вид': [StatusEnum.NEURAL, '_wow'],
                         'Производитель': [StatusEnum.NEURAL, '_wow'],
                         'Направление': [StatusEnum.NEURAL, '_wow'],
                         'Прибор': [StatusEnum.NEURAL, '_wow'],
                         'Параметр': [StatusEnum.NEURAL, '_wow'],
                         'Артикул': [StatusEnum.NEURAL, '_wow']},
            'н0000019': {'Вид': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR, '_wow']},
            'н0000020': {'Вид': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow']},
            'н0000021': {'Вид': [StatusEnum.AROUND, '_wow'],
                         'Производитель': [StatusEnum.AROUND, '_wow'],
                         'Направление': [StatusEnum.AROUND, '_wow'],
                         'Прибор': [StatusEnum.AROUND, '_wow'],
                         'Параметр': [StatusEnum.AROUND, '_wow'],
                         'Артикул': [StatusEnum.AROUND, '_wow']},
            'н0000022': {'Вид': [StatusEnum.SCROLLING, '_wow'],
                         'Производитель': [StatusEnum.SCROLLING, '_wow'],
                         'Направление': [StatusEnum.SCROLLING, '_wow'],
                         'Прибор': [StatusEnum.SCROLLING, '_wow'],
                         'Параметр': [StatusEnum.SCROLLING, '_wow'],
                         'Артикул': [StatusEnum.SCROLLING, '_wow']},
            'н0000023': {'Вид': [StatusEnum.MANUAL, '_wow'],
                         'Производитель': [StatusEnum.MANUAL, '_wow'],
                         'Направление': [StatusEnum.MANUAL, '_wow'],
                         'Прибор': [StatusEnum.MANUAL, '_wow'],
                         'Параметр': [StatusEnum.MANUAL, '_wow'],
                         'Артикул': [StatusEnum.MANUAL, '_wow']},
            'н0000024': {'Вид': [StatusEnum.CONTRACT, '_wow'],
                         'Производитель': [StatusEnum.CONTRACT, '_wow'],
                         'Направление': [StatusEnum.CONTRACT, '_wow'],
                         'Прибор': [StatusEnum.CONTRACT, '_wow'],
                         'Параметр': [StatusEnum.CONTRACT, '_wow'],
                         'Артикул': [StatusEnum.CONTRACT, '_wow']},
            'н0000025': {'Вид': [StatusEnum.EMPTY, '_wow'],
                         'Производитель': [StatusEnum.EMPTY, '_wow'],
                         'Направление': [StatusEnum.EMPTY, '_wow'],
                         'Прибор': [StatusEnum.EMPTY, '_wow'],
                         'Параметр': [StatusEnum.EMPTY, '_wow'],
                         'Артикул': [StatusEnum.EMPTY, '_wow']},
            'н0000026': {'Вид': [StatusEnum.NEURAL, '_wow'],
                         'Производитель': [StatusEnum.NEURAL, '_wow'],
                         'Направление': [StatusEnum.NEURAL, '_wow'],
                         'Прибор': [StatusEnum.NEURAL, '_wow'],
                         'Параметр': [StatusEnum.NEURAL, '_wow'],
                         'Артикул': [StatusEnum.NEURAL, '_wow']},
            'н0000027': {'Вид': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR, '_wow']},
            'н0000028': {'Вид': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow']},
            'н0000029': {'Вид': [StatusEnum.AROUND, '_wow'],
                         'Производитель': [StatusEnum.AROUND, '_wow'],
                         'Направление': [StatusEnum.AROUND, '_wow'],
                         'Прибор': [StatusEnum.AROUND, '_wow'],
                         'Параметр': [StatusEnum.AROUND, '_wow'],
                         'Артикул': [StatusEnum.AROUND, '_wow']},
            'н0000030': {'Вид': [StatusEnum.SCROLLING, '_wow'],
                         'Производитель': [StatusEnum.SCROLLING, '_wow'],
                         'Направление': [StatusEnum.SCROLLING, '_wow'],
                         'Прибор': [StatusEnum.SCROLLING, '_wow'],
                         'Параметр': [StatusEnum.SCROLLING, '_wow'],
                         'Артикул': [StatusEnum.SCROLLING, '_wow']},
            'н0000031': {'Вид': [StatusEnum.MANUAL, '_wow'],
                         'Производитель': [StatusEnum.MANUAL, '_wow'],
                         'Направление': [StatusEnum.MANUAL, '_wow'],
                         'Прибор': [StatusEnum.MANUAL, '_wow'],
                         'Параметр': [StatusEnum.MANUAL, '_wow'],
                         'Артикул': [StatusEnum.MANUAL, '_wow']},
            'н0000032': {'Вид': [StatusEnum.CONTRACT, '_wow'],
                         'Производитель': [StatusEnum.CONTRACT, '_wow'],
                         'Направление': [StatusEnum.CONTRACT, '_wow'],
                         'Прибор': [StatusEnum.CONTRACT, '_wow'],
                         'Параметр': [StatusEnum.CONTRACT, '_wow'],
                         'Артикул': [StatusEnum.CONTRACT, '_wow']},
            'н0000033': {'Вид': [StatusEnum.EMPTY, '_wow'],
                         'Производитель': [StatusEnum.EMPTY, '_wow'],
                         'Направление': [StatusEnum.EMPTY, '_wow'],
                         'Прибор': [StatusEnum.EMPTY, '_wow'],
                         'Параметр': [StatusEnum.EMPTY, '_wow'],
                         'Артикул': [StatusEnum.EMPTY, '_wow']},
            'н0000034': {'Вид': [StatusEnum.NEURAL, '_wow'],
                         'Производитель': [StatusEnum.NEURAL, '_wow'],
                         'Направление': [StatusEnum.NEURAL, '_wow'],
                         'Прибор': [StatusEnum.NEURAL, '_wow'],
                         'Параметр': [StatusEnum.NEURAL, '_wow'],
                         'Артикул': [StatusEnum.NEURAL, '_wow']},
            'н0000035': {'Вид': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR, '_wow']},
            'н0000036': {'Вид': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Производитель': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Направление': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Прибор': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Параметр': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow'],
                         'Артикул': [StatusEnum.CLASSIFICATOR_AND_NEURAL, '_wow']},
            'н0000037': {'Вид': [StatusEnum.AROUND, '_wow'],
                         'Производитель': [StatusEnum.AROUND, '_wow'],
                         'Направление': [StatusEnum.AROUND, '_wow'],
                         'Прибор': [StatusEnum.AROUND, '_wow'],
                         'Параметр': [StatusEnum.AROUND, '_wow'],
                         'Артикул': [StatusEnum.AROUND, '_wow']},
            'н0000038': {'Вид': [StatusEnum.SCROLLING, '_wow'],
                         'Производитель': [StatusEnum.SCROLLING, '_wow'],
                         'Направление': [StatusEnum.SCROLLING, '_wow'],
                         'Прибор': [StatusEnum.SCROLLING, '_wow'],
                         'Параметр': [StatusEnum.SCROLLING, '_wow'],
                         'Артикул': [StatusEnum.SCROLLING, '_wow']},
            'н0000039': {'Вид': [StatusEnum.MANUAL, '_wow'],
                         'Производитель': [StatusEnum.MANUAL, '_wow'],
                         'Направление': [StatusEnum.MANUAL, '_wow'],
                         'Прибор': [StatusEnum.MANUAL, '_wow'],
                         'Параметр': [StatusEnum.MANUAL, '_wow'],
                         'Артикул': [StatusEnum.MANUAL, '_wow']},
            'н0000040': {'Вид': [StatusEnum.CONTRACT, '_wow'],
                         'Производитель': [StatusEnum.CONTRACT, '_wow'],
                         'Направление': [StatusEnum.CONTRACT, '_wow'],
                         'Прибор': [StatusEnum.CONTRACT, '_wow'],
                         'Параметр': [StatusEnum.CONTRACT, '_wow'],
                         'Артикул': [StatusEnum.CONTRACT, '_wow']}}

        # when:
        items = handler.read_file()

        # then:
        self.assertEqual(40, len(items))
        for item in items:
            expected_value_for_item = expected_values[item.id]
            for column in item.columns:
                self.assertEqual(
                    expected_value_for_item[column.name][0],
                    column.status
                )
                self.assertEqual(
                    expected_value_for_item[column.name][1],
                    column.value
                )

    def test_read_source_real(self):
        # given:
        file_path = get_file_source_path(os.path.join('file_handler', '25_Владельцы_анализаторов_обработка.xlsx'))
        reading_info = ReadingInfo(
            id_column_name='ID Позиции Базы',
            columns_for_copy=[ColumnToRead(column_name='Вид', status_name='Артикул'),
                              ColumnToRead(column_name='Направление', status_name='Статус вид'),
                              ColumnToRead(column_name='Производитель', status_name='Статус направление'),
                              ColumnToRead(column_name='Прибор', status_name='Статус прибор'),
                              ColumnToRead(column_name='Параметр', status_name='Статус параметр'),
                              ColumnToRead(column_name='Артикул', status_name='Статус артикул')]
        )
        handler = SourceFileHandler(reading_info, file_path)
        df = handler.read_file()
        print(df)
