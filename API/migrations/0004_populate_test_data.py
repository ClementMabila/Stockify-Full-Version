from django.db import migrations
from django.utils import timezone
from datetime import timedelta
import random

def populate_test_data(apps, schema_editor):
    # Get the models
    User = apps.get_model('auth', 'User')  # Get the User model
    Investment = apps.get_model('API', 'Investment')  # Replace 'API' with your app name
    Stock = apps.get_model('API', 'Stock')  # Replace 'API' with your app name
    StockInvestment = apps.get_model('API', 'StockInvestment')  # Replace 'API' with your app name
    Supplier = apps.get_model('API', 'Supplier')  # Replace 'API' with your app name
    Organization = apps.get_model('API', 'Organization')  # Replace 'API' with your app name

    # Fetch existing users, stocks, suppliers, and organizations
    users = User.objects.all()
    stocks = Stock.objects.all()
    suppliers = Supplier.objects.all()
    organizations = Organization.objects.all()

    if not users.exists() or not stocks.exists() or not suppliers.exists() or not organizations.exists():
        raise ValueError("Make sure you have users, stocks, suppliers, and organizations populated in the database!")

    # Generate 100 test investments and link them to stocks
    for _ in range(100):  # You can adjust the number of test entries here
        user = random.choice(users)
        stock = random.choice(stocks)
        supplier = random.choice(suppliers)
        organization = stock.organization  # assuming stock belongs to an organization

        amount = round(random.uniform(500, 5000), 2)  # Random investment amount between 500 and 5000
        percentage_profit = round(random.uniform(3, 10), 2)  # Random percentage profit between 3 and 10%

        # Random date within the last 90 days
        random_days_ago = random.randint(1, 90)
        date_invested = timezone.now() - timedelta(days=random_days_ago)

        # Create an Investment
        investment = Investment.objects.create(
            organization=organization,
            user=user,
            supplier=supplier,
            amount=amount,
            percentage_profit=percentage_profit,
            date_invested=date_invested
        )

        # Link the Investment to a Stock (StockInvestment)
        StockInvestment.objects.create(
            investment=investment,
            stock=stock,
            date_linked=date_invested  # Use the same date for linking
        )

def reverse_func(apps, schema_editor):
    # Reverse the data insertion (delete the test data)
    Investment = apps.get_model('API', 'Investment')  # Replace 'API' with your app name
    StockInvestment = apps.get_model('API', 'StockInvestment')  # Replace 'API' with your app name

    StockInvestment.objects.all().delete()
    Investment.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_stockreview_stockinvestment'),
    ]

    operations = [
        migrations.RunPython(populate_test_data, reverse_code=reverse_func),
    ]
