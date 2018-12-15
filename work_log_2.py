"""
Python Web Development Techdegree
Project 4 - Work Log application w/ Database
by Maxwell Hunter
follow me on GitHub @mHunterAK
--------------------------------
"""
from peewee import (
                    Model, SqliteDatabase,
                    DateField, DateTimeField, TextField, IntegerField
                    )
import datetime
import os
import re

'''
As a user of the script, I should be able to choose whether to add a new entry
or lookup previous entries.
As a user of the script, if I choose to enter a new work log, I should be able
to provide my name, a task name, a number of minutes spent working on it, and
any additional notes I want to record.
As a user of the script, if I choose to find a previous entry, I should be
presented with four options: find by employee, find by date, find by time
spent, find by search term.
As a user of the script, if finding by employee, I should be presented with a
list of employees with entries and be able to choose one to see entries from.
As a user of the script, if finding by employee, I should be allowed to enter
employee name and then be presented with entries with that employee as their
creator.
As a user of the script, if finding by date, I should be presented with a list
of dates with entries and be able to choose one to see entries from.
As a user of the script, if finding by time spent, I should be allowed to
enter the amount of time spent on the project and then be presented with
entries containing that amount of time spent. As a user of the script, if
finding by a search term, I should be allowed to
enter a string and then be presented with entries containing that string in
the task name or notes.

As a fellow developer, I should find at least 50% of the code covered by tests.
I would use coverage.py to validate this amount of coverage.
'''

if __name__ == "__main__":  # pragma: no cover
    DATABASE = SqliteDatabase('web_log_2.db')
else:
    DATABASE = SqliteDatabase('TESTING_web_log_2.db')


TEST_MOCK_INPUT = [' ', ' ']


# function for clearing the terminal console
def clear_screen():
    os.system("clear")


# if the script is running tests,
# get next command from the test script
# otherwise, get the input from the user
def test_or_input(input_prompt):
    if __name__ == "__main__":  # pragma: no cover
        return input(input_prompt)
    else:
        try:
            return TEST_MOCK_INPUT.pop(0)
        except IndexError:
            raise EnnuiError('Looked for work to do, but none was found.')


# MODELS
class Entry(Model):
    # model attributes

    # user_name is the name of the user who created task
    user_name = TextField()
    # task_name is the name of the task
    task_name = TextField()
    # date is like a calendar box the task is referencing
    date = DateField()
    date_as_datetime = DateTimeField()
    # time is the number of minutes spent on the task
    time = IntegerField()
    # notes are any additional information about the task
    notes = TextField(
        # unlike the rest of the attributes, it can be blank
        null=True
    )
    # timestamp is of the most recent edit
    timestamp = DateTimeField()

    # validate and standardize are subclasses to separate out those functions
    class standardize():
        # function for standardizing user input: date
        # going from database into string
        def get_date(date):
            # split date into a list for day, month, and year
            d_list = date.split('/')
            # create datetime object from the string
            date_obj = datetime.date(
                # year
                int(d_list[2]),
                # month
                int(d_list[1]),
                # date
                int(d_list[0]),
            )
            # return the date, formatted in a way the database will accept
            # and humans can understand
            return date_obj.strftime("%d/%m/%Y")

        # going from string into database
        def set_date(string):
            # split date into a list for day, month, and year
            d_list = string.split('/')
            # build a datetime date from the list
            return datetime.date(
                int(d_list[2]),
                int(d_list[1]),
                int(d_list[0]),
                )

    class validate():
        def validate_date(date):
            try:
                # split date into a list for day, month, and year
                d_list = date.split('/')
                # build a datetime date from the list
                date = datetime.date(
                    int(d_list[2]),
                    int(d_list[1]),
                    int(d_list[0]),
                    )
                # date is valid
                return True
            # if we get a ValueError or IndexError
            except (ValueError, IndexError):
                # date is invalid
                return False

        # function for validating user input: time
        def validate_time(minutes):
            # if the submitted input is only digits, it's allowed
            return minutes.isdigit()

        # function for validating user input: user_name or task_name
        def validate_name(name):
            # must not be blank
            return len(name) > 0

    # print the entry preview
    # on one line, for query results
    def print_entry(self):
        print('{}.) {} ({}) by {} - {} minutes'.format(
            self.id,
            self.task_name,
            self.date,
            self.user_name,
            self.time,
            )
        )
        return True

    # print the entry details
    # on many lines, for query details
    def print_entry_details(self):
        print("{}.) {} by {}".format(
            self.id,
            self.task_name,
            self.user_name,
            )
        )
        print('''Last updated:
{}'''.format(
            self.timestamp
            )
        )
        print('Task Date: {}'.format(
            self.date
            )
        )
        print('{} minutes spent'.format(
            self.time
            )
        )
        print('notes: {}'.format(
            self.notes
            )
        )
        return True

    def delete_task(self):
        self.delete_instance()

    class Meta:
        database = DATABASE
        order_by = ('-id', )


