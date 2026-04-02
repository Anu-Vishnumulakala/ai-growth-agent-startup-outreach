# AI Growth Agent for Startup Outreach

An AI-powered system that helps prioritize startup leads, rank the best opportunities, and generate personalized outreach messages — turning raw data into clear business decisions.

## Problem

Most teams don’t struggle to find leads.  
They struggle to decide **who to contact first**.

Existing tools provide data, but not clear prioritization.

## Solution

This project builds an **AI Growth Agent** that:

- analyzes startup leads from a CSV file  
- compares them across key business factors  
- ranks them based on real opportunity  
- suggests the best company to contact first  
- generates a ready-to-send outreach message  

## How it works

Each company is evaluated comparatively using:

-  Market size & growth  
-  B2B relevance  
-  Scalability  
-  Outreach potential  

Instead of scoring companies in isolation,  
the system compares them **against each other** to produce meaningful rankings.

## Example Output

From a list of startup leads, the system:

- identifies the highest-priority company  
- explains the reasoning behind the ranking  
- generates a personalized outreach message  

Example:  
Recommends **Doctolib** as the top lead due to strong B2B adoption and scalable healthcare infrastructure.

## Tech Stack

- Python  
- OpenAI API  
- Prompt Engineering  
- Streamlit  
- Pandas

## Project Structure

ai-growth-agent-startup-outreach/
│
├── app.py
├── main.py
├── lead_analyzer.py
├── openai_client.py
├── utils.py
├── sample_leads.csv
├── requirements.txt
└── README.md

## Key Value

This project shows how AI can move beyond content generation and become a decision-support system.

It helps:

reduce manual research
prioritize leads faster
improve outreach efficiency

## How to Run

1. Clone the repository
```bash
git clone https://github.com/your-username/ai-growth-agent-startup-outreach.git
cd ai-growth-agent-startup-outreach

2. Create virtual environment
python -m venv .venv

3. Activate environment
Windows:
        .venv\Scripts\activate
Mac/Linux:
         source .venv/bin/activate

4.Install Dependencies
pip install -r requirements.txt

5. Add OpenAI API key
Create a .env file:
         OPENAI_API_KEY=your_api_key_here

6. Run the app
streamlit run app.py

