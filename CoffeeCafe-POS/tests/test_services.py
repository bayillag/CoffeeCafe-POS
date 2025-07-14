# A comprehensive test_services.py file for testing your CoffeeCafe-POS services with pytest

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from app.services import DatabaseService, AuthService, InventoryService, ReportingService, LoyaltyService
from app.models import Product, Order, Employee, Customer

@pytest.fixture
def mock_db():
    with patch('app.services.database.create_client') as mock_client:
        mock_db = DatabaseService()
        mock_db.client = MagicMock()
        yield mock_db

@pytest.fixture
def sample_product():
    return Product(
        id="prod_123",
        name="Espresso",
        category="Coffee",
        price=3.50,
        cost=1.00
    )

@pytest.fixture
def sample_order():
    order = Order()
    order.add_item("prod_123", 2, 3.50)
    return order

@pytest.fixture
def sample_employee():
    return Employee(
        id="emp_123",
        name="John Doe",
        email="john@coffeecafe.com",
        role="manager"
    )

class TestDatabaseService:
    def test_get_product(self, mock_db, sample_product):
        # Mock the Supabase response
        mock_db.client.table().select().eq().execute.return_value.data = [{
            'id': sample_product.id,
            'name': sample_product.name,
            'category': sample_product.category,
            'price': sample_product.price,
            'cost': sample_product.cost
        }]
        
        result = mock_db.get_product(sample_product.id)
        assert result['id'] == sample_product.id
        assert result['name'] == sample_product.name
        mock_db.client.table().select().eq().execute.assert_called_once()

    def test_create_order(self, mock_db, sample_order):
        mock_db.client.table().insert().execute.return_value.data = [{
            'id': 'order_123',
            'total_amount': sample_order.total,
            'status': 'completed'
        }]
        
        order_data = sample_order.to_dict()
        result = mock_db.create_order(order_data)
        assert result['id'] == 'order_123'
        mock_db.client.table().insert().execute.assert_called_once()

class TestAuthService:
    def test_authenticate_employee_success(self, mock_db, sample_employee):
        auth = AuthService()
        auth.db = mock_db
        
        # Mock successful authentication
        mock_db.client.table().select().eq().execute.return_value.data = [{
            'id': sample_employee.id,
            'name': sample_employee.name,
            'email': sample_employee.email,
            'role': sample_employee.role,
            'password_hash': 'hashed_password'
        }]
        
        with patch('passlib.hash.pbkdf2_sha256.verify', return_value=True):
            with patch('jwt.encode', return_value="fake_token"):
                result = auth.authenticate_employee(sample_employee.email, "password")
                assert result['token'] == "fake_token"
                assert result['employee']['name'] == sample_employee.name

    def test_authenticate_employee_failure(self, mock_db):
        auth = AuthService()
        auth.db = mock_db
        
        # Mock failed authentication
        mock_db.client.table().select().eq().execute.return_value.data = []
        
        result = auth.authenticate_employee("wrong@email.com", "wrongpass")
        assert result is None

class TestInventoryService:
    def test_get_stock_level(self, mock_db):
        inventory = InventoryService()
        inventory.db = mock_db
        
        mock_db.client.table().select().eq().execute.return_value.data = [{
            'quantity': 10
        }]
        
        assert inventory.get_stock_level("prod_123") == 10

    def test_update_stock(self, mock_db):
        inventory = InventoryService()
        inventory.db = mock_db
        
        # Mock current stock
        mock_db.client.table().select().eq().execute.return_value.data = [{
            'quantity': 10
        }]
        
        # Mock upsert
        mock_db.client.table().upsert().execute.return_value = True
        
        assert inventory.update_stock("prod_123", -2) is True
        assert inventory.update_stock("prod_123", -15) is False  # Would go negative

class TestReportingService:
    def test_get_sales_report(self, mock_db):
        reporting = ReportingService()
        reporting.db = mock_db
        
        test_data = [{
            'id': 'order_123',
            'created_at': datetime.now().isoformat(),
            'total_amount': 10.50,
            'order_items': [{
                'product_id': 'prod_123',
                'quantity': 2,
                'unit_price': 5.25
            }]
        }]
        
        mock_db.client.table().select().gte().lte().execute.return_value.data = test_data
        
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        result = reporting.get_sales_report(start_date, end_date)
        assert len(result) == 1
        assert result[0]['total_amount'] == 10.50

class TestLoyaltyService:
    def test_add_points(self, mock_db):
        loyalty = LoyaltyService()
        loyalty.db = mock_db
        
        # Mock RPC call
        mock_db.client.rpc().execute.return_value = True
        
        assert loyalty.add_points("cust_123", 10.50) is True
        mock_db.client.rpc.assert_called_with('increment_points', {
            'customer_id': 'cust_123',
            'points': 10  # 1 point per $1 spent
        })

    def test_redeem_points_success(self, mock_db):
        loyalty = LoyaltyService()
        loyalty.db = mock_db
        
        # Mock current points
        mock_db.client.table().select().eq().execute.return_value.data = [{
            'points': 100
        }]
        
        # Mock RPC call
        mock_db.client.rpc().execute.return_value = True
        
        discount = loyalty.redeem_points("cust_123", 20)
        assert discount == 1.00  # 20 points * $0.05 per point

    def test_redeem_points_failure(self, mock_db):
        loyalty = LoyaltyService()
        loyalty.db = mock_db
        
        # Mock insufficient points
        mock_db.client.table().select().eq().execute.return_value.data = [{
            'points': 10
        }]
        
        assert loyalty.redeem_points("cust_123", 20) is None