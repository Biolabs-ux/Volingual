import os
import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volingual.settings')
django.setup()

from users.models import CustomUser

# Create a Faker instance
fake = Faker()


# A function to create a fake user
def create_user():
    CustomUser.objects.create(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        country=fake.country(),
        is_active=fake.boolean(),
        is_staff=fake.boolean(),
    )


# Create 10 fake users
for _ in range(10):
    create_user()
