class AppResponseDto:
    def __init__(self, success, messages):
        self.success = success
        if type(messages) == list:
            self.full_messages = messages
        elif type(messages) == str:
            self.full_messages = [messages]
        else:
            self.full_messages = []

    def get_data(self):
        return {
            'success': self.success,
            'full_messages': self.full_messages
        }


class ErrorResponseDto(AppResponseDto):
    def __init__(self, messages):
        super(ErrorResponseDto, self).__init__(False, messages)


class SuccessResponseDto(AppResponseDto):
    def __init__(self, messages=None):
        super(SuccessResponseDto, self).__init__(True, messages)
