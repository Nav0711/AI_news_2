import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from vernacular.orchestrator import translate_with_context

try:
    result = translate_with_context(
        title="Reliance Industries Q4 Results",
        content="Reliance Industries reported a net profit of Rs 19,299 crore for the quarter ended March 2024. The telecom and retail segments showed strong growth.",
        language_code="hi",
        include_simplification=False
    )
    print("\n--- Fallback Translation Output ---")
    print(f"Language: {result['language']}")
    print("--- Detailed ---")
    print(result["translated_content"])
except Exception as e:
    print(f"Error: {str(e)}")
