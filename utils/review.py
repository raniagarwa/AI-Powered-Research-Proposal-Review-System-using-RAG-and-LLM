from utils.llm import ask_llm


def review_proposal(context):
    """
    Generate a complete review of the uploaded research proposal.
    """

    review_question = """
Review the research proposal and provide the following sections:

1. Research Objective
2. Problem Statement
3. Methodology Summary
4. Strengths
5. Weaknesses
6. Suggestions for Improvement
7. Overall Assessment

If any section is not available in the proposal, clearly mention that the information is not available.

Format the answer using Markdown headings and bullet points.
"""

    return ask_llm(context, review_question)