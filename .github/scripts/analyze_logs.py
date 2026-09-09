import sys
import os
import http.client
import json

def analyze_logs(log_file_path):
    # Ensure log_file_path is treated as a clean string path
    if not os.path.exists(log_file_path):
        print(f"### ⚠️ Error: Build log file not found at path: {log_file_path}")
        return

    with open(log_file_path, 'r', encoding='utf-8') as f:
        log_lines = f.readlines()
        log_content = "".join(log_lines[-500:])

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("### ❌ Error: GEMINI_API_KEY environment variable is missing.")
        return

    prompt = f"""
    You are an expert DevOps and Performance Engineer. 
    Analyze the following CI/CD build log. Identify bottlenecks, slow steps, 
    caching inefficiencies, or compilation errors. 
    
    Provide your output formatted strictly in Clean Markdown with two clear sections:
    1. ### 🚀 Performance Bottlenecks / Errors Identified
    2. ### 💡 Actionable Optimization Suggestions
    
    Build Log Snippet:
    \"\"\"
    {log_content}
    \"\"\"
    """

    # FIXED: Uses production v1 mapping path with the query parameter token string
    host = "generativelanguage.googleapis.com"
    path = f"/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", path, body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()

        result = json.loads(data)
        
        if 'candidates' in result and len(result['candidates']) > 0:
            markdown_output = result['candidates']['content']['parts']['text']
            print(markdown_output)
        else:
            print("### ⚠️ AI Engine Note\nGemini API connected, but returned empty content structural mapping.")
            print(f"Debug Info: {data}")
            
    except Exception as e:
        print(f"### ❌ AI Analysis Failed\nAn error occurred during Gemini processing: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <path_to_log_file>")
        sys.exit(1)
    # FIXED: Index target specified to grab the actual string parameter 'build_output.log'
    analyze_logs(sys.argv[1])
