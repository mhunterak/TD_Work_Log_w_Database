"""
Python Web Development Techdegree
Project 4 - Work Log application w/ Database
by Maxwell Hunter
follow me on GitHub @mHunterAK
--------------------------------
"""
from peewee import (Model, SqliteDatabase,
                    DateField, DateTimeField, TextField, IntegerField
                    )  # pragma: no cover
import datetime
import os
import re

'''
Instructions:
Create a command line application that will allow employees to enter
their name, time worked, task worked on, and general notes about the
task into a database. There should be a way to add a new entry,
list all entries for a particular employee, and list all entries that match
a date or search term. Print a report of this information to the screen,
including the date, title of task, time spent, employee, and general notes.
'''

if __name__ == "__main__":  # pragma: no cover
    DATABASE = SqliteDatabase('web_log_2.db')
else:
    DATABASE = SqliteDatabase('TESTING_web_log_2.db')

# variable for mocking user input by tests.py
TEST_MOCK_INPUT = []


# function for clearing the terminal console
def clear_screen():
    os.system("clear")


# function for mocking user input
def test_or_input(input_prompt):
    # if the script is running as __main__,
    if __name__ == "__main__":  # pragma: no cover - tested manually
        # get the input from the user
        return input(input_prompt)
    # if the script is running tests,
    else:
        try:
            # get next command from the test mock input list
            return TEST_MOCK_INPUT.pop(0)
        # if the input list is empty,
        except IndexError:
            # raise Ennui Error
            raise EnnuiError('Looked for work to do, but nothing was found.')


# ERRORS
class EnnuiError(Exception):
    def __init__(self, value):
        self.value = value


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

    # subclass for data validation
    class validate():
        # function for validating user input: dates
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
    def print_entry(self):
        # on one line, for query results
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
    def print_entry_details(self):
        # on many lines, for query details
        print("{}.) {} by {}".format(
            self.id,
            self.task_name,
            self.user_name,
            )
        )
        print('''Last updated:
{}'''.format(self.timestamp)
        )
        print('Task Date: {}'.format(self.date))
        print('{} minutes spent'.format(self.time))
        print('notes: {}'.format(self.notes))
        return True

    # self destruct sequence
    def delete_task(self):
        self.delete_instance()

    # database info
    class Meta:
        database = DATABASE
        order_by = ('-id', )


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


# TASK CRUD: update task
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
        print("[L]ookup existing entry")
    print("[Q]uit")
    print()
    print("At any time, enter blank input to go back one menu level")
    print()
    menu_selection = test_or_input("Enter your selection now > ")
    # As a user of the script,
    if menu_selection not in ['n', 'l', 'q']:
        clear_screen()
        test_or_input("invalid selection 2.")
    # if I choose to enter a new work log,
    elif menu_selection.lower() == 'n':
        if new_task():
            print('New Task Created!')
    # As a user of the script, if I choose to find a existing entry,
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
    while True:
        entries = load_tasks()
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
        if menu_selection in ['', ' ']:
            break
        results_menu(menu_selection)


def results_menu(menu_selection):
        # return to the previous menu
        if menu_selection == '':
            return False

        if menu_selection not in ['a', 'd', 'e', 'm', 'p', 't', ]:
            test_or_input("invalid selection 3. ")
            # back one menu
            return False

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

        elif menu_selection[0].lower() == 'm':
            # ask for time spent
            query_selection = test_or_input(
                "Enter the Employee name query > ")
            select_by_id = show_query_results(
                'employee', query_selection)

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

        if not select_by_id.isdigit() and select_by_id not in ['n', 'p']:
            # if an number or next/previous is not provided, restart loop
            return False

        entry_menu(select_by_id)


# function for performing search and showing the results
# arguably, this could be it's own submenu - but for UX reasons,
# we don't want people stuck in a loop for it.
def show_query_results(query_type, query_selection):
    # if query is blank
    if query_selection == "":
        # return blank
        return ""

    # for showing all entries
    if query_type == 'all':
        # all entries sorted by date
        entries = Entry.select().order_by(Entry.date)

    if query_type == 'date':
        # split query into start and end dates
        dates = query_selection.split("||")
        # remove trailing list item, the extra pipes (||)
        del dates[-1]
        # separate start and end dates
        start_date = Entry.standardize.set_date(dates[0])
        end_date = Entry.standardize.set_date(dates[1])
        # query database
        entries = Entry.select().where(
            Entry.date_as_datetime > start_date and
            Entry.date_as_datetime < end_date
        )

    # for searching employee name
    elif query_type == 'employee':
        # query database
        entries = Entry.select().where(
            Entry.user_name.contains(query_selection)
            )

    # for showing by time spent
    elif query_type == 'time':
        # query database
        entries = Entry.select().where(Entry.time == int(query_selection))

    # for searching entry name and notes
    elif query_type == 'exact':
        # query database
        entries = Entry.select().where(
            Entry.task_name.contains(query_selection) or
            Entry.notes.contains(query_selection)
            )

    # for searching by regex
    elif query_type == 'pattern':
        # query database
        entries = Entry.select()
        # I don't like peewee's regex search options,
        # so it's being handled at a higher level
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
            test_or_input("Invalid Selection 1. ")
            return ""
    # if query returned no results,
    else:
        test_or_input('No Search Results found.')
        return ""


# submenu under lookup_menu
# menu  - layer 4
def entry_menu(select_by_id):
    # loop menu until return to previous menu with break
    while True:
        # if input variable is not blank
        if select_by_id is not "":
            clear_screen()
            try:
                # load entry from id
                entry = Entry.get(Entry.id == select_by_id)
            # if no entry is found,
            except Entry.DoesNotExist:
                # alert user
                test_or_input("Couldn't find that task {}.".format(
                    select_by_id))
                # return to previous menu
                break
            else:
                # show detailed entry information
                entry.print_entry_details()
            # controller: if they want next or previous, or to edit or delete
            print("Enter [N]ext or [P]revious entry")
            edit_delete_input = test_or_input(
                'Or, would you like to [E]dit or [D]elete this post? > ')
            # if no selection is made,
            if edit_delete_input.lower() == '':
                break

            # if delete is selected,
            if edit_delete_input.lower() == 'd':
                # delete entry
                Entry.get(select_by_id).delete_task()
                # return to previous menu
                break

            elif edit_delete_input.lower() == 'e':
                # edit entry
                edit_task(select_by_id)
                # return to previous menu
                break
            if edit_delete_input.lower() == 'n':
                # show next entry, by date
                newer_entries = Entry.select(
                    Entry.date_as_datetime > (
                        entry.date_as_datetime
                        )
                    ).order_by(
                    Entry.date_as_datetime)
                for entry in newer_entries:
                    select_by_id = entry.id
                    break
            elif edit_delete_input.lower() == 'p':
                # show previous entry, by date
                newer_entries = Entry.select(
                    Entry.date_as_datetime < (
                        entry.date_as_datetime)
                    ).order_by(
                    -Entry.date_as_datetime)
                for entry in newer_entries:
                    select_by_id = entry.id
                    break
            entry_menu(select_by_id)
            clear_screen()
            test_or_input('Invalid Selection. 4')


def initialize():
    # open database connection
    DATABASE.connect()
    # create tables, if they don't exist
    DATABASE.create_tables([Entry], safe=True)
    # close database connection
    DATABASE.close()
    # return success
    return True


if __name__ == "__main__":  # pragma: no cover
    initialize()
    while True:
        main_menu()
