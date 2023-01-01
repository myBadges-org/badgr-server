# TODO

### 1. fix the api specification
- apispec-djangorestframework is not compatible with Django>2.x.x
- I didnt find a good replacement, so I just commented out all occurences in the code

### 2. adjust database
- mysql had to be updated to 5.7
- since then there are lots of warnings on startup of the containers
- also ```TemplateSyntaxError``` when http://localhost:8000/staff/login/?next=/staff/

### 3. add some versions in requirements.txt
- some packages dont have versions, because I wasnt sure yet. They should be added