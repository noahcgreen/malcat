class AppError(Exception):
    """A generic error."""
    def __init__(self, message, *args, **kwargs):
        self.message = message

    def __repr__(self):
        return self.message
