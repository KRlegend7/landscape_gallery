import pytest
from unittest.mock import patch, Mock
from gallery.utils.image_handler import ImageHandler
from PIL import Image
from io import BytesIO

class TestImageHandler:
    @pytest.fixture
    def image_handler(self):
        return ImageHandler()

    @pytest.fixture
    def mock_image(self):
        # Create a small test image
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io

    def test_generate_filename(self, image_handler):
        filename = image_handler.generate_filename()
        assert filename.startswith('landscapes/')
        assert filename.endswith('.jpg')
        assert len(filename) > 20  # UUID should make it long enough

    @patch('requests.get')
    def test_download_image(self, mock_get, image_handler, mock_image):
        mock_response = Mock()
        mock_response.content = mock_image.getvalue()
        mock_get.return_value = mock_response

        result = image_handler.download_image('https://example.com/test.jpg')
        assert isinstance(result, BytesIO)

    def test_process_image(self, image_handler, mock_image):
        result = image_handler.process_image(mock_image)
        assert isinstance(result, BytesIO)

        # Verify the processed image
        img = Image.open(result)
        assert img.mode == 'RGB'
        assert img.size[0] <= image_handler.max_size[0]
        assert img.size[1] <= image_handler.max_size[1]