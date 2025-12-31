from orchestrator.agent_state import PPTAgentState, SlideValidation
from app.dependencies import llm as get_llm, get_rag_pipeline


def ReviewerAgent(state: PPTAgentState) -> PPTAgentState:
    """Review and validate expanded content for accuracy"""
    expanded_content = state.expanded_content
    topic = state.topic

    # Get RAG context once for all validations
    rag_context = ""
    try:
        rag = get_rag_pipeline()
        relevant_docs = rag.query(topic)
        rag_context = "\n\n".join([doc.page_content for doc in relevant_docs[:5]])
    except:
        pass

    # Use structured output for validation
    llm = get_llm()

    # Loop through each slide and validate individually
    all_validations = []

    for slide in expanded_content:
        # Build single slide text
        slide_text = f"Slide: {slide.title}\nContent:\n" + "\n".join(
            f"- {point}" for point in slide.detailed_points
        )

        # Create structured LLM for single slide validation
        structured_llm = llm.with_structured_output(SlideValidation)

        prompt = f"""Review each statement in this slide for factual accuracy.

Topic: {topic}

{slide_text}

Reference Information:
{rag_context}

For each statement, validate if it's factually correct and supported by the reference information.
- Mark as "accurate" if factually correct and supported
- Mark as "needs_review" if uncertain, unsupported, or potentially incorrect (provide reason)

Validate all statements in this slide."""

        result = structured_llm.invoke(prompt)
        all_validations.append(result)

    state.validation_results = all_validations
    return state
