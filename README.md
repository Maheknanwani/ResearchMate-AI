# ResearchMate AI
### AI-Powered Research and Analysis Agent

## 1. Project Overview
ResearchMate AI is an AI-powered research assistant that accepts user questions, creates research plans, retrieves information from the web and generates structured research reports using Google Gemini.

## 2. Technologies Used
- Python
- Streamlit
- Google Gemini API
- DuckDuckGo Search
- BeautifulSoup
- Requests
- Pydantic

## 3. System Architecture
The application follows this workflow:

User Question → Gemini Planner → Web Search → Information Filtering → Webpage Reader → Gemini Synthesis → Structured Research Report.

## 4. Key Features
- AI-powered research planning.
- Automated web searching.
- Webpage content extraction.
- Information filtering.
- AI-generated research reports.
- Confidence and limitation reporting.
- Downloadable research reports.

## 5. Tools
**Tool 1: Web Search**  
Uses DuckDuckGo to retrieve relevant web search results.

**Tool 2: Webpage Reader**  
Uses Requests and BeautifulSoup to extract webpage content.

## 6. Error Handling
The application handles search failures, inaccessible webpages, missing API keys and AI generation errors using exception handling and fallback planning.

## 7. Installation
1. Install Python.
2. Clone the repository.
3. Create a virtual environment.
4. Install dependencies using `pip install -r requirements.txt`.
5. Create a `.env` file and configure your Gemini API key.
6. Run `streamlit run app.py`.

## 8. Limitations
- Search results depend on internet availability.
- Some websites block automated access.
- Source filtering uses basic domain-based filtering.
- AI-generated findings require independent verification.

## 9. Future Improvements
- Advanced source credibility scoring.
- Claim-level citation verification.
- Research history and caching.
- Automated evaluation.
- Improved observability and performance monitoring.

## 10. AI Tool Disclosure
Google Gemini is used for research planning and report synthesis. AI coding assistance was used during development; the code was reviewed, tested and modified as part of the implementation.
