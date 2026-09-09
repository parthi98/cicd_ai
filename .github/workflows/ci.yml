name: CI Build with AI Optimization

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # Install Ollama to handle open source models locally
      - name: Install Ollama
        run: |
          curl -fsSL https://ollama.com | sh
          # Start the Ollama background engine service
          ollama serve & 
          sleep 5

      # Download your chosen open source model (llama3.3 or qwen2.5-coder)
      - name: Pull Open Source AI Model
        run: ollama pull qwen2.5-coder:7b

      - name: Execute Application Build
        id: run_build
        run: |
          echo "Starting application build dependency validation..."
          pip install -r requirements.txt 2>&1 | tee build_output.log
        continue-on-error: true

      - name: Run Open Source Log Optimization Agent
        if: always()
        run: |
          python .github/scripts/analyze_logs.py build_output.log > ai_suggestions.md
          cat ai_suggestions.md >> $GITHUB_STEP_SUMMARY
