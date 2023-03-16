from unittest.mock import patch, MagicMock, TestCase

from src.storage import retrieve_artefact, store_artefact


class TestStoreArtefact(TestCase):

    def setUp(self):
        self.model_id = 'test-model'
        self.artefact_file_path = '/path/to/artefact'
        self.bucket_name = 'test-bucket'

    @patch('mymodule.s3.Object')
    def test_store_artefact_success(self, mock_s3):
        """
        Test that the function stores the artefact correctly and returns the key.

        It should use a mock for the S3.Object and verify that the mock's upload_file method is called with the correct arguments.
        """
        mock_upload_file = MagicMock()
        mock_s3.return_value.upload_file = mock_upload_file

        key = store_artefact(self.model_id, self.artefact_file_path)

        mock_s3.assert_called_once_with(self.bucket_name, f'{self.model_id}/artefact')
        mock_upload_file.assert_called_once_with(self.artefact_file_path)
        self.assertEqual(key, f'{self.model_id}/artefact')

    @patch('mymodule.s3.Object')
    def test_store_artefact_failure(self, mock_s3):
        """
        Test that the function raises an exception if the artefact cannot be stored.

        It should use a mock for the S3.Object and verify that the mock's upload_file method raises an exception.
        """
        mock_upload_file = MagicMock(side_effect=Exception)
        mock_s3.return_value.upload_file = mock_upload_file

        with self.assertRaises(Exception):
            store_artefact(self.model_id, self.artefact_file_path)

        mock_s3.assert_called_once_with(self.bucket_name, f'{self.model_id}/artefact')
        mock_upload_file.assert_called_once_with(self.artefact_file_path)

    @patch('mymodule.s3.Object')
    def test_store_artefact_file_already_exists(self, mock_s3):
        """
        Test that the function raises an exception if the artefact file already exists in S3.

        It should use a mock for the S3.Object and verify that the mock's upload_file method raises an exception with an appropriate message.
        """
        error_message = 'An error occurred (EntityAlreadyExists) when calling the UploadPart operation: Object already exists'
        mock_upload_file = MagicMock(side_effect=Exception(error_message))
        mock_s3.return_value.upload_file = mock_upload_file

        with self.assertRaises(Exception) as cm:
            store_artefact(self.model_id, self.artefact_file_path)

        mock_s3.assert_called_once_with(self.bucket_name, f'{self.model_id}/artefact')
        mock_upload_file.assert_called_once_with(self.artefact_file_path)
        self.assertEqual(str(cm.exception), error_message)

    @patch('mymodule.s3.Object')
    def test_store_artefact_s3_error(self, mock_s3):
        """
        Test that the function raises an exception if there is an S3 error.

        It should use a mock for the S3.Object and verify that the mock's upload_file method raises an exception with an appropriate message.
        """
        error_message = 'An error occurred when calling the UploadPart operation: The bucket you are attempting to access must be addressed using the specified endpoint. Please send all future requests to this endpoint.'
        mock_upload_file = MagicMock(side_effect=Exception(error_message))
        mock_s3.return_value.upload_file = mock_upload_file

        with self.assertRaises(Exception) as cm:
            store_artefact('test_model', '/path/to/artefact')

        self.assertEqual(str(cm.exception), error_message)


class TestRetrieveArtefact(TestCase):
    @patch('mymodule.s3.Object')
    def test_retrieve_artefact_success(self, mock_s3):
        """
        Test that the function successfully retrieves the artefact from S3.

        It should use a mock for the S3.Object and verify that the mock's download_file method is called with the appropriate arguments.
        """
        model_id = 'test_model'
        local_file_path = '/tmp/test_artefact'
        mock_download_file = MagicMock()
        mock_s3.return_value.download_file = mock_download_file

        retrieve_artefact(model_id, local_file_path)

        mock_s3.assert_called_once_with('test_bucket', f'{model_id}/artefact')
        mock_download_file.assert_called_once_with(local_file_path)

    @patch('mymodule.s3.Object')
    def test_retrieve_artefact_not_found(self, mock_s3):
        """
        Test that the function raises an exception if the artefact is not found.

        It should use a mock for the S3.Object and verify that the mock's download_file method raises an exception with an appropriate message.
        """
        model_id = 'test_model'
        local_file_path = '/tmp/test_artefact'
        error_message = 'An error occurred (404) when calling the HeadObject operation: Not Found'
        mock_download_file = MagicMock(side_effect=Exception(error_message))
        mock_s3.return_value.download_file = mock_download_file

        with self.assertRaises(Exception) as cm:
            retrieve_artefact(model_id, local_file_path)

        mock_s3.assert_called_once_with('test_bucket', f'{model_id}/artefact')
        mock_download_file.assert_called_once_with(local_file_path)
        self.assertEqual(str(cm.exception), f'Artefact not found for model {model_id}')

    @patch('mymodule.s3.Object')
    def test_retrieve_artefact_s3_error(self, mock_s3):
        """
        Test that the function raises an exception if there is an S3 error.

        It should use a mock for the S3.Object and verify that the mock's download_file method raises an exception with an appropriate message.
        """
        model_id = 'test_model'
        local_file_path = '/tmp/test_artefact'
        error_message = 'An error occurred when calling the GetObject operation: Access Denied'
        mock_download_file = MagicMock(side_effect=Exception(error_message))
        mock_s3.return_value.download_file = mock_download_file

        with self.assertRaises(Exception) as cm:
            retrieve_artefact(model_id, local_file_path)

        mock_s3.assert_called_once_with('test_bucket', f'{model_id}/artefact')
        mock_download_file.assert_called_once_with(local_file_path)
        self.assertEqual(str(cm.exception), f'Failed to retrieve artefact for model {model_id}')

    @patch('mymodule.s3.Object')
    def test_retrieve_artefact_other_error(self, mock_s3):
        """
        Test that the function raises an exception for other errors.

        It should use a mock for the S3.Object and verify that the mock's download_file method raises an exception with an appropriate message.
        """
        model_id = 'test_model'
        local_file_path = '/tmp/test_artefact'
        error_message = 'An unknown error occurred'
        mock_download_file = MagicMock(side_effect=Exception(error_message))
        mock_s3.return_value.download_file = mock_download_file
        with self.assertRaises(Exception) as cm:
            retrieve_artefact(model_id, local_file_path)
        
        self.assertEqual(str(cm.exception), error_message)
        mock_s3.return_value.download_file.assert_called_once_with(local_file_path)
