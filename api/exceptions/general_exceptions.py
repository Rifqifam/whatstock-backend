class ResourceNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class BadRequest(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class InternalServerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Unauthorized(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value