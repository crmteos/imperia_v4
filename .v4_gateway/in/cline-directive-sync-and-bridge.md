# Directive for Cline: Gateway Restoration & Environment Telemetry Sync

**Target Directory**: `.v4_gateway/in/`
**Directive ID**: `cline-directive-sync-and-bridge`
**Target Agent**: Local Engineer (Cline / Roo Code)
**Execution Protocol**: Single-Pass Autonomous Execution & Git Seal

---

## 🎯 Primary Objective
Perform an infrastructure audit of the local environment following the Windows 11 clean installation and Git configuration, sync the gateway state files, update `.v4_gateway/out/STATE_CONTEXT_BRIDGE.md`, and seal the changes into Git.

---

## 📋 Execution Steps

### Step 1: Environment & Git Verification
1. Open PowerShell terminal in the workspace root (`C:\Users\crmte\OneDrive\Desktop\Projects\imperia_v4`).
2. Run `git status` to inspect current modified and untracked files.
3. Verify that Git configuration is active:
   - `git config user.name` -> should return `DY-github-crypto`
   - `git config user.email` -> should return `141924033+DY-github-crypto@users.noreply.github.com`

### Step 2: Gateway File Synchronization
1. Check contents of `.v4_gateway/in/` and `.v4_gateway/out/`.
2. Update `.v4_gateway/out/STATE_CONTEXT_BRIDGE.md` with the following status entries:
   - **Infrastructure Stack**: Windows 11 Enterprise x64 (Clean Install), Git 2.56.0, Node.js v26.13.0, Python 3.15.2, VS Code + Cline.
   - **Role Level Status**: Active & Configured (Git identity sealed).
   - **Gateway Isolation**: Complete (Separation of Infrastructure Stack from Metaphysical/Mathematical Core).

### Step 3: Git Seal and Synchronization
1. Stage all pending changes:
   ```powershell
   git add .
   ```
2. Commit the changes:
   ```powershell
   git commit -m "chore(gateway): restore gateway bridge telemetry and role-level git configuration"
   ```
3. Push to GitHub:
   ```powershell
   git push origin main
   ```

---

## 📊 Verification & Exit Criteria
- `STATE_CONTEXT_BRIDGE.md` updated in `.v4_gateway/out/`.
- Working directory clean (`git status` shows no untracked/modified files).
- Git push completed successfully to `origin main`.
