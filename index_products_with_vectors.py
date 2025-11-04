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

# Initialize the embedding model (384 dimensions)
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

