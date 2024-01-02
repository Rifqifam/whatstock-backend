class UserAlreadyExist(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class ResourceAlreadyExist(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class AuthFailed(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
