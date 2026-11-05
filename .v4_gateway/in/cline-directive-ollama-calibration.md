# Directive: Local AI (Ollama + qwen2.5-coder) Calibration & Optimization

**Target**: Role Level AI Executor (Cline / VS Code)
**Goal**: Calibrate local Ollama engine, expand context window to 32,768 tokens, establish `.clinerules` for JSON tool-calling syntax, and eliminate model freezing.

---

## 1. System Diagnosis & Prerequisites

When running `qwen2.5-coder` via Ollama's OpenAI-compatible endpoint (`http://localhost:11434/v1`), two bottlenecks cause freezing or raw JSON text dumping:
1. **Default Context Truncation**: Ollama defaults to a 2,048-token context window unless explicitly instructed via a custom Modelfile (`num_ctx 32768`).
2. **Tool-Calling Syntax Drift**: Open-weights 7B models require explicit system constraints (`.clinerules`) to output strict tool-call JSON blocks without surrounding conversational prose.

---

## 2. Step-by-Step Calibration Tasks for Cline

### Step 1 — Ollama Context Window Expansion (32k Modelfile)
In the terminal, execute the following commands to create a dedicated 32k-context model alias:
```powershell
# Create temporary Modelfile
Set-Content -Path "Modelfile.qwen32k" -Value "FROM qwen2.5-coder:latest`nPARAMETER num_ctx 32768"

# Register 32k model alias in Ollama
ollama create qwen2.5-coder-32k -f Modelfile.qwen32k

# Clean up temporary Modelfile
Remove-Item "Modelfile.qwen32k"
```

### Step 2 — Project Root `.clinerules` Verification
Ensure `.clinerules` in the root of `imperia_v4` contains the following strict execution rules for local models:
```markdown
# Local LLM Execution Rules (Ollama / qwen2.5-coder)

1. **Tool Calling Precision**:
   - Output exactly ONE tool call block per turn.
   - Ensure all JSON argument objects are valid and closed before ending response.
   - Do not wrap tool calls in conversational preamble or extra markdown blocks.

2. **Terminal & File Hygiene**:
   - Use absolute or standard workspace-relative paths (`.v4_gateway/in/`, `.v4_gateway/out/`).
   - Run commands non-interactively. Avoid commands requiring stdin input.

3. **Gateway Protocol**:
   - Read directives from `.v4_gateway/in/`.
   - Record final telemetry to `.v4_gateway/out/STATE_CONTEXT_BRIDGE.md`.
```

### Step 3 — Cline Settings Profile (Ollama Mode)
When switching Cline to local Ollama execution:
- **API Provider**: `OpenAI Compatible`
- **Base URL**: `http://localhost:11434/v1`
- **API Key**: `ollama` (or leave empty/dummy)
- **Model ID**: `qwen2.5-coder-32k`
- **Context Window**: `32768`

---

## 3. Verification & Gateway State Logging

After completing Steps 1 and 2:
1. Verify model availability: `ollama list`
2. Update `.v4_gateway/out/STATE_CONTEXT_BRIDGE.md` under **Local AI Engine Status**:
   - `Ollama Engine`: Active on `http://localhost:11434`
   - `Calibrated Model`: `qwen2.5-coder-32k` (Context: 32,768 tokens)
   - `.clinerules`: Configured & Active
3. Seal changes in Git:
   ```powershell
   git add .
   git commit -m "chore(ollama): calibrate qwen2.5-coder-32k model alias and clinerules"
   git push origin main
   ```
