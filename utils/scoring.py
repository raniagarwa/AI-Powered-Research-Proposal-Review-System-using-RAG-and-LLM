import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def score_proposal(context):
    """
    Generate scores for different aspects of the research proposal.
    """

    prompt = f"""
You are an expert professor evaluating a research proposal.

Evaluate ONLY the proposal provided below.

Proposal:
{context}

Give scores (out of 10) for:

1. Novelty
2. Technical Quality
3. Methodology
4. Clarity
5. Feasibility

Also provide:

- Overall Score (out of 10)
- A short justification for each score.

If any category cannot be evaluated because the proposal lacks sufficient information,
write "Insufficient information" for that category instead of guessing.

Format the output using Markdown headings and bullet points.
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"