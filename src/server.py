from typing import Dict, Union
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import uvicorn

from operations.models import create_model, read_model, update_model, delete_model

app = FastAPI()

security = HTTPBasic()


class ModelCreateRequest(BaseModel):
    """
    Pydantic Model for creating a new model.
    """
    name: str
    description: Union[str, None] = None
    tags: Union[Dict[str, Union[str, int]], None] = None


class ModelUpdateRequest(BaseModel):
    """
    Pydantic Model for updating an existing model.
    """
    name: Union[str, None] = None
    description: Union[str, None] = None
    tags: Union[Dict[str, Union[str, int]], None] = None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticates the user based on the provided HTTPBasic credentials.

    Args:
        credentials (HTTPBasicCredentials, optional): The HTTPBasic credentials to use (default: Depends(security)).

    Raises:
        HTTPException: Raises an HTTPException with a 401 status code if the credentials are incorrect.

    """
    correct_username = "user"
    correct_password = "password"
    if not (credentials.username == correct_username and credentials.password == correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/models")
def create_new_model(request: ModelCreateRequest, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Creates a new model in the ModelTable.

    Args:
        request (ModelCreateRequest): Pydantic Model for creating a new model.
        credentials (HTTPBasicCredentials, optional): The HTTPBasic credentials to use (default: Depends(security)).

    Returns:
        dict: Dictionary representation of the created model.

    """
    authenticate_user(credentials)
    new_model = create_model(model_id=str(datetime.now().timestamp()), name=request.name,
                             description=request.description, tags=request.tags)
    return new_model.attribute_values


@app.get("/models/{model_id}")
def read_model_by_id(model_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Reads a model from the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.
        credentials (HTTPBasicCredentials, optional): The HTTPBasic credentials to use (default: Depends(security)).

    Returns:
        dict: Dictionary representation of the model if it exists, otherwise raises an HTTPException.

    """
    authenticate_user(credentials)
    model = read_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    else:
        return model.attribute_values


@app.put("/models/{model_id}")
def update_model_by_id(model_id: str, request: ModelUpdateRequest,
                       credentials: HTTPBasicCredentials = Depends(security)):
    """
    Updates an existing model in the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.
        request (ModelUpdateRequest): Pydantic Model for updating an existing model.
        credentials (HTTPBasicCredentials, optional): The HTTPBasic credentials to use (default: Depends(security)).

    Returns:
        dict: Dictionary representation of the updated model if it exists, otherwise raises an HTTPException.

    """
    authenticate_user(credentials)
    model = read_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    # Only update fields that are provided in the request
    updated_fields = {}
    if request.name is not None:
        updated_fields['name'] = request.name
    if request.description is not None:
        updated_fields['description'] = request.description
    if request.tags is not None:
        updated_fields['tags'] = request.tags

    # Perform the update and return the updated model
    updated_model = update_model(model_id, updated_fields)
    return updated_model.attribute_values


@app.delete("/models/{model_id}")
def delete_model_by_id(model_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Deletes a model from the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.
        credentials (HTTPBasicCredentials, optional): The HTTPBasic credentials to use (default: Depends(security)).

    Returns:
        dict: Dictionary representation of the deleted model if it exists, otherwise raises an HTTPException.

    """
    authenticate_user(credentials)
    model = read_model(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    else:
        delete_model(model_id)
        return model.attribute_values


@app.post("/models/{model_id}/artefact")
async def store_artefact(model_id: str, artefact: UploadFile = File(...)):
    """
    Uploads a model artefact file to S3.

    Args:
        model_id (str): The ID of the model the artefact belongs to.
        artefact (UploadFile): The uploaded artefact file.
    """
    key = f'{model_id}/artefact'
    store_artefact(s3, bucket_name, key, artefact.file)
    return {"message": f"Artefact {key} uploaded successfully"}


@app.get("/models/{model_id}/artefact")
async def retrieve_artefact(model_id: str):
    """
    Downloads a model artefact file from S3.

    Args:
        model_id (str): The ID of the model the artefact belongs to.

    Returns:
        The downloaded artefact file.
    """
    key = f'{model_id}/artefact'
    artefact_file = retrieve_artefact(s3, bucket_name, key)
    return StreamingResponse(iter(artefact_file.read()), media_type='application/octet-stream')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


