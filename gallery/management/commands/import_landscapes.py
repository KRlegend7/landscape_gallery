import csv
import os
from django.core.management.base import BaseCommand, CommandError
from gallery.models import Landscape, ImportHistory
from gallery.utils import S3ImageUploader
from django.db import transaction

class Command(BaseCommand):
    help = 'Import landscapes from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        successful_records = 0
        failed_records = 0
        error_log = []

        # Check if file exists
        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Validate headers
                required_fields = {'name', 'description', 'image_url'}
                if not required_fields.issubset(set(reader.fieldnames)):
                    raise CommandError(
                        f'Missing required fields. Required: {required_fields}'
                    )

                # Create import history record
                import_history = ImportHistory.objects.create(
                    file_name=file_path
                )

                # Process records
                for row_num, row in enumerate(reader, start=2):
                    try:
                        Landscape.objects.create(
                            name=row['name'].strip(),
                            description=row['description'].strip(),
                            image_url=row['image_url'].strip()
                        )
                        successful_records += 1
                    except Exception as e:
                        failed_records += 1
                        error_log.append(f'Row {row_num}: {str(e)}')

                # Update import history
                import_history.successful_records = successful_records
                import_history.failed_records = failed_records
                import_history.error_log = '\n'.join(error_log)
                import_history.save()

                # Report results
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Import completed. Success: {successful_records}, Failed: {failed_records}'
                    )
                )
                
                if error_log:
                    self.stdout.write(self.style.WARNING('\nErrors:'))
                    for error in error_log:
                        self.stdout.write(self.style.WARNING(error))
                        
        s3_uploader = S3ImageUploader()

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Validate headers
                required_fields = {'name', 'description', 'image_url'}
                if not required_fields.issubset(set(reader.fieldnames)):
                    self.stderr.write(f'Missing required fields. Required: {required_fields}')
                    return

                import_history = ImportHistory.objects.create(
                    file_name=file_path
                )

                for row_num, row in enumerate(reader, start=2):
                    try:
                        with transaction.atomic():
                            # Upload image to S3
                            s3_url = s3_uploader.process_image_url(row['image_url'])

                            # Create landscape record
                            Landscape.objects.create(
                                name=row['name'].strip(),
                                description=row['description'].strip(),
                                original_image_url=row['image_url'].strip(),
                                s3_image_url=s3_url
                            )
                            successful_records += 1
                            self.stdout.write(f"Processed row {row_num}: {row['name']}")

                    except Exception as e:
                        failed_records += 1
                        error_message = f"Error in row {row_num}: {str(e)}"
                        error_log.append(error_message)
                        self.stderr.write(error_message)

                # Update import history
                import_history.successful_records = successful_records
                import_history.failed_records = failed_records
                import_history.error_log = '\n'.join(error_log)
                import_history.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Import completed. Success: {successful_records}, Failed: {failed_records}'
                    )
                )


        except Exception as e:
            raise CommandError(f'Error processing file: {str(e)}')