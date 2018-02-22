Read me first!


In order to run the library management system, you need first install python-2.7, python-dev, virtualenv(python-virtualenv), mysql-server, mysql-client, libmysqld-dev, in which python-dev & libmysqld-dev is for flask-mysql.

After installation, run install_flask.sh to build flask.

Use command line, go into db_data folder, log in to mysql to create database system using:
source create-library-data-for-MySQL.sql

Then exit or open another command line window, go to db_data folder, import basic data using:
./insert.py
take 10 minutes

After that, import book_loans and fine data using ./db_data/insert_book_loans_and_fine.py
finished immediately

Next step, run server, go to parent directory using: “cd ..”, then “./run.py”

Open a web browser, type: localhost:5000

Then you will get the library management system!

0002179687
1