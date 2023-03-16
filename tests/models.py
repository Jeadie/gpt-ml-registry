import unittest

from pynamodb.models import Model
from src.models import ModelTable

class TestModelTable(unittest.TestCase):
    def setUp(self):
        # Set up a test table
        self.table_name = 'test-table'
        ModelTable.Meta.table_name = self.table_name
        ModelTable.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    def tearDown(self):
        # Delete the test table
        ModelTable.delete_table()

    def test_create_and_retrieve_model(self):
        # Create a new model and save it to the table
        model = ModelTable(
            model_id='1',
            name='test-model',
            description='A test model',
            tags={'test': True},
        )
        model.save()

        # Retrieve the model from the table
        retrieved_model = ModelTable.get('1')

        # Ensure that the retrieved model has the same attributes as the original model
        self.assertEqual(retrieved_model.name, model.name)
        self.assertEqual(retrieved_model.description, model.description)
        self.assertEqual(retrieved_model.tags, model.tags)

    def test_update_model(self):
        # Create a new model and save it to the table
        model = ModelTable(
            model_id='1',
            name='test-model',
            description='A test model',
            tags={'test': True},
        )
        model.save()

        # Update the model's attributes and save the changes
        model.name = 'new-name'
        model.description = 'new-description'
        model.tags = {'new-tag': True}
        model.save()

        # Retrieve the updated model from the table
        retrieved_model = ModelTable.get('1')

        # Ensure that the retrieved model has the updated attributes
        self.assertEqual(retrieved_model.name, model.name)
        self.assertEqual(retrieved_model.description, model.description)
        self.assertEqual(retrieved_model.tags, model.tags)

    def test_delete_model(self):
        # Create a new model and save it to the table
        model = ModelTable(
            model_id='1',
            name='test-model',
            description='A test model',
            tags={'test': True},
        )
        model.save()

        # Delete the model from the table
        model.delete()

        # Ensure that the model is no longer in the table
        with self.assertRaises(Model.DoesNotExist):
            ModelTable.get('1')
