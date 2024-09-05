import datetime
from decimal import Decimal

from ninja import ModelSchema, NinjaAPI, Schema

from .models import Expense, ExpenseCategory

api = NinjaAPI()


class ExpenseIn(Schema):
    description: str
    amount: Decimal
    category: ExpenseCategory
    time: datetime.date


class ExpenseOut(ModelSchema):
    class Meta:
        model = Expense
        fields = '__all__'


@api.post('/expense', tags=['expenses'])
def create_expense(request, payload: ExpenseIn) -> ExpenseOut:
    expense = Expense.objects.create(**payload.dict())
    return ExpenseOut(**expense.__dict__)


@api.get('/expenses', tags=['expenses'])
def list_expenses(request) -> list[ExpenseOut]:
    return [ExpenseOut(**expense.__dict__) for expense in Expense.objects.all()]
