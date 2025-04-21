from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class Landscape(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name of the landscape"
    )
    
    description = models.TextField(
        help_text="Description of the landscape"
    )
    
    image_url = models.URLField(
        max_length=1000,
        validators=[URLValidator()],
        help_text="URL of the landscape image"
    )
    
    s3_image_url = models.URLField(max_length=1000, blank=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Landscape'
        verbose_name_plural = 'Landscapes'

    def __str__(self):
        return self.name

    def clean(self):
        if not self.name.strip():
            raise ValidationError({'name': 'Name cannot be empty'})
        
        if not self.description.strip():
            raise ValidationError({'description': 'Description cannot be empty'})
        
        try:
            URLValidator()(self.image_url)
        except ValidationError:
            raise ValidationError({'image_url': 'Invalid URL format'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ImportHistory(models.Model):
    file_name = models.CharField(
        max_length=255
    )
    
    date_imported = models.DateTimeField(
        auto_now_add=True
    )
    
    successful_records = models.PositiveIntegerField(
        default=0
    )
    
    failed_records = models.PositiveIntegerField(
        default=0
    )
    
    error_log = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['-date_imported']
        verbose_name = 'Import History'
        verbose_name_plural = 'Import Histories'

    def __str__(self):
        return f"{self.file_name} ({self.date_imported.strftime('%Y-%m-%d %H:%M')})"