## User API Overview
**User API**
- user registration
- creating auth token
- viewing/ updating profile

**Endpoints**
- user/create/
  - POST, register a new user
- user/token/
  - POST, creatw new token
- user/me/
  - PUR/PATCH, update profile
  - GET, view profile


## Create A New App
- Run `docker-compose run --rm app sh -c "python manage.py startapp user"` in the terminal to create a new app - user inside our django proj. Here is the new structure:
```
    ├── app/
    │  ├── app/
    |  └── core/
    |  └── user/   
    |  └── .flake8
    |  └── manage.py
```
- Inside user/, remove `migrations/`, `admin.py`, `models.py`, since we are gonna keep all the three in core app
- remove `tests.py`. And create `tests/` instead, do not forget create `__init__.py` inside it
- add this new user app to `INSTALLED_APPS` at `.app/app/settings.py`


## Build User API
### Create public Tests 
- public tests mean unauthenticated requests, i.g. registering a new user.
- create `app/user/tests/test_user_api.py`
- import:
    ```python
    from django.test import TestCase  # base class for tests
    from django.contrib.auth import get_user_model  # helper function to get the default user model
    from django.urls import reverse  # can be used to return an absolute path reference

    from rest_framework.test import APIClient # Extends Django's existing Client class, used to test api endpoint, simulates a user making requests to the API.
    from rest_framework import status 
    ```
- add the user api url that gonna be testing (the url is going to be configure later in the inplementation)
- create class `PublicUserApiTests`
  - create an APIClient in `setUp`
  - test if create a user successfully:
    1. create an dict to pass all the info we need for creating a user
    2. make a http post request to create url and pass in the data
    3. check if the endpoint returns `status.HTTP_201_CREATED`
    4. retrive the user data from the database with the email we register at step 2
    5. check the user at step 4 has the same password that we passed in at step 2
    6. check there is no key called `password` in the reponse that returned from the api
  - test edge case 1: the email has already in the db
    1. create an dict to pass all the info we need for creating a user
    2. create a user in the db
    3. use the same email to make a http post request to create url
    4. check if the endpoint returns `status.HTTP_400_BAD_REQUEST`
  - test edge case 2: password is shorter than 5 charts
    1. create an dict to pass all the info we need for creating a user, but with a very short pass
    2. make a http post request to create url and pass in the data
    3. check if the endpoint returns `status.HTTP_400_BAD_REQUEST`
    4. retrive the user status from db by filtering the same email
    5. assert the status should be false
- Run `docker-compose run --rm app sh -c "python manage.py test"`, it should be failed

### Implement create user API
- create `app/user/serializers.py`
  - import `from rest_framework import serializers`, serializer is simply a way to convert objects to and from python objects. It takes a json input that might be posted from the API and validates the input to make sure it is secure and correct as part of validation rules. And then it converts it to either a python object that we can use or a model in our actual database.
  - create class `UserSerializer`
    - `serializers.ModelSerializer` They allow us to automatically validate and save things to a specific model that we define in our serialization.
    - create class `Meta` So this is where we tell the Django rest framework, the model and the fields and any additional arguments that we want to pass to the serialize set and the serialized needs to know which model it's representing and the way it does. is_active and is_staff are not set here, since it can only be modified by admin.
    - `create` method, only been called after the validation done by serializer
- create a view that uses this serializer
  - head over to `app/user/views.py`
  - import 
    - `from rest_framework import generics`, we use `generics.CreateAPIView`. The Create API view handles a http post request that's designed for creating objects. So creating objects in the database handles all of that logic for you. All you need to do is define the serialization, which we've already done, and then set the serialize across on this view. So Django rest framework knows what serialize that we want to use.
    - `from user.serializers import UserSerializer`, the class we just built
- wire up an url to this view(the reverse url we set in the test)
  - create `app/user/urls.py`, set reverse mapping. any request that gets passed to that URL is going to be handled by the view that we defined here.
  - head over to `app/app/urls.py`, connect the view in our main app


## Build Token API
### Token Authentication Overview
- types of authentication
  - basic: send username and password with each request the client make (bad, means the client needs to store the username and password)
  - token: use a token in the http header (this course will use), balance of simplicity and security, supported out of the box by DRF, well support by most clients
  - json web tokens(JWT): use an access and refresh token, advanced, requires some external apps and libreries
  - session: use cookies
- how token works
  
  ![image](notes/images/16_token.png)

- pros and cons of using token authentication
  - pros
    - supported out of the box
    - simple to use
    - supported by all clients
    - avoid sending username/password each time
  - cons
    - token needs to be secure
    - requires database requests
- token loggoing out: happens on the client side, delete token

### Create Tests 
- location: `app/user/tests/test_user_api.py`
- add the token url that gonna be testing (the url is going to be configure later in the inplementation) at the top
- create method `test_create_token_for_user` :
  - create a new user
  - generate a payload that has the new user's email address and password
  - post the payload to the token url
  - check that the responds.data includes token
  - check the status code
- test edge case 1: bad credencials `test_create_token_bad_credentials`
- test edge case 2: blank password `test_create_token_blank_password`
- Run `docker-compose run --rm app sh -c "python manage.py test"`, it should be failed

### Implement token API
- add `'rest_framework.authtoken'` in settings.py's INSTALLED_APPS
- head over to `app/user/serializers.py`
  - import `django.contrib.auth.authenticate` a function comes with django that allows you to authenticate with the authentication system
  - create class `AuthTokenSerializer`

    **Purpose**
    - Handles user login authentication.
    - Validates email + password and returns the authenticated user.

    **Fields**
    - `email = serializers.EmailField()`
    - Ensures value is a valid email format.
    - `password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)`
    - Accepts raw password input.
    - Not trimming whitespace prevents removing intentional spaces.

    **validate(self, attrs)**
    - Extract `email` and `password` from `attrs`.
    - Call `authenticate()` using:
    - `request=self.context.get('request')`
    - `username=email` (because email is the login identifier)
    - `password=password`
    - `authenticate()` tries to find a user with the given email, checks if the password is correct, and returns the user object if successful — otherwise returns None.
    - If authentication fails:
    - raise `serializers.ValidationError('Unable to authenticate with provided credentials')`
    - If authentication succeeds:
    - add the authenticated user into `attrs` → `attrs['user'] = user`
    - return `attrs`

    **Key** **Outcome**
    - Returns validated data containing the authenticated user.
    - Allows the view to create and return an authentication token.

  - create a view that uses this serializer at `app/user/views.py`
  - since we've already connected this url module to our root url when build user api, no need to do it again here


## Build Manage User API
### Purpose

### Create Tests
- public test
`test_retrieve_user_unauthorized`: This test pretends to be a user who isn’t logged in and tries to access the /me endpoint, and checks that the API correctly rejects the request with a 401 Unauthorized response. 
- private test
  - create a new class `PrivateUserApiTests`, we are gonna force authentication to the APIClient in `setUp` method, thats why we separate this apart from public test.
  - `force_authenticate(user=...)` (used in tests)
    - Bypasses the entire authentication process
    - It does not check passwords, tokens, or login endpoints
    - It simply marks the test client as “already authenticated as this user”
    - Useful when you're testing logic behind authenticated endpoints and don't want to repeatedly deal with login steps
  - Real authentication (in actual application or test using login/token)
    - Goes through the real authentication system
    - Usually means: sending credentials to a /login/ or /token/ endpoint, or creating a token and sending it in Authorization: Bearer <token>
    - It tests: password validation, token generation, authentication backend,permission checks 
  - `test_retrieve_profile_success`: Test retrieving profile for logged in and authenticated user
  - `test_post_me_not_allowed`: Test http POST method is not allowed for the me endpoint. Http POST should only be used when **creating** obj in the system. This api is used for modifying users
  - `test_update_user_profile`: Test updating the user profile by authenticated user