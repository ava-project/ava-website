# ava-website
The repository of the AVA website, Django here

[![Requirements Status](https://requires.io/github/ava-project/ava-website/requirements.svg?branch=develop)](https://requires.io/github/ava-project/ava-website/requirements/?branch=develop) [![Build Status](https://travis-ci.org/ava-project/ava-website.svg?branch=develop)](https://travis-ci.org/ava-project/ava-website) [![Code Health](https://landscape.io/github/ava-project/ava-website/develop/landscape.svg?style=flat)](https://landscape.io/github/ava-project/ava-website/develop)


## Build

Commands to run to pull the latest changes

```sh
git pull
docker-compose build
docker-compose run --rm web python manage.py migrate
docker-compose up
```

## Create admin

You can create a superuser with this command

```sh
docker-compose run --rm web python manage.py createsuperuser
```

or from the Django shell

```sh
docker-compose run --rm web python manage.py shell
```

```python
from django.contrib.auth.models import User
u = User.objects.get(username='username of the user you want to promote')
u.is_staff = True
u.is_superuser = True
u.save()
```

# In-site Documentation

 - Make sure you have an admin account.
 - Go to [this page](http://localhost:8000/admin/doc/views/#ns|user) when docker is started
