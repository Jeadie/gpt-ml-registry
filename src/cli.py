import typer
from typing import Optional
from model_table_operations import create_model, delete_model_by_id, get_model_by_id, list_models, update_model_by_id
from pydantic import BaseModel


class Model(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    tags: Optional[list] = None


app = typer.Typer()


@app.command()
def create(id: str, name: str, description: Optional[str] = None, tags: Optional[str] = None):
    """
    Create a new model with the given ID, name, description, and tags.

    Args:
        id (str): The ID of the model to create.
        name (str): The name of the model to create.
        description (str, optional): The description of the model to create.
        tags (str, optional): The tags of the model to create.
    """
    model = Model(id=id, name=name, description=description, tags=tags)
    create_model(model)


@app.command()
def get(id: str):
    """
    Retrieve the model with the given ID.

    Args:
        id (str): The ID of the model to retrieve.
    """
    model = get_model_by_id(id)
    if model is None:
        typer.echo(f"Model with ID '{id}' not found.")
    else:
        typer.echo(model.json(indent=2))


@app.command()
def update(id: str, name: Optional[str] = None, description: Optional[str] = None, tags: Optional[str] = None):
    """
    Update the model with the given ID.

    Args:
        id (str): The ID of the model to update.
        name (str, optional): The new name of the model.
        description (str, optional): The new description of the model.
        tags (str, optional): The new tags of the model.
    """
    update_fields = {}
    if name is not None:
        update_fields['name'] = name
    if description is not None:
        update_fields['description'] = description
    if tags is not None:
        update_fields['tags'] = tags

    update_model_by_id(id, update_fields)


@app.command()
def delete(id: str):
    """
    Delete the model with the given ID.

    Args:
        id (str): The ID of the model to delete.
    """
    delete_model_by_id(id)


@app.command()
def list():
    """
    List all models in the ModelTable.
    """
    models = list_models()
    typer.echo('\n'.join([model.json(indent=2) for model in models]))

import typer
import boto3

app = typer.Typer()

s3 = boto3.resource('s3')
bucket_name = 'my-model-bucket'

@app.command()
def store_artefact(model_id: str, artefact: str):
    """
    Uploads a model artefact file to S3.

    Args:
        model_id (str): The ID of the model the artefact belongs to.
        artefact (str): The path to the artefact file to be uploaded.
    """
    key = f'{model_id}/artefact'
    with open(artefact, 'rb') as f:
        store_artefact(s3, bucket_name, key, f)
    typer.echo(f"Artefact {key} uploaded successfully")


@app.command()
def retrieve_artefact(model_id: str, output_file: str):
    """
    Downloads a model artefact file from S3.

    Args:
        model_id (str): The ID of the model the artefact belongs to.
        output_file (str): The path to save the downloaded artefact file.
    """
    key = f'{model_id}/artefact'
    with open(output_file, 'wb') as f:
        artefact_file = retrieve_artefact(s3, bucket_name, key)
        f.write(artefact_file.read())
    typer.echo(f"Artefact {key} downloaded successfully")


if __name__ == "__main__":
    app() 
