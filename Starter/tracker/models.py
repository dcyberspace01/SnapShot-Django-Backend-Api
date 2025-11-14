from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
class User(AbstractUser):
    pass


#Transaction is only expenses
#Transaction has an amount
#tranaction is tied to a user so will need a foreign key
#transaction will need a date
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('expense', 'expense'),

    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=7, choices=TRANSACTION_TYPE_CHOICES
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    date = models.DateField(default=date.today)

    def __str__(self):
        return (
            
            f"{self.type} of {self.amount}, \n"
            f"on {self.date},\n"
            f"by {self.user}\n"
       )
    class Meta:
        ordering = ['-date']