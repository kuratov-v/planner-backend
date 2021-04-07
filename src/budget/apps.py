from django.apps import AppConfig


class BudgetConfig(AppConfig):
    name = 'src.budget'

    def ready(self):
        from . import signals
