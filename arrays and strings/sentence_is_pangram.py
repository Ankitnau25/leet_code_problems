class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        return len(set(sentence)) == 26

import mlflow
import mlflow.onnx
import onnx
from mlflow.models.signature import infer_signature, ModelSignature
from mlflow.types import Schema, ColSpec
import pandas as pd
import numpy as np
import onnxruntime as rt

# Load the ONNX model from a file
onnx_model_path = "/dbfs/models/flashrank.onnx"
onnx_model = onnx.load(onnx_model_path)

# Define the input schema
input_schema = Schema([
    ColSpec("string", "query"),
    ColSpec("string", "passages")
])

# Define the output schema
output_schema = Schema([
    ColSpec("string", "id"),
    ColSpec("string", "text"),
    ColSpec("string", "meta")
])

# Create the model signature
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

# Start an MLflow run
with mlflow.start_run() as run:
    # Log the ONNX model with the signature
    mlflow.onnx.log_model(onnx_model, artifact_path="flashrank_onnx_model", signature=signature)

    # Register the model in the Model Registry
    model_uri = f"runs:/{run.info.run_id}/flashrank_onnx_model"
    mlflow.register_model(model_uri=model_uri, name="FlashRankONNXModel")

print("ONNX Model registered successfully!")
 
