import unittest
from unittest.mock import patch
from utils.tokenReader import get_snyk_token, get_github_token, get_gitlab_token

class TestHelper(unittest.TestCase):

    @patch('utils.helper.os.environ.get')
    def test_get_snyk_token(self, mock_get):
        mock_get.return_value = "12345678-1234-1234-1234-123456789012"
        token = get_snyk_token()
        self.assertEqual(token, "12345678-1234-1234-1234-123456789012")

    @patch('utils.helper.os.environ.get')
    def test_get_github_token(self, mock_get):
        mock_get.return_value = "ghp_123456789012345678901234567890123456"
        token = get_github_token()
        self.assertEqual(token, "ghp_123456789012345678901234567890123456")

    @patch('utils.helper.os.environ.get')
    def test_get_gitlab_token(self, mock_get):
        mock_get.return_value = "glpat-12345678901234567890"
        token = get_gitlab_token()
        self.assertEqual(token, "glpat-12345678901234567890")

if __name__ == '__main__':
    unittest.main() 