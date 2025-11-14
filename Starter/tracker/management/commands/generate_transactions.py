import random
from faker import Faker
from django.core.management.base import BaseCommand
from tracker.models import User, Transaction


class Command(BaseCommand):
    help = 'Generate transactions for testing'  
    def handle(self, *args, **options):
        fake = Faker()

        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='castlecash' )
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        for i in range(20):
            Transaction.objects.create(
                user = user,
                amount = random.uniform(1, 2500),
                date=fake.date_between(start_date = '-1yr', end_date ='today'),
                type=random.choice(types)
            )
            
