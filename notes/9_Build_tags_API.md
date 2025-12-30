**TO BE REVISITED**
- mixins in views.py
- the difference between viewsets.ModelViewSet and viewsets.GenericViewSet. and why apply different view set in recipe and tag views

## Tags API Design
**In this section**
- add ability to add recipe tags
- create model for tags
- add tag api endpoints
- update recipe endpoint (adding and listing tags)
  
**Tag model**
- name, name of tag to create
- user, user who created/ owns tag

**Tag endpoint**
/api/recipe/tags
- POST, create tag
- PUT/PATCH, update tags
- DELETE, remove tags
- GET, list available tags


## Add tag model and create migrations
### create tests
`core/tests/test_models.py`
- create a test user
- create a tag by using the method we are going to create
- assert the name of the tag
- Run `docker-compose run --rm app sh -c "python manage.py test"`, it should fail

### Implement tag model
`app/core/models.py`
- create a class `Recipe`
- **feilds**
    - user, set foreign key to map to user , `on_delete=models.CASCADE` if deleted a user, the recipes that the user created will be deleted as well
    - name
- `__str__`, the special method of the class allows you to the string representation of that obj, this affects how is displayed in django admin
- add tags inside the class Recipe, the relationship is many to many
- add the recipe in `core/admin`, make sure the new tag model is managable through our django admin interface
- create the migrations by running `docker-compose run --rm app sh -c "python manage.py makemigrations"`
- run the test, it should pass.


## Build tag listing API
### write test
create `app/recipe/tests/test_tags_api.py`

### Implement
`app/recipe/serializers.py`
`app/recipe/views.py`
`app/recipe/urls.py`

same logic as writing recipe listing api.