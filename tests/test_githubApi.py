import unittest
from unittest.mock import patch, Mock
from utils.githubApi import get_archived_repos_urls

class TestGithubApi(unittest.TestCase):

    @patch('utils.githubApi.requests.get')
    def test_get_archived_repos_urls(self, mock_get):
        # Mock response for the GitHub API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"html_url": "https://github.com/org/repo1", "archived": True},
            {"html_url": "https://github.com/org/repo2", "archived": False},
            {"html_url": "https://github.com/org/repo3", "archived": True}
        ]
        mock_get.return_value = mock_response

        # Call the function
        archived_repos = get_archived_repos_urls("org", "fake_token")

        # Assert the results
        self.assertEqual(len(archived_repos), 2)
        self.assertIn("https://github.com/org/repo1", archived_repos)
        self.assertIn("https://github.com/org/repo3", archived_repos)

if __name__ == '__main__':
    unittest.main() 