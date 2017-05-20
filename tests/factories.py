import uuid

import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )

    id = factory.Sequence(lambda n: uuid.uuid4())
    username = factory.Sequence(lambda n: 'testuser{}'.format(n))
    password = factory.Faker('password', length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'links.Category'
        django_get_or_create = ('name', )

    id = factory.Sequence(lambda n: uuid.uuid4())
    name = factory.Sequence(lambda n: 'name{}'.format(n))


class TagFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'links.Tag'
        django_get_or_create = ('name', )

    id = factory.Sequence(lambda n: uuid.uuid4())
    name = factory.Sequence(lambda n: 'name{}'.format(n))


class LinkFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'links.Link'
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: uuid.uuid4())
    title = factory.Sequence(lambda n: 'title{}'.format(n))
    url = factory.Faker('url')
    description = factory.Sequence(lambda n: 'description{}'.format(n))
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
