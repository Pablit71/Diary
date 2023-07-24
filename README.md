# Diary

## 1) Stack

1. Python 3.10, Django , DRF - backend
2. DATABASE - Postgresql

## 2) Main tasks of the project
### Description
The project was implemented to create some tasks with certain categories and goals for notes in the to-do list
### Main functions of the project:

- The possibility of authorization through VK
- Registration with mail binding
- Editing user data
- Creation of some boards for the possibility of combining several participants
- Role definitions from the board creator to other members (reader, editor)
- Creating categories for specific boards
- Creating goals with the ability to set a deadline, leave comments to participants, set the degree of importance of the goal
- Verify the Telegram bot for the convenience of creating goals and Categories
- Telegram bot - https://t.me/onebotlis_bot


## 3) Sequence for starting a project

1.  Install dependencies:
    - **pip install -r todolist/requirements.txt**
2. Create an .env file at the root of the folder and set all the necessary variables for the settings
3. Raise the database to run
4. Make migrations
5. Make a configuration to run the project through DjangoServer
6. creating a superuser goes through the command:
    - **./manage.py createsuperuser**
    
## 4) Additional information
- All data for the project is kept secret
- Deploy was used to install the project on the server
- Yandex.Cloud was used for the server ( https://cloud.yandex.ru)
- 

