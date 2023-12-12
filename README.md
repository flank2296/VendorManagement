# VendorManagement - [![Codacy Badge](https://app.codacy.com/project/badge/Grade/730e09029eb04eacbc13de845fde58d8)](https://app.codacy.com/gh/flank2296/VendorManagement/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

This system handles vendor profiles, track purchase orders, and calculate vendor performance metrics

####Requirements
- Python 3.12
- Mysql 8.2.0

###Installation Guide -
- Install poetry. Read more at [https://python-poetry.org/docs/]
- After installing poetry, Go to VendorManagement directory and create a type `poetry shell`. This will create a new virtual environment.
- After this, make sure that you are in the directory where `pyproject.toml` is present and type `portry install`. This will install all dependencies that are needed for running this application.
- Once everything is installed, type `python manage.py check` to ensure that this is working properly.
- Type `python manage.py migrate` to run all migrations
- We need a one superuser for the apis to work. So type `python manage.py createsuperuser` to create a new user.
- Once migrations are completed successfully, type `python manage.py runserver` to start the django server
- Log in to the system using `http://localhost:<your-port>/admin` and make sure to install and turn on the postman interceptor for your browser. Since we will need session cookies to run the apis.
- I have added postman collection json in the repository. You can check that and use APIs accordingly.
- I have commited `settings.py` just for your convenience. On production project, we must not expose the `settings.py` file directly.
