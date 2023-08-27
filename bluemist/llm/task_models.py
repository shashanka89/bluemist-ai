# Author: Shashank Agrawal
# License: MIT
# Version: 0.1.3
# Email: dew@bluemist-ai.one
# Created:  Jul 17, 2023
# Last modified: Aug 27, 2023

import os
from huggingface_hub import list_models
from transformers.pipelines import get_supported_tasks


class TaskModels:
    """
    Class representing a collection of tasks and their associated models.

    This class provides methods to retrieve information about available tasks
    and models. It also allows accessing the pipeline task name for a given task.

    Attributes:
        tasks (dict): A dictionary mapping tasks to a list of associated models
            and their corresponding pipeline task names.

    Example usage:
    ```
    # Instantiate the TaskModels class
    task_models = TaskModels()

    # Retrieve a list of available tasks
    tasks = task_models.get_all_tasks()
    print("Available tasks:", tasks)

    # Retrieve the list of models for a specific task
    task = "question-answering"
    models = task_models.get_models_for_task(task)
    print(f"Models for {task} task:", models)

    # Check if a specific task supports questions
    task = "document-question-answering"
    is_supported = task_models.is_question_supported(task)
    print(f"Does {task} support questions:", is_supported)
    ```
    """

    def __init__(self):
        """
        Initialize the TaskModels instance.

        This constructor initializes the `tasks` attribute, which contains the
        predefined tasks and their associated models.
        """
        self.tasks = {}
        self.populate_tasks()

        TESSDATA_PREFIX = os.environ.get("TESSDATA_PREFIX")
        if TESSDATA_PREFIX is None:
            import sys
            current_environment = sys.prefix
            tessdata_path = os.path.join(current_environment, 'share', 'tessdata')
            os.environ["TESSDATA_PREFIX"] = tessdata_path
        print("TESSDATA_PREFIX:", os.environ.get("TESSDATA_PREFIX"))

    def populate_tasks(self):
        """
        Populates the tasks dictionary with tasks supported by Bluemist AI
        """
        self.tasks = {
            "Document Question Answering": {
                "task_name": "document-question-answering",
                "question_support": True,
            },
            "Question Answering": {
                "task_name": "question-answering",
                "question_support": True,
            },
            "Summarize": {
                "task_name": "summarization",
                "question_support": False,
            },
            "Sentiment Analysis": {
                "task_name": "sentiment-analysis",
                "question_support": False,
            }
        }

    @staticmethod
    def is_model_supported_by_task(model, task_name):
        """
        Check if a specific model is supported by a given task.

        Args:
            model (str): The name of the model to check for support.
            task_name (str): The name of the task to check model support against.

        Returns:
            bool: True if the model is supported by the task, False otherwise.
        """

        models = TaskModels.get_models_for_task(task_name, limit=None)
        return model in models

    @staticmethod
    def get_models_for_task(task_name, limit):
        """
        Retrieves the available models for a given task.

        Args:
            task_name (str): The task for which to retrieve the models.
            limit (int, optional): The maximum number of models to retrieve

        Returns:
            list: A list of available models for the specified task.
        """
        models = list_models(filter=task_name, sort='downloads', direction='-1', limit=limit)
        return [model.modelId for model in models]

    def get_all_tasks(self):
        """
        Retrieves all available tasks.

        Returns:
            list: A list of all available tasks.
        """
        hf_supported_tasks = get_supported_tasks()
        print(hf_supported_tasks)
        matching_task_names = [task["task_name"] for task in self.tasks.values() if
                               task["task_name"] in hf_supported_tasks]

        return matching_task_names

    def is_question_supported(self, task_name):
        """
        Check if the given task supports questions.

        Args:
            task_name (str): The task name to check.

        Returns:
            bool: True if the task supports questions, False otherwise.
        """
        for task_info in self.tasks.values():
            if task_info["task_name"] == task_name:
                return task_info["question_support"]

        return False

    def get_context_input_type(self, task_name):
        """
        Get the input type required for the given task's context.

        Args:
            task_name (str): The name of the task to check.

        Returns:
            bool: The context input type if the task supports questions, None otherwise.
        """
        for task_info in self.tasks.values():
            if task_info["task_name"] == task_name:
                return task_info["context_input_type"]

        return None
