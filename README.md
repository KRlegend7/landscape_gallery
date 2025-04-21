# ```markdown
# Landscape Gallery

A Django application for managing landscape images with AWS S3 integration and CSV import functionality. Features include OAuth authentication, automated image processing, and comprehensive testing.

## Features
- OAuth authentication with Google
- CSV file import for landscape data
- Automatic image upload to AWS S3
- Image processing and optimization
- Docker containerization
- Comprehensive test coverage

## Prerequisites
- Python 3.10+
- Docker and Docker Compose
- AWS Account with S3 access
- Google OAuth credentials

## Quick Start

1. Clone and Setup:
```bash
# Clone repository
git clone <repository-url>
cd landscape_gallery

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS

# Install dependencies
pip install -r requirements.txt
```

2. Configure Environment:
Create `.env` file in project root:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Google OAuth
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret

# AWS Settings
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

3. Run with Docker:
```bash
# Build and start containers
docker-compose up --build

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Configuration

### AWS S3 Setup
1. Create S3 bucket with public access
2. Configure CORS settings
3. Create IAM user with S3 access
4. Get access credentials

### Google OAuth Setup
1. Go to Google Cloud Console
2. Create new project
3. Configure OAuth consent screen
4. Create OAuth 2.0 credentials
5. Add redirect URIs:
   - http://localhost:8000/social-auth/complete/google-oauth2/
   - http://127.0.0.1:8000/social-auth/complete/google-oauth2/

## Usage

### CSV Import
Format your CSV file:
```csv
name,description,image_url
Mountain,"Beautiful mountain scenery","https://example.com/mountain.jpg"
Ocean,"Calm ocean view","https://example.com/ocean.jpg"
```

Run import:
```bash
python manage.py import_landscapes your_file.csv
```

### Development Server
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Testing

Run tests:
```bash
# All tests
pytest

# Specific test file
pytest tests/test_models.py

# With coverage
coverage run -m pytest
coverage report
```

Test Structure:
- `test_models.py`: Database model tests
- `test_s3_handler.py`: AWS S3 integration tests
- `test_image_handler.py`: Image processing tests
- `test_import_command.py`: CSV import command tests
- `test_integration.py`: End-to-end integration tests

## Project Structure
```
landscape_gallery/
├── core/                 # Project settings
├── gallery/             # Main application
│   ├── management/      # Management commands
│   ├── migrations/      # Database migrations
│   ├── templates/       # HTML templates
│   ├── utils/           # Utility functions
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   └── admin.py         # Admin interface
├── tests/               # Test suite
├── static/              # Static files
├── templates/           # Global templates
├── .env                 # Environment variables
├── docker-compose.yml   # Docker configuration
├── Dockerfile          # Docker build file
└── requirements.txt    # Python dependencies
```

## Models

### Landscape
- `name`: CharField(max_length=200)
- `description`: TextField
- `original_image_url`: URLField
- `s3_image_url`: URLField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

### ImportHistory
- `file_name`: CharField
- `date_imported`: DateTimeField
- `successful_records`: IntegerField
- `failed_records`: IntegerField
- `error_log`: TextField

## Security Considerations

1. Environment Variables
   - Keep sensitive data in .env
   - Never commit credentials

2. AWS Security
   - Use minimal IAM permissions
   - Enable bucket encryption
   - Configure CORS properly

3. Authentication
   - OAuth2 implementation
   - Session security
   - CSRF protection

## Performance Features

1. Image Processing
   - Automatic resizing
   - Format optimization
   - Quality compression

2. Database
   - Indexed fields
   - Efficient queries
   - Proper relationships

## Error Handling
- CSV validation
- Image processing errors
- S3 upload issues
- Authentication errors
- Detailed error logging

## Future Improvements

1. Features
   - Bulk export
   - Image categories
   - User roles
   - API endpoints

2. Technical
   - Async processing
   - Caching
   - Rate limiting
   - WebSocket notifications

3. Infrastructure
   - CI/CD pipeline
   - Monitoring
   - Backup strategy
   - Load balancing

## Troubleshooting

Common Issues:
1. S3 Upload Failures
   - Check AWS credentials
   - Verify bucket permissions
   - Confirm CORS settings

2. OAuth Errors
   - Verify redirect URIs
   - Check consent screen setup
   - Confirm credentials

3. Image Processing
   - Check file permissions
   - Verify memory limits
   - Confirm file types

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
MIT License - see LICENSE file

## Support
Create issue or contact Kearamirezgu@unal.edu.co
```
