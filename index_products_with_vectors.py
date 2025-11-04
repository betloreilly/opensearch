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

# Initialize the embedding model (384 dimensions)
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

# Sample products
products = [
    {
        "product_id": "P-1001",
        "name": "Wireless Headphones",
        "description": "Over-ear wireless headphones with active noise cancellation",
        "category": "Electronics",
        "price": 89.99
    },
    {
        "product_id": "P-1002",
        "name": "Bluetooth Earbuds",
        "description": "Compact in-ear earbuds with long battery life",
        "category": "Electronics",
        "price": 49.50
    },
    {
        "product_id": "P-1003",
        "name": "Noise Canceling Headset",
        "description": "Professional headset with advanced noise cancellation for calls",
        "category": "Electronics",
        "price": 129.99
    },
    {
        "product_id": "P-1004",
        "name": "Portable Speaker",
        "description": "Waterproof Bluetooth speaker with 360-degree sound",
        "category": "Electronics",
        "price": 59.99
    }
]

# Generate embeddings and index products
for product in products:
    # Generate vector from description
    vector = model.encode(product['description']).tolist()
    
    # Add vector to product
    product['description_vector'] = vector
    
    # Index the product
    response = client.index(
        index='products_vector',
        id=product['product_id'],
        body=product
    )
    
    print(f"Indexed {product['product_id']}: {response['result']}")

print("\nAll products indexed successfully!")

