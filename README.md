### Django Course Registration  
![Alt text](registration/static/courses/logo.png?raw=true)

### A Djagno/PostgreSQL app that allows users to search for courses by subject/keyword/teacher availablility, enroll/unenroll, and view course schedule on their profile page. To run locally, you will need PostgreSQL installed, and to store these variable in a .env file.  

```
export DB_NAME= # your db name
export DB_USER= # your db username
export DB_PASSWORD= # your db password
export DEBUG_VALUE=True
```
Then run the following commands:
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Additionally, you can seed the database with the seed.json file provided like so:
```
python manage.py loaddata seed.json
```
The project is set up to be deployed to Heroku, and a live demo can be found here:  
[Course Registration](https://fierce-wave-09727.herokuapp.com/)