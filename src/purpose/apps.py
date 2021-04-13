from django.apps import AppConfig


class PurposeConfig(AppConfig):
    name = "src.purpose"

    def ready(self):
        from . import signals
