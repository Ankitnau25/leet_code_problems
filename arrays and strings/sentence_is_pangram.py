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

from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.ppt import partition_pptx
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc

class TextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        if self.file_path.endswith(".pdf"):
            return partition_pdf(
                          filename="path/to/your/pdf_file.pdf",                  # mandatory
                          strategy="hi_res",                                     # mandatory to use ``hi_res`` strategy
                          extract_images_in_pdf=True,                            # mandatory to set as ``True``
                          extract_image_block_types=["Image", "Table"],          # optional
                          extract_image_block_to_payload=False,                  # optional
                          extract_image_block_output_dir="path/to/save/images",  # optional - only works when ``extract_image_block_to_payload=False``
                          )

        elif self.file_path.endswith(".docx"):
            return partition_docx(self.file_path)

        elif self.file_path.endswith(".doc"):
            return partition_doc(self.file_path)

        elif self.file_path.endswith(".ppt"):  
            return partition_doc(self.file_path)

        elif self.file_path.endswith(".pptx"):
            return partition_pptx(self.file_path )

        else:
            return partition(self.file_path)

# Example usage:
unstructured_io = UnstructuredIO("/content/document.pdf")
text = unstructured_io.extract_text()
print(text)

class TextChunker:
    def __init__(self, text):
        self.text = text

    def chunk_by_sentence(self):
        import nltk
        sentences = nltk.sent_tokenize(self.text)
        return sentences

    def chunk_by_paragraph(self):
        paragraphs = self.text.split("\n\n")
        return paragraphs

    def chunk_by_word(self):
        words = self.text.split()
        return words
# aws:
#   access_key_id: YOUR_ACCESS_KEY_ID
#   secret_access_key: YOUR_SECRET_ACCESS_KEY
#   endpoint_url: https://s3.eu-central-1.amazonaws.com
# s3:  
#   bucket_name: YOUR_BUCKET_NAME
#   region_name: eu-central-1

    def chunk_by_character(self):
        characters = list(self.text)
        return characters
