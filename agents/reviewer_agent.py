from orchestrator.agent_state import ValidationPoint, SlideValidation, ContentExpansion
from app.dependencies import llm as get_llm
from rag_pipeline.pipeline import RAGPipeline
from typing import List


def ReviewerAgent(state: dict) -> dict:
    """Review and validate expanded content for accuracy"""
    expanded_content = state.get("expanded_content", [])
    context = state.get("context", "")
    topic = state.get("topic", "")

    rag = RAGPipeline()
    try:
        rag.load()
    except:
        pass

    llm = get_llm()
    validated_slides = []

    for slide in expanded_content:
        if not isinstance(slide, ContentExpansion):
            continue

        validations = []

        for point in slide.detailed_points:
            # Query RAG for fact-checking information
            fact_check_context = ""
            try:
                fact_docs = rag.query(point)
                fact_check_context = "\n".join(
                    [doc.page_content for doc in fact_docs[:2]]
                )
            except:
                pass

            prompt = f"""
Review this statement for factual accuracy:

"{point}"

Context: {context}

Reference Information from Knowledge Base:
{fact_check_context}

Compare the statement with the reference information and respond with:
- "accurate" if the statement is factually correct and supported by the reference
- "needs_review" if uncertain, unsupported, or potentially incorrect

If needs_review, provide a brief reason.
"""

            response = llm.invoke(prompt)
            content = response.content.lower()

            if "needs_review" in content:
                status = "needs_review"
                reason = (
                    response.content.split("needs_review", 1)[1].strip()
                    if "needs_review" in response.content
                    else "Requires fact checking"
                )
            else:
                status = "accurate"
                reason = None

            validations.append(
                ValidationPoint(point=point, status=status, reason=reason)
            )

        validated_slides.append(
            SlideValidation(title=slide.title, validation=validations)
        )

    return {"validated_content": validated_slides}
