from django.templatetags.static import static


class StaticWrapper:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return static(self.path)
