import sys
import os
from openai import OpenAI

def analyze_logs(log_file_path):
    if not os.path.exists(log_file_path):
        print("### ⚠️ Error: Build log file not found.")
        return

    with open(log_file_path, 'r', encoding='utf-8') as f:
        log_lines = f.readlines()
        # Grab the last 500 lines to prevent hitting AI token limits
        log_content = "".join(log_lines[-500:])

    # The library automatically looks for the OPENAI_API_KEY env variable
    client = OpenAI()

    prompt = f"""
    You are an expert DevOps and Performance Engineer. 
    Analyze the following CI/CD build log. Identify bottlenecks, slow steps, 
    caching inefficiencies, or compilation errors. 
    
    Provide your output formatted strictly in Clean Markdown with two clear sections:
    1. ### 🚀 Performance Bottlenecks / Errors Identified
    2. ### 💡 Actionable Optimization Suggestions (Include exact code/config changes if applicable)
    
    Build Log Snippet:
    \"\"\"
    {log_content}
    \"\"\"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # You can use gpt-4o-mini to save costs
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        print(response.choices.message.content)
    except Exception as e:
        print(f"### ❌ AI Analysis Failed\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <path_to_log_file>")
        sys.exit(1)
    analyze_logs(sys.argv[1])
