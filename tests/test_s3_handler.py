import pytest
from unittest.mock import Mock, patch
from gallery.utils.s3_handler import S3Handler
from botocore.exceptions import ClientError

class TestS3Handler:
    @pytest.fixture
    def s3_handler(self):
        return S3Handler()

    @patch('boto3.client')
    def test_successful_upload(self, mock_boto3_client, s3_handler, mock_s3_response):
        # Mock the S3 client
        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.upload_fileobj.return_value = mock_s3_response

        # Test file upload
        file_obj = Mock()
        result = s3_handler.upload_file(file_obj, 'test.jpg')
        
        assert 's3.example.com' in result
        assert mock_s3.upload_fileobj.called

    @patch('boto3.client')
    def test_upload_failure(self, mock_boto3_client, s3_handler):
        # Mock S3 client to raise an error
        mock_s3 = Mock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.upload_fileobj.side_effect = ClientError(
            {'Error': {'Code': '403', 'Message': 'Access Denied'}},
            'upload_fileobj'
        )

        with pytest.raises(ClientError):
            s3_handler.upload_file(Mock(), 'test.jpg')