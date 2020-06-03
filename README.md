# Setup

1. **pip3 install django**
2. **cd /workspace/.pip-modules/lib/python3.8/site-packages/**
3. **ls -la** *- this will show django with all other files that came in with it, any packages that gets installed with pip3 will end up in this site-packages directory*
4. **cd -** *- this will take you back to the main directory we are working from*
5. **django-admin startproject django_todo .** *- this will create 2 instances **first** - django_todo folder with four .py files inside it and **second** - manage.py*
6. **python3 manage.py runserver** *- this will run the server and will create 2 instances db.sqlite3 and pycache folder inside django_todo folder*
7. **ctrl+c**
8. **python3 manage.py startapp todo** *- this will create a todo folder for our todo application*
9. *inside todo/views.py add:* 

        from django.shortcuts import render, HttpResponse

        # Create your views here.
        def say_hello(request):
            return HttpResponse("Hello there!")

10. *inside django_todo/urls.py add:*

        from django.contrib import admin
        from django.urls import path
        from todo.views import say_hello

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('hello/', say_hello, name='hello')
        ]

11. **python3 manage.py runserver**
12. *at the end of the address bar type **/hello/** to view our project*
13. **ctrl+c**
14. *inside **todo** folder create **templates** folder*
15. *inside **templates** folder create another folder **todo***
16. *inside **todo** folder create a file **todo_list.html***
17. *inside **todo/templates/todo/todo_list.html** add some content*
18. *inside **todo/views.py** replace content with:*

        from django.shortcuts import render

        # Create your views here.
        def get_todo_list(request):
            return render(request, 'todo/todo_list.html')

19. *inside **django_todo/urls.py** replace content with:*

        from django.contrib import admin
        from django.urls import path
        from todo.views import get_todo_list

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', get_todo_list, name='home')
        ]

20. *inside **django_todo/settings.py** inside **INSTALLED_APPS** add **'todo',***
21. **python3 manage.py migrate** *- this will migrate necessary files for admin, authentications etc.*
22. **python3 manage.py createsuperuser**

        username: kydzoster
        password: pass123

23. *inside **todo/models.py** add new class:*

        class Item(models.Model):
            name = models.CharField(max_length=50, null=False, blank=False)
            done = models.BooleanField(null=False, blank=False, default=False)

            def __str__(self):
                return self.name

24. **python3 manage.py makemigrations --dry-run** *- this will show what we are about to migrate, to migrate for real remove **--dry-run***
25. **python3 manage.py showmigrations** *-will show where*
26. **python3 manage.py migrate**
27. *inside todo/admin.py add:*

        from .models import Item

        # Register your models here.
        admin.site.register(Item)

28. *go to the website app under the **/admin** we just created and add some items under TODO list.*
29. *inside todo/views.py add:*

        from django.shortcuts import render
        from .models import Item

        # Create your views here.


        def get_todo_list(request):
            items = Item.objects.all()
            context = {
                'items': items
            }
            return render(request, 'todo/todo_list.html', context)

30. *inside todo/templates/todo/todo_list.html add:*

        <h1>Things I need to do:</h1>
        <table>
            {% for item in items %}
                <tr>
                {% if item.done %}
                    <td><strike>{{ item.name }}</strike></td>
                {% else %}
                    <td>{{ item.name }}</td>
                {% endif %}
                </tr>
            <!--if the task item list is empty it will promt this line of code-->
            {% empty %}
                <tr><td>There are no Tasks in your TODO app!</td></tr>
            {% endfor %}
        </table>
        <a href="/add">Add an item</a>

31. *duplicate todo_list.html and rename it to add_item.html, then change Heading and replace table with:*

        <form method="POST" action="add">
            <div>
                <p>
                    <label for="id_name">Name:</label>
                    <input type="text" name="item_name" id="id_name">
                </p>
            </div>
            <div>
                <p>
                    <label for="id_done">Done:</label>
                    <input type="checkbox" name="done" id="id_done">
                </p>
            </div>
            <div>
                <p>
                    <button type="submit">Add Item</button>
                </p>
            </div>
        </form>

32. *inside todo/views.py add:*

        def add_item(request):
            return render(request, 'todo/add_item.html')

33. *inside django_todo/urls.py add in import **add_item** and inside urlpatterns add:*

        path('add', add_item, name='add')

