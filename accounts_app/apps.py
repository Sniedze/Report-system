from django.apps import AppConfig


class AccountsAppConfig(AppConfig):
    name = 'accounts_app'

    def ready(self):
        import accounts_app.signals

