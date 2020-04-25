from django.apps import AppConfig


class AccountsAppConfig(AppConfig):
    name = 'accounts_app'

    def ready(self):
        from .signals import create_user_profile

