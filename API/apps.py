from django.apps import AppConfig
from django.db.utils import ProgrammingError, OperationalError

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API'

    def ready(self):
        # Import signals
        import API.signals
        
        # Try to create groups, but fail gracefully if tables don't exist
        try:
            self.create_groups()
        except (ProgrammingError, OperationalError):
            # Tables don't exist yet, skip group creation
            pass

    def create_groups(self):
        """Ensure the required groups are created."""
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name="Admin")
        Group.objects.get_or_create(name="Investor")
        Group.objects.get_or_create(name="Supplier")
        Group.objects.get_or_create(name="Financial Admin")