# Document Processing and Metadata Extraction

This project allows users to preprocess their documents and then query the processed data. The preprocessing module handles document chunk creation using the Unstructured library and metadata extraction using LlamaIndex and Mistral. The inference module deploys these functionalities as a Databricks endpoint.

## Project Structure

```
.
├── code
│   ├── notebooks
│   │   ├── preprocessing_notebook.ipynb
│   │   └── inference_notebook.ipynb
│   ├── inference
│   │   ├── llm_models
│   │   │   ├── __init__.py
│   │   │   ├── mistral.py
│   │   │   └── prompt_template.json
│   │   ├── agent
│   │   │   ├── rephrase_agent.py
│   │   │   ├── query_intent.py
│   │   │   └── predict_strategy.py
│   │   ├── doc_search
│   │   │   ├── doc_search.json
│   │   │   └── document_retriever.py
│   │   ├── api_contracts
│   │   │   └── custom_classes.py
│   │   ├── dbutils
│   │   │   └── db_connect.py
│   │   └── requirements.txt
│   └── preprocessing
│       ├── doc_processing.py
│       ├── extractor.py
│       └── requirements.txt
├── .env
├── README.md
└── env.py
```

## Project Description

This project enables users to preprocess their documents and then ask queries based on the processed documents. Preprocessing involves converting PDFs to DOCX (if possible), chunking the documents, and extracting metadata. The inference module allows querying the processed data through a deployed Databricks endpoint.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/document-processing.git
   cd document-processing
   ```

2. **Install dependencies for preprocessing:**

   ```sh
   pip install -r code/preprocessing/requirements.txt
   ```

3. **Install dependencies for inference:**

   ```sh
   pip install -r code/inference/requirements.txt
   ```

4. **Set environment variables:**

   Create a `.env` file in the root directory with the required environment variables, including output paths and API tokens.

5. **Manage environment variables:**

   The `env.py` script can be used to load all environment variables.

   ```python
   # env.py
   from dotenv import load_dotenv
   import os

   def load_env():
       load_dotenv()
       return {
           "output_path": os.getenv("OUTPUT_PATH"),
           "api_token": os.getenv("API_TOKEN"),
           "db_url": os.getenv("DB_URL")
       }
   ```

## Preprocessing

The preprocessing module handles document processing as batch processing, and the code is available under the `notebooks` folder.

- [Preprocessing Notebook](code/notebooks/preprocessing_notebook.ipynb)

### Document Processing

The `doc_processing` module converts PDFs to DOCX format (if possible) and creates document chunks using the Unstructured library. If the conversion to DOCX fails, it processes the PDF directly. It also uses the YOLO model in Unstructured to extract table data.

### Extractor

The `extractor` module uses LlamaIndex and Mistral to extract metadata such as summaries of current, previous, and next chunks, and titles. The processed chunks and metadata are stored in a Delta table for efficient retrieval and querying.

## Inference

The inference module is deployed as a Databricks endpoint and is available under the `notebooks` folder.

- [Inference Notebook](code/notebooks/inference_notebook.ipynb)

### LLM Models

The `llm_models` module defines LLMs using the OpenAI client. You can define and implement any LLM by following the structure provided for Mistral.

```python
# Example class structure for an LLM
class LLMModel:
    def __init__(self, url, token, model_name):
        self.url = url
        self.token = token
        self.model_name = model_name

    def get_response(self, prompt):
        # Implementation using OpenAI client
        pass

    def predict_intent(self, input_text):
        # Predict intent
        pass

    def predict_strategy(self, input_text):
        # Predict strategy
        pass
```

### Agent Modules

The `agent` submodule contains:

- **Rephrasing Agent:** Rephrases user prompts.
- **Workflow Agent:** Uses query intent and predict strategy to decide the workflow.
- **Supervising Agent:** Implements the RAG workflow and calls both rephrase and supervising agents to answer user queries.

### Document Search Agent

The `doc_search` module contains:

- **doc_search.json:** Contains preprocessed documents' metadata.
- **document_retriever.py:** Retrieves document names.

### API Contracts and DB Utils

- **API Contracts:** Contains custom classes to support the workflow.
- **DB Utils:** Connects to the vector search index.

## Libraries

- [Unstructured](https://unstructured-io.github.io/unstructured/)
- [LlamaIndex](https://llamaindex.ai/)

## Requirements

Refer to `requirements.txt` in both the preprocessing and inference directories for the necessary Python packages.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
