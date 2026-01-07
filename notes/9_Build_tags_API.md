**TO BE REVISITED**
- mixins in views.py
- the difference between viewsets.ModelViewSet and viewsets.GenericViewSet. and why apply different view set in recipe and tag views
- getting to know more about DRF

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


## Build tag updating(patch) API
### write test
create test in `app/recipe/tests/test_tags_api.py`

### Implement
`app/recipe/views.py`
the test will pass by simply add a new base class `mixins.UpdateModelMixin`

same logic as writing recipe update api.


## Build tag deleting API
### write test
create test in `app/recipe/tests/test_tags_api.py`

### Implement
`app/recipe/views.py`
the test will pass by simply add a new base class `mixins.DestroyModelMixin`

same logic as writing recipe delete api.


## Build creating tags API
### Nested serilizers
nestes serilizers will be used in this part.
**What are nested serilizers?**
- Serializer within a serializer
- Used for firlds which are objects
**Limitaions**
- Read only by default
- custom logic to make writable
  
### write test
create test in `app/recipe/tests/test_recipe_api.py`, because we are gonna support creating tags directly through our recipe. So when ppl are using the api, typically when theu are using the recipes, we are gonna allow them to specify tags in that recipe and assign the existing tags or if thoes tags don't exist, we are gonna create them and assign them to the recipe
- Import:
  - from core.models import Tag
  - Create two test: `test_create_recipe_with_new_tags` and `test_create_recipe_with_existing_tags`. The only difference is in the second test, we need to check if the existing tag is already in the new recipe's tags that we created.

### Implement
assign the tag serializer as a nested serializer to our recipe serializer
- move the `TagSerializer` class above `RecipeSerializer`
- create a new `TagSerializer` tags inside `RecipeSerializer`
- and tags into fields. But so far, the tags are read only
- override the `create` method:
  1. remove the tags data from validated_data and assign it to a varible named tags
  2. create a recipe with the rest of validated_data
  3. Identifying the Authenticated User
  4. process each tag. For every tag: The system checks if a tag with the same name already exists for the user. If it exists, it is reused. If it does not exist, it is created
  5. return the fully created recipe (with tags attached). DRF then: serializes the recipe, sends it back as the API response