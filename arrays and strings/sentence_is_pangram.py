class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        return len(set(sentence)) == 26
import boto3
import unstructured
import os
import yaml


def download_s3_docs(config_file_path='config.yaml', local_dir='input_docs'):
    """Downloads documents from an S3 bucket based on configurations in a YAML file.

    Args:
        config_file_path (str): Path to the configuration YAML file.
        local_dir (str): Local directory to save downloaded documents.
    """

    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)

    # Get required information from the config
    aws_access_key_id = config['aws']['access_key_id']
    aws_secret_access_key = config['aws']['secret_access_key']
    s3_bucket_name = config['s3']['bucket_name']
    s3_prefix = config['s3']['prefix'] if 'prefix' in config['s3'] else None  # Handle optional prefix

    # Create a boto3 S3 client using the provided credentials
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    s3_client = session.client('s3')

    # Create the local directory if it doesn't exist
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Download files from S3
    for obj in s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_prefix)['Contents']:
        file_key = obj['Key']
        local_file_path = os.path.join(local_dir, os.path.basename(file_key))

        print(f"Downloading: {file_key} to {local_file_path}")
        s3_client.download_file(s3_bucket_name, file_key, local_file_path)
    return local_dir 

class DocumentIngestor:
    def __init__(self, source_type, source_path):
        self.source_type = source_type
        self.source_path = source_path

    def ingest(self):
        if self.source_type == "folder":
            return self.source_path

        elif self.source_type == "s3":
            res_path = download_s3_docs()
            return res_path

        else:
            raise ValueError("Invalid source type.")

        return None

# Example usage:
ingestor = DocumentIngestor(source_type="folder", source_path="/content/documents")
documents = ingestor.ingest()

# Or:
ingestor = DocumentIngestor(source_type="s3", source_path="s3://my-bucket/documents")
documents = ingestor.ingest()


import json
from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.ppt import partition_pptx
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
from unstructured.staging.base import elements_to_json
from unstructured.chunking.basic import chunk_elements
from unstructured.chunking.title import chunk_by_title

class TextChunker:
    def __init__(self, elements):
        self.elements = elements

    def chunk_by_tilte(self):
        return chunk_by_title(self.elements)

    def chunk_elements(self):
        return chunk_elements(self.elements)


class TextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        if self.file_path.name.endswith(".pdf"):
            return partition_pdf(
                          filename=self.file_path,                  # mandatory
                          strategy="hi_res",                                     # mandatory to use ``hi_res`` strategy
                          extract_images_in_pdf=True,                            # mandatory to set as ``True``
                          extract_image_block_types=["Image", "Table"],          # optional
                          extract_image_block_to_payload=False,                  # optional
                          extract_image_block_output_dir="path/to/save/images",  # optional - only works when ``extract_image_block_to_payload=False``
                          )

        elif self.file_path.name.endswith(".docx"):
            return partition_docx(self.file_path)

        elif self.file_path.name.endswith(".doc"):
            return partition_doc(self.file_path)

        elif self.file_path.name.endswith(".ppt"):
            return partition_doc(self.file_path)

        elif self.file_path.name.endswith(".pptx"):
            return partition_pptx(self.file_path )

        else:
            return partition(self.file_path)

    def extract_title_meta_data(self,elements):
        li_title = []
        li_elements = json.loads(elements_to_json(elements))
        for elem in  li_elements:
                if elem['type'] == 'Title':
                    li_title.append(elem['text'])
        filename = li_elements[0]['metadata']['filename']
        filetype = li_elements[0]['metadata']['filetype']
        meta_dict = {'title_list':li_title,
                    'filename': 'table.pdf',
                    'filetype': 'application/pdf'}
        return meta_dict
        
ingestor = DocumentIngestor(source_type="folder", source_path="/content/data")
doc_dir = ingestor.ingest()
for file_ in os.listdir(doc_dir):
    file_path = doc_dir.joinpath(file_)
    if file_path.is_file():
      te_obj =  TextExtractor(file_path)
      elements = te_obj.extract_text()
      output = te_obj.extract_title_meta_data(elements)
      chunks = TextChunker(elements).chunk_by_tilte()
      output['chunks'] = json.loads(elements_to_json(chunks))
