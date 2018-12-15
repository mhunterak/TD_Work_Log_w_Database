import unittest
import work_log_2

TEST_MOCK_INPUT = [' ', ' ']


# this should always be the first test run
class Test_A_database(unittest.TestCase):
    def test_db(self):
        self.assertEqual(work_log_2.DATABASE.database, 'TESTING_web_log_2.db')

    def test_initialize(self):
        # test initialize
        self.assertTrue(work_log_2.initialize())


class Test_A_tabla_rasa(unittest.TestCase):
    # should always be the second test run
    def test_main_menu_tabla_rasa(self):
        work_log_2.TEST_MOCK_INPUT = ['x', '']
        work_log_2.main_menu()


class Test_entryMethods(unittest.TestCase):
    def test_validate_date(self):
        self.assertTrue(work_log_2.Entry.validate.validate_date('2/2/2'))
        self.assertFalse(work_log_2.Entry.validate.validate_date('2/22'))

    def test_validate_time(self):
        self.assertTrue(work_log_2.Entry.validate.validate_time('220'))
        self.assertFalse(work_log_2.Entry.validate.validate_time('two'))

    def test_get_date(self):
        self.assertEqual(
            work_log_2.Entry.standardize.get_date('2/2/2'), '02/02/0002')

    def test_set_date(self):
        self.assertEqual(
            work_log_2.Entry.standardize.set_date("2/2/2").day, 2
        )

    def test_validate_name(self):
        self.assertTrue(work_log_2.Entry.validate.validate_name('Valid'))
        self.assertFalse(work_log_2.Entry.validate.validate_name(''))


class Test_C_mockInputs(unittest.TestCase):
    def test_create_edit_print_entry_delete_task(self):
        # set mock inputs for CREATE test, invalid then valid
        work_log_2.TEST_MOCK_INPUT = [
            '', 'PYTHON UNITTEST',
            '', 'TESTING NEW TASK',
            '12/15', '13/12/2018',
            "one", '111',
            '', '', ''
        ]
        work_log_2.new_task()
        # get the newly created entry
        entry = work_log_2.Entry.get()
        select_by_id = entry.id

        # test PRINT print_entry function
        entry.print_entry()
        entry.print_entry_details()

        work_log_2.TEST_MOCK_INPUT = [
            '12/15', '13/12/18',
            'one', '111',
            '', 'TESTING NEW TASK',
            'abcdefghijklm', ''
        ]
        self.assertTrue(
            work_log_2.edit_task(select_by_id)
        )

        # test querying, should return the test task
        # show_query_results(query_type, query_selection)

        query_types = [
            'all',
            'time',
            'date',
            'exact',
            'exact',
            'pattern',
            'pattern',
            'all',
            ]
        queries = [
            # all
            '',
            # time
            '111',
            # date
            '1/1/1||9/9/9||',
            # exact
            'TESTING',
            'NOTFOUND',
            # pattern
            '[A-Z]{3}',
            '[a-z]{10}',
            ' ',
        ]

        work_log_2.TEST_MOCK_INPUT = [' '] * (len(query_types) * 2)
        for query_type in query_types:
            work_log_2.show_query_results(
                query_type,
                queries.pop(0),
            )

        # additional test for selecting an id from options
        work_log_2.TEST_MOCK_INPUT = ['1']
        work_log_2.show_query_results(
                'all',
                ' ',
            )

        work_log_2.TEST_MOCK_INPUT = ['']
        work_log_2.show_query_results(
                'all',
                ' ',
            )

        work_log_2.TEST_MOCK_INPUT = [
            '', ' '
        ]
        select_by_id = work_log_2.Entry.get().id


class Test_entryInstance(unittest.TestCase):
    def test_print_query_entry(self):
        entries = work_log_2.Entry.select()
        for entry in entries:
            self.assertTrue(entry.print_entry())
            self.assertTrue(entry.print_entry_details())
            # only need to do this for one entry
            break

    def test_load_tasks(self):
        work_log_2.load_tasks()


class Test_E_menus(unittest.TestCase):
    def test_m_main_menu_invalid_entry(self):
        # TODO: testing the menu - only enter valid data
        # data validation is tested elsewhere (test_mockInputs)
        work_log_2.TEST_MOCK_INPUT = [
            # invalid inputs
            'x',
            ' ',
            'q',
            ' '
            ]
        work_log_2.main_menu()

    def test_main_menu_new_task(self):
        work_log_2.TEST_MOCK_INPUT = [
            # new task
            'n',
            'unittest.main',
            'main_menu_test_entry',
            '13/12/18',
            '111',
            'TESTING MENUS',
            'no notes!',
            '',
            '',
        ]
        work_log_2.main_menu()

    def test_main_menu_lookup_task(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'l',
            'a',
            '',
            '',
        ]
        work_log_2.main_menu()

    def test_main_menu_quit(self):
        work_log_2.TEST_MOCK_INPUT = [
            # new task
            'q',
            '',
        ]
        try:
            work_log_2.main_menu()
        # this is the error we're looking for
        except SystemExit:
            pass

    def test_lookup_menu_select_invalid(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'l',
            'a',
            '9999',
            '',
            '',
            '',
        ]
        work_log_2.lookup_menu()

        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'l',
            'a',
            '',
        ]
        work_log_2.lookup_menu()

    def test_lookup_menu_by_time(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            't',
            '111',
            '',
            '',
        ]
        work_log_2.lookup_menu()

    def test_lookup_menu_by_date(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'd',
            '111',
            ' ',
            '1/1/1',
            '999',
            ' ',
            '9/9/9',
            '',
            '',
        ]
        work_log_2.lookup_menu()

    def test_lookup_menu_by_exact(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'e',
            'unit',
            '',
            '',
        ]
        work_log_2.lookup_menu()

    def test_lookup_menu_by_regex(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'p',
            '[a-z]{3}',
            '',
            '',
        ]
        work_log_2.lookup_menu()

    def test_Z_lookup_menu_select_by_id(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'a',
            str(work_log_2.Entry.get().id),
            '1',
            ' ',
            '',
        ]
        work_log_2.lookup_menu()

    def test_lookup_menu_select_by_id_invalid(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'a',
            '999',
            '',
            '',
            '',
        ]
        work_log_2.lookup_menu()

    def test_Z_lookup_menu_select_by_id_continue(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'a',
            str(work_log_2.Entry.get().id),
            '',
            '',
            '',
            '',
            '',
        ]
        work_log_2.lookup_menu()

    def test_Y_lookup_menu_select_by_id_edit(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'a',
            str(
                work_log_2.Entry.get().id
                ),
            'e',
            # this behavior should skip the input keeping it the same
            #            '',
            #            '',
            #            '',
            '7/7/7',
            '777',
            'seven',
            '',
            ''
        ]
        work_log_2.lookup_menu()

    def test_Z_lookup_menu_select_by_id_delete(self):
        work_log_2.TEST_MOCK_INPUT = [
            # lookup task
            'a',
            str(work_log_2.Entry.get().id),
            'd',
            ''
        ]
        work_log_2.lookup_menu()

    def test_ennui(self):
        work_log_2.TEST_MOCK_INPUT = []
        try:
            work_log_2.main_menu()
        # this is the error we're looking for
        except work_log_2.EnnuiError:
            pass


class test_ZZZ_clean_up_orphan_entries(unittest.TestCase):
    def clean_up_orphan_entries(self):
        for Entry in work_log_2.load_tasks():
            work_log_2.TEST_MOCK_INPUT.append('')
            work_log_2.delete_task(Entry.id)


if __name__ == '__main__':  # pragma: no cover
    work_log_2.clear_screen()
    unittest.main(verbosity=2)
