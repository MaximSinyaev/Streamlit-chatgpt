from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import os

filename = "foobar.pdf"
prompt = "Extract the content from the file provided without altering it. Just output its exact content and nothing else."

secrets = toml.load("../.secrets.toml")

api_key = secrets["openai"]["api_key"]

client = OpenAI(api_key=api_key)

