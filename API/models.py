from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
from datetime import timedelta
from django.contrib.auth.models import Group

class Organization(models.Model):
    PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=100, unique=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    date_established = models.DateField()
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended')],
        default='Active',
    )
    subscription_plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default='Free',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_organizations')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Investor', 'Investor'),
        ('StockChecker', 'StockChecker'),
        ('FinancialAdmin', 'Financial Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.organization.name}"

class InvestorMessage(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='investor_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor_received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} to {self.receiver} at {self.timestamp}"

class ChatMessage(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} at {self.timestamp}"

class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suppliers")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="suppliers")
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    is_open_for_investment = models.BooleanField(default=False)

    class Meta:
        unique_together = ('organization', 'email')

    def __str__(self):
        return self.name

    def total_investments(self):
        return self.investments.count()

    def total_amount_invested(self):
        return self.investments.aggregate(Sum('amount'))['amount__sum'] or 0

    def investors(self):
        return self.investments.values('user__username').annotate(total_invested=Sum('amount'))

    def sales_this_month(self):
        today = now().date()
        first_day = today.replace(day=1)
        return self.sales_in_period(start=first_day)
    
    def sales_this_year(self):
        today = now().date()
        first_day = today.replace(month=1, day=1)
        return self.sales_in_period(start=first_day)

    def sales_in_period(self, start, end=None):
        end = end or now()
        return Sale.objects.filter(
            product__supplier=self,
            sale_date__range=(start, end)
        ).aggregate(total=Sum('sale_price'))['total'] or 0

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_size = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    reorder_level = models.PositiveIntegerField(default=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="products")

    class Meta:
        unique_together = ('organization', 'sku')

    def __str__(self):
        return self.name

class Stock(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="stocks")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"

    def reduce_stock(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available")

class Customer(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="customers")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    class Meta:
        unique_together = ('organization', 'email'), ('organization', 'phone')

    def __str__(self):
        return self.name

class Order(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

class Sale(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="sales")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    quantity_sold = models.PositiveIntegerField()
    sku = models.CharField(max_length=50)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled')
    ], default='Completed')

    def __str__(self):
        return f"{self.quantity_sold} x {self.product.name} - {self.sale_price}"

    def save(self, *args, **kwargs):
        if not self.pk:
            stock = self.product.stock
            starting_quantity = stock.quantity
            stock.reduce_stock(self.quantity_sold)

            StockHistory.objects.create(
                organization=self.organization,
                transaction_type='Sale',
                product=self.product,
                sku=self.sku,
                stock_change=-self.quantity_sold,
                starting_stock=starting_quantity,
                total_revenue=self.sale_price
            )

        super().save(*args, **kwargs)

class StockHistory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="stock_history")
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=50, choices=[('Restock', 'Restock'), ('Sale', 'Sale')])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_history")
    sku = models.CharField(max_length=50)
    stock_change = models.IntegerField()
    starting_stock = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.stock_change}"

class RestockRequest(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="restock_requests")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="restock_requests")
    requested_quantity = models.PositiveIntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Restock Request for {self.product.name} - {self.status}"

class Investment(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='investments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_profit = models.DecimalField(max_digits=5, decimal_places=2, help_text="e.g., 5.00 for 5%")
    date_invested = models.DateTimeField(auto_now_add=True)
      
    def profit_amount(self):
        return self.amount * (self.percentage_profit / 100)

    def total_return(self):
        return self.amount + self.profit_amount()

    def __str__(self):
        return f"{self.user.username} invested {self.amount} in {self.supplier.name}"



class Withdrawal(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='withdrawals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_withdrawn = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} withdrew {self.amount} from investment {self.investment.id}"

class InvestmentPerformance(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="investment_performances")
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE, related_name="performance")
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    growth_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.investment.user.username} - Performance"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('Investment', 'Investment'),
        ('Stock', 'Stock'),
        ('Message', 'Message'),
        ('System', 'System'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='System')

    def __str__(self):
        return f"{self.title} ({self.notification_type})"

class Invitation(models.Model):
    organization = models.ForeignKey(
        'Organization', 
        on_delete=models.CASCADE, 
        related_name='invitations'
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expires_at = models.DateTimeField()
    group = models.ForeignKey(
        'auth.Group',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Expired', 'Expired'),
        ],
        default='Pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'email')

    def is_expired(self):
        if now() > self.expires_at:
            self.status = 'Expired'
            self.save(update_fields=['status'])
            return True
        return False

    def __str__(self):
        return f"Invitation to {self.email} for {self.organization.name} (Status: {self.status})"

class OTPCode(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='otp_codes')
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expiration_time = models.DateTimeField()

    class Meta:
        unique_together = ('organization', 'email', 'code')

    def __str__(self):
        return f"{self.email} - {self.code}"

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            self.expiration_time = self.created_at + timedelta(minutes=10)
        super().save(*args, **kwargs)

class MonthlySalesStock(models.Model):
    YEAR_CHOICES = [(r, r) for r in range(2020, 2031)]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='monthly_sales_stocks')
    year = models.IntegerField(choices=YEAR_CHOICES)
    month = models.CharField(max_length=10) 
    sales = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    class Meta:
        unique_together = ('organization', 'year', 'month')
        ordering = ['year', 'month']

    def __str__(self):
        return f"{self.month} {self.year} - Sales: {self.sales}, Stock: {self.stock}"
    
class MonthlyInvestment(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="monthly_investments")
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name="monthly_values")
    month = models.DateField(help_text="Use the first day of the month for consistency, e.g., 2025-04-01")
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('investment', 'month')
        ordering = ['month']

    def __str__(self):
        return f"{self.investment.user.username} - {self.month.strftime('%b %Y')} - {self.value}"
    
class StockInvestment(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='stock_investments')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='investments')
    date_linked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('investment', 'stock')

    def __str__(self):
        return f"{self.investment.user.username} invested in {self.stock.product.name}"

class StockReview(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review on {self.stock.product.name}"
