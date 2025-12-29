## Overview

### Features
- create
- list
- view detail by recipe id
- update
- delete
All the features will be availble for the recipe of the authenticated user

### Endpoints
- /recipes/
  - GET, list all recipes
  - POST, create recipes
- /recipes/<recipe_id>/
  - GET, view details of recipes
  - PUT/PATCH, update recipes
  - DELETE, delete recipes

### APIView V.S. Viewsets
**What is a view?**
- handles a request made to a URL
- django uses fuctions
- DRF uses classes
  - reusable logic
  - override behaviour
- DRF also supports decorators
- APIView and Viewsets = DRF base classes

**APIView**
- focused around HTTP methods
- class methods for HTTP methods
  - GET, POST, PUT, PATCH, DELETE
- provide flexibility over URLs and logic
- useful for non CRUD APIs
  - avoid for simple Create, Read, Update, Delete APIs
  - bespoke logic (eg: auth, creating jobs, external apis)
  
**Viewsets**
- focus around actions
  - retrieve, list, update, partial update, destory
- map to django models
- use Routers to generate URLs
- create for CRUD oprations on models


## Build Recipe Model
### Write test for recipe model
- `app/core/tests/test_models.py`, the core app is where we store all shared methods over all apps
  - import `from decimal import Decimal`, used for storing price for recipe obj, accuate: integer > decimal > floats
  - add new method `test_create_recipe`.
    - create a test user
    - create a recipe by using the method we are going to create
    - assert the title of the model
- Run `docker-compose run --rm app sh -c "python manage.py test"`, it should fail
  
### Implement recipe model
`app/core/models.py`
- import `from django.conf import settings` to set up a relationship between recipe model and user model
- create a class `Recipe`
  - **feilds**
    - user, set foreign key to map to user , `on_delete=models.CASCADE` if deleted a user, the recipes that the user created will be deleted as well
    - title
    - description
    - time_minutes, minutes take to create a recipe
    - price
    - link
  - `__str__`, the special method of the class allows you to the string representation of that obj, this affects how is displayed in django admin
  - add the recipe in `core/admin`
  - create the migrations by running `docker-compose run --rm app sh -c "python manage.py makemigrations"`
  - run the test, it should pass (the Django test run out will automatically apply all the migrations every time you run it. So it applies all the migrations and it clears all of the database and resupplies migrations every single time you run a test in the test suite. So that's why we didn't need to run the migration when we run our application.)


| Command | Full Name | Purpose | What It Does | When To Use |
|---------|-----------|---------|--------------|-------------|
| `python manage.py makemigrations` | Make Migrations | Prepare changes | Scans model changes and **creates migration files** (but does *not* touch the database) | Whenever you **add, remove, or modify fields/models** |
| `python manage.py migrate` | Apply Migrations | Execute changes | Reads migration files and **updates the database schema** (creates tables, adds columns, etc.) | After `makemigrations`, or when setting up a new project or pulling changes |

## Build Recipe Listing API


## Build Recipe Detail API


## Build Recipe Creating API


## Test recipe API in browser