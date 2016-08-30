from werkzeug.exceptions import BadRequest, NotFound


class MissingArgError(BadRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if len(args) == 1:
            self.description = 'Missing argument: {}'.format(args[0])
        else:
            self.description = 'Missing arguments: {}'.format(', '.join(args))


class WhoTheHellAreYouError(NotFound):
    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.description = 'The user {} does not exist.'.format(self.username)
