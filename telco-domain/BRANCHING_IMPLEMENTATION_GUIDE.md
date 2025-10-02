# Branching Strategy Implementation Guide

## Quick Start for Git Branching Adoption

### 1. Setup Branch Structure
```bash
# Create and switch to develop branch
git checkout -b develop
git push -u origin develop

# Set develop as default branch for new features
git config branch.develop.remote origin
git config branch.develop.merge refs/heads/develop
```

### 2. Branch Naming Conventions
```bash
feature/department-routing-v2     # New features
feature/ui-panel-improvements     # UI enhancements
feature/gemini-model-upgrade      # AI model updates

hotfix/critical-sentiment-bug     # Emergency production fixes
hotfix/api-connection-issue       # Urgent API problems

release/v1.0.0                    # Release preparation
release/v1.1.0-beta              # Beta releases
```

### 3. Daily Workflow Commands

#### Starting New Feature
```bash
git checkout develop              # Switch to develop
git pull origin develop          # Get latest changes
git checkout -b feature/my-feature # Create feature branch
```

#### Working on Feature
```bash
git add .                        # Stage changes
git commit -m "Add feature component" # Commit with clear message
git push -u origin feature/my-feature # Push to remote
```

#### Creating Pull Request
1. Go to GitHub repository
2. Click "Compare & pull request" 
3. Set base branch to `develop`
4. Add detailed description
5. Create pull request

#### After PR Approval
```bash
git checkout develop             # Switch back to develop
git pull origin develop          # Get merged changes
git branch -d feature/my-feature # Delete local branch
```

### 4. Emergency Hotfix Process
```bash
git checkout main                # Start from production
git checkout -b hotfix/critical-issue # Create hotfix branch
# ... make fix ...
git add . && git commit -m "Fix critical issue"
git push -u origin hotfix/critical-issue
# Create PR to main for immediate deployment
```

### 5. GitHub Settings Configuration

#### Branch Protection Rules (main)
- Require pull request reviews before merging
- Require status checks to pass before merging  
- Require branches to be up to date before merging
- Restrict pushes that create files larger than 100MB

#### Branch Protection Rules (develop)  
- Require pull request reviews before merging
- Allow administrators to bypass restrictions

### 6. Automated Workflows (.github/workflows/branch-ci.yml)
```yaml
name: Branch CI
on:
  pull_request:
    branches: [ develop, main ]
    
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.13'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/ -v
```

### 7. Commit Message Standards
```bash
# Format: <type>(<scope>): <description>

feat(routing): add department priority logic
fix(ui): resolve panel height calculation  
docs(readme): update branching workflow
refactor(classifier): optimize gemini prompts
test(routing): add edge case coverage
```

### 8. Troubleshooting Common Issues

#### Merge Conflicts
```bash
git checkout develop
git pull origin develop
git checkout feature/my-feature
git rebase develop               # Rebase onto latest develop
# Resolve conflicts in VS Code
git add .
git rebase --continue
```

#### Accidentally Committed to Main
```bash
git log --oneline -5             # Find commit hash
git reset --soft HEAD~1          # Undo last commit, keep changes
git stash                        # Stash changes temporarily
git checkout develop             # Switch to correct branch
git checkout -b feature/my-fix   # Create proper feature branch
git stash pop                    # Restore changes
git add . && git commit          # Commit to correct branch
```

### 9. Branch Cleanup
```bash
# List all branches
git branch -a

# Delete merged local branches
git branch --merged develop | grep -v develop | xargs -n 1 git branch -d

# Delete remote tracking branches that no longer exist
git remote prune origin
```

### 10. Integration with VS Code

#### VS Code Extensions
- GitLens - Git supercharged
- Git Graph - Visualize branch structure  
- GitHub Pull Requests - Manage PRs in editor

#### VS Code Settings
```json
{
  "git.defaultCloneDirectory": "C:/DEV",
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true
}
```

This guide provides practical steps for implementing the branching strategy outlined in the strategic documents.