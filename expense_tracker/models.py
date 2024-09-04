from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.owner.name + ' - ' + self.category + ' - ' + str(self.amount) + ' - ' + str(self.date)
