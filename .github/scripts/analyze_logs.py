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
    
    You MUST format your output into separate stages using Markdown dividers (---).
    Use this exact structural layout:

    # 📊 CI/CD BUILD EXTRACTION SUMMARY
    
    ---
    
    ## 🔍 STAGE 1: LOG ANALYTICS & ERRORS IDENTIFIED
    * **Status:** [State if build succeeded or had explicit compile errors]
    * **Primary Logs Evaluated:** [Briefly note what the log snippet shows]
    
    ---
    
    ## 🚀 STAGE 2: PERFORMANCE BOTTLENECKS
    * **Slow Step Found:** [Detail the specific slow library or network tracking metrics found]
    * **Impact Level:** [High / Medium / Low bottleneck footprint]
    
    ---
    
    ## 💡 STAGE 3: ACTIONABLE OPTIMIZATION PLAYBOOK
    * **Caching Strategy:** [Detail exact cache setup recommendations]
    * **Workflow Speed Changes:** [Detail step improvements or parallel configurations]
    
    Build Log Snippet to Analyze:
    \"\"\"
    {log_content}
    \"\"\"
    """

    host = "127.0.0.1"
    port = 11434
    path = "/api/generate"
    
    headers = {"Content-Type": "application/json"}
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
            print(result['response'])
        else:
            print("### ⚠️ AI Engine Note\nReturned empty content mapping.")
    except Exception as e:
        print(f"### ❌ Local AI Analysis Failed\nError: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <path_to_log_file>")
        sys.exit(1)
    analyze_logs(sys.argv[1])
