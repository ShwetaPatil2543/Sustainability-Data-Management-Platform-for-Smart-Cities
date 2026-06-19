from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F

from emissions.models import CarbonEmission


class Command(BaseCommand):
    help = "Backfill `total_emission` for CarbonEmission records in batches."

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=1000, help='Number of records to process per batch')

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        qs = CarbonEmission.objects.filter(total_emission__isnull=True).order_by('id')
        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS('No records to backfill.'))
            return

        self.stdout.write(f'Starting backfill of {total} records (batch size {batch_size})...')
        processed = 0
        while True:
            ids = list(qs.values_list('id', flat=True)[:batch_size])
            if not ids:
                break
            with transaction.atomic():
                CarbonEmission.objects.filter(id__in=ids).update(
                    total_emission=(F('co2_emission') + F('methane_emission') + F('nitrous_oxide'))
                )
            processed += len(ids)
            self.stdout.write(f'Processed {processed}/{total}...')

        self.stdout.write(self.style.SUCCESS(f'Backfill completed. Processed {processed} records.'))
