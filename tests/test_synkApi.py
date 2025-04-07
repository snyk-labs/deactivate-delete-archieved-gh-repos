import unittest
from unittest.mock import patch, Mock
from utils.synkApi import get_snyk_targets, get_snyk_projects_by_target_id, deactivate_project, delete_project

class TestSynkApi(unittest.TestCase):

    @patch('utils.synkApi.snyk_rest_endpoint')
    def test_get_snyk_targets(self, mock_snyk_rest_endpoint):
        mock_snyk_rest_endpoint.return_value = {"data": [{"id": "1", "attributes": {"url": "https://example.com"}}]}
        result = get_snyk_targets("tenant", "orgId")
        self.assertEqual(result, {"data": [{"id": "1", "attributes": {"url": "https://example.com"}}]})

    @patch('utils.synkApi.snyk_rest_endpoint')
    def test_get_snyk_projects_by_target_id(self, mock_snyk_rest_endpoint):
        mock_snyk_rest_endpoint.return_value = {"data": [{"id": "1", "attributes": {"name": "Project1"}}]}
        result = get_snyk_projects_by_target_id("tenant", "orgId", "targetId")
        self.assertEqual(result, {"data": [{"id": "1", "attributes": {"name": "Project1"}}]})

    @patch('utils.synkApi.snyk_rest_endpoint')
    def test_deactivate_project(self, mock_snyk_rest_endpoint):
        mock_snyk_rest_endpoint.return_value = 200
        result = deactivate_project("tenant", "orgId", "projectId")
        self.assertEqual(result, 200)

    @patch('utils.synkApi.snyk_rest_endpoint')
    def test_delete_project(self, mock_snyk_rest_endpoint):
        mock_snyk_rest_endpoint.return_value = 204
        result = delete_project("tenant", "orgId", "projectId")
        self.assertEqual(result, 204)

if __name__ == '__main__':
    unittest.main() 