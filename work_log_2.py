"""
Python Web Development Techdegree
Project 4 - Work Log application w/ Database
by Maxwell Hunter
follow me on GitHub @mHunterAK
--------------------------------
HINT: run the following code to activate virtual environment

source env/bin/activate


TODO: at least 50% of the code covered by tests as detirmined by coverage
TODO: EXTRA CREDOT: at least 50% of the code covered by tests (coverage)

TODO: build function to get user input, or mock user input with a string

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

DATABASE = SqliteDatabase('web_log_2.db')


# function for clearing the terminal console
def clear_screen():
    os.system("clear")


# MODELS
class Entry(Model):
    # model attributes

    # user_name is the name of the user who created task
    user_name = TextField()
    # task_name is the name of the task
    task_name = TextField()
    # date is like a calendar box the task is referencing
    date = DateField()
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
        entries = Entry.select()

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
        select_by_id = input('Select entry by id to view details > ')
        # return the selected id
        if select_by_id.isdigit():
            return select_by_id
        elif select_by_id == '':
            return ""
        else:
            clear_screen()
            input("Invalid Selection. ")
            return ""
    # if query returned no results,
    else:
        input('No Search Results found.')
        return ""


# TASK CRUD: create task
def new_task():
    clear_screen()
    # I should be able to provide my name,
    user_name = ""
    while not Entry.validate.validate_name(user_name):
        user_name = input("Enter Your Name > ")
        if not Entry.validate.validate_name(user_name):
            print("Names may not be blank.")

    # a task name,
    task_name = ""
    while not Entry.validate.validate_name(task_name):
        task_name = input("Enter Task Name > ")
        if not Entry.validate.validate_name(task_name):
            print("Names may not be blank.")

    date = ""
    while not Entry.validate.validate_date(date):
        date = input("Enter date for this task, 'd/m/y' > ")
        if Entry.validate.validate_date(date):
            date = Entry.standardize.get_date(date)
        else:
            print("Invalid date. please try again.")

    time = ""
    while not Entry.validate.validate_time(time):
        # a number of minutes spent working on it,
        time = input("Minutes spent working on it > ")
        if not Entry.validate.validate_time(time):
            print("Please enter Minutes spent in whole integers")

    # and any additional notes I want to record.
    notes = input("Enter any additional notes > ")
    # if there is no entry,
    if not len(notes):
        # return a space (to avoid back option)
        notes = " "

    Entry.create(
        task_name=task_name,
        user_name=user_name,
        date=date,
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
        date = input(
            'Enter new date (currently {}) > '.format(model_entry.date))

        valid_date = Entry.validate.validate_date(date)
        if valid_date:
            date = Entry.standardize.get_date(date)
        else:
            print("Invalid date. please try again.")
    model_entry.date = date

    time_input = ""
    while Entry.validate.validate_time(time_input) is False:
        time_input = input(
            'Enter new time (currently {} minutes) > '.format(
                model_entry.time
                ))
    model_entry.time = int(time_input)

    # user_name may not be changed intentionally

    task_name_input = ""
    while Entry.validate.validate_name(task_name_input) is False:
        task_name_input = input(
            'Enter new task name (currently {}) > '.format(
                model_entry.task_name
                ))
    model_entry.task_name = task_name_input

    model_entry.notes = input(
        'Enter new notes (currently {}) > '.format(
            model_entry.notes
            ))
    model_entry.timestamp = datetime.datetime.now()

    model_entry.save()
    input("Post Updated.")


# TASK CRUD - DELETE TASK
def delete_task(select_by_id):
    Entry.get(Entry.id == select_by_id).delete_instance()
    input('Post #{} deleted.'.format(select_by_id))


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
    menu_selection = input("Enter your selection now > ")
    # As a user of the script,
    if menu_selection not in ['n', 'l', 'q']:
        clear_screen()
        input("invalid selection.")
    # if I choose to enter a new work log,
    elif menu_selection.lower() == 'n':
        if new_task():
            print('New Task Created!')
    # As a user of the script, if I choose to find a previous entry,
    if menu_selection.lower() == 'l':
        if number_of_tasks > 0:
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
        # find by employee,
            # As a user of the script, if finding by employee,
            # I should be presented with a list of employees with entries
            # and be able to choose one to see entries from.

            # As a user of the script, if finding by employee,
            # I should be allowed to enter employee name and then be
            # presented with entries with that employee as their creator.

        # find by date,
            # As a user of the script, if finding by date, I should be
            # presented with a list of dates with entries and be able to
            # choose one to see entries from.

        # find by time spent,
            # As a user of the script, if finding by time spent,
            # I should be allowed to enter the amount of time spent on the
            # project and then be presented with entries containing that
            # amount of time spent.

        # find by search term.
            # As a user of the script, if finding by a search term,
            # I should be allowed to enter a string and then be presented with
            # entries containing that string in the task name or notes.

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
        print("Find old entry by [D]ate")
        # find by time spent
        print("Find old entry by [T]ime Spent")
        # find by exact search
        print("Find old entry by [E]xact Search")
        # find by pattern
        print("Find old entry by regex [P]attern")
        print()
        # back to main menu
        menu_selection = input("Enter your selection now > ")
        clear_screen()

        # return to the previous menu
        if menu_selection == '':
            break

        if menu_selection not in ['d', 't', 'e', 'p']:
            input("invalid selection.")
            # start loop over
            continue

        elif menu_selection[0].lower() == 'd':
            # TODO: separate all tasks (current) into search by date (desired)
            select_by_id = show_query_results(
                'all', 'd')

        elif menu_selection[0].lower() == 't':
            # ask for time spent
            query_selection = input(
                "Enter your time spent query in number of minutes > ")
            select_by_id = show_query_results(
                'time', query_selection)

        elif menu_selection[0].lower() == 'e':
            # ask for exact search
            query_selection = input(
                "Enter your exact search now > ")
            select_by_id = show_query_results(
                'exact', query_selection)

        elif menu_selection[0].lower() == 'p':
            # ask for pattern
            query_selection = input(
                "Enter your regex pattern now > ")
            select_by_id = show_query_results(
                'pattern', query_selection)
        if not select_by_id.isdigit():
            # if an number is not provided, start loop over
            continue
        # if the id requested is greater than the number of entries,
        if int(select_by_id) > (len(entries)):
            clear_screen()
            input("Invalid task id.")
            continue

        # TODO: separate this out into separate entry_menu (entry or entry.id)
        # if id is not blank
        if select_by_id != "":
            clear_screen()
            # get entry from id
            entry = Entry.get(Entry.id == select_by_id)
            # show detailed entry information
            entry.print_entry_details()

            # controller: if they want to edit or delete
            edit_delete_input = input(
                'Would you like to [E]dit or [D]elete this post? > ')
            # if so, show edit or delete screen
            if edit_delete_input.lower() == 'd':
                delete_task(select_by_id)
                break
            elif edit_delete_input.lower() == 'e':
                edit_task(select_by_id)
                break
            # up one menu
            elif edit_delete_input == "":
                continue
            else:
                clear_screen()
                input('Invalid Selection. ')
            # refresh query_selection for next loop
            query_selection = ''
        else:
            # go back to lookup menu
            continue


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
    return True


if __name__ == "__main__":  # pragma: no cover
    initialize()
    while True:
        main_menu()
