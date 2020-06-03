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