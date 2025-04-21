import pytest
from django.core.management import call_command
from gallery.utils.s3_handler import S3Handler
from gallery.utils.image_handler import ImageHandler

@pytest.mark.django_db
class TestIntegration:
    @pytest.fixture
    def setup_handlers(self):
        return {
            's3_handler': S3Handler(),
            'image_handler': ImageHandler()
        }

    def test_full_import_process(self, tmp_path, sample_csv_content, setup_handlers):
        # Create test CSV
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(sample_csv_content)

        # Run import
        call_command('import_landscapes', str(csv_file))

        # Check results
        from gallery.models import Landscape, ImportHistory
        
        # Verify landscapes were created
        landscapes = Landscape.objects.all()
        assert landscapes.count() == 2
        
        # Verify import history
        history = ImportHistory.objects.first()
        assert history.successful_records == 2
        assert history.failed_records == 0

        # Verify S3 URLs
        for landscape in landscapes:
            assert landscape.s3_image_url.startswith('https://')
            assert '.s3.' in landscape.s3_image_url