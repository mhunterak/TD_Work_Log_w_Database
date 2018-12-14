import unittest
import work_log_2

# TODO: the rest of the functions needed to test require manual input.
# working on a better way to do it.


class test_database(unittest.TestCase):
    def test_db(self):
        self.assertEqual(work_log_2.DATABASE.database, 'web_log_2.db')

    def test_initialize(self):
        # test initialize
        self.assertTrue(work_log_2.initialize())


class test_entryMethods(unittest.TestCase):
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


class test_entryInstance(unittest.TestCase):
    def test_print_entry(self):
        entry = work_log_2.Entry.get()
        self.assertTrue(entry.print_entry())
        self.assertTrue(entry.print_entry_details())

    def test_load_tasks(self):
        work_log_2.load_tasks()
        pass

    def test_show_query_results(self):
        self.assertEqual(work_log_2.show_query_results('all', ''), '')


'''
    def test_new_task(self):
        self.assertTrue(work_log_2.new_task())


        print()
        print('----------------------------------')
        print("TEST NOTES: ENTER '1' ON NEXT LINE")
        print('----------------------------------')
        print()
        self.assertTrue(
            len(work_log_2.show_query_results('all', 'date')) > 0
            )

        print()
        print('----------------------------------')
        print("TEST NOTES: ENTER '1' ON NEXT LINE")
        print('----------------------------------')
        print()
        self.assertTrue(
            len(work_log_2.show_query_results('time', '222')) > 0
            )

        print()
        print('----------------------------------')
        print("TEST NOTES: ENTER '1' ON NEXT LINE")
        print('----------------------------------')
        print()
        self.assertTrue(
            len(work_log_2.show_query_results('exact', 'one')) > 0
            )

        print()
        print('----------------------------------')
        print("TEST NOTES: ENTER '1' ON NEXT LINE")
        print('----------------------------------')
        print()
        self.assertTrue(
            len(work_log_2.show_query_results('pattern', '[a-z]{3}')) > 0
            )
'''

if __name__ == '__main__':  # pragma: no cover
    work_log_2.clear_screen()
    unittest.main(verbosity=2)
