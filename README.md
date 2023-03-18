# Model Registry

This is a Python project that provides a model registry for storing and managing models and their associated artefacts. The project uses DynamoDB to store metadata about the models and Amazon S3 to store the artefact files.

## Installation

To install the necessary packages for this project, run:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the project, you'll need to set up the following environment variables:

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `AWS_DEFAULT_REGION`: The AWS region where your resources are located.
- `MODEL_REGISTRY_TABLE_NAME`: The name of the DynamoDB table to be used for storing model metadata.

## Usage
### Typer CLI
The project includes a command-line interface (CLI) that can be used to interact with the model registry. To see the available commands, run:

```bash
python src/cli.py --help
```

### FastAPI Server
The project also includes a RESTful API that can be used to interact with the model registry. To start the server, run:
```bash
uvicorn server:app --reload
```
This will start the server on http://localhost:8000 by default.

The following endpoints are available:

- `GET /models`: Returns a list of all models in the registry.
- `GET /models/{model_id}`: Returns metadata about a specific model.
- `POST /models`: Creates a new model in the registry.
- `PUT /models/{model_id}`: Updates metadata about a specific model.
- `DELETE /models/{model_id}`: Deletes a specific model from the registry.
- `POST /models/{model_id}/artefact`: Uploads an artefact file for a specific model to S3.
- `GET /models/{model_id}/artefact`: Downloads the artefact file for a specific model from S3.

### Example
Here's an example of how to use the CLI to create a new model and upload an artefact:

```bash
# Create a new model
python src/cli.py create_model --model_id 123 --name "My Model" --description "This is my model"

# Upload an artefact
python src/cli.py store_artefact --model_id 123 --artefact my_model.pkl
```

Here's an example of how to use the FastAPI API to retrieve metadata about a model:
```bash
curl http://localhost:8000/models/123
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
