from typing import Optional, List, Any

from pydantic import BaseModel

from deeploy.enums import PredictionMethod


class DeployOptions(BaseModel):
    """
    Class that contains the options for deploying a model

    Attributes:
      name: name of the deployment
      model_serverless: boolean indicating whether to deploy the model in 
        a serverless fashion. Defaults to False
      explainer_serverless: boolean indicating whether to deploy the model in 
        a serverless fashion. Defaults to False
      method: string indication which prediction function to use. Only applicable
        to sklearn and xgboost models. Defaults to 'predict'
      description: string with the description of the deployment
      example_input: list of example input parameters for the model
      example_output: list of example output for the model
      model_class_name: string indicating the name of the class containing a 
        PyTorch model.
    """
    name: str
    model_serverless = False
    explainer_serverless = False
    method = PredictionMethod.PREDICT
    description: Optional[str]
    example_input: Optional[List[Any]]
    example_output: Optional[List[Any]]
    model_class_name: Optional[str]
    pytorch_model_file_path: Optional[str]
