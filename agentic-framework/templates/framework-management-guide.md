# Framework Management & Project Initialization Guide

## Overview

This guide explains how to use the agentic SDLC framework across multiple projects while ensuring framework enhancements flow back to the core template for continuous improvement.

## Framework Structure

The agentic SDLC framework has two distinct layers:

### 1. Core Framework (Template Repository)

- **Location**: `<FRAMEWORK_ROOT>` (your template/trunk - see "Deployment Scenarios" section below)
  - Local: `~/projects/agentic-framework` (Linux/Mac) or `C:\projects\agentic-framework` (Windows)
  - PyPI: Installed via `pip install agentic-framework`
  - GitHub: Clone from `https://github.com/<org>/agentic-framework.git`
- **Purpose**: Master template with reusable components
- **Contents**: Agent definitions, development standards, workflow templates, automation scripts
- **Maintenance**: Enhanced based on project learnings and improvements

### 2. Project Instances (Working Copies)

- **Location**: Individual project directories
- **Purpose**: Active development with project-specific customizations
- **Contents**: Framework copy + project-specific code, data, configurations
- **Lifecycle**: Created from template, customized for project, contributes back to template

## Deployment Scenarios

The framework supports multiple deployment models to suit different workflows:

### Scenario 1: Local Development (Single Developer)

**Setup**:
```bash
# Linux/Mac
mkdir -p ~/projects/agentic-framework
cd ~/projects/agentic-framework
git clone https://github.com/<org>/agentic-framework.git .

# Windows
mkdir C:\projects\agentic-framework
cd C:\projects\agentic-framework
git clone https://github.com/<org>/agentic-framework.git .
```

**Environment Variable** (optional but recommended):
```bash
# Linux/Mac: Add to ~/.bashrc or ~/.zshrc
export AGENTIC_FRAMEWORK_ROOT=~/projects/agentic-framework

# Windows: Add to system environment variables
setx AGENTIC_FRAMEWORK_ROOT "C:\projects\agentic-framework"
```

**Usage**:
```bash
cd $AGENTIC_FRAMEWORK_ROOT  # or %AGENTIC_FRAMEWORK_ROOT% on Windows
python scripts/framework_manager.py init my-new-project --type web-app
```

### Scenario 2: PyPI Package Installation (Future)

**Setup**:
```bash
pip install agentic-framework
```

**Usage**:
```bash
# Direct CLI usage
agentic-framework init my-new-project --type api

# Or Python module usage
python -m agentic_framework init my-new-project --type api
```

**Framework Location**: Installed in Python's site-packages (e.g., `~/.local/lib/python3.x/site-packages/agentic_framework/`)

### Scenario 3: GitHub/GitLab Organization Template

**Setup** (one-time by framework maintainer):
```bash
# Create template repository
git clone https://github.com/<org>/agentic-framework.git agentic-framework-template
cd agentic-framework-template
git remote set-url origin https://github.com/<org>/agentic-framework-template.git
git push -u origin main

# Mark as template in GitHub/GitLab repository settings
```

**Usage** (by team members):
```bash
# Use "Use this template" button in GitHub/GitLab UI
# Or via GitHub CLI
gh repo create my-new-project --template <org>/agentic-framework-template

# Or via git clone
git clone https://github.com/<org>/agentic-framework-template.git my-new-project
cd my-new-project
python scripts/framework_manager.py init my-new-project --type dashboard
```

### Scenario 4: Docker Container (Portable Development Environment)

**Setup**:
```bash
# Pull pre-configured container with framework
docker pull <org>/agentic-framework:latest

# Or build locally
docker build -t agentic-framework .
```

**Usage**:
```bash
# Run interactive container
docker run -it -v $(pwd):/workspace agentic-framework bash

# Inside container
cd /workspace
agentic-framework init my-new-project --type ml-model
```

### Scenario 5: Multi-Project Workspace

**Setup**:
```bash
# Recommended structure for multiple projects sharing framework
workspace/
├── agentic-framework/          # Shared framework (git submodule or clone)
├── project-a/                   # Project A
│   └── .agentic-framework/     # -> symlink or submodule to ../agentic-framework
├── project-b/                   # Project B
│   └── .agentic-framework/     # -> symlink or submodule to ../agentic-framework
└── project-c/                   # Project C
    └── .agentic-framework/     # -> symlink or submodule to ../agentic-framework
```

**Implementation**:
```bash
# Linux/Mac: Use symlinks
cd workspace/project-a
ln -s ../agentic-framework .agentic-framework

# Windows: Use junction or symlink (requires admin)
cd workspace\project-a
mklink /J .agentic-framework ..\agentic-framework

# Or use git submodules for better portability
cd workspace/project-a
git submodule add ../agentic-framework .agentic-framework
```

### Path Placeholders Used in This Guide

Throughout this document, you'll see these generic placeholders:

- **`<FRAMEWORK_ROOT>`**: Root directory of the framework installation
  - Local: `~/projects/agentic-framework` (Linux/Mac) or `C:\projects\agentic-framework` (Windows)
  - PyPI: Python site-packages location
  - Docker: `/opt/agentic-framework` or similar

- **`<FRAMEWORK_REPO_PATH>`**: Path or URL to framework repository
  - Local: `file:///home/user/agentic-framework` or `file:///C:/projects/agentic-framework`
  - GitHub: `https://github.com/<org>/agentic-framework.git`
  - GitLab: `https://gitlab.com/<org>/agentic-framework.git`

- **`<yourorg>`**: Your organization or username in GitHub/GitLab

Replace these placeholders with your actual paths when following the examples.

## Project Initialization Strategies

### Option 1: Framework-as-Submodule (Recommended)

This approach keeps the framework separate from project code while allowing easy updates:

```bash
# Step 1: Create new project directory
mkdir my-new-project
cd my-new-project

# Step 2: Initialize project git repo
git init

# Step 3: Add agentic SDLC as a submodule
# Option A: Local framework repository
git submodule add <FRAMEWORK_REPO_PATH> .agentic-framework
# Examples:
#   git submodule add file:///home/user/agentic-framework .agentic-framework  (Linux/Mac)
#   git submodule add file:///C:/projects/agentic-framework .agentic-framework (Windows)
#
# Option B: GitHub/remote repository
#   git submodule add https://github.com/<org>/agentic-framework.git .agentic-framework

# Step 4: Create project structure
mkdir src tests docs data
mkdir -p config/environments

# Step 5: Create project-specific files
cp .agentic-framework/templates/project-brief-template.md project-brief.md

# Step 6: Initialize project with enhanced CLI (if available)
python .agentic-framework/scripts/framework_manager.py init my-project --type web-app
```

**Advantages**:

- Framework updates can be pulled easily: `git submodule update --remote`
- Clear separation between framework and project code
- Framework improvements can be pushed back to trunk
- Multiple projects share the same framework version or can upgrade independently

### Option 2: Framework-as-Copy (Simpler Setup)

For simpler scenarios where you want full control:

```bash
# Step 1: Use the framework manager (if available)
cd <FRAMEWORK_ROOT>
python scripts/framework_manager.py init my-project --type api --copy

# Or manually copy the framework:
# Linux/Mac:
#   cp -r ~/projects/agentic-framework my-project
# Windows:
#   xcopy C:\projects\agentic-framework my-project /E /I

# This creates a complete copy with:
# - All framework files copied
# - Git repository initialized
# - Project-specific structure created
# - Configuration files customized
```

**Advantages**:

- Self-contained project
- No submodule complexity
- Full customization freedom

**Disadvantages**:

- Manual effort to sync framework improvements
- Framework changes need to be manually merged back

### Option 3: Framework-as-Template-Repo (GitHub/GitLab)

For organizations with multiple teams:

1. **Setup** (done once by framework maintainer):

   ```bash
   # Create template repository from framework
   git clone <FRAMEWORK_REPO_PATH> agentic-framework-template
   # Examples:
   #   git clone ~/projects/agentic-framework agentic-framework-template
   #   git clone https://github.com/<org>/agentic-framework.git agentic-framework-template
   
   cd agentic-framework-template
   # Push to your Git hosting service as template repository
   git remote add origin https://github.com/<yourorg>/agentic-framework-template.git
   git push -u origin main
   ```

2. **Usage** (for each new project):

   ```bash
   # Use "Use this template" button in GitHub/GitLab
   # Or clone and reinitialize:
   git clone https://github.com/<yourorg>/agentic-framework-template.git my-new-project
   cd my-new-project
   
   # If framework_manager.py is available:
   python scripts/framework_manager.py init my-project --type dashboard
   ```

## Recommended Project Structure

```
my-project/
├── .agentic-framework/          # Framework submodule (Option 1)
│   ├── master-agent.md
│   ├── sub-agents/
│   ├── development-standards/
│   ├── scripts/
│   └── quality-gates.md
├── project-brief.md             # Customized from template
├── .agentic-state/              # Project workflow state
│   ├── current-state.json
│   ├── agent-assignments.json
│   └── quality-gates-status.json
├── src/                         # Your project code
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── data/                        # Project-specific data
│   ├── raw/
│   ├── processed/
│   └── external/
├── docs/
│   ├── architecture.md
│   ├── api-documentation.md
│   └── deployment-guide.md
├── config/
│   ├── agentic-config.json      # Project-specific agent config
│   └── environments/
│       ├── development.env
│       ├── staging.env
│       └── production.env
├── agentic-scripts/             # Local automation scripts
│   ├── cli.py                   # Project CLI wrapper
│   └── project_manager.py
└── agentic-enhancements/        # Framework improvements to merge back
    ├── new-agents/
    ├── standard-updates/
    └── script-improvements/
```

## Framework Enhancement Workflow

### 1. Identify Enhancement During Project

During development, you may discover improvements that would benefit the core framework:

```markdown
# File: agentic-enhancements/enhancement-log.md

## Enhancement: Better Error Handling in Agent Integration

- **Date**: 2025-09-24
- **Project**: Customer Analytics Platform
- **Issue**: Agent integration script doesn't handle API timeouts gracefully
- **Solution**: Add retry logic with exponential backoff
- **Files Modified**: scripts/agent_integration.py
- **Impact**: All projects using agent automation
```

### 2. Implement Enhancement in Project Context

```bash
# Create enhancement branch
python agentic-scripts/cli.py enhance "better-error-handling" "Add retry logic to agent integration"

# Implement your improvements
# Test thoroughly in project context
# Document the changes in agentic-enhancements/better-error-handling/
```

### 3. Merge Enhancement Back to Framework

```bash
# For submodule approach
cd .agentic-framework
git checkout -b enhancement/better-error-handling

# Copy your improvements
cp ../agentic-enhancements/better-error-handling/agent_integration.py scripts/

# Commit and create PR
git add .
git commit -m "Enhancement: Add retry logic to agent integration

- Adds exponential backoff for API timeouts
- Improves resilience in agent communication  
- Tested in Customer Analytics Platform project
- Addresses issue: agents failing on network hiccups"

git push origin enhancement/better-error-handling
```

## Practical Usage Commands

### Starting a New Project

```bash
# Option 1: Submodule approach (recommended)
cd <FRAMEWORK_ROOT>
python scripts/framework_manager.py init customer-analytics --type dashboard

# Option 2: Copy approach
python scripts/framework_manager.py init customer-analytics --type dashboard --copy

# Navigate to project
cd customer-analytics

# Check status
python agentic-scripts/cli.py status

# Start workflow
python agentic-scripts/cli.py start
```

### Managing Framework Updates

```bash
# Update framework in submodule project
cd my-project
python agentic-scripts/cli.py update

# Check what changed
git diff HEAD~1 .agentic-framework

# Test with updated framework
python agentic-scripts/cli.py status
```

### Contributing Enhancements

```bash
# In your project directory
# Document enhancement need
python agentic-scripts/cli.py enhance "performance-optimization" "Optimize workflow state persistence"

# Implement and test changes
# ... development work ...

# Prepare for merge back
python agentic-scripts/cli.py merge performance-optimization

# Follow the guided process to create PR
```

## Quality Assurance for Framework Changes

### Before Merging to Framework

1. **Test in Multiple Project Types**:

   ```bash
   # Test enhancement in different project types
   python scripts/framework_manager.py init test-web-app --type web-app
   python scripts/framework_manager.py init test-ml-model --type ml-model
   python scripts/framework_manager.py init test-pipeline --type data-pipeline
   ```

2. **Backward Compatibility Check**:

   ```bash
   # Ensure existing projects still work
   cd existing-project
   python agentic-scripts/cli.py status  # Should work without errors
   ```

3. **Documentation Update**:
   - Update relevant agent files
   - Update development standards if needed
   - Update this guide if process changes

### Framework Release Management

```bash
# In framework repository
git tag -a v1.1.0 -m "Release v1.1.0: Enhanced agent integration with retry logic"
git push origin v1.1.0

# Notify all project teams
# Update template repository if using Option 3
```

## Example: Complete Project Lifecycle

### 1. Project Start

```bash
# Initialize new fintech dashboard project
cd <FRAMEWORK_ROOT>
python scripts/framework_manager.py init fintech-dashboard --type dashboard

cd fintech-dashboard
# Edit project-brief.md with specific requirements
# Commit initial setup
git add . && git commit -m "Initial project setup"
```

### 2. Development Phase

```bash
# Start agentic workflow
python agentic-scripts/cli.py start

# Work with agents through the workflow
# Monitor status
python agentic-scripts/cli.py status

# During development, identify framework improvement
python agentic-scripts/cli.py enhance "streamlit-components" "Add reusable Streamlit components for financial charts"
```

### 3. Enhancement Implementation

```bash
# Implement the enhancement
# Create: agentic-enhancements/streamlit-components/financial_charts.py
# Document: agentic-enhancements/streamlit-components/README.md
# Test in project context
```

### 4. Contributing Back

```bash
# Prepare enhancement for framework
python agentic-scripts/cli.py merge streamlit-components

# Follow prompts to:
# - Copy files to framework
# - Create feature branch
# - Commit changes
# - Push for review
```

### 5. Framework Update

```bash
# After enhancement is approved and merged
python agentic-scripts/cli.py update

# Framework now includes your improvement
# Available for all future projects
```

## Troubleshooting Common Issues

### Submodule Update Conflicts

```bash
# If submodule update creates conflicts
cd .agentic-framework
git stash  # Save any local changes
git pull origin main
cd ..
git add .agentic-framework
git commit -m "Update framework to latest version"
```

### Framework Manager Not Found

```bash
# If framework_manager.py is missing in submodule setup
cd .agentic-framework
git pull origin main  # Update to latest framework version

# Or if you have a copy-based project:
# Manually copy the new framework_manager.py from the master template
# Example:
#   cp <FRAMEWORK_ROOT>/scripts/framework_manager.py scripts/
```

### Project Configuration Issues

```bash
# Reset project configuration
python agentic-scripts/cli.py status --reset
python agentic-scripts/cli.py init --reconfigure
```

## Best Practices Summary

1. **Always use the framework manager** for project initialization
2. **Document enhancements** as you identify them during development  
3. **Test framework changes** in multiple project contexts before merging
4. **Keep enhancements focused** - one improvement per enhancement branch
5. **Update framework regularly** in active projects
6. **Communicate changes** to team members when framework updates
7. **Version your enhancements** for better tracking and rollback capability

This approach ensures your agentic SDLC framework continuously evolves and improves based on real project experience while maintaining consistency across all your development efforts.