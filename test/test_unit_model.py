import unittest

from source.model.dto import StatusEnum, SourceItem, SourceColumnData, search


class ModelTests(unittest.TestCase):
    def test_search_status(self):
        # given:
        data = [
            ('Контракт', StatusEnum.CONTRACT),
            ('Контракт_', StatusEnum.EMPTY),
            ('', StatusEnum.EMPTY),
            (None, StatusEnum.EMPTY)
        ]

        # when:
        for str_value, status in data:
            # then:

            self.assertEqual(search(str_value), status)

    def test_compare_status(self):
        # given:
        data = [
            (StatusEnum.CONTRACT, StatusEnum.CONTRACT, True),
            (StatusEnum.CONTRACT, StatusEnum.MANUAL, True),
            (StatusEnum.CONTRACT, StatusEnum.AROUND, True),
            (StatusEnum.CONTRACT, StatusEnum.SCROLLING, True),
            (StatusEnum.CONTRACT, StatusEnum.ALT_BASE, True),
            (StatusEnum.CONTRACT, StatusEnum.CLASSIFICATOR, True),
            (StatusEnum.CONTRACT, StatusEnum.CLASSIFICATOR_AND_NEURAL, True),
            (StatusEnum.CONTRACT, StatusEnum.EMPTY, True),

            (StatusEnum.MANUAL, StatusEnum.CONTRACT, False),
            (StatusEnum.MANUAL, StatusEnum.MANUAL, True),
            (StatusEnum.MANUAL, StatusEnum.AROUND, True),
            (StatusEnum.MANUAL, StatusEnum.SCROLLING, True),
            (StatusEnum.MANUAL, StatusEnum.ALT_BASE, True),
            (StatusEnum.MANUAL, StatusEnum.CLASSIFICATOR, True),
            (StatusEnum.MANUAL, StatusEnum.CLASSIFICATOR_AND_NEURAL, True),
            (StatusEnum.MANUAL, StatusEnum.EMPTY, True),

            (StatusEnum.AROUND, StatusEnum.CONTRACT, False),
            (StatusEnum.AROUND, StatusEnum.MANUAL, False),
            (StatusEnum.AROUND, StatusEnum.AROUND, True),
            (StatusEnum.AROUND, StatusEnum.SCROLLING, True),
            (StatusEnum.AROUND, StatusEnum.ALT_BASE, True),
            (StatusEnum.AROUND, StatusEnum.CLASSIFICATOR, True),
            (StatusEnum.AROUND, StatusEnum.CLASSIFICATOR_AND_NEURAL, True),
            (StatusEnum.AROUND, StatusEnum.EMPTY, True),

            (StatusEnum.SCROLLING, StatusEnum.CONTRACT, False),
            (StatusEnum.SCROLLING, StatusEnum.MANUAL, False),
            (StatusEnum.SCROLLING, StatusEnum.AROUND, True),
            (StatusEnum.SCROLLING, StatusEnum.SCROLLING, True),
            (StatusEnum.SCROLLING, StatusEnum.ALT_BASE, True),
            (StatusEnum.SCROLLING, StatusEnum.CLASSIFICATOR, True),
            (StatusEnum.SCROLLING, StatusEnum.CLASSIFICATOR_AND_NEURAL, True),
            (StatusEnum.SCROLLING, StatusEnum.EMPTY, True),

            (StatusEnum.ALT_BASE, StatusEnum.CONTRACT, False),
            (StatusEnum.ALT_BASE, StatusEnum.MANUAL, False),
            (StatusEnum.ALT_BASE, StatusEnum.AROUND, True),
            (StatusEnum.ALT_BASE, StatusEnum.SCROLLING, True),
            (StatusEnum.ALT_BASE, StatusEnum.ALT_BASE, True),
            (StatusEnum.ALT_BASE, StatusEnum.CLASSIFICATOR, True),
            (StatusEnum.ALT_BASE, StatusEnum.CLASSIFICATOR_AND_NEURAL, True),
            (StatusEnum.ALT_BASE, StatusEnum.EMPTY, True),

            (StatusEnum.CLASSIFICATOR, StatusEnum.CONTRACT, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.MANUAL, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.AROUND, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.SCROLLING, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.ALT_BASE, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.CLASSIFICATOR, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.CLASSIFICATOR_AND_NEURAL, False),
            (StatusEnum.CLASSIFICATOR, StatusEnum.EMPTY, True),

            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.CONTRACT, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.MANUAL, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.AROUND, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.SCROLLING, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.ALT_BASE, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.CLASSIFICATOR, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.CLASSIFICATOR_AND_NEURAL, False),
            (StatusEnum.CLASSIFICATOR_AND_NEURAL, StatusEnum.EMPTY, True),

            (StatusEnum.EMPTY, StatusEnum.CONTRACT, False),
            (StatusEnum.EMPTY, StatusEnum.MANUAL, False),
            (StatusEnum.EMPTY, StatusEnum.AROUND, False),
            (StatusEnum.EMPTY, StatusEnum.SCROLLING, False),
            (StatusEnum.EMPTY, StatusEnum.ALT_BASE, False),
            (StatusEnum.EMPTY, StatusEnum.CLASSIFICATOR, False),
            (StatusEnum.EMPTY, StatusEnum.CLASSIFICATOR_AND_NEURAL, False),
            (StatusEnum.EMPTY, StatusEnum.EMPTY, False),
        ]

        # when:
        for source_status, target_status, need_to_refresh in data:
                # then:
                self.assertEqual(
                    source_status.need_to_refresh(target_status),
                    need_to_refresh
                )

    def test_source_status_compare(self):
        # given:
        source = SourceItem(
            id='test-id',
            id_name='test-name',
            columns=[SourceColumnData(
                name='test-column',
                value='test-value',
                status_name='test-status',
                status=StatusEnum.ALT_BASE)]
        )
        xls_status = StatusEnum.CLASSIFICATOR_AND_NEURAL

        # when:
        need_to_refresh_test_column = source.columns[0].status.need_to_refresh(xls_status)

        # then:
        self.assertTrue(need_to_refresh_test_column)
