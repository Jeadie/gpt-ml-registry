import boto3

s3 = boto3.resource('s3')
bucket_name = 'my-model-bucket'


def store_artefact(model_id: str, artefact_file_path: str) -> str:
    """
    Uploads a model artefact file to S3.

    Args:
        model_id (str): The ID of the model the artefact belongs to.
        artefact_file_path (str): The local file path of the artefact file.

    Returns:
        str: The S3 key of the uploaded artefact file.
    """
    key = f'{model_id}/artefact'
    s3.Object(bucket_name, key).upload_file(artefact_file_path)
    return key


def retrieve_artefact(model_id: str, local_file_path: str) -> None:
    """
    Downloads a model artefact file from S3.

    Args:
        model_id (str): The ID of the model the artefact belongs to.
        local_file_path (str): The local file path to download the artefact file to.
    """
    key = f'{model_id}/artefact'
    s3.Object(bucket_name, key).download_file(local_file_path)
