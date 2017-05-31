import uuid

from django.contrib.contenttypes.models import ContentType

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
        model = 'categories.Category'
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
    owner = factory.SubFactory(UserFactory)
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


class LikeFactory(factory.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        exclude = ['content_object']
        abstract = True


class LikeLinkFactory(LikeFactory):
    user = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(LinkFactory)

    class Meta:
        model = 'likes.Like'
