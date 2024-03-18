from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):

    title = models.CharField(max_length=200)

    options = (
        ('expenses', 'expenses'),
        ('income', 'income'),
    )

    type = models.CharField(max_length=200, choices=options, default='expenses')

    cat_options = (
        ('food', 'food'),
        ('fuel', 'fuel'),
        ('entertainment', 'entertainment'),
        ('emi', 'emi'),
        ('bills', 'bills'),
        ('rent', 'rent'),
        ('miscellaneous', 'miscellaneous'),    
    )

    category = models.CharField(max_length=200, choices=cat_options, default='miscellaneous')

    amount = models.PositiveIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)

    # user = models.CharField(max_length=200)
    user_object=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        
        return self.title