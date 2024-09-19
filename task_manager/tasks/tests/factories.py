import factory
from faker import Faker

from tasks.models import Task

fake = Faker()


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    completed = factory.Faker('boolean')
