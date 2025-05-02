import json
import csv
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, generics
from rest_framework.exceptions import PermissionDenied, NotFound
from dateutil.relativedelta import relativedelta
from io import TextIOWrapper
import pandas as pd
from django.middleware.csrf import get_token
from django.db.models import Sum, Q, Max
from .forms import CreateUserForm
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import CreateUserForm
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils.timezone import now, timezone
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_backends
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
import json
from dj_rest_auth.registration.views import SocialLoginView
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
import random
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
import uuid
import logging
from collections import defaultdict
from django.contrib.auth import login, get_backends
from django.contrib.auth import get_user_model
import datetime
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Sum, Count
from .models import RestockRequest, Sale, MonthlySalesStock, StockHistory, Stock, Product, Supplier, Invitation, OTPCode, Investment, Withdrawal, UserProfile, Organization, Customer, MonthlyInvestment, StockInvestment, InvestorMessage, ChatMessage
from .serializers import (
    StockAlertSerializer,
    SalesEntrySerializer,
    StockHistorySerializer,
    InventorySerializer,
    SupplierSerializer,
    DashboardStatsSerializer,
    SupplierInvestmentSerializer, 
    UserProfileSerializer,
    UserRegistrationAndOrganizationSerializer,
    CustomerSerializer,
    InvestmentPerformanceSerializer,
    DetailedInvestmentSerializer,
    InvestableStockSerializer,
    MessageSerializer,  # Added import for MessageSerializer
    UserSerializer  # Added import for UserSerializer
)

User = get_user_model()


class UserRegistrationAndOrganizationCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationAndOrganizationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                login(request, user)
                return Response({"detail": "User and organization created, and user logged in."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "User created but login failed."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def some_function():
    from .forms import CreateUserForm

def get_email_from_token(request, token):
    try:
        invitation = Invitation.objects.get(token=token)
        return JsonResponse({"email": invitation.email})
    except Invitation.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=404)

@csrf_exempt
def register_from_invite(request, token):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match"}, status=400)

        try:
            invitation = Invitation.objects.get(token=token, email=email)
        except Invitation.DoesNotExist:
            return JsonResponse({"error": "Invalid or expired invitation"}, status=400)

        user = User.objects.create(
            username=email,
            email=email,
            password=make_password(password),
            is_active=False
        )

        if invitation.group:
            invitation.group.user_set.add(user)

            invitation.delete()  

        otp = str(uuid.uuid4())[:6]  
                
        organization = invitation.organization 
        print(f"[DEBUG] The organization found for registartion: {organization}")
        
        role = invitation.group.name
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            organization=organization
        )

        otp_code = OTPCode.objects.create(
            email=email,
            code=otp,
            is_used=False,
            organization=organization, 
            created_at=datetime.now()
        )

        send_mail(
            "Your OTP Code",
            f"Your OTP is: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({"message": "OTP sent to your email"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_groups(request):
    groups = Group.objects.all().values("id", "name")
    return JsonResponse({"groups": list(groups)})

@csrf_exempt
def send_invitation(request):

    print("DEBUG: User =", request.user)
    print("DEBUG: Authenticated =", request.user.is_authenticated)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated"}, status=401)
    
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        group_name = data.get("group")  # Optional group

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        try:
            organization = request.user.userprofile.organization
        except AttributeError:
            return JsonResponse({"error": "User is not associated with any organization"}, status=403)

        # Optional group assignment
        group = None
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                return JsonResponse({"error": "Invalid group"}, status=400)

        try:
            # Ensure unique invite (org + email)
            existing = Invitation.objects.get(organization=organization, email=email)
            return JsonResponse({"error": "An invitation has already been sent to this email"}, status=400)
        except Invitation.DoesNotExist:
            pass

        token = str(uuid.uuid4())
        expires_at = now() + timedelta(days=1)

        invitation = Invitation.objects.create(
            organization=organization,
            email=email,
            token=token,
            group=group,
            expires_at=expires_at,
        )

        invite_link = f"{settings.FRONTEND_URL}/register/{token}/"

        send_mail(
            subject="You're Invited to Join an Organization",
            message=f"You've been invited to join {organization.name}. Click the link to register:\n\n{invite_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({"message": "Invitation sent successfully!"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_protect
@require_http_methods(["POST"])
def verify_otp(request):
    print("[DEBUG] verify_otp view called.")

    try:
        body = request.body
        print(f"[DEBUG] Raw request.body: {body}")
        data = json.loads(body)
        print(f"[DEBUG] Parsed JSON data: {data}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {e}")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    otp = data.get("otp")
    email = data.get("email")

    print(f"[DEBUG] Extracted OTP: {otp}, Email: {email}")

    if not otp or not email:
        print("[ERROR] OTP or Email missing from request.")
        return JsonResponse({"error": "OTP and Email are required."}, status=400)

    try:
        otp_record = OTPCode.objects.get(email=email, code=otp, is_used=False)
        print(f"[DEBUG] OTP record found: {otp_record}")
    except OTPCode.DoesNotExist:
        print("[ERROR] OTP record not found or already used.")
        return JsonResponse({"error": "Invalid OTP or OTP already used"}, status=400)

    if otp_record.expiration_time < now():
        print(f"[ERROR] OTP expired at {otp_record.expiration_time}, now is {now()}")
        return JsonResponse({"error": "OTP has expired"}, status=400)

    otp_record.is_used = True
    otp_record.save()
    print(f"[DEBUG] OTP marked as used.")

    try:
        user = User.objects.get(email=email)
        print(f"[DEBUG] User found: {user.username}")
        user.is_active = True
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        print("[DEBUG] User logged in and session started.")
        otp_record.delete()  # Clean up OTP record after successful login   
        return JsonResponse({
        'success': True,
        'message': 'OTP verified and user logged in.',
        'email': user.email
        })
    except User.DoesNotExist:
        print("[ERROR] User not found.")
        return JsonResponse({"error": "User not found."}, status=404)
    
@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})

