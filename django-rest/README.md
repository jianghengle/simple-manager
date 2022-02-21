# Django REST

This is the backend, which is a [Django website](https://www.djangoproject.com/) serving the REST API and admin site.

## Prerequisites
- Python 3: Ubuntu 20.04 should have Python 3 by default. Otherwise, you can follow [this instruction](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server) to install.
- [Postgresql](https://www.postgresql.org/): Follow [this instruction](https://www.postgresql.org/) to install. You do not have to create new role or user but just install the Postgresql and let it create the default user `postgres`. You might need to set the user `postgres` password and you can make it simple like `postgres`, because this is the development datatbase and no one else would assces it. But you need to rememeber the password. At the end, you should be able to login the database by `psql -U postgres`.

## Development

### 1. Create DB
```
psql -U postgres
CREATE DATABASE simple_manager_test;
\l
```
Now you should see the database `simple_manager_test` has been created. And then you can `exit`.

### 2. Create venv and install dependencies
Go in the `django-rest` directory:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment variables
Create a new file `.env` under `config/settings/` directory
Copy the content of `config/settings/env.example` into the new file. You may want to update the `DATABASE_PASSWORD` based on yours. Also update AWS keys accordingly.

### 4. Migrate DB
Migrate database by command below. This will create all the tables in the database `simple_manager_test`.
```
python manage.py migrate
```

### 5. Create super user
Create the super user and make sure the username is same with email with all lower case letters.
```
python manage.py createsuperuser
```

### 6. Run server
Launch the development server
```
python manage.py runserver
```

### 7. Test admin
Open your browser and go to http://localhost:8000/admin, and login with your super user credential and make sure you can see all the tables there. 

### 8. Develpment server
Usually, to start the development server you just need to activate the virtual environment and start the dev server
```
cd django-rest
source venv/bin/activate
python manage.py runserver
```

## Deployment

### 1. Collect statics
```
cd django-rest
source venv/bin/activate
python manage.py collectstatic
```
### 2. Init Elastic Beanstalk
If your `venv` is active, first deactivate it by `deactivate`. 

And then, you can either following [the instruction](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html#python-django-deploy) and run `eb init` but make the configs look like [this configs](https://github.com/jianghengle/simple-manager/blob/main/resources/.elasticbeanstalk/config.yml) (you do not need to do the SSH part), or you can also copy the [.elasticbeanstalk](https://github.com/jianghengle/simple-manager/tree/main/resources/.elasticbeanstalk) directory into you local `django-rest` directory.

### 3. Eb create or Check env and its variables
First run `eb status` to confirm the environment `django-rest-prod` exists. If you cannot find the environment from the output and also the AWS console, you will need to create the environment by `eb create django-rest-prod`.

And then, go the environment from the AWS console, and on the environment configuration page click the `Edit` button on `Software` category, and make sure it has all the environment variables needed as in [production.py](https://github.com/jianghengle/simple-manager/blob/main/django-rest/config/settings/production.py) and also `STAGE` environment variable should be `production`.

### 4. eb deploy
```
eb deploy
```
