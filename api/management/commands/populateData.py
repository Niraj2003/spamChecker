from django.core.management.base import BaseCommand
from api.models import Contact
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the Contact table with random sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_contacts = 100  # Adjust the number of contacts you want to create

        for _ in range(num_contacts):
            name = fake.name()
            phone_number = fake.phone_number()
            spam_count = random.randint(1, num_contacts)
            
            phone_number = phone_number[:13]

            try:
                contact = Contact(name=name, phone_number=phone_number, spam_count=spam_count)
                contact.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added contact {name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding contact {name}: {e}'))
