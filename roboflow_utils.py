import os
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

# This looks for the .env file and loads the variables
load_dotenv()

# Retrieve the key from the environment instead of hardcoding it
api_key = os.getenv("ROBOFLOW_API_KEY")

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=api_key
)

def run_inference(image_path: str):
    result = CLIENT.run_workflow(
        workspace_name="alrazels-workspace",
        workflow_id="fish-freshness-scanner-1778118664597",
        images={"image": image_path},
        use_cache=True
    )
    return result