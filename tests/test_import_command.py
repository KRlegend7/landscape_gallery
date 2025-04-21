import pytest
from django.core.management import call_command
from io import StringIO
from django.core.management.base import CommandError

@pytest.mark.django_db
class TestImportCommand:
    def test_successful_import(self, tmp_path, sample_csv_content):
        # Create temporary CSV file
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(sample_csv_content)

        # Capture output
        out = StringIO()
        call_command('import_landscapes', str(csv_file), stdout=out)

        # Check database
        from gallery.models import Landscape, ImportHistory
        assert Landscape.objects.count() == 2
        assert ImportHistory.objects.count() == 1

        # Check output
        output = out.getvalue()
        assert "Import completed" in output
        assert "Success: 2" in output

    def test_invalid_csv_format(self, tmp_path, invalid_csv_content):
        # Create temporary CSV file with invalid format
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_text(invalid_csv_content)

        with pytest.raises(ValueError) as exc_info:
            call_command('import_landscapes', str(csv_file))
        
        assert "Missing required fields" in str(exc_info.value)

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            call_command('import_landscapes', 'nonexistent.csv')