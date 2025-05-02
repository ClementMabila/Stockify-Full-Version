from django.urls import path
from . import views
from .views import get_notifications, FetchStockInvestments, MyInvestmentView, CustomerViewSet, GoogleLogin, sales_stock_data, dashboard_stats, mark_notifications_seen, StockAlertViewSet, SupplierViewSet,  send_invitation, verify_otp, register_from_invite, UploadCSVView, UploadProductCSVView, export_products_to_csv, SalesEntryViewSet, StockHistoryViewSet, InventoryViewSet, UserRegistrationAndOrganizationCreateView, InvestmentPerformanceView, InvestableStockListView, InvestInStockView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stock-alerts', StockAlertViewSet, basename='stock-alert')
router.register(r'sales-entries', SalesEntryViewSet, basename='sales-entry')
router.register(r'stock-history', StockHistoryViewSet, basename='stock-history')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('api/register-and-create-organization/', UserRegistrationAndOrganizationCreateView.as_view(), name='register_and_create_organization'),
    path('api/set-csrf-token/', views.set_csrf_token, name='set_csrf_token'),
    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_request, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/get_user_info', views.get_user_info, name='get_user_info'),
    path('api/register/<str:token>/', register_from_invite, name='register_from_invite'),
    path('api/', include(router.urls)),
    path('api/upload-csv/', UploadCSVView.as_view(), name='upload-csv'),
    path('export_products_to_csv/', export_products_to_csv, name='export_products_to_csv'),
    path('api/upload-product-csv/', UploadProductCSVView.as_view(), name='upload-product-csv'),
    path('api/export_products_to_csv/', views.export_products_to_csv, name='export_products_to_csv'),
    path("api/send-invitation/", send_invitation, name="send_invitation"),
    path("api/fetch-stock-investments/", FetchStockInvestments.as_view(), name='fetch-stock-investments'),
    path("api/register-from-invite/<str:token>/", register_from_invite, name="register_from_invite"),
    path("api/verify-otp/", verify_otp, name="verify_otp"),
    path('api/get-email-from-token/<uuid:token>/', views.get_email_from_token, name='get_email_from_token'),
    path('generate-invite-url/', views.generate_invite_url, name='generate_invite_url'),
    path("api/generate-invite-url/", views.generate_invite_url, name="generate_invite_url"),
    path('api/notifications/', get_notifications, name="get_notifications"),
    path('api/investment-performance/', InvestmentPerformanceView.as_view(), name='investment-performance'),
    path('api/mark-notifications-seen/', mark_notifications_seen, name="mark_notifications_seen"),
    path('api/dashboard-stats/', dashboard_stats, name='dashboard_stats'),
    path('api/sales-stock/', sales_stock_data, name='sales_stock_data'),
    path('api/groups/', views.get_groups, name='get_user_groups'),
    path('api/current-user/', views.current_user_api, name='get_current_user'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/investments/me/', MyInvestmentView.as_view(), name='investment-me'),
    path('api/investable-stocks/', InvestableStockListView.as_view()),
    path('api/investments/invest-stock/', InvestInStockView.as_view()),
    path('api/stock-candlestick-data/', views.stock_investment_candlestick_data, name='stock_candlestick_data'),
    path('api/recommended_suppliers/', views.recommended_suppliers, name='recommended_suppliers'),
    path('api/messages/contacts/', views.get_message_contacts, name='get_message_contacts'),
    path('api/messages/conversation/<int:user_id>/', views.get_conversation, name='get_conversation'),
    path('api/messages/send/<int:user_id>/', views.send_message, name='send_message'),
    path('api/user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/user/profile/update/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    
    # Organization related endpoints
    path('api/organization/members/', views.OrganizationMembersView.as_view(), name='organization-members'),
    
]