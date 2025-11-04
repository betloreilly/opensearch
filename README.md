# OpenSearch Advanced Workshop

A comprehensive hands-on workshop for building production-ready search systems with OpenSearch.

## What You'll Learn

- Core OpenSearch concepts (indexes, mappings, analyzers)
- Full-text search with relevance tuning
- Aggregations for real-time analytics
- Vector search and hybrid search
- Performance optimization and scaling
- Production best practices

## Prerequisites

- Docker & Docker Compose
- Python 3.8+ (for vector search examples)
- Basic understanding of REST APIs and JSON

## Quick Start

### 1. Start OpenSearch

```bash
docker-compose up -d
```

Wait ~30 seconds for OpenSearch to start, then verify:

Security disabled (dev):

```bash
curl http://localhost:9200
```

Security enabled:

```bash
curl -k -u admin:MyStrongPassword123! https://localhost:9200
```

### 2. Access OpenSearch Dashboards

Security disabled (dev): `http://localhost:5601`

Security enabled: `https://localhost:5601` (admin / MyStrongPassword123!)

### 3. Follow the Workshop

Open `opensearch_workshop_final.md` and follow along step-by-step.

## Vector Search Setup

For the vector search section (Section 16), you'll need Python:

### 1. Create a virtual environment

```bash
python3 -m venv opensearch-venv
source opensearch-venv/bin/activate  # On Windows: opensearch-venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install sentence-transformers opensearch-py
```

### 3. Set up environment variables (optional)

For production or custom setups, create a `.env` file:

```bash
cp env.example .env
# Edit .env if you use security-enabled clusters
```

### 4. Run the vector search scripts

```bash
# Index products with embeddings
python index_products_with_vectors.py

# Search with vectors
python search_with_vectors.py
```

## Connection Profiles

The examples work with both dev (security disabled) and secure clusters.

- Dev (security disabled): no username/password, `http://localhost:9200`
- Secure: basic auth over HTTPS

The Python scripts read these environment variables if present:

- `OPENSEARCH_URL` (default: `http://localhost:9200`)
- `OPENSEARCH_USERNAME` (optional)
- `OPENSEARCH_PASSWORD` (optional)
- `OPENSEARCH_VERIFY_CERTS` (default: `false` for http, `true` for https)

If `OPENSEARCH_USERNAME`/`OPENSEARCH_PASSWORD` are not set, the scripts connect without auth.

## Security Notes (production)

1. Change defaults and rotate credentials
2. Use TLS with valid certificates
3. Assign least-privilege roles

## Files

- `opensearch_workshop_final.md` - Main workshop document
- `docker-compose.yml` - OpenSearch cluster setup
- `index_products_with_vectors.py` - Generate and index product embeddings
- `search_with_vectors.py` - Search using vector similarity
- `env.example` - Example environment variables file

## Cleanup

To stop and remove all containers:

```bash
docker-compose down -v
```

## Troubleshooting

See Section 17 in the workshop document for common issues and solutions.

## License

This workshop is provided for educational purposes.

