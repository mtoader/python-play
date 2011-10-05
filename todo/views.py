# Create your views here.
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from todo.forms import DeleteListForm, CreateListForm, EditListForm, CreateItemForm
from todo.models import List, Item

@login_required()
def lists(request):
    return render_to_response(
        'todo/lists.html',
            {
            'lists': List.objects.filter(user=request.user).all()
        },
        context_instance=RequestContext(request))


@login_required()
def list_new(request):
    form = CreateListForm({"name": "New List"})

    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            list = List.objects.create(user=request.user, name=form.cleaned_data['name'])
            list.save()
            return redirect('/lists/%d/' % list.id)

    return render_to_response(
        'todo/list_new.html',
            {
            'form': form
        },
        context_instance=RequestContext(request))


@login_required()
def list_rename(request):
    form = EditListForm(request.GET)

    if request.method == 'POST':
        form = EditListForm(request.POST)
        if form.is_valid():
            list = List.objects.filter(user=request.user).get(pk=form.cleaned_data['id'])
            list.name = form.cleaned_data['name']
            list.save()
            return redirect('/lists/%d/' % list.id)

    try:
        list = List.objects.filter(user=request.user).get(pk=form.cleaned_data['id'])
        return render_to_response(
            'todo/list_edit.html',
            {
                'list': list,
                'form': form
            },
            context_instance=RequestContext(request))
    except Exception:
        return redirect('/lists/')


@login_required()
def list(request, list_id=None):
    if list_id is None:
        return redirect('todo.views.lists')

    try:
        list = List.objects.filter(user=request.user).get(pk=list_id)
    except Exception:
        return redirect('todo.views.lists')

    return render_to_response(
        'todo/list.html',
        {
            'list': list,
            'items': Item.objects.filter(list=list).all()
        },
        context_instance=RequestContext(request))


@login_required()
def list_delete(request):
    if request.method != 'POST':
        return redirect('todo.views.lists')

    try:
        form = DeleteListForm(request.POST)
        if form.is_valid():
            list = List.objects.filter(user=request.user).get(pk=form.cleaned_data['id'])
            Item.objects.filter(list=list.id).delete()
            list.delete()

    except Exception as e:
        pass

    return redirect('todo.views.lists')


@login_required()
def item_new(request, list_id=None):

    form = CreateItemForm({'text':'New text'})
    
    if list_id is None:
        return redirect('todo.views.lists')

    try:
        list = List.objects.filter(user=request.user).get(pk=list_id)

        if request.method == 'POST':
            form = CreateItemForm(request.POST)

            if form.is_valid():
                item = Item.objects.create(
                    list = list,
                    text = form.cleaned_data['text'],
                    due_on = form.cleaned_data['due_on'],
                    started_on = form.cleaned_data['started_on'],
                    priority = form.cleaned_data['priority'],
                    completed = form.cleaned_data['completed']
                )
                
                item.save()
                return redirect('/lists/%d/' % list.id)

        return render_to_response(
            'todo/item_new.html',
                {
                    'form': form
                },
            context_instance=RequestContext(request))
    except Exception as e:
        return redirect('todo.views.lists')



