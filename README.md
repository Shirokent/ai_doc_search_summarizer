# AI Document Search & Summarizer

A containerized FastAPI service for uploading, indexing, searching, and summarizing text documents using modern NLP techniques.  

## Features
- **Upload documents** via REST API  
- **Search** indexed content with keyword queries  
- **Summarize** search results into concise responses  

## Tech Stack
- **FastAPI** for API endpoints  
- **Uvicorn** as ASGI server  
- **Python 3.10**  
- **Docker & docker-compose** for containerization  
- **NLP libraries** for embeddings and summarization  

## Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Setup
```bash
cp .env.example .env
docker compose up --build
```

The API will be available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- OpenAPI spec: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)  

### Example Usage
1. **Upload a file**  
   ```
   POST /upload/
   ```
   Form-data with `file=@yourfile.txt`

2. **Search content**  
   ```
   GET /search/?query=example
   ```

3. **Summarize results**  
   ```
   GET /summarize/?query=example
   ```

## Development
- Update dependencies in `requirements.txt`
- Rebuild with:
  ```bash
  docker compose up --build
  ```

## License
MIT License  
