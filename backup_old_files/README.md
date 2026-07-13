# OmniSight AI

AI-powered business intelligence assistant built during internship training.

## Features

* FastAPI backend
* PostgreSQL database
* Dockerized PostgreSQL
* Ollama local LLM
* pgvector vector database
* Semantic search
* Retrieval-Augmented Generation (RAG)

## Endpoints

### Business Summary

GET /business-summary

Returns customer, order and revenue statistics.

### RAG Question Answering

GET /rag/{question}

Uses vector search and Ollama to answer company-related questions.

## Technologies

* Python
* FastAPI
* PostgreSQL
* Docker
* Ollama
* Sentence Transformers
* pgvector
