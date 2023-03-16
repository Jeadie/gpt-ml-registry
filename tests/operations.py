import unittest

from src.operations import create_model, read_model, update_model, delete_model, ModelTable


class TestModelTableFunctions(unittest.TestCase):
    """
    Test suite for functions that interact with ModelTable.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating a new ModelTable object.
        """
        self.test_model_id = str(uuid.uuid4())
        self.test_model_name = "Test Model"
        self.test_model_description = "This is a test model"
        self.test_model_tags = {"version": "1.0", "owner": "Test User"}
        self.test_model = create_model(self.test_model_id, self.test_model_name,
                                       self.test_model_description, self.test_model_tags)

    def tearDown(self) -> None:
        """
        Clean up the test environment by deleting the test model from ModelTable.
        """
        delete_model(self.test_model_id)

    def test_create_model(self):
        """
        Test that create_model function creates a new model in ModelTable.
        """
        new_model_id = str(uuid.uuid4())
        new_model_name = "New Test Model"
        new_model_description = "This is a new test model"
        new_model_tags = {"version": "2.0", "owner": "New Test User"}

        new_model = create_model(new_model_id, new_model_name, new_model_description, new_model_tags)

        self.assertIsInstance(new_model, ModelTable)
        self.assertEqual(new_model.model_id, new_model_id)
        self.assertEqual(new_model.name, new_model_name)
        self.assertEqual(new_model.description, new_model_description)
        self.assertEqual(new_model.tags, new_model_tags)

        delete_model(new_model_id)

    def test_read_model(self):
        """
        Test that read_model function retrieves an existing model from ModelTable.
        """
        retrieved_model = read_model(self.test_model_id)

        self.assertIsInstance(retrieved_model, ModelTable)
        self.assertEqual(retrieved_model.model_id, self.test_model_id)
        self.assertEqual(retrieved_model.name, self.test_model_name)
        self.assertEqual(retrieved_model.description, self.test_model_description)
        self.assertEqual(retrieved_model.tags, self.test_model_tags)

    def test_read_missing_model(self):
        """
        Test that read_model function returns None if a model does not exist in ModelTable.
        """
        missing_model_id = str(uuid.uuid4())

        retrieved_model = read_model(missing_model_id)

        self.assertIsNone(retrieved_model)

    def test_update_model(self):
        """
        Test that update_model function updates an existing model in ModelTable.
        """
        updated_model_name = "Updated Test Model"
        updated_model_description = "This is an updated test model"
        updated_model_tags = {"version": "1.1", "owner": "Updated Test User"}

        updated_model = update_model(self.test_model_id, updated_model_name,
                                     updated_model_description, updated_model_tags)

        self.assertIsInstance(updated_model, ModelTable)
        self.assertEqual(updated_model.model_id, self.test_model_id)
        self.assertEqual(updated_model.name, updated_model_name)
        self.assertEqual(updated_model.description, updated_model_description)
        self.assertEqual(updated_model.tags, updated_model_tags)

    def test_update_missing_model(self):
        """
        Test that update_model function returns None if a model does not exist in ModelTable.
        """
        missing_model_id = str(uuid.uuid4())

        updated_model = update_model(missing_model_id, "New Name", "New Description", {"new_tag": "new_value"})

        self.assertIsNone(updated_model)

    def test_delete_model(self):
        """
        Test that an existing model can be deleted from the ModelTable.

        Steps:
        1. Create a new model.
        2. Try to delete the model using the `delete_model` function.
        3. Check that the function returns True.
        4. Try to read the model using the `read_model` function.
        5. Check that the function returns None.

        """
        model_id = 'model-1'
        name = 'Test Model'
        description = 'A test model'
        tags = {'environment': 'dev'}
        create_model(model_id, name, description, tags)

        # verify that the model was created successfully
        model = read_model(model_id)
        self.assertIsNotNone(model)
        self.assertEqual(model.model_id, model_id)
        self.assertEqual(model.name, name)
        self.assertEqual(model.description, description)
        self.assertDictEqual(model.tags, tags)

        # delete the model
        deleted = delete_model(model_id)
        self.assertTrue(deleted)

        # verify that the model was deleted
        model = read_model(model_id)
        self.assertIsNone(model)

        # delete the model again
        deleted = delete_model(model_id)
        self.assertFalse(deleted)
