from rest_framework import serializers
from .models import  Sale, StockHistory, StockInvestment, OTPCode, Organization, UserProfile, Product, RestockRequest, Supplier, Investment, Supplier, Stock, Customer
from django.contrib.auth.models import User, Group
from django.db.models import Sum
import uuid
from datetime import datetime
from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
import uuid
from datetime import datetime

class UserRegistrationAndOrganizationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    
    organization_name = serializers.CharField(max_length=100)
    organization_description = serializers.CharField()
    organization_address = serializers.CharField()
    organization_phone_number = serializers.CharField(max_length=15, required=False)
    organization_email = serializers.EmailField()
    organization_date_established = serializers.DateField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )

        organization = Organization.objects.create(
            name=validated_data['organization_name'],
            identifier=uuid.uuid4(),
            description=validated_data['organization_description'],
            address=validated_data['organization_address'],
            phone_number=validated_data.get('organization_phone_number', ''),
            email=validated_data['organization_email'],
            date_established=validated_data['organization_date_established'],
            status='Active',
            subscription_plan='Free',
            admin=user,
        )

        UserProfile.objects.create(
            user=user,
            role='Admin',
            organization=organization
        )

        try:
            admin_group = Group.objects.get(name='Admin')
        except Group.DoesNotExist:
            admin_group = Group.objects.create(name='Admin')
        user.groups.add(admin_group)

        otp = str(uuid.uuid4())[:6]

        OTPCode.objects.create(
            email=user.email,
            code=otp,
            is_used=False,
            organization=organization,
            created_at=datetime.now()
        )

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'organization', 'bio', 'location', 'avatar']

class StockAlertSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name') 
    sku = serializers.CharField(source='product.sku') 

    class Meta:
        model = RestockRequest
        fields = ['request_date', 'product', 'sku', 'requested_quantity', 'status']

class SalesEntrySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    
    class Meta:
        model = Sale
        fields = [
            'id', 'sale_date', 'product', 'customer', 'sku',
            'quantity_sold', 'sale_price', 'status', 'organization'
        ]
        read_only_fields = ['sale_date', 'sku', 'organization']

class StockHistorySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()  # to show product name

    class Meta:
        model = StockHistory
        fields = [
            'id',
            'transaction_date',
            'transaction_type',
            'product',
            'total_revenue',
        ]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'contact']

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'organization',
            'name',
            'category',
            'sku',
            'unit_price',
            'available_size',
            'location',
            'reorder_level',
            'supplier'
        ]


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = Stock
        fields = ['quantity', 'product']

class InventorySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source='supplier', write_only=True
    )
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'user', 'organization', 'name', 'category', 'sku',
            'unit_price', 'available_size', 'location', 'reorder_level',
            'supplier', 'supplier_id', 'stock'
        ]
        read_only_fields = ['user', 'organization']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['organization'] = self.context['request'].user.userprofile.organization
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class DashboardStatsSerializer(serializers.Serializer):
    today_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock_available = serializers.IntegerField()
    sold_items = serializers.IntegerField()
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    active_stock = serializers.IntegerField()

class SupplierInvestmentSerializer(serializers.ModelSerializer):
    total_investments = serializers.SerializerMethodField()
    total_amount_invested = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'total_investments', 'total_amount_invested']

    def get_total_investments(self, obj):
        return obj.total_investments()

    def get_total_amount_invested(self, obj):
        return obj.total_amount_invested()
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'organization'] 
        read_only_fields = ['organization']

class InvestmentPerformanceSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=2)

class StockInvestmentSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = StockInvestment
        fields = ['id', 'stock', 'date_linked']

class DetailedInvestmentSerializer(serializers.ModelSerializer):
    performance = serializers.SerializerMethodField()
    total_return = serializers.SerializerMethodField()
    profit_amount = serializers.SerializerMethodField()
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    stock_investments = StockInvestmentSerializer(many=True, read_only=True)

    class Meta:
        model = Investment
        fields = [
            'id', 'organization', 'user', 'supplier_name', 'amount',
            'percentage_profit', 'date_invested', 'total_return',
            'profit_amount', 'performance', 'stock_investments'
        ]

    def get_total_return(self, obj):
        return obj.total_return()

    def get_profit_amount(self, obj):
        return obj.profit_amount()

    def get_performance(self, obj):
        if hasattr(obj, 'performance') and obj.performance:
            return {
                'current_value': obj.performance.current_value,
                'growth_rate': obj.performance.growth_rate,
            }
        return None  # Gracefully handle missing performance
    
# serializers.py
class InvestableStockSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source='organization.name')
    supplier = serializers.CharField(source='product.supplier.name')
    product = serializers.CharField(source='product.name')
    number_of_investors = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ['id', 'organization', 'supplier', 'product', 'quantity', 'number_of_investors']

    def get_number_of_investors(self, obj):
        return obj.investments.values('investment__user').distinct().count()


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Organization, InvestorMessage, ChatMessage, StockHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'logo', 'subscription_plan', 
                  'status', 'date_established', 'website', 'email', 'phone_number']


class UserProfileSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'organization', 'bio', 'location', 'avatar']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'avatar', 'first_name', 'last_name', 'email']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        # Update User model fields
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()
        
        # Update UserProfile model fields
        if 'bio' in validated_data:
            instance.bio = validated_data['bio']
        if 'location' in validated_data:
            instance.location = validated_data['location']
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        instance.save()
        
        return instance



class UserMemberSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']
    
    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except:
            return None


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMemberSerializer(read_only=True)
    receiver = UserMemberSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp']


class MessageCreateSerializer(serializers.ModelSerializer):
    receiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['receiver_id', 'message']
    
    def create(self, validated_data):
        receiver_id = validated_data.pop('receiver_id')
        user = self.context['request'].user
        organization = user.userprofile.organization
        
        try:
            receiver = User.objects.get(id=receiver_id)
            # Check if receiver is in the same organization
            if receiver.userprofile.organization.id != organization.id:
                raise serializers.ValidationError("Cannot send message to user in different organization")
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found")
        
        message = ChatMessage.objects.create(
            sender=user,
            receiver=receiver,
            organization=organization,
            message=validated_data['message']
        )
        
        return message


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    
    class Meta:
        model = User
        fields = ['user', 'profile']