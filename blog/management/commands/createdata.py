import datetime

from blog.models import Blog, Comment

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from faker import Faker
from faker.generator import random

UserModel = get_user_model()
fake = Faker(['en_US'])

post_num = 100
comments_num = 5000


class Command(BaseCommand):
    help = "Create random posts and comments"  # noqa:A003

    def handle(self, *args, **options):
        objs = [
            UserModel(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.name(),
                email=fake.email(),
                password=make_password('Sample&Password!')
            )
            for _ in range(1, 51)
        ]
        UserModel.objects.bulk_create(objs)
        blog = [Blog(
            title=fake.company(),
            short_description=fake.paragraph(nb_sentences=1),
            image=fake.image_url(),
            full_description=fake.paragraph(nb_sentences=50, variable_nb_sentences=False),
            user_id=random.randint(1, 2),
            posted=random.choice([True or False]),
            rating=round(random.uniform(1, 5), 2))
            for _ in range(1, post_num + 1)]

        Blog.objects.bulk_create(blog)

        post_ids = Blog.objects.values_list("id", flat=True)
        comments = [Comment(
            name=fake.first_name(),
            email=fake.email(),
            post_id=random.choice(post_ids),
            text=fake.paragraph(nb_sentences=1),
            # parent_id=random.randint(1, 10),
            created=datetime.date.today(),

            active=random.choice([True or False]))
            for _ in range(1, comments_num + 1)]
        Comment.objects.bulk_create(comments)
        print('Successfully added')  # noqa T001
