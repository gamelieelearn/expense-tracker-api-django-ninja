import datetime
from decimal import Decimal

from django.http.request import HttpRequest
from ninja import ModelSchema, NinjaAPI, Router, Schema
from ninja.security import django_auth

from .models import Expense, ExpenseCategory

api = NinjaAPI(csrf=True)
router = Router(tags=['expenses'])


class ExpenseIn(Schema):
    description: str
    amount: Decimal
    category: ExpenseCategory
    time: datetime.datetime


class ExpenseOut(ModelSchema):
    class Meta:
        model = Expense
        fields = '__all__'


@router.post('/expense', auth=django_auth)
def create_expense(request: HttpRequest, payload: ExpenseIn) -> ExpenseOut:
    expense_data = payload.dict()
    user = request.auth
    if user is None:
        raise ValueError('User is not authenticated')
    expense = Expense.objects.create(owner=user, **expense_data)
    return expense


@router.put('/expense/{expense_id}')
def update_expense(request, expense_id: int, payload: ExpenseIn) -> ExpenseOut:
    expense = Expense.objects.get(id=expense_id)
    for attr, value in payload.dict().items():
        setattr(expense, attr, value)
    expense.save()
    return expense


@router.delete('/expense/{expense_id}')
def delete_expense(request, expense_id: int):
    expense = Expense.objects.get(id=expense_id)
    expense.delete()
    return {'success': True}


@router.get('/expenses')
def list_expenses(request) -> list[ExpenseOut]:
    expenses = Expense.objects.all()
    return [ExpenseOut.from_orm(expense) for expense in expenses]
