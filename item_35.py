class Field(object):

    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Meta(type):

    def __new__(mcs, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(mcs, name, bases, class_dict)
        return cls


class DatabaseRow(object, metaclass=Meta):

    pass


class Customer(DatabaseRow):

    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

foo = Customer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
print('After:', repr(foo.first_name), foo.__dict__)