# function for performing search and showing the results
def show_query_results(query_type, query_selection):
    # if query is blank
    if query_selection == "":
        # return blank
        return ""

    # for showing all entries
    if query_type == 'all':
        entries = Entry.select().order_by(Entry.date)

    if query_type == 'date':
        # split query into start and end dates
        dates = query_selection.split("||")
        # remove trailing list item
        del dates[-1]
        start_date = Entry.standardize.set_date(dates[0])
        end_date = Entry.standardize.set_date(dates[1])
        entries = Entry.select().where(
            Entry.date_as_datetime > start_date and
            Entry.date_as_datetime < end_date
        )

    # for showing by time spent
    elif query_type == 'time':
        entries = Entry.select().where(Entry.time == int(query_selection))

    # for searching entry name and notes
    elif query_type == 'exact':
        entries = Entry.select().where(
            Entry.task_name.contains(query_selection) or
            Entry.notes.contains(query_selection)
            )

    # for searching by regex
    elif query_type == 'pattern':
        entries = Entry.select()
        regex_match = []
        for entry in entries:
            if re.match(query_selection, entry.task_name):
                regex_match.append(entry)
            elif re.match(query_selection, entry.notes):
                regex_match.append(entry)
        entries = regex_match

    # print search results
    for entry in entries:
        entry.print_entry()

    # if query returned results,
    if len(entries) > 0:
        # ask for an id to view details
        select_by_id = test_or_input('Select entry by id to view details > ')
        # return the selected id
        if select_by_id.isdigit():
            return select_by_id
        elif select_by_id == '':
            return ""
        else:
            clear_screen()
            test_or_input("Invalid Selection. ")
            return ""
    # if query returned no results,
    else:
        test_or_input('No Search Results found.')
        return ""


# TASK CRUD: create task
def new_task():
    clear_screen()
    # I should be able to provide my name,
    user_name = ""
    while not Entry.validate.validate_name(user_name):
        user_name = test_or_input("Enter Your Name > ")
        if not Entry.validate.validate_name(user_name):
            print("Names may not be blank.")

    # a task name,
    task_name = ""
    while not Entry.validate.validate_name(task_name):
        task_name = test_or_input("Enter Task Name > ")
        if not Entry.validate.validate_name(task_name):
            print("Names may not be blank.")

    date = ""
    while not Entry.validate.validate_date(date):
        date = test_or_input("Enter date for this task, 'd/m/y' > ")
        if Entry.validate.validate_date(date):
            std_date = Entry.standardize.get_date(date)
            date_as_datetime = Entry.standardize.set_date(date)
        else:
            print("Invalid date. please try again.")

    time = ""
    while not Entry.validate.validate_time(time):
        # a number of minutes spent working on it,
        time = test_or_input("Minutes spent working on it > ")
        if not Entry.validate.validate_time(time):
            print("Please enter Minutes spent in whole integers")

    # and any additional notes I want to record.
    notes = test_or_input("Enter any additional notes > ")
    # if there is no entry,
    if not len(notes):
        # return a space (to avoid back option)
        notes = " "

    Entry.create(
        task_name=task_name,
        user_name=user_name,
        date=std_date,
        date_as_datetime=date_as_datetime,
        time=time,
        notes=notes,
        timestamp=datetime.datetime.now(),
    )
    # true is success
    return True


# TASK CRUD: recall task
def load_tasks():
    return Entry.select()


def edit_task(select_by_id):
    clear_screen()
    model_entry = Entry.get(Entry.id == select_by_id)

    valid_date = False
    while valid_date is False:
        date = test_or_input(
            'Enter new date (currently {}) > '.format(model_entry.date))

        valid_date = Entry.validate.validate_date(date)
        if valid_date:
            std_date = Entry.standardize.get_date(date)
            date_as_datetime = Entry.standardize.set_date(date)
        else:
            print("Invalid date. please try again.")
    model_entry.date = std_date
    model_entry.date_as_datetime = date_as_datetime

    time_input = ""
    while Entry.validate.validate_time(time_input) is False:
        time_input = test_or_input(
            'Enter new time (currently {} minutes) > '.format(
                model_entry.time
                ))
    model_entry.time = int(time_input)

    # user_name may not be changed intentionally

    task_name_input = ""
    while Entry.validate.validate_name(task_name_input) is False:
        task_name_input = test_or_input(
            'Enter new task name (currently {}) > '.format(
                model_entry.task_name
                ))
    model_entry.task_name = task_name_input

    model_entry.notes = test_or_input(
        'Enter new notes (currently {}) > '.format(
            model_entry.notes
            ))
    model_entry.timestamp = datetime.datetime.now()

    model_entry.save()
    test_or_input("Post Updated.")
    return True


# MVC View - main menu
# menu prime - layer 0
def main_menu():
    menu_selection = ""
    # I should be prompted
    # with a menu to choose whether to add a new entry or
    # lookup previous entries.
    clear_screen()
    print("--------")
    print("MAIN MENU")
    print("--------")
    # load tasks
    task_list = load_tasks()
    # get number of tasks
    number_of_tasks = len(task_list)
    # if there are tasks, show how many there are
    if number_of_tasks > 0:
        print("{} tasks available. ".format(number_of_tasks))
    print("[N]ew Entry")
    if number_of_tasks:
        print("[L]ookup previous entry")
    print("[Q]uit")
    print()
    print("At any time, enter blank input to go back one menu level")
    print()
    menu_selection = test_or_input("Enter your selection now > ")
    # As a user of the script,
    if menu_selection not in ['n', 'l', 'q']:
        clear_screen()
        test_or_input("invalid selection.")
    # if I choose to enter a new work log,
    elif menu_selection.lower() == 'n':
        if new_task():
            print('New Task Created!')
    # As a user of the script, if I choose to find a previous entry,
    if menu_selection.lower() == 'l':
        # one menu deeper
        lookup_menu()
    # EXTRA CREDIT: quit program
    if menu_selection.lower() == 'q':
        print("Thanks, bye!")
        quit()


# submenu under main_menu
# menu alpha - layer 1
def lookup_menu():
    # TODO: As a user of the script, if I choose to find a previous entry,
    # I should be presented with four options:

        # TODO find by employee,
            # As a user of the script, if finding by employee,
            # I should be presented with a list of employees with entries
            # and be able to choose one to see entries from.

            # As a user of the script, if finding by employee,
            # I should be allowed to enter employee name and then be
            # presented with entries with that employee as their creator.

    while True:
        entries = load_tasks()
        query_selection = ""
        clear_screen()
        print("--------")
        print("LOOKUP MENU")
        print("--------")
        print("{} available entries.".format(len(entries)))
        print()
        # I should be presented with four options:

        # find by date

        # As a user of the script, if finding by date, I should be
        # presented with a list of dates with entries and be able to
        # choose one to see entries from.

        # show all entries
        print("Show [A]ll entries sorted by date")
        # fine entry by employee
        print("Show entries for a specific e[M]ployee")
        # fine entry by date
        print("Find old entry by [D]ate")
        # find by time spent
        print("Find old entry by [T]ime Spent")
        # find by exact search
        print("Find old entry by [E]xact Search")
        # find by pattern
        print("Find old entry by regex [P]attern")
        print()
        # back to main menu
        menu_selection = test_or_input("Enter your selection now > ")
        clear_screen()

        # return to the previous menu
        if menu_selection == '':
            break

        if menu_selection not in ['a', 'd', 'e', 'm', 'p', 't', ]:
            test_or_input("invalid selection.")
            # start loop over
            continue

        elif menu_selection[0].lower() == 'a':
            select_by_id = show_query_results(
                'all', 'd')

        # select entries by date range
        elif menu_selection[0].lower() == 'd':
            # take two date entries, a start and end to get a date range
            date_range = ['start', 'end']
            # save the dates selected in a dictionary
            selected_dates = []
            # for both dates in date_range
            for i in range(len(date_range)):
                # clear date variable
                valid_date = False
                # while we don't have a valid date
                while valid_date is False:
                    # get user input
                    date = test_or_input(
                        "Enter your {} time range query > ".format(
                            date_range[i]
                            )
                    )
                    # validate date input
                    if Entry.validate.validate_date(date):
                        selected_dates.append(
                            Entry.standardize.get_date(date))
                        valid_date = True
                    # if invalid, try again
                    else:
                        print("Invalid date. please try again.")
                        valid_date = False
                # combine both date strings to pass into show_query_results
                query_selection = ""
                # for both dates in date_range
                for i in range(len(selected_dates)):
                    query_selection += selected_dates[i] + "||"
            select_by_id = show_query_results(
                'date', query_selection)

        elif menu_selection[0].lower() == 't':
            # ask for time spent
            query_selection = test_or_input(
                "Enter your time spent query in number of minutes > ")
            select_by_id = show_query_results(
                'time', query_selection)

        elif menu_selection[0].lower() == 'e':
            # ask for exact search
            query_selection = test_or_input(
                "Enter your exact search now > ")
            select_by_id = show_query_results(
                'exact', query_selection)

        elif menu_selection[0].lower() == 'p':
            # ask for pattern
            query_selection = test_or_input(
                "Enter your regex pattern now > ")
            select_by_id = show_query_results(
                'pattern', query_selection)

        if not select_by_id.isdigit():
            # if an number is not provided, start loop over
            continue
        # TODO: separate this out into separate entry_menu (entry or entry.id)
        # if id is not blank
        if select_by_id != "":
            clear_screen()
            try:
                # get entry from id
                entry = Entry.get(Entry.id == select_by_id)
            except Entry.DoesNotExist:
                test_or_input("Invalid task id.")
                continue
            # show detailed entry information
            entry.print_entry_details()

            # controller: if they want to edit or delete
            edit_delete_input = test_or_input(
                'Would you like to [E]dit or [D]elete this post? > ')
            # if so, show edit or delete screen
            if edit_delete_input.lower() == 'd':
                Entry.get(select_by_id).delete_task()
                break
            elif edit_delete_input.lower() == 'e':
                edit_task(select_by_id)
                break
            # up one menu
            elif edit_delete_input == "":
                continue
            else:
                clear_screen()
                test_or_input('Invalid Selection. ')
            # refresh query_selection for next loop
            query_selection = ''


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
    return True


if __name__ == "__main__":  # pragma: no cover
    initialize()
    while True:
        main_menu()


class EnnuiError(Exception):
    def __init__(self, value):
        self.value = value
