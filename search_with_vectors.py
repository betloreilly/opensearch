from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
import urllib3
import os

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get credentials from environment variables (or use defaults for local dev)
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST', 'localhost')
OPENSEARCH_PORT = int(os.getenv('OPENSEARCH_PORT', '9200'))
OPENSEARCH_USER = os.getenv('OPENSEARCH_USER', 'admin')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD', 'MyStrongPassword123!')

# Initialize the same model
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!\n")

# Try to connect to OpenSearch
# First try HTTPS (default Docker setup)
print("Connecting to OpenSearch...")
try:
    client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )
    # Test the connection
    info = client.info()
    print(f"Connected via HTTPS to OpenSearch {info['version']['number']}\n")
except Exception as e:
    print(f"HTTPS connection failed: {e}")
    print("Trying HTTP connection...\n")
    # Try HTTP connection (if SSL is disabled in Docker)
    client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        use_ssl=False
    )
    info = client.info()
    print(f"Connected via HTTP to OpenSearch {info['version']['number']}\n")

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

