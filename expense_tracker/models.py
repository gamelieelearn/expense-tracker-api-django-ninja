from django.contrib.auth import get_user_model
from django.db import models


class ExpenseCategory(models.TextChoices):
    GROCERIES = 'Groceries'
    LEISURE = 'Leisure'
    ELECTRONICS = 'Electronics'
    UTILITIES = 'Utilities'
    CLOTHING = 'Clothing'
    HEALTH = 'Health'
    OTHERS = 'Others'


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=ExpenseCategory.choices)
    description = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return self.owner.username + ' - ' + self.category + ' - ' + str(self.amount) + ' - ' + str(self.time)
