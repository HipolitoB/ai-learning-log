# Lesson 46: Code execution and the Files API

**Course:** Building with the Claude API (Anthropic Academy — Lesson 46 of 67)  
**Date:** 2026-11-27

## Core Architecture & Workflow

1. **Files API (`upload` / `download`):**
   - Instead of sending large raw files as base64 in every request, you upload a file once to receive a metadata object containing a unique `file_id`.
   - You pass that `file_id` into the message via a `{"type": "container_upload", "file_id": ...}` content block so the isolated Docker container (which has no internet/network access) can read it.
2. **Server-Side Code Execution (`code_execution_20250825`):**
   - Enabled by adding `{"type": "code_execution_20250825", "name": "code_execution"}` to the `tools` parameter alongside `betas=["code-execution-2025-08-25", "files-api-2025-04-14"]`—no client-side execution logic is needed.
   - Claude runs Python iteratively inside the container across multiple steps, returning `server_tool_use` blocks (the Python code executed), `code_execution_tool_result` / `bash_code_execution_tool_result` blocks (`stdout`/`stderr`), and final text explanations.
3. **Retrieving Generated Artifacts:**
   - Any chart, CSV, or report created inside the container is exposed via response blocks containing `"type": "bash_code_execution_output"`, which carry the new `item.file_id` you pass to `client.beta.files.download(item.file_id)`.

## Complete End-to-End Python Implementation

```python
import anthropic

client = anthropic.Anthropic()

# 1. Upload streaming.csv via the Files API
with open("streaming.csv", "rb") as f:
    file_metadata = client.beta.files.upload(
        file=("streaming.csv", f, "text/csv"),
    )

# 2. Send the container_upload block + enable the code_execution tool
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "files-api-2025-04-14"],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Run a detailed analysis to determine major drivers of"
                        " churn. Your final output should include at least one"
                        " detailed plot summarizing your findings."
                    ),
                },
                {"type": "container_upload", "file_id": file_metadata.id},
            ],
        }
    ],
)

# 3. Inspect text blocks and download any generated plot files
for block in response.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "bash_code_execution_tool_result":
        content = block.content
        if hasattr(content, "content"):
            for item in content.content:
                if getattr(item, "type", None) == "bash_code_execution_output":
                    output_data = client.beta.files.download(item.file_id)
                    with open(f"{item.file_id}.png", "wb") as out:
                        out.write(output_data.read())
                    print(f"Saved generated file: {item.file_id}.png")
```
