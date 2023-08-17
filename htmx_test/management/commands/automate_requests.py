# automate_requests.py

from django.core.management.base import BaseCommand

import logging


class Command(BaseCommand):
    help = 'Automatically send requests to an external API'

    def handle(self, *args, **options):
        logger = logging.getLogger('django_cronjob')
        logger.info('Cron job started')
        import time
        time.sleep(2.5)
        # Your cron job logic here
        self.stdout.write(self.style.SUCCESS('Automated requests complete vcvbgghhghfgfdfgf'))
        logger.info('Cron job finished')


