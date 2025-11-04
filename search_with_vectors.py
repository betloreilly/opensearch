from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
from urllib.parse import urlparse
import urllib3
import os

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connection settings (credentials optional)
OPENSEARCH_URL = os.getenv('OPENSEARCH_URL', 'http://localhost:9200')
OPENSEARCH_USERNAME = os.getenv('OPENSEARCH_USERNAME')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')
VERIFY_CERTS_ENV = os.getenv('OPENSEARCH_VERIFY_CERTS')

parsed = urlparse(OPENSEARCH_URL)
host = parsed.hostname or 'localhost'
port = parsed.port or (443 if parsed.scheme == 'https' else 9200)
use_ssl = parsed.scheme == 'https'
verify_certs = (
    (VERIFY_CERTS_ENV.lower() in ('1', 'true', 'yes')) if isinstance(VERIFY_CERTS_ENV, str)
    else use_ssl
)

# Initialize the same model
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!\n")

print("Connecting to OpenSearch...")
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD) if (OPENSEARCH_USERNAME and OPENSEARCH_PASSWORD) else None,
    use_ssl=use_ssl,
    verify_certs=verify_certs,
    ssl_assert_hostname=verify_certs,
    ssl_show_warn=verify_certs,
)
info = client.info()
scheme = 'HTTPS' if use_ssl else 'HTTP'
print(f"Connected via {scheme} to OpenSearch {info['version']['number']} at {host}:{port}\n")

# User's search query
query_text = "noise blocking headphones"

# Generate vector for the query
query_vector = model.encode(query_text).tolist()

# Search using the vector
response = client.search(
    index='products_vector',
    body={
        "size": 5,
        "query": {
            "knn": {
                "description_vector": {
                    "vector": query_vector,
                    "k": 5
                }
            }
        }
    }
)

# Print results
print(f"Found {response['hits']['total']['value']} results:\n")
for hit in response['hits']['hits']:
    print(f"Score: {hit['_score']:.4f}")
    print(f"Product: {hit['_source']['name']}")
    print(f"Description: {hit['_source']['description']}")
    print()

