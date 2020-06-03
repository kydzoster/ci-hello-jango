from django.shortcuts import render, redirect
from .models import Item

# Create your views here.


def get_todo_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'todo/todo_list.html', context)


# when someone hits add_item, if its a get request-
# -it will return add_item template
def add_item(request):
    # if its a POST it will generate template to add a new item
    if request.method == 'POST':
        name = request.POST.get('item_name')
        done = 'done' in request.POST
        Item.objects.create(name=name, done=done)
        return redirect('get_todo_list')
    return render(request, 'todo/add_item.html')
