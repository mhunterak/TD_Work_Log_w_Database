# TD_Work_Log_w_Database

Run the following code to activate virtual environment:

> source env/bin/activate

Install required packages, if running your own virtual environment:

>  sudo -H pip3 install -r requirements.txt

To see coverage report, visit /htmlcov/index.html

Run Tests: (omit environment packages)

> coverage run --omit */env/* tests.py && coverage html

Run Production:

> Python3 work_log_2.py