@require_http_methods(['POST'])
def login_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            print(f"[DEBUG]User name: {username}")
            print(f"[DEBUG]User password: {password}")
        except Exception:
            return JsonResponse({"error": "Invalid request"}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_active:
                return JsonResponse({"error": "Please verify your account first."}, status=403)

            otp = str(uuid.uuid4())[:6]
            OTPCode.objects.create(
                email=user.email,
                code=otp,
                is_used=False,
                organization=user.userprofile.organization,
                created_at=now()
            )

            send_mail(
                subject="Your OTP Code",
                message=f"Your login OTP is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return JsonResponse({"message": "OTP sent to your email", "email": user.email})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=401)

    return JsonResponse({"error": "Method not allowed"}, status=405)

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})

@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {'username': request.user.username, 'email': request.user.email}
        )
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )

@api_view(['GET'])
def get_user_info(request):
    user = request.user
    role = get_user_role(user)
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": role,
    })

@csrf_exempt
def current_user_api(request):
    print(f"[DEBUG] Session ID: {request.session.session_key}")
    print(f"[DEBUG] Auth User ID: {request.session.get('_auth_user_id')}")
    
    if request.user.is_authenticated:
        return JsonResponse({
            "username": request.user.username,
            "email": request.user.email,
        })
    return JsonResponse({"error": "Not authenticated"}, status=401)

class StockAlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockAlertSerializer

    def get_queryset(self):
        user = self.request.user
        print(f"DEBUG: User: {user}, Authenticated: {user.is_authenticated}")
        if user.is_authenticated:
            user_org = user.userprofile.organization
            user_role = user.userprofile.role  # Assuming you have a `role` field in profile

            if user_role in ['stock_checker', 'Admin']:
                return RestockRequest.objects.filter(organization=user_org)

        return RestockRequest.objects.none()


class IsFinancialAdminOrAdmin(permissions.BasePermission):
    """Allow only Financial Admin and Admin users"""
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role in ['Financial Admin', 'Admin']

class SalesEntryViewSet(viewsets.ModelViewSet):
    serializer_class = SalesEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsFinancialAdminOrAdmin]

    def get_queryset(self):
        # Only show sales for the user's organization
        return Sale.objects.filter(
            organization=self.request.user.userprofile.organization
        ).order_by('-sale_date')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Allow read-only for all authenticated users
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        if role not in ['Financial Admin', 'Admin']:
            raise PermissionDenied("You don't have permission to create sales")

        organization = self.request.user.userprofile.organization

        # Get last sale to determine next SKU
        last_sale = Sale.objects.filter(organization=organization).order_by('-id').first()
        if last_sale and last_sale.sku and last_sale.sku.startswith("SK"):
            last_number = int(last_sale.sku[2:])
            next_sku = f"SK{last_number + 1}"
        else:
            next_sku = "SK1001"

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            organization=organization,
            sku=next_sku
        )

    def perform_update(self, serializer):
        role = get_user_role(self.request.user)
        if role not in ['Financial Admin', 'Admin']:
            raise PermissionDenied("You don't have permission to update sales")
        serializer.save()

    def perform_destroy(self, instance):
        role = get_user_role(self.request.user)
        if role not in ['Financial Admin', 'Admin']:
            raise PermissionDenied("You don't have permission to delete sales")
        instance.delete()

class StockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        role = get_user_role(self.request.user)
        print(f"Stock History user role: {role}")
        if role not in ['Admin', 'Financial Admin', 'Inventory Manager']:
            return StockHistory.objects.none()

        return StockHistory.objects.filter(
            organization=self.request.user.userprofile.organization
        ).order_by('-transaction_date')

