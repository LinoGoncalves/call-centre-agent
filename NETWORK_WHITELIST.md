# Call Centre Agent - Package Whitelist for Network Team

## Core Python Packages (for pip install)
streamlit
plotly
pandas
numpy
google-generativeai
python-dotenv
pinecone-client
openai
backoff
fastapi
uvicorn
pydantic
scikit-learn
PyYAML
beautifulsoup4
lxml
markupsafe
requests
pathlib2
pytest
pytest-cov

## Package Repository URLs (for firewall/proxy configuration)
https://pypi.org/
https://pypi.org/simple/
https://files.pythonhosted.org/

## API Endpoints (for runtime access)
# Google Gemini API
https://generativelanguage.googleapis.com/
https://ai.google.dev/

# Pinecone Vector Database
https://api.pinecone.io/
https://*.pinecone.io/

# OpenAI API (for embeddings)
https://api.openai.com/

## Download Sources (during pip install)
# PyPI package index
pypi.org
files.pythonhosted.org
pypi.python.org

# Package dependencies may pull from
github.com (for some packages)
raw.githubusercontent.com

## Required Ports
# HTTPS for API calls and package downloads
Port 443 (HTTPS)
Port 80 (HTTP - redirects to HTTPS)

## Local Application
# Streamlit demo server
localhost:8502

# FastAPI health endpoints  
localhost:8000

## Optional (for enhanced features)
# Ollama local LLM (if implemented)
localhost:11434