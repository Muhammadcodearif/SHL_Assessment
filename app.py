import streamlit as st
import requests
import json
import re
import pandas as pd
from urllib.parse import urlparse
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables!")
    st.stop()

genai.configure(api_key=api_key)

# Create a FastAPI app instance
app = FastAPI(title="SHL Assessment Recommendation API", 
              description="API for recommending SHL assessments based on job descriptions",
              version="1.0.0")

# Define models
class AssessmentRecommendation(BaseModel):
    name: str
    url: str
    remote_testing: bool
    adaptive_irt_support: bool
    duration: str
    test_type: str
    relevance_score: float

class RecommendationResponse(BaseModel):
    recommendations: List[AssessmentRecommendation]
    query: str

class RecommendationRequest(BaseModel):
    query: str

# Load SHL product data
def load_shl_data():
    # In a real application, this would scrape or load from the SHL catalog
    # For demonstration, we'll use a sample dataset
    data = [
        {
            "name": "Verify G+ General Ability",
            "url": "https://www.shl.com/solutions/products/verify-g-plus/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "24 minutes",
            "test_type": "Cognitive Ability"
        },
        {
            "name": "Verify Numerical Ability",
            "url": "https://www.shl.com/solutions/products/verify-numerical/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "18 minutes",
            "test_type": "Numerical Reasoning"
        },
        {
            "name": "Java Programming Test",
            "url": "https://www.shl.com/solutions/products/java-programming/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "40 minutes",
            "test_type": "Technical Skills"
        },
        {
            "name": "Python Programming Test",
            "url": "https://www.shl.com/solutions/products/python-programming/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "45 minutes",
            "test_type": "Technical Skills"
        },
        {
            "name": "SQL Assessment",
            "url": "https://www.shl.com/solutions/products/sql-assessment/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "35 minutes",
            "test_type": "Technical Skills"
        },
        {
            "name": "JavaScript Assessment",
            "url": "https://www.shl.com/solutions/products/javascript-assessment/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "30 minutes",
            "test_type": "Technical Skills"
        },
        {
            "name": "OPQ Leadership Report",
            "url": "https://www.shl.com/solutions/products/opq-leadership/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "25 minutes",
            "test_type": "Personality"
        },
        {
            "name": "Situational Judgement Test",
            "url": "https://www.shl.com/solutions/products/situational-judgement/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "30 minutes",
            "test_type": "Behavioral Assessment"
        },
        {
            "name": "Business Analyst Assessment",
            "url": "https://www.shl.com/solutions/products/business-analyst/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "45 minutes",
            "test_type": "Role-specific"
        },
        {
            "name": "Data Science Assessment",
            "url": "https://www.shl.com/solutions/products/data-science/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "50 minutes",
            "test_type": "Technical Skills"
        },
        {
            "name": "Communication Skills Assessment",
            "url": "https://www.shl.com/solutions/products/communication-skills/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "20 minutes",
            "test_type": "Soft Skills"
        },
        {
            "name": "Teamwork Assessment",
            "url": "https://www.shl.com/solutions/products/teamwork-assessment/",
            "remote_testing": True,
            "adaptive_irt_support": False,
            "duration": "15 minutes",
            "test_type": "Soft Skills"
        },
        {
            "name": "Full-Stack Developer Assessment",
            "url": "https://www.shl.com/solutions/products/fullstack-developer/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "60 minutes",
            "test_type": "Technical Skills"
        },
        {
            "name": "Critical Thinking Assessment",
            "url": "https://www.shl.com/solutions/products/critical-thinking/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "25 minutes",
            "test_type": "Cognitive Ability"
        },
        {
            "name": "Analytical Thinking Assessment",
            "url": "https://www.shl.com/solutions/products/analytical-thinking/",
            "remote_testing": True,
            "adaptive_irt_support": True,
            "duration": "35 minutes",
            "test_type": "Cognitive Ability"
        }
    ]
    return data

# Function to extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        else:
            return None
    except Exception as e:
        return None

# Function to recommend assessments using Gemini
def recommend_assessments(query, max_recommendations=10):
    shl_data = load_shl_data()
    
    # Use Gemini to match the query with appropriate assessments
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Given the following job description or query: 
        
        "{query}"
        
        And the following list of available SHL assessments:
        
        {json.dumps(shl_data, indent=2)}
        
        Recommend at most {max_recommendations} SHL assessments (minimum 1) that would be most relevant for evaluating candidates based on this job description or query.
        
        For each assessment, assign a relevance score between 0.0 and 1.0, where 1.0 is most relevant.
        
        Return your response in JSON format with the following structure:
        {{
            "recommendations": [
                {{
                    "name": "Assessment Name",
                    "url": "Assessment URL",
                    "remote_testing": true/false,
                    "adaptive_irt_support": true/false,
                    "duration": "Duration",
                    "test_type": "Test Type",
                    "relevance_score": 0.95
                }},
                ...
            ]
        }}
        
        Ensure the recommendations are ordered by relevance_score in descending order.
        Only include the JSON in your response, no additional text.
        """
        
        response = model.generate_content(prompt)
        
        # Extract JSON from the response
        response_text = response.text
        
        # Try to find JSON in the response using regex
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response_text
            
        # Clean the string and parse JSON
        result = json.loads(json_str)
        
        # Ensure we have at most max_recommendations
        recommendations = result.get("recommendations", [])
        if len(recommendations) > max_recommendations:
            recommendations = recommendations[:max_recommendations]
            
        # Ensure we have at least 1 recommendation
        if not recommendations:
            # Default to the first assessment if no matches
            recommendations = [
                {**shl_data[0], "relevance_score": 0.5}
            ]
            
        return {"recommendations": recommendations, "query": query}
        
    except Exception as e:
        print(f"Error in recommendation: {str(e)}")
        # Return a default assessment if there's an error
        return {
            "recommendations": [
                {**shl_data[0], "relevance_score": 0.5}
            ],
            "query": query
        }

# API Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    result = recommend_assessments(request.query)
    return result

# Streamlit App
def main():
    st.set_page_config(
        page_title="SHL Assessment Recommendation System",
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("SHL Assessment Recommendation System")
    st.markdown("""
    This application helps hiring managers find the right SHL assessments for their job openings.
    Enter a job description or search query below to get relevant recommendations.
    """)
    
    # Input options
    input_type = st.radio(
        "Select input type:",
        ["Natural Language Query", "Job Description URL"]
    )
    
    query = ""
    
    if input_type == "Natural Language Query":
        query = st.text_area(
            "Enter your requirements:",
            height=150,
            placeholder="Example: I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes."
        )
    else:
        url = st.text_input(
            "Enter job description URL:",
            placeholder="https://example.com/job-description"
        )
        if url:
            if not urlparse(url).scheme:
                st.error("Please enter a valid URL including http:// or https://")
            else:
                with st.spinner("Extracting text from URL..."):
                    text = extract_text_from_url(url)
                    if text:
                        query = text
                        st.success("Successfully extracted text from URL")
                        st.expander("View extracted text").write(text[:500] + "..." if len(text) > 500 else text)
                    else:
                        st.error("Failed to extract text from the provided URL")
    
    submit_button = st.button("Get Recommendations")
    
    if submit_button and query:
        with st.spinner("Generating recommendations..."):
            result = recommend_assessments(query)
            
            # Display results
            st.subheader("Recommended Assessments")
            
            recommendations = result.get("recommendations", [])
            
            if recommendations:
                # Convert to DataFrame for better display
                df = pd.DataFrame(recommendations)
                
                # Format the DataFrame
                df_display = df.copy()
                df_display['relevance_score'] = df_display['relevance_score'].apply(lambda x: f"{x:.2f}")
                
                # Create clickable links
                def make_clickable(val):
                    return f'<a href="{val}" target="_blank">{val}</a>'
                
                df_display['url'] = df_display['url'].apply(make_clickable)
                
                # Display as HTML to enable clickable links
                st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
                
                # Alternative display as a Streamlit table (without clickable links)
                st.subheader("Assessment Details")
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"{i}. {rec['name']} - Relevance: {rec['relevance_score']:.2f}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Assessment:** {rec['name']}")
                            st.markdown(f"**URL:** [{rec['url']}]({rec['url']})")
                            st.markdown(f"**Duration:** {rec['duration']}")
                        with col2:
                            st.markdown(f"**Remote Testing:** {'Yes' if rec['remote_testing'] else 'No'}")
                            st.markdown(f"**Adaptive/IRT Support:** {'Yes' if rec['adaptive_irt_support'] else 'No'}")
                            st.markdown(f"**Test Type:** {rec['test_type']}")
            else:
                st.error("No recommendations found for the given query.")
    
    # API information
    st.sidebar.header("API Information")
    st.sidebar.markdown("""
    ### Available Endpoints:
    
    #### 1. Health Check
    - Endpoint: `/health`
    - Method: GET
    - Response: `{"status": "healthy"}`
    
    #### 2. Recommendations
    - Endpoint: `/recommend`
    - Method: POST
    - Request Body:
    ```json
    {
        "query": "Your job description or query here"
    }
    ```
    - Response: JSON with recommended assessments
    """)

if __name__ == "__main__":
    main()