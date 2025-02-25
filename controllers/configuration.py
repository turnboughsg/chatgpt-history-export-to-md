"""Module for handling user configuration and updating the models."""

from json import dump as json_dump
from json import load as json_load
from typing import Any

from models.conversation import Conversation
from models.conversation_set import ConversationSet
from models.message import Message
from models.node import Node
from views.prompt_user import prompt_user

from .file_system import default_output_folder, get_most_recently_downloaded_zip


def get_user_configs() -> dict[str, Any]:
    """Loads the default configs and calls the prompt_user function with those defaults.
    Returns the new configuration.
    """
    with open(file="config.json", encoding="utf-8") as file:
        default_configs = json_load(fp=file)

    if not default_configs["zip_file"]:
        default_configs["zip_file"] = get_most_recently_downloaded_zip()

    if not default_configs["output_folder"]:
        default_configs["output_folder"] = default_output_folder()

    return prompt_user(default_configs=default_configs)


def save_configs(user_configs: dict[str, Any]) -> None:
    """Update the config file with the new configuration options."""
    with open(file="config.json", mode="w", encoding="utf-8") as file:
        json_dump(obj=user_configs, fp=file, indent=2)


def set_model_configs(configs: dict[str, Any]) -> None:
    """Set the configuration for all models."""
    Conversation.configuration = configs.get("conversation", {})
    ConversationSet.configuration = configs.get("conversation_set", {})
    Message.configuration = configs.get("message", {})
    Node.configuration = configs.get("node", {})
