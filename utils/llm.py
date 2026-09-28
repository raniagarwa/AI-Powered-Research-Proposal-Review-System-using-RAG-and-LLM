import os
import time
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_llm(context, question):
    """
    Send context and question to Gemini.
    """

    prompt = f"""
    You are an experienced university professor reviewing a research proposal.

    Your task is to answer the user's question using ONLY the information provided in the context below.

    Rules:
    1. Use only the provided context.
    2. Do not use outside knowledge.
    3. Do not guess or invent information.
    4. If the answer is not found in the context, reply exactly:
       "The uploaded proposal does not contain enough information to answer this question."
    5. Keep the answer concise and well structured.
    6. Use bullet points whenever appropriate.

    Context:
    {context}
  
    Question:
    {question}

    Answer:
    """

    try:

        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )

                return response.text

            except Exception as e:

                error = str(e)

                if "503" in error or "UNAVAILABLE" in error:

                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue

                    return "⚠️ Gemini service is temporarily unavailable. Please try again in a few minutes."

                elif "429" in error:
                    return "⚠️ Gemini API quota exceeded. Please wait and try again later."

                else:
                    return f"Unexpected Error:\n{error}"

    except Exception as e:
        return f"Unexpected Error:\n{str(e)}"

        if "503" in error or "UNAVAILABLE" in error:
            return "⚠️ Gemini service is temporarily unavailable. Please try again in a few minutes."

        elif "429" in error:
            return "⚠️ Gemini API quota exceeded. Please wait and try again later."

        else:
            return f"Unexpected Error:\n{error}"