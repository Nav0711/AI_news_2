import os

files_to_update = [
    "backend/api/main.py",
    "backend/rag/llm_gemini.py",
    "backend/vernacular/translator.py",
    "backend/vernacular/orchestrator.py",
    "backend/vernacular/simplifier.py",
    "backend/video/generator.py"
]

for file_path in files_to_update:
    full_path = os.path.join("/Users/navdeeop/Developer/projects/AI_news_2", file_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            content = f.read()
        
        updated_content = content.replace("gemini-1.5-flash", "gemini-2.0-flash")
        updated_content = updated_content.replace("gemini-2.5-flash", "gemini-2.0-flash")
        
        with open(full_path, "w") as f:
            f.write(updated_content)
        print(f"Updated {file_path}")
