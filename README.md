# SHL Assessment Recommendation System

This application helps hiring managers find relevant SHL assessments based on job descriptions or natural language queries.

## Features

- Natural language query input
- Job description URL extraction
- Recommendations of up to 10 relevant SHL assessments
- Assessment details in a tabular format
- API endpoint for programmatic access

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (https://ai.google.dev/gemini-api/docs/get-started)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/shl-recommendation-system.git
   cd shl-recommendation-system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your browser and navigate to http://localhost:8501

### Using the API

The application provides a FastAPI backend with two endpoints:

1. Health Check:
   ```
   GET /health
   ```

2. Get Recommendations:
   ```
   POST /recommend
   Content-Type: application/json
   
   {
     "query": "Your job description or query"
   }
   ```

To start the API server separately:
```
uvicorn app:app --reload
```

## Approach

This application uses:

1. **Google's Gemini Pro API** for semantic understanding and matching of job requirements to assessment characteristics
2. **Streamlit** for the user interface
3. **FastAPI** for the API endpoints
4. **BeautifulSoup** for URL content extraction
5. **Pandas** for data manipulation and display

The recommendation engine analyzes the job description or query, extracts key requirements and skills, and matches them with SHL's assessment catalog based on:
- Technical skills required
- Time constraints
- Assessment types needed
- Role-specific requirements

## Evaluation Metrics

The system is designed with the following evaluation metrics in mind:
- Mean Recall@3: Measures how many relevant assessments are retrieved in the top 3 recommendations
- MAP@3: Evaluates both relevance and ranking order of retrieved assessments
