import pytest
from django.core.exceptions import ValidationError
from gallery.models import Landscape, ImportHistory

@pytest.mark.django_db
class TestLandscapeModel:
    def test_create_valid_landscape(self):
        landscape = Landscape.objects.create(
            name="Mountain",
            description="Beautiful mountain scenery",
            image_url="https://example.com/image.jpg"
        )
        assert landscape.name == "Mountain"
        assert landscape.description == "Beautiful mountain scenery"
        assert landscape.image_url == "https://example.com/image.jpg"

    def test_empty_name(self):
        with pytest.raises(ValidationError):
            Landscape.objects.create(
                name="",
                description="Test description",
                image_url="https://example.com/image.jpg"
            )

    def test_empty_description(self):
        with pytest.raises(ValidationError):
            Landscape.objects.create(
                name="Test",
                description="",
                image_url="https://example.com/image.jpg"
            )

    def test_invalid_url(self):
        with pytest.raises(ValidationError):
            Landscape.objects.create(
                name="Test",
                description="Test description",
                image_url="invalid-url"
            )

    def test_duplicate_name(self):
        Landscape.objects.create(
            name="Mountain",
            description="Test description",
            image_url="https://example.com/image.jpg"
        )
        with pytest.raises(ValidationError):
            Landscape.objects.create(
                name="Mountain",
                description="Another description",
                image_url="https://example.com/image2.jpg"
            )