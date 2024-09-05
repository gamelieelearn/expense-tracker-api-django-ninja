from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient

from .api import router
from .models import Expense, ExpenseCategory


class ExpenseAPITestCase(TestCase):
    def setUp(self):
        self.client: TestClient = TestClient(router)
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        # Set the authentication for the TestClient
        self.client.force_authenticate(user=self.user)
        self.expense_data = {
            'description': 'Test Expense',
            'amount': '50.00',
            'category': ExpenseCategory.GROCERIES,
            'time': timezone.now().isoformat(),
        }

    def test_create_expense(self):
        response = self.client.post('/expense', json=self.expense_data)
        assert response.status_code == 200, response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        assert expense is not None
        self.assertEqual(expense.description, 'Test Expense')
        self.assertEqual(expense.amount, Decimal('50.00'))
        self.assertEqual(expense.category, ExpenseCategory.GROCERIES)

    def test_update_expense(self):
        expense = Expense.objects.create(owner=self.user, **self.expense_data)
        updated_data = self.expense_data.copy()
        updated_data['description'] = 'Updated Expense'
        updated_data['amount'] = '75.00'

        response = self.client.put(f'/expense/{expense.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        expense.refresh_from_db()
        self.assertEqual(expense.description, 'Updated Expense')
        self.assertEqual(expense.amount, Decimal('75.00'))

    def test_list_expenses(self):
        Expense.objects.create(owner=self.user, **self.expense_data)
        Expense.objects.create(
            owner=self.user,
            description='Second Expense',
            amount='25.00',
            category=ExpenseCategory.LEISURE,
            time=timezone.now(),
        )

        response = self.client.get('/expenses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_invalid_expense_data(self):
        invalid_data = self.expense_data.copy()
        invalid_data['amount'] = 'not a number'

        response = self.client.post('/expense', json=invalid_data)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_expense_not_found(self):
        response = self.client.put('/expense/999', json=self.expense_data)
        self.assertEqual(response.status_code, 404)
