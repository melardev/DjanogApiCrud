class TodoListResponseDto:
    def __init__(self, todos):
        self.data = [TodoDto(todo, include_details=False).get_data() for todo in todos]


class TodoDto:
    def __init__(self, todo, include_details=False):
        self.id = todo.id
        self.title = todo.title
        self.completed = todo.completed
        self.created_at = str(todo.created_at)
        self.updated_at = str(todo.updated_at)
        self.include_details = include_details
        if include_details:
            self.description = todo.description

    def get_data(self):
        data = {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self.include_details:
            data['description'] = self.description

        return data
