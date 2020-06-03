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
            path('', get_todo_list, name='get_todo_list')
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

        from django.shortcuts import render, redirect
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
            {% csrf_token %}
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

        # when someone preses add_item if its a get request it will return add_item template
        def add_item(request):
            # if its a POST it will generate template to add a new item
            if request.method == 'POST':
                name = request.POST.get('item_name')
                done = 'done' in request.POST
                Item.objects.create(name=name, done=done)
                return redirect('get_todo_list')
            return render(request, 'todo/add_item.html')

33. *inside django_todo/urls.py add in import **add_item** and inside urlpatterns add:*

        path('add', add_item, name='add')

34. *inside todo folder create a file forms.py and add:*

        from django import forms
        from .models import Item


        class ItemForm(forms.ModelForm):
            class Meta:
                model = Item
                fields = ['name', 'done']

35. *inside todo/views.py add a new import form:*

        from .forms import ItemForm

    *and replace **def add_item(request):** code with:*

        def add_item(request):
            # if its a POST it will generate template to add a new item
            if request.method == 'POST':
                form = ItemForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('get_todo_list')
            form = ItemForm()
            context = {
                'form': form
            }
            return render(request, 'todo/add_item.html', context)

36. *now, with the new form we can delete an old add_item form and instead render the form just like any other template variable:*

        <form method="POST" action="add">
            {% csrf_token %}
            {{ form }}
            <div>
                <p>
                    <button type="submit">Add Item</button>
                </p>
            </div>
        </form>

37. *inside todo_list.html after {% endif %} add:*

        <td>
            <a href="/edit/{{ item.id }}">
            <button>Edit</button>
            </a>
        </td>

38. *inside views.py add get_object_or_404 to **django.shortcuts import** and add a new request:*

        def edit_item(request, item_id):
            # this will get an instance with the item_id or 404 if page has not found
            item = get_object_or_404(Item, id=item_id)
            # if its a POST it will generate template to update an old post
            if request.method == 'POST':
                form = ItemForm(request.POST, instance=item)
                if form.is_valid():
                    form.save()
                    return redirect('get_todo_list')
            form = ItemForm(instance=item)
            context = {
                'form': form
            }
            return render(request, 'todo/edit_item.html', context)

39. *duplicate add_item and rename it to edit_item, then change content with:*

        <h1>Edit a TODO item:</h1>
        <form method="POST">
            {% csrf_token %}
            <!--.as_p is a vertical styling, without it it will be a default horizontal styling-->
            {{ form.as_p }}
            <div>
                <p>
                    <button type="submit">Update Item</button>
                </p>
            </div>
        </form>

40. *inside urls.py update todo.views import by adding edit_item and inside urlpatterns add new path:*

        path('edit/<item_id>', edit_item, name='edit')

41. *inside todo_list.html under {% endif %} add two new codes:*

        <td>
            <a href="/toggle/{{ item.id }}">
            <button>Toggle</button>
            </a>
        </td>

        <td>
            <a href="/delete/{{ item.id }}">
            <button>Delete</button>
            </a>
        </td>

42. *inside urls.py, because it is getting crowded we implement a django built in **views** and replace all content with and add two new paths:*

        from django.contrib import admin
        from django.urls import path
        from todo import views

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', views.get_todo_list, name='get_todo_list'),
            path('add', views.add_item, name='add'),
            path('edit/<item_id>', views.edit_item, name='edit'),
            path('toggle/<item_id>', views.toggle_item, name='toggle'),
            path('delete/<item_id>', views.delete_item, name='delete')
        ]

43. *inside views.py add 2 new requests:*

        def toggle_item(request, item_id):
            # this will get an instance with the item_id or 404 if page has
            # not found when user hits the toggle button
            item = get_object_or_404(Item, id=item_id)
            # if the item is done it will change it to not done and vice versa
            item.done = not item.done
            item.save()
            return redirect('get_todo_list')


        def delete_item(request, item_id):
            # this will get an instance with the item_id or 404 if page has
            # not found when user hits the toggle button
            item = get_object_or_404(Item, id=item_id)
            item.delete()
            return redirect('get_todo_list')

44. *Added 3 test files*
45. **pip3 install coverage** *- this will show how much code we have actually tested*
46. *run coverage* - **coverage run --source=todo manage.py test**
47. *to view the report* - **coverage report**
48. *to see specifics on what we have missed, we can view it in an interactive HTML report.* - **coverage html**
49. *to view this report seperate from django server type -* **python3 -m http.server** *open link and click on **htmlcov/** link*
50. *when clicked on todo/models.py we see that it is missing a test for string method, lets add it:*

    inside test_models.py add:

        def test_item_string_method_returns_name(self):
        item = Item.objects.create(name='Test TODO item')
        self.assertEqual(str(item), 'Test TODO item')

51. *run coverage once again - **coverage run --source=todo manage.py test** and view the report - **coverage report** - generate HTML report **coverage html***
52. *Test coverage shows that we have covered 97% the missing percantage is django code itself*
53. 