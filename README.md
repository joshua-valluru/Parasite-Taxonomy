# Manakin Parasite Taxonomy Retrieval Pipeline

This repository contains a retrieval pipeline for the Manakin Parasite Taxonomy project, including preprocessing steps. The system is designed to allow users to upload parasite dye sample data and retrieve the most relevant samples using similarity search.

## Getting Started

To launch the app and try it out locally:

```bash
uvicorn app.main:app --reload
```

Once the server is running, open your browser and navigate to:

```
http://localhost:8000/docs
```

This will bring up the interactive Swagger UI where you can explore and test the API routes.

## Setup Instructions

Before running the app, make sure to set up your `.env` file with the following required values:

- `PINECONE_API_KEY`: Your API key for the vector store.
- `PINECONE_ENV`: The region of the vector store.
- `PINECONE_INDEX_NAME`: The name of the index to use for retrieval.

The `.env` file should be placed in the root directory of the project.

Example `.env` file:
```env
PINECONE_API_KEY=your-api-key-here
PINECONE_ENV=us-west-1
PINECONE_INDEX_NAME=manakin-parasite-index
```

## License

MIT License
