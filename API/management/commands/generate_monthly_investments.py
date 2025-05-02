# management/commands/generate_monthly_investments.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from API.models import Investment, MonthlyInvestment
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Generate monthly investment profit entries'

    def handle(self, *args, **options):
        today = timezone.now().date()
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - relativedelta(months=1)

        for investment in Investment.objects.all():
            # Skip if the investment was made after last month
            if investment.date_invested.date() > last_month:
                continue

            profit = investment.amount * (investment.percentage_profit / 100)

            # Avoid duplicate entries
            if not MonthlyInvestment.objects.filter(investment=investment, month=last_month).exists():
                MonthlyInvestment.objects.create(
                    organization=investment.organization,
                    investment=investment,
                    month=last_month,
                    value=profit
                )
                self.stdout.write(f"Recorded {profit} for {investment} in {last_month}")
