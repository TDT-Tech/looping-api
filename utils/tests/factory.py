from datetime import datetime

import factory
from faker import Faker

from groups.models import Group, Member
from newsletters.models import Answer, Newsletter, Question
from users.models import User

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = faker.name()
    email = faker.email()


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = faker.word()


class GroupAdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    role = Member.Roles.ADMIN


class UserWithGroupFactory(UserFactory):
    membership = factory.RelatedFactory(GroupAdminFactory, factory_related_name="user")


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question = faker.text()
    author = faker.name()
    group = factory.SubFactory(GroupAdminFactory)


class NewsletterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Newsletter

    issue_date = faker.date_between(start_date=datetime.now())
    group = factory.SubFactory(GroupAdminFactory)
    status = Newsletter.Status.INPROGRESS

    @factory.post_generation
    def questions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.questions.add(*extracted)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    answer = faker.text()
    submitter = faker.name()
    question = factory.SubFactory(QuestionFactory)
    newsletter = factory.SubFactory(NewsletterFactory)
