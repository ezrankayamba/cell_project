from django.apps import AppConfig


class CellConfig(AppConfig):
    name = 'cell'

    def ready(self):
        import cell.signals
