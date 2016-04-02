__author__ = 'erhmutlu'


class DocTypeRequiredError(TypeError):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return "Doc Type is required!, but given is %s" % self.value