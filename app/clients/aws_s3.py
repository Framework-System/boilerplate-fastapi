import base64
import json
import tempfile
from typing import Dict

import boto3

from app.settings import settings


class AwsS3Client:
    """AWS S3 Client."""

    def __init__(self, bucket: str = ""):
        """
        AWS S3 Client.

        :param bucket: The name of the S3 bucket.
        """
        self._client: boto3.session.Session.client = boto3.client("s3")
        self._bucket: str = bucket or settings.default_bucket

    def upload_json(
        self,
        json_content: Dict[str, object],
        file_name: str,
        bucket_path: str = "",
    ) -> None:
        """
        Uploads a json file to an S3 bucket.

        :param json_content: The json content to be uploaded.
        :param file_name: The name of the file without extension to be uploaded.
        :param bucket_path: The path to the S3 bucket.
        """
        self._client.put_object(
            Bucket=self._bucket,
            Key=f"{bucket_path}/{file_name}.json",
            Body=json.dumps(json_content),
        )

    def upload_base64_image(
        self,
        base64_image: str,
        file_name: str,
        bucket_path: str = "",
    ) -> None:
        """
        Uploads a base64 image to an S3 bucket.

        :param base64_image: The base64 encoded image.
        :param file_name: The name of the file without extension to be uploaded.
        :param bucket_path: The path to the S3 bucket.
        """
        image_data = base64.b64decode(base64_image)

        with tempfile.NamedTemporaryFile("wb") as temp_file:
            temp_file.write(image_data)

            with open(temp_file.name, "rb") as file_reader:
                self._client.upload_fileobj(
                    file_reader,
                    self._bucket,
                    f"{bucket_path}/{file_name}.png",
                )

    def get_json_content(
        self,
        file_name: str,
        bucket_path: str = "",
    ) -> Dict[str, str]:
        """
        Retrieves the json content from an S3 bucket.

        :param file_name: The name of the file without extension.
        :param bucket_path: The path to the S3 bucket.
        :return: The json content.
        """
        response = self._client.get_object(
            Bucket=self._bucket,
            Key=f"{bucket_path}/{file_name}.json",
        )
        json_data = response.get("Body").read().decode("utf-8")
        return dict(json.loads(json_data))
