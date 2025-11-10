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

- **Docker Desktop** 4.x+
- **4 GB RAM** free (8 GB recommended)
- **Python 3.8+** (only for vector search examples in Section 16)
- **Browser** (Chrome/Firefox)
- Basic understanding of REST APIs and JSON

## Quick Start

### 1. Set Up OpenSearch Cluster

> **Note**: This setup uses a development Docker Compose file with security disabled. **This configuration should only be used in test environments.**

1. Create a directory for your OpenSearch cluster:

```bash
mkdir opensearch-cluster
cd opensearch-cluster
```

2. Create a `docker-compose.yml` file in this directory and copy the contents of the [Docker Compose file for development](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/#sample-docker-compose-file-for-development) into this file.

3. Start the cluster:

```bash
docker compose up -d
```

4. Wait ~30 seconds, then verify that containers are running:

```bash
docker compose ps
```

You should see output similar to:

```
NAME                    COMMAND                  SERVICE               STATUS
opensearch-dashboards   "./opensearch-dashb…"    opensearch-dashboards running
opensearch-node1        "./opensearch-docker…"   opensearch-node1      running
opensearch-node2        "./opensearch-docker…"   opensearch-node2      running
```

5. Verify that OpenSearch is running:

```bash
curl http://localhost:9200
```

You should see JSON with cluster info.

### 2. Access OpenSearch Dashboards

Open `http://localhost:5601/` in your browser.

Go to **Dev Tools** (hamburger menu → Management → Dev Tools) to run queries.

### 3. Follow the Workshop

Open `opensearch_workshop_final.md` and follow along step-by-step.

> **Note**: Section 16 (Vector Search) requires Python 3.8+. Setup instructions are provided in that section.

## Files

- `opensearch_workshop_final.md` - Main workshop document
- `index_products_with_vectors.py` - Generate and index product embeddings
- `search_with_vectors.py` - Search using vector similarity
- `env.example` - Example environment variables for Python scripts

## Cleanup

To stop and remove all containers, run this from your `opensearch-cluster` directory:

```bash
docker compose down -v
```

To remove workshop indexes from OpenSearch, see Section 18 (Teardown) in the workshop document.

## Troubleshooting

See Section 17 in the workshop document for common issues and solutions.

## License

This workshop is provided for educational purposes.

