import json

from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from shared.serializers import ErrorResponseDto, SuccessResponseDto
from todos.models import Todo
from todos.serializers import TodoListResponseDto, TodoDto


@csrf_exempt
def get_or_delete_all(request, *args, **kwargs):
    if request.method == 'GET':
        return get_todos_list(request)
    elif request.method == 'DELETE':
        Todo.objects.all().delete()
        return HttpResponse('', content_type='application/json', status=204)
    elif request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description', '')
        completed = data.get('completed', False)

        # todo = Todo.objects.create(title=title, description=description, completed=completed)
        # or
        todo = Todo.objects.create(**data)
        return get_response(TodoDto(todo, include_details=True).get_data())


def get_completed(request, *args, **kwargs):
    return get_todos_list(request, completed=True)


def get_pending(request, *args, **kwargs):
    return get_todos_list(request, completed=False)


def read_or_write_by_id(request, *args, **kwargs):
    try:
        todo = Todo.objects.get(pk=kwargs['id'])
        if request.method == 'GET':

            dto = TodoDto(todo, include_details=True).get_data()
            return get_response(dto)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            todo.title = data.get('title')
            description = data.get('description', None)

            if description is not None:
                todo.description = description

            todo.completed = data.get('completed', False)
            todo.save()
            return get_response(TodoDto(todo, include_details=True).get_data())
        elif request.method == 'DELETE':
            todo.delete()
            return HttpResponse('', content_type='application/json', status=204)

    except Todo.DoesNotExist:
        return get_response(ErrorResponseDto('Todo not found').get_data())


def get_todos_list(request, completed=None):
    queryset = Todo.objects
    if completed is True or completed is False:
        queryset = queryset.filter(completed=completed)

    todos = queryset.order_by('-created_at').only('id', 'title', 'created_at', 'updated_at').all()

    return HttpResponse(json.dumps(TodoListResponseDto(todos).data), content_type='application/json')


def get_response(dto):
    return HttpResponse(json.dumps(dto), content_type='application/json')
