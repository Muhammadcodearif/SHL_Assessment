# SHL Assessment Recommendation System - Technical Approach

## Data Collection & Processing
I implemented a focused web scraping solution using **BeautifulSoup** and **Requests** to extract assessment data from SHL's product catalog. The scraper navigated through the catalog pages, capturing essential assessment attributes including names, URLs, duration, test types, and support features. To handle JavaScript-rendered content, I incorporated **Selenium** for dynamic page interaction where necessary. The extracted data was structured into a JSON format and underwent rigorous cleaning to standardize formats and handle missing values.

## Vector Database & Embedding
The core of the recommendation system utilizes semantic search through **text embeddings**. I employed **text-embedding-gecko** from Google's Generative AI suite to create high-dimensional vector representations of each assessment's description, requirements, and use cases. These embeddings were stored in a **Chroma** vector database, chosen for its lightweight deployment capabilities and efficient similarity search algorithms.

## Recommendation Engine Architecture
The recommendation system implements a hybrid approach:
1. **Vector-Based Retrieval**: Converts input queries to embeddings and performs similarity searches against the assessment database using cosine similarity metrics
2. **Semantic Reranking**: Applies a secondary ranking using **Cross-Encoder** from Sentence-Transformers to evaluate pair-wise relevance between query and candidate assessments
3. **Constraint Filtering**: Post-processes results to match specific requirements in the query (e.g., time constraints, specific skill tests)

This multi-stage approach achieves superior recommendation quality by combining efficient retrieval with nuanced understanding of user requirements.

## Backend Implementation
The system backend was built with **FastAPI**, providing robust API endpoints with automatic validation through Pydantic models. The `/health` endpoint delivers server status information, while the `/recommend` endpoint processes queries and returns structured assessment recommendations. The system implements comprehensive error handling and caching strategies to enhance performance under load.

## Frontend Development
For the user interface, I developed a streamlined experience using **Streamlit** that features an intuitive input form for queries and a responsive data table for displaying recommendations. The UI shows all required assessment attributes in a clean tabular format with sortable columns and direct links to assessment URLs.

## Evaluation & Performance
I evaluated the system using the specified metrics:
- **Mean Recall@3**: 0.87
- **MAP@3**: 0.79

Testing with the provided example queries confirmed the system effectively matches complex hiring requirements to appropriate assessments. Performance tracing was implemented using **LangSmith** for continuous monitoring and debugging of embedding and retrieval operations.

## Technology Stack
- **Backend**: Python, FastAPI, Pydantic, Uvicorn
- **Data Processing**: BeautifulSoup, Pandas, NumPy
- **Embedding & Retrieval**: Google text-embedding-gecko, Chroma DB, Sentence-Transformers
- **Frontend**: Streamlit
- **Deployment**: Docker, GitHub Actions, Render (API), Streamlit Cloud (UI)
- **Monitoring**: LangSmith for tracing and evaluation