def get_user_role(user):
    try:
        return user.userprofile.role
    except Exception:
        return None


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        print("Debug: request.user =", user)
        print("Debug User role:", role)
        print("Is authenticated:", user.is_authenticated)

        print("User role:", role)

        try:
            organization_id = user.userprofile.organization.id
            print("User's organization:", organization_id)
        except Exception as e:
            print("Error accessing user organization:", e)
            return Product.objects.none()

        if role in ['Admin', 'StockChecker', 'FinancialAdmin', 'Investor']:

            queryset = Product.objects.filter(organization_id=organization_id)

            for p in queryset:
                print(f"Product: {p.name}, Org ID: {p.organization_id}, Org Name: {p.organization.name}")

            print(f"products for org {organization_id}:", list(queryset))
            return queryset
        
        return Product.objects.none()
    

    def create(self, request, *args, **kwargs):
        role = get_user_role(request.user)
        if role not in ['Admin', 'StockChecker', 'FinancialAdmin']:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        try:
            organization = request.user.userprofile.organization
            print("Organization ID:", organization.id)
        except AttributeError as e:
            print("Organization error:", str(e))
            return Response(...)

        product_data = request.data.copy()
        product_data['organization'] = organization.id
        print("Modified product data:", product_data) 

        serializer = self.get_serializer(data=product_data)
        print("Serializer data pre-validation:", serializer.initial_data)
        
        is_valid = serializer.is_valid()
        print("Is valid:", is_valid)
        if not is_valid:
            print("Validation errors:", serializer.errors)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        role = get_user_role(request.user)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if role == 'FinancialAdmin':
            allowed_fields = ['unit_price', 'available_size']
            for field in request.data:
                if field not in allowed_fields:
                    return Response(
                        {"error": "You can only update unit price and size"},
                        status=status.HTTP_403_FORBIDDEN
                    )

        if role in ['StockChecker', 'Admin', 'FinancialAdmin']:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        role = get_user_role(request.user)
        if role != 'Admin':
            return Response({"error": "Only Admins can delete products"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class UploadCSVView(APIView):
    def post(self, request):
        if 'csv_file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file)

            required_columns = ['product_id', 'transaction_type', 'sku', 'stock_change', 'starting_stock', 'total_revenue']
            if not all(col in df.columns for col in required_columns):
                return Response({'error': 'CSV file is missing required columns'}, status=status.HTTP_400_BAD_REQUEST)

            for index, row in df.iterrows():
                try:
                    product = Product.objects.get(id=row['product_id'])
                    stock_change = int(row['stock_change'])
                    starting_stock = int(row['starting_stock'])
                    total_revenue = float(row['total_revenue'])

                    StockHistory.objects.create(
                        transaction_type=row['transaction_type'],
                        product=product,
                        sku=row['sku'],
                        stock_change=stock_change,
                        starting_stock=starting_stock,
                        total_revenue=total_revenue,
                    )
                except Product.DoesNotExist:
                    return Response({'error': f"Product with ID {row['product_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)
                except ValueError as e:
                    return Response({'error': f"Invalid data in CSV file: {e}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'CSV data uploaded successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"Error processing CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

def export_products_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Price'])

    print(Product.objects.all())
    products = Product.objects.all()
    for product in products:
        writer.writerow([product.id, product.name, product.unit_price])

    return response

class UploadProductCSVView(APIView):
    def post(self, request):
        if 'csv_file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file)

            required_columns = ['name', 'category', 'sku', 'unit_price', 'available_size', 'location', 'reorder_level']
            if not all(col in df.columns for col in required_columns):
                return Response({'error': 'CSV file is missing required columns'}, status=status.HTTP_400_BAD_REQUEST)

            for _, row in df.iterrows():
                try:
                    Product.objects.create(
                        name=row['name'],
                        category=row['category'],
                        sku=row['sku'],
                        unit_price=row['unit_price'],
                        available_size=row['available_size'],
                        location=row['location'],
                        reorder_level=row['reorder_level']
                    )
                except ValidationError as e:
                    return Response({'error': f"Error with product {row['sku']}: {e}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Products uploaded successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"Error processing CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

def cors_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response
    return middleware

logger = logging.getLogger(__name__)


@csrf_exempt
def generate_invite_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        token = str(uuid.uuid4())
        invitation = Invitation.objects.create(email=email, token=token, expires_at=now() + timedelta(days=1))

        invite_link = f"{settings.FRONTEND_URL}/register/{token}/"

        return JsonResponse({"invite_link": invite_link}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_notifications(request):
    notifications = RestockRequest.objects.filter(status="Pending").order_by("-request_date")
    
    last_seen = request.session.get('notifications_last_seen')
    if not last_seen:
        unseen_count = notifications.count()
    else:
        unseen_count = notifications.filter(request_date__gt=last_seen).count()
    
    data = [
        {
            "id": request.id,
            "product": request.product.name,
            "quantity": request.requested_quantity,
            "status": request.status,
            "date": request.request_date.strftime("%Y-%m-%d %H:%M")
        }
        for request in notifications
    ]
    
    return JsonResponse({
        "notifications": data,
        "unseen_count": unseen_count
    })

def mark_notifications_seen(request):
    request.session['notifications_last_seen'] = timezone.now().isoformat()
    return JsonResponse({"status": "success"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    if not hasattr(user, 'userprofile'):
        return Response({"detail": "User profile not found."}, status=403)

    org = user.userprofile.organization
    print(f"[DEBUG] User's organization: {org}")
    
    today = now().date()

    today_sales = Sale.objects.filter(
        sale_date__date=today, organization=org
    ).aggregate(total=Sum('sale_price'))['total'] or 0

    total_sales = Sale.objects.filter(
        organization=org
    ).aggregate(total=Sum('sale_price'))['total'] or 0

    stock_available = Stock.objects.filter(
        organization=org
    ).aggregate(total=Sum('quantity'))['total'] or 0

    sold_items = Sale.objects.filter(
        organization=org
    ).aggregate(total=Sum('quantity_sold'))['total'] or 0

    total_expenses = StockHistory.objects.filter(
        transaction_type='Restock', organization=org
    ).aggregate(total=Sum('total_revenue'))['total'] or 0

    active_stock = Stock.objects.filter(
        organization=org, quantity__gt=0
    ).count()

    data = {
        "today_sales": today_sales,
        "total_sales": total_sales,
        "stock_available": stock_available,
        "sold_items": sold_items,
        "total_expenses": total_expenses,
        "active_stock": active_stock,
    }

    serializer = DashboardStatsSerializer(data)
    return Response(serializer.data)

@api_view(['GET'])
def sales_stock_data(request):
    records = MonthlySalesStock.objects.all()
    data = {}
    for record in records:
        year = str(record.year)
        if year not in data:
            data[year] = []
        data[year].append({
            "month": record.month,
            "Sales": record.sales,
            "Stock": record.stock,
        })
        
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for year in data:
        data[year].sort(key=lambda x: month_order.index(x["month"]))

    return Response(data)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:5173'

def get_visible_investments(user):
    return Investment.objects.exclude(user=user).values('supplier__name', 'date_invested')

def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            if user.groups.filter(name__in=group_names).exists() or user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investor_view(request):
    suppliers = Supplier.objects.all()
    serializer = SupplierInvestmentSerializer(suppliers, many=True)
    return Response(serializer.data)

@login_required
@group_required("Financial Admin")
def financial_dashboard(request):
    total_sales = Sale.objects.aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    total_invested = Investment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawn = Withdrawal.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'dashboard/financial_admin.html', {
        'total_sales': total_sales,
        'total_invested': total_invested,
        'total_withdrawn': total_withdrawn
    })

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(organization=self.request.user.userprofile.organization)
    
class InvestmentPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get all investments for the user
        investments = Investment.objects.filter(user=user)
        if not investments.exists():
            return Response({"performance": [], "current_value": 0})

        # Get related monthly investment entries
        monthly_entries = MonthlyInvestment.objects.filter(investment__in=investments).order_by('month')
        if not monthly_entries.exists():
            return Response({"performance": [], "current_value": 0})

        # Normalize first investment date
        first_date = investments.earliest('date_invested').date_invested
        if isinstance(first_date, datetime.date) and not isinstance(first_date, datetime.datetime):
            first_date = datetime.datetime.combine(first_date, datetime.time.min)
        if timezone.is_naive(first_date):
            first_date = timezone.make_aware(first_date)
        first_date = first_date.date()  # Convert to date for compatibility with `entry.month`

        # Group data in 3-month intervals
        grouped = defaultdict(lambda: 0)
        for entry in monthly_entries:
            months_passed = (entry.month.year - first_date.year) * 12 + (entry.month.month - first_date.month)
            group = (months_passed // 3) + 1
            label = f"{(group - 1) * 3 + 1}-{group * 3}"
            grouped[label] += entry.value

        # Serialize grouped data
        performance_data = [{"label": label, "value": value} for label, value in sorted(grouped.items())]
        current_value = sum(investment.total_return() for investment in investments)

        return Response({
            "performance": InvestmentPerformanceSerializer(performance_data, many=True).data,
            "current_value": current_value
        })
    

class MyInvestmentView(generics.RetrieveAPIView):
    """
    GET /api/investments/me/
    Only Admins or Investors may hit this.
    Returns the single Investment object for the current user & org.
    """
    serializer_class = DetailedInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        role = get_user_role(user)
        print(f"[DEBUG] User role: {role}")
        print(f"[DEBUG] User: {user}")

        # 1) Role check
        if role not in ['Admin', 'Investor']:
            raise PermissionDenied("Your role does not allow viewing investments.")

        try:
            org_id = user.userprofile.organization.id
            print(f"[DEBUG] User's organization ID: {org_id}")
        except Exception:
            raise PermissionDenied("Your account is not tied to a valid organization.")

        # Fetch the most recent investment
        inv = Investment.objects.filter(user=user, organization_id=org_id).order_by('-date_invested').first()

        if not inv:
            raise NotFound("No investment found for your account.")
        
        print(f"[DEBUG] Investment found: {inv}")
        return inv

class FetchStockInvestments(generics.ListAPIView):
    serializer_class = DetailedInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)

        if role not in ['Admin', 'Investor']:
            raise PermissionDenied("Your role does not allow viewing investments.")

        try:
            org_id = user.userprofile.organization.id
        except Exception:
            raise PermissionDenied("Your account is not tied to a valid organization.")
        
        return Investment.objects.filter(user=user, organization_id=org_id).prefetch_related(
            'stock_investments__stock__product',
            'supplier'
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})  # <-- Wrap response

class InvestableStockListView(generics.ListAPIView):
    """
    GET /api/investable-stocks/
    Only Admins or Investors may access this.
    Returns stocks that are open for investment and belong to the user's organization.
    """
    serializer_class = InvestableStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = get_user_role(user)
        print(f"[DEBUG] User role: {role}")

        if role not in ['Admin', 'Investor']:
            raise PermissionDenied("Your role does not allow accessing investable stocks.")

        org_id = user.userprofile.organization.id

        print(f"[Debug] {Stock.objects.filter(organization_id=org_id, product__supplier__is_open_for_investment=True)}")
        # 2) Organization check
        return Stock.objects.filter(
            organization_id=org_id,
            product__supplier__is_open_for_investment=True
        )
    

class InvestInStockView(APIView):
    """
    POST /api/investments/invest-stock/
    Payload: { "stock_id": 1, "amount": 500.00 }
    Only Admins or Investors may perform this action.
    Creates a new Investment and links it to the Stock, unless one already exists.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        role = get_user_role(user)

        if role not in ['Admin', 'Investor']:
            raise PermissionDenied("Your role does not allow investing in stocks.")

        stock_id = request.data.get('stock_id')
        amount = request.data.get('amount')

        if not stock_id or amount is None:
            raise ValidationError("Both stock_id and amount are required.")

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValidationError("Amount must be greater than zero.")
        except (InvalidOperation, TypeError):
            raise ValidationError("Invalid amount format.")

        try:
            stock = Stock.objects.get(
                id=stock_id,
                product__supplier__is_open_for_investment=True
            )
        except Stock.DoesNotExist:
            raise NotFound("Stock not available for investment.")

        organization = user.userprofile.organization

        # Check if the user already invested in this stock
        already_invested = StockInvestment.objects.filter(
            investment__user=user,
            investment__organization=organization,
            stock=stock
        ).exists()

        if already_invested:
            raise ValidationError("You have already invested in this stock.")

        supplier = stock.product.supplier

        # Create new Investment and StockInvestment
        investment = Investment.objects.create(
            user=user,
            organization=organization,
            supplier=supplier,
            amount=amount,
            percentage_profit=10  # Placeholder logic
        )

        StockInvestment.objects.create(
            investment=investment,
            stock=stock
        )

        return Response({'message': f'Successfully invested {amount} in stock.'})


@login_required
def stock_investment_candlestick_data(request):
        organization = request.user.userprofile.organization  # assuming `User` has `organization` FK

        # Monthly investment stats
        monthly_data = (
            StockInvestment.objects.filter(stock__organization=organization)
            .annotate(month=TruncMonth("date_linked"))
            .values("month")
            .annotate(
                total_amount=Sum("investment__amount"),
                investors=Count("investment__user", distinct=True)
            )
            .order_by("month")
        )

        # Daily investment stats
        daily_data = (
            StockInvestment.objects.filter(stock__organization=organization)
            .annotate(day=TruncDay("date_linked"))
            .values("day")
            .annotate(
                total_amount=Sum("investment__amount"),
                investors=Count("investment__user", distinct=True)
            )
            .order_by("day")
        )
        print("Monthly data:", monthly_data)
        print("Daily data:", daily_data)
        return JsonResponse({
            "monthly_data": list(monthly_data),
            "daily_data": list(daily_data)
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_suppliers(request):
    """
    Returns recommended suppliers based on multiple criteria:
    1. Total sales volume
    2. Number of products
    3. Average product rating (if available)
    4. Investment opportunities (suppliers open for investment)
    5. Recent sales activity
    """
    # Get the organization from the current user's session
    organization = request.user.userprofile.organization
    
    # Define time periods for analysis
    today = now().date()
    thirty_days_ago = today - timedelta(days=30)
    ninety_days_ago = today - timedelta(days=90)
    
    # Get suppliers with their metrics
    suppliers = Supplier.objects.filter(organization=organization)
    
    # Prepare the response data
    recommended = []
    
    for supplier in suppliers:
        # Get recent sales data
        recent_sales = supplier.sales_in_period(start=thirty_days_ago)
        previous_period_sales = supplier.sales_in_period(
            start=ninety_days_ago,
            end=thirty_days_ago
        )
        
        # Calculate growth rate
        growth_rate = 0
        if previous_period_sales > 0:
            growth_rate = ((recent_sales - previous_period_sales) / previous_period_sales) * 100
        
        # Get product count
        product_count = supplier.products.count()
        
        # Calculate recommendation score (simple algorithm)
        # Higher scores indicate more recommended suppliers
        score = (
            (recent_sales * 0.5) +  # Recent sales have high weight
            (growth_rate * 0.3) +   # Growth rate has medium weight
            (product_count * 10) +  # More products is better
            (30 if supplier.is_open_for_investment else 0)  # Bonus for investment opportunities
        )
        
        # Add to recommended list
        recommended.append({
            'id': supplier.id,
            'name': supplier.name,
            'contact': supplier.contact,
            'email': supplier.email,
            'products_count': product_count,
            'recent_sales': recent_sales,
            'growth_rate': round(growth_rate, 2),
            'is_open_for_investment': supplier.is_open_for_investment,
            'total_investments': supplier.total_investments(),
            'total_amount_invested': float(supplier.total_amount_invested()),
            'score': score,
        })
    
    # Sort by score (descending)
    recommended.sort(key=lambda x: x['score'], reverse=True)
    
    return JsonResponse({
        'recommended_suppliers': recommended
    })

@login_required
@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_message_contacts(request):
    """Get list of users the current user has chatted with, including last message and unread count"""
    try:
        # Get the current user's profile
        user = request.user
        user_profile = user.userprofile
        organization = user_profile.organization
        
        # Get all conversations the user is involved in
        conversations = InvestorMessage.objects.filter(
            Q(sender=user) | Q(receiver=user),
            organization=organization
        ).values(
            'sender', 'receiver'
        ).annotate(
            last_message_time=Max('timestamp'),
            message_count=Count('id')
        ).order_by('-last_message_time')
        
        # Extract unique contacts from conversations
        contact_ids = set()
        for conv in conversations:
            contact_id = conv['receiver'] if conv['sender'] == user.id else conv['sender']
            contact_ids.add(contact_id)
        
        # Get all users in the organization (for starting new conversations)
        all_org_users = UserProfile.objects.filter(
            organization=organization
        ).exclude(
            user=user
        ).select_related('user')
        
        # Add additional users who haven't had conversations yet
        for profile in all_org_users:
            contact_ids.add(profile.user.id)
        
        # Get contact details
        contacts_data = []
        for contact_id in contact_ids:
            try:
                contact_user = User.objects.get(id=contact_id)
                contact_profile = UserProfile.objects.get(user=contact_user)
                
                # Get last message between users
                last_message = InvestorMessage.objects.filter(
                    Q(sender=user, receiver=contact_user) | 
                    Q(sender=contact_user, receiver=user),
                    organization=organization
                ).order_by('-timestamp').first()
                
                # Get unread message count
                unread_count = InvestorMessage.objects.filter(
                    sender=contact_user,
                    receiver=user,
                    organization=organization,
                    is_read=False
                ).count()
                
                contacts_data.append({
                    'id': contact_user.id,
                    'username': contact_user.username,
                    'full_name': f"{contact_user.first_name} {contact_user.last_name}".strip() or contact_user.username,
                    'role': contact_profile.role,
                    'avatar': contact_profile.avatar.url if contact_profile.avatar else None,
                    'last_message': last_message.message[:50] + '...' if last_message and len(last_message.message) > 50 else (last_message.message if last_message else None),
                    'last_message_time': last_message.timestamp.isoformat() if last_message else None,
                    'unread_count': unread_count,
                    'is_online': True  # This could be implemented with channels/websockets
                })
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                continue
        
        # Sort contacts by last message time (most recent first)
        contacts_data.sort(key=lambda x: x['last_message_time'] or "1970-01-01", reverse=True)
        
        return JsonResponse({'contacts': contacts_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_conversation(request, user_id):
    """Get message history between current user and specified user"""
    try:
        # Validate that the other user exists and is in the same organization
        try:
            other_user = User.objects.get(id=user_id)
            other_profile = UserProfile.objects.get(user=other_user)
            user_profile = request.user.userprofile
            
            if other_profile.organization.id != user_profile.organization.id:
                return JsonResponse({'error': 'User not in same organization'}, status=403)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        
        # Get all messages between the two users
        messages = InvestorMessage.objects.filter(
            (Q(sender=request.user, receiver=other_user) | 
             Q(sender=other_user, receiver=request.user)),
            organization=user_profile.organization
        ).order_by('timestamp')
        
        # Mark messages as read
        unread_messages = messages.filter(receiver=request.user, is_read=False)
        for message in unread_messages:
            message.is_read = True
            message.save()
        
        # Format messages for response
        messages_data = [{
            'id': message.id,
            'sender_id': message.sender.id,
            'receiver_id': message.receiver.id,
            'message': message.message,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read,
            'is_mine': message.sender == request.user
        } for message in messages]
        
        # Get user info for the other user
        other_user_data = {
            'id': other_user.id,
            'username': other_user.username,
            'full_name': f"{other_user.first_name} {other_user.last_name}".strip() or other_user.username,
            'role': other_profile.role,
            'avatar': other_profile.avatar.url if other_profile.avatar else None,
            'is_online': True  # This could be implemented with channels/websockets
        }
        
        return JsonResponse({
            'messages': messages_data,
            'user': other_user_data
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@ensure_csrf_cookie
@require_http_methods(["POST"])
def send_message(request, user_id):
    """Send a message to another user"""
    try:
        data = json.loads(request.body)
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Validate that the other user exists and is in the same organization
        try:
            other_user = User.objects.get(id=user_id)
            other_profile = UserProfile.objects.get(user=other_user)
            user_profile = request.user.userprofile
            
            if other_profile.organization.id != user_profile.organization.id:
                return JsonResponse({'error': 'User not in same organization'}, status=403)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        
        # Create the message
        message = InvestorMessage.objects.create(
            organization=user_profile.organization,
            sender=request.user,
            receiver=other_user,
            message=message_text,
            is_read=False
        )
        
        # Format response
        message_data = {
            'id': message.id,
            'sender_id': message.sender.id,
            'receiver_id': message.receiver.id,
            'message': message.message,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read,
            'is_mine': True
        }
        
        return JsonResponse({'message': message_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


class UserProfileView(generics.RetrieveAPIView):
    """
    Get the current user's profile information
    """
    permission_classes = [IsAuthenticated]
    from .serializers import UserProfileDetailSerializer  # Ensure this import exists at the top of the file
    serializer_class = UserProfileDetailSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        profile_serializer = UserProfileSerializer(user.userprofile)
        
        return Response({
            'user': serializer.data,
            'profile': profile_serializer.data
        })


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Update the current user's profile
    """
    permission_classes = [IsAuthenticated]
    from .serializers import UserProfileUpdateSerializer  # Ensure this import exists at the top of the file
    serializer_class = UserProfileUpdateSerializer
    
    def get_object(self):
        return self.request.user.userprofile
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return updated user and profile data
        user_serializer = UserSerializer(self.request.user)
        profile_serializer = UserProfileSerializer(instance)
        
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        })


class OrganizationMembersView(generics.ListAPIView):
    """
    List all members of the user's organization
    """
    permission_classes = [IsAuthenticated]
    from .serializers import UserMemberSerializer  # Ensure this import exists at the top of the file
    serializer_class = UserMemberSerializer
    
    def get_queryset(self):
        user = self.request.user
        try:
            organization = user.userprofile.organization
            return User.objects.filter(userprofile__organization=organization)
        except:
            return User.objects.none()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            from .serializers import MessageCreateSerializer
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Check if user role allows messaging
        role = get_user_role(user)
        if role not in ['Admin', 'Investor']:
            return ChatMessage.objects.none()
            
        return ChatMessage.objects.filter(
            organization=user.userprofile.organization
        ).filter(
            # Get messages where user is sender or receiver
            sender=user
        ) | ChatMessage.objects.filter(
            receiver=user
        ).order_by('-timestamp')
    
    def perform_create(self, serializer):
        role = get_user_role(self.request.user)
        
        # Only Admin and Investor can send messages
        if role not in ['Admin', 'Investor']:
            return Response(
                {"detail": "You don't have permission to send messages."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer.save(sender=self.request.user)


class StockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for stock history
    """
    serializer_class = StockHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        role = get_user_role(self.request.user)
        if role not in ['Admin', 'Financial Admin', 'Inventory Manager', 'Investor']:
            return StockHistory.objects.none()

        return StockHistory.objects.filter(
            organization=self.request.user.userprofile.organization
        ).order_by('-transaction_date')


def get_user_role(user):
    """Helper function to get user role"""
    try:
        return user.userprofile.role
    except Exception:
        return None