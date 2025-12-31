from agents.outline_generator_agent import OutlineAgent
from agents.content_expansion_agent import ContentExpansionAgent
from agents.reviewer_agent import ReviewerAgent
from agents.export_agent import ExportAgent
from orchestrator.agent_state import PPTAgentState

# Initialize Pydantic state
state = PPTAgentState(topic="Agentic AI using langchain", slides=7)

print("=" * 80)
print("STEP 1: OUTLINE GENERATION")
print("=" * 80)

# Run Outline Agent
state = OutlineAgent(state)

print(f"\nTopic: {state.topic}")
print(f"Number of slides: {len(state.outline.slides)}\n")

for i, slide in enumerate(state.outline.slides, 1):
    print(f"Slide {i}: {slide.title}")
    for bullet in slide.bullet_points:
        print(f"  • {bullet}")
    print()

print("\n" + "=" * 80)
print("STEP 2: CONTENT EXPANSION")
print("=" * 80)

# Run Content Expansion Agent
state = ContentExpansionAgent(state)

for i, slide in enumerate(state.expanded_content, 1):
    print(f"\nSlide {i}: {slide.title}")
    print("-" * 60)
    for j, point in enumerate(slide.detailed_points, 1):
        print(f"{j}. {point}")
    print()

print("\n" + "=" * 80)
print("STEP 3: CONTENT VALIDATION")
print("=" * 80)

# Run Reviewer Agent
state = ReviewerAgent(state)

accurate_count = 0
review_count = 0


for i, slide in enumerate(state.validation_results, 1):
    print(f"\nSlide {i}: {slide.title}")
    print("-" * 60)
    for j, validation in enumerate(slide.validation, 1):
        status_icon = "✓" if validation.status == "accurate" else "⚠"
        print(f"{status_icon} Statement {j}: {validation.status.upper()}")
        print(f"   {validation.point[:100]}...")
        if validation.reason:
            print(f"   Reason: {validation.reason}")
        print()

        if validation.status == "accurate":
            accurate_count += 1
        else:
            review_count += 1

print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print(f"✓ Accurate: {accurate_count} | ⚠ Needs review: {review_count}")

print("\n" + "=" * 80)
print("STEP 4: EXPORT TO POWERPOINT")
print("=" * 80)

# Run Export Agent (works directly with validation results)
state = ExportAgent(state)

print("\n" + "=" * 80)
print("✓ PIPELINE COMPLETE - ALL 4 AGENTS EXECUTED SUCCESSFULLY")
print("=" * 80)
print("=" * 80)
