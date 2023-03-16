from datetime import datetime

from models.models import ModelTable
from typing import Dict, Optional, Union
from datetime import datetime


def create_model(model_id: str, name: str, description: Optional[str] = None,
                 tags: Optional[Dict[str, Union[str, int]]] = None) -> ModelTable:
    """
    Creates a new model in the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.
        name (str): Name of the model.
        description (str, optional): Description of the model (default: None).
        tags (dict, optional): Dictionary of key-value pairs to associate with the model (default: None).

    Returns:
        ModelTable: The newly created model.

    """
    new_model = ModelTable(
        model_id=model_id,
        name=name,
        description=description,
        tags=tags
    )
    new_model.save()
    return new_model


def read_model(model_id: str) -> Optional[ModelTable]:
    """
    Reads a model from the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.

    Returns:
        ModelTable or None: The model if it exists, otherwise None.

    """
    try:
        return ModelTable.get(model_id)
    except ModelTable.DoesNotExist:
        return None


def update_model(model_id: str, name: Optional[str] = None, description: Optional[str] = None,
                 tags: Optional[Dict[str, Union[str, int]]] = None) -> Optional[ModelTable]:
    """
    Updates an existing model in the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.
        name (str, optional): New name for the model (default: None).
        description (str, optional): New description for the model (default: None).
        tags (dict, optional): New dictionary of key-value pairs to associate with the model (default: None).

    Returns:
        ModelTable or None: The updated model if it exists, otherwise None.

    """
    existing_model = read_model(model_id)
    if existing_model is not None:
        if name is not None:
            existing_model.name = name
        if description is not None:
            existing_model.description = description
        if tags is not None:
            existing_model.tags = tags
        existing_model.last_updated_at = datetime.utcnow()
        existing_model.save()
        return existing_model
    else:
        return None


def delete_model(model_id: str) -> bool:
    """
    Deletes an existing model from the ModelTable.

    Args:
        model_id (str): Unique identifier for the model.

    Returns:
        bool: True if the model was deleted, False otherwise.

    """
    existing_model = read_model(model_id)
    if existing_model is not None:
        existing_model.delete()
        return True
    else:
        return False
