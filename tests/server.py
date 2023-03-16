import io
from typing import List, Dict
import unittest
from unittest.mock import patch, MagicMock
from unittest import mock, TestCase

import boto3
from fastapi.testclient import TestClient

from src.server import app
from src.models import ModelTable
from src.server import ModelUpdateRequest

s3 = boto3.resource('s3')
bucket_name = 'my-model-bucket'


class TestReadModelById(unittest.TestCase):

    @mock.patch('app.read_model_by_id')
    def test_read_model_by_id_success(self, mock_read_model_by_id):
        """
        Test read_model_by_id function successfully returns a model when given a valid model id.
        """
        # Define a model dictionary
        model_dict: Dict[str, str] = {
            "id": "1",
            "name": "model1",
            "description": "This is model 1",
            "created_at": "2023-03-15T12:00:00.000Z"
        }
        # Convert the model dictionary to a Model object
        model_obj: ModelTable = ModelTable(**model_dict)

        # Set up mock return value for read_model_by_id function
        mock_read_model_by_id.return_value = model_obj

        # Call the read_model_by_id function with the valid model id
        response = app.test_client().get('/models/1')

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response data is the expected model dictionary
        self.assertEqual(response.json, model_dict)

    @mock.patch('app.read_model_by_id')
    def test_read_model_by_id_not_found(self, mock_read_model_by_id):
        """
        Test read_model_by_id function returns a 404 Not Found error when given an invalid model id.
        """
        # Set up mock return value for read_model_by_id function
        mock_read_model_by_id.return_value = None

        # Call the read_model_by_id function with an invalid model id
        response = app.test_client().get('/models/invalid_id')

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, 404)

        # Assert that the response data is the expected error message
        self.assertEqual(response.json, {"error": "Model not found"})


class TestUpdateModelById(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.model_id = "1"
        self.update_fields = {
            "name": "updated_model",
            "description": "updated description",
            "tags": ["updated_tag1", "updated_tag2"]
        }
        self.request = ModelUpdateRequest(**self.update_fields)
        self.credentials = ("user", "password")
        self.url = f"/models/{self.model_id}"

    @mock.patch("app.routes.models.update_model")
    def test_update_model_by_id_success(self, mock_update_model):
        mock_update_model.return_value = {
            "id": self.model_id,
            "name": self.update_fields["name"],
            "description": self.update_fields["description"],
            "tags": self.update_fields["tags"]
        }

        response = self.client.put(
            self.url,
            json=self.update_fields,
            auth=self.credentials
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_update_model.return_value["attribute_values"])
        mock_update_model.assert_called_once_with(self.model_id, self.update_fields)

    @mock.patch("app.routes.models.update_model")
    def test_update_model_by_id_not_found(self, mock_update_model):
        mock_update_model.return_value = None

        response = self.client.put(
            self.url,
            json=self.update_fields,
            auth=self.credentials
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Model not found"})
        mock_update_model.assert_called_once_with(self.model_id, self.update_fields)

    def test_update_model_by_id_unauthorized(self):
        response = self.client.put(
            self.url,
            json=self.update_fields,
            auth=("wrong_user", "wrong_password")
        )

        self.assertEqual(response.status_code, 401)


class TestDeleteModelById(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.model_id = "123"

    @mock.patch("app.api.delete_model")
    @mock.patch("app.api.read_model")
    def test_delete_model_by_id_success(self, mock_read_model, mock_delete_model):
        # Mock dependencies
        mock_read_model.return_value = ModelTable(self.model_id, "model_name", "model_description", ["tag1", "tag2"])
        mock_delete_model.return_value = None

        # Make request
        response = self.client.delete(f"/models/{self.model_id}",
                                       headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": self.model_id, "name": "model_name",
                                            "description": "model_description", "tags": ["tag1", "tag2"]})

        # Verify dependencies
        mock_read_model.assert_called_once_with(self.model_id)
        mock_delete_model.assert_called_once_with(self.model_id)

    @mock.patch("app.api.read_model")
    def test_delete_model_by_id_not_found(self, mock_read_model):
        # Mock dependency
        mock_read_model.return_value = None

        # Make request
        response = self.client.delete(f"/models/{self.model_id}",
                                       headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})

        # Verify response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Model not found"})

        # Verify dependency
        mock_read_model.assert_called_once_with(self.model_id)

    def test_delete_model_by_id_unauthorized(self):
        # Make request
        response = self.client.delete(f"/models/{self.model_id}")

        # Verify response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})


class TestStoreArtefact(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.model_id = "test_model"

    def test_store_artefact_success(self):
        with mock.patch('app.api.api_v1.endpoints.store_artefact') as mock_store_artefact:
            # Mock successful store_artefact function call
            mock_store_artefact.return_value = {"message": f"Artefact {self.model_id}/artefact uploaded successfully"}

            # Send POST request to store the artefact
            response = self.client.post(f"/models/{self.model_id}/artefact", files={"artefact": ("test_artefact.txt", b"test artefact content")})

            # Verify that the artefact was successfully stored and that the response message matches the expected message
            mock_store_artefact.assert_called_once_with(s3, bucket_name, f"{self.model_id}/artefact", mock.ANY)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": f"Artefact {self.model_id}/artefact uploaded successfully"})

    def test_store_artefact_failure(self):
        with mock.patch('app.api.api_v1.endpoints.store_artefact') as mock_store_artefact:
            # Mock failed store_artefact function call
            mock_store_artefact.side_effect = Exception("Error storing artefact")

            # Send POST request to store the artefact
            response = self.client.post(f"/models/{self.model_id}/artefact", files={"artefact": ("test_artefact.txt", b"test artefact content")})

            # Verify that the artefact was not stored and that an HTTPException with status code 500 was raised
            mock_store_artefact.assert_called_once_with(s3, bucket_name, f"{self.model_id}/artefact", mock.ANY)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Error storing artefact"})


class TestRetrieveArtefact(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch.object(boto3.S3Bucket, 'retrieve_artefact')
    def test_retrieve_artefact_success(self, mock_retrieve_artefact):
        # Arrange
        model_id = "my_model"
        expected_artefact_data = b'artefact data'
        mock_file = MagicMock(spec=io.BytesIO)
        mock_file.read.return_value = expected_artefact_data
        mock_retrieve_artefact.return_value = mock_file

        # Act
        response = self.client.get(f"/models/{model_id}/artefact")

        # Assert
        assert response.status_code == 200
        assert response.content == expected_artefact_data
        mock_retrieve_artefact.assert_called_once_with(boto3.S3Bucket(), "bucket-name", f"{model_id}/artefact")

    @patch.object(boto3.S3Bucket, 'retrieve_artefact')
    def test_retrieve_artefact_not_found(self, mock_retrieve_artefact):
        # Arrange
        model_id = "my_model"
        mock_retrieve_artefact.return_value = None

        # Act
        response = self.client.get(f"/models/{model_id}/artefact")

        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Model artefact not found"}
        mock_retrieve_artefact.assert_called_once_with(boto3.S3Bucket(), "bucket-name", f"{model_id}/artefact")
