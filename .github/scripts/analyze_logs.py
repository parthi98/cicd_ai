import sys
import os
import http.client
import json

def analyze_logs(log_file_path):
    if not os.path.exists(log_file_path):
        print(f"### ⚠️ Error: Build log file not found at path: {log_file_path}")
        return

    with open(log_file_path, 'r', encoding='utf-8') as f:
        log_lines = f.readlines()
        log_content = "".join(log_lines[-500:])

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

    # POINTING TO LOCAL OLLAMA CONNECTION
    host = "127.0.0.1"
    port = 11434
    path = "/api/generate"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False
    }

    try:
        conn = http.client.HTTPConnection(host, port)
        conn.request("POST", path, body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()

        result = json.loads(data)
        
        if 'response' in result:
            markdown_output = result['response']
            print(markdown_output)
        else:
            print("### ⚠️ AI Engine Note\nLocal open-source model connected, but returned empty content mapping.")
            print(f"Debug Info: {data}")
            
    except Exception as e:
        print(f"### ❌ Local AI Analysis Failed\nAn error occurred during local model processing: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <path_to_log_file>")
        sys.exit(1)
    # Safely extract target string parameter
    analyze_logs(sys.argv[1])
