import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for db')
        db_conn = None
        max_retries = 30
        
        for _ in range(max_retries):
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database is available'))
                return
            except OperationalError:
                time.sleep(1)
        
        self.stdout.write(self.style.ERROR('Database is not available after 30 seconds'))
        return OperationalError('Could not connect to database')