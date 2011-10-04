# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from todo.forms import DeleteListForm
from todo.models import List, Item

@login_required()
def lists(request):
    return render_to_response(
        'todo/lists.html',
            {
                'lists': List.objects.filter(user = request.user).all()
            },
        context_instance=RequestContext(request))


@login_required()
def list_new(request):
    return render_to_response(
        'todo/lists.html',
            {
                'lists': List.objects.filter(user = request.user).all()
            },
        context_instance=RequestContext(request))

@login_required()
def list(request, list_id=None):

    if list_id is None:
        return redirect('todo.views.lists')

    try:
        list = List.objects.filter(user = request.user).get(pk = list_id)
    except Exception:
        return redirect('lists')

    return render_to_response(
        'todo/list.html',
            {
                'list': list,
                'items': Item.objects.filter(list = list).all()
            },
        context_instance=RequestContext(request))

@login_required()
def list_delete(request):
    if request.method != 'POST':
        return redirect('todo.views.lists')

    try:
        form = DeleteListForm(request.POST)
        if form.is_valid():
            list = List.objects.filter(user = request.user).get(pk = form.cleaned_data['id'])
            Item.objects.filter(list = list.id).delete()
            list.delete()

    except Exception as e:
        pass

    return redirect('todo.views.lists')
