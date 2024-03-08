## Reddit clone webapp
#### A website where you can post and link youtube links with a reactive layout and dynamic post loading.
#### Site uses Python/Django with Htmx and Hyperscript for animations.
#### For testing im using SQLite but changing the database is not a problem.
#### The site uses email verification for your accounts. (django local email test directory enabled)
- Still need to implement changing password functionality and password validation for password size and allowed characters.

#### Getting Started
- Python 3.12.0
- Django 4.2.7

#### Cloning Repo
~~~
git clone https://github.com/4ntim4tter/blogsite.git
cd blogsite
~~~
#### Install Requirements
~~~
pip install requirements.txt
~~~
#### To start the server
~~~
py manage.py runserver - for powershell
python manage.py runserver - for bash
~~~
