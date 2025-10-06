# Git Workflow Standards

**Version**: 1.0  
**Last Updated**: 2025-10-03  
**Applies To**: All projects using the Agentic Framework  
**Compliance**: MANDATORY for production projects, RECOMMENDED for toy/learning projects

---

## 🎯 Purpose

This document establishes standardized version control workflows to ensure code quality, enable effective collaboration, and maintain production stability across all projects using the Agentic Framework.

**Key Principles**:
- **Code Review First**: All changes go through peer/AI review before merging
- **Branch Protection**: Production and integration branches are protected
- **Clear History**: Meaningful commit messages and clean git history
- **Workflow Automation**: CI/CD pipelines enforce quality gates
- **AI Agent Compliance**: AI assistants must validate workflow before committing

---

## 📋 Table of Contents

1. [Branching Strategy](#branching-strategy)
2. [Branch Protection Rules](#branch-protection-rules)
3. [Commit Message Standards](#commit-message-standards)
4. [Pull Request Workflow](#pull-request-workflow)
5. [Merge Strategies](#merge-strategies)
6. [AI Agent Compliance](#ai-agent-compliance)
7. [Emergency Procedures](#emergency-procedures)
8. [Project Type Variations](#project-type-variations)

---

## 1. Branching Strategy

### Git Flow Model (Default)

We use a **Git Flow variant** optimized for team collaboration and production stability.

#### Branch Types

| Branch Type | Naming | Created From | Merged To | Lifespan | Protection |
|-------------|--------|--------------|-----------|----------|------------|
| **main** | `main` | N/A | N/A | Permanent | 🔒 Protected |
| **develop** | `develop` | `main` | N/A | Permanent | 🔒 Protected |
| **feature** | `feature/<description>` | `develop` | `develop` | Temporary | ⚠️ None |
| **hotfix** | `hotfix/<description>` | `main` | `main` + `develop` | Temporary | ⚠️ None |
| **release** | `release/v<version>` | `develop` | `main` + `develop` | Temporary | ⚠️ None |
| **bugfix** | `bugfix/<description>` | `develop` | `develop` | Temporary | ⚠️ None |

#### Branch Purposes

**`main` Branch** (Production)
- **Purpose**: Production-ready code only
- **Deployment**: Every commit triggers production deployment
- **Quality**: Must pass ALL quality gates
- **Protection**: Require PR reviews, status checks, no direct commits

**`develop` Branch** (Integration)
- **Purpose**: Integration and pre-production testing
- **Quality**: Must pass unit tests and linting
- **Protection**: Require PR reviews, allow admin bypass for emergencies
- **Stability**: Generally stable, but may contain work-in-progress features

**`feature/*` Branches** (New Features)
- **Purpose**: Individual feature development
- **Naming**: `feature/user-authentication`, `feature/ticket-routing-logic`
- **Lifecycle**: Created from `develop`, merged back to `develop` via PR
- **Quality**: Must pass CI checks before merge approval

**`hotfix/*` Branches** (Emergency Fixes)
- **Purpose**: Critical production bug fixes
- **Naming**: `hotfix/security-patch-cve-2025-1234`, `hotfix/payment-gateway-timeout`
- **Lifecycle**: Created from `main`, merged to both `main` AND `develop`
- **Priority**: Expedited review process (1-2 hours max)

**`release/*` Branches** (Release Preparation)
- **Purpose**: Final QA, version bumps, release notes
- **Naming**: `release/v1.2.0`, `release/v2.0.0-beta`
- **Lifecycle**: Created from `develop`, merged to `main` (tagged) and back to `develop`
- **Quality**: Full regression testing, performance validation

---

## 2. Branch Protection Rules

### Main Branch Protection (MANDATORY)

```yaml
Branch: main
Protections:
  - require_pull_request_reviews: true
    required_approving_review_count: 1
  - require_status_checks_before_merge: true
    status_checks:
      - "ci/tests"
      - "ci/linting" 
      - "ci/security-scan"
  - enforce_admins: true
  - require_linear_history: false  # Allow merge commits
  - allow_force_pushes: false
  - allow_deletions: false
  - require_signed_commits: true  # Production projects only
```

### Develop Branch Protection (RECOMMENDED)

```yaml
Branch: develop
Protections:
  - require_pull_request_reviews: true
    required_approving_review_count: 1
  - require_status_checks_before_merge: true
    status_checks:
      - "ci/tests"
      - "ci/linting"
  - enforce_admins: false  # Allow admin bypass for emergency fixes
  - allow_force_pushes: false
  - allow_deletions: false
```

### Feature/Hotfix Branches

- **No protection required** (short-lived, disposable)
- **CI checks run automatically** on push
- **Deleted after merge** to keep repo clean

---

## 3. Commit Message Standards

### Conventional Commits Format (MANDATORY)

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear, parsable commit history.

#### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

#### Types

| Type | Purpose | Example |
|------|---------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(routing): resolve null pointer in classifier` |
| `docs` | Documentation only | `docs(readme): update installation steps` |
| `style` | Code style/formatting | `style(ui): fix indentation in dashboard` |
| `refactor` | Code refactor (no behavior change) | `refactor(api): extract validation logic` |
| `perf` | Performance improvement | `perf(db): add index on ticket_id` |
| `test` | Add/update tests | `test(routing): add edge case coverage` |
| `build` | Build system/dependencies | `build(deps): upgrade FastAPI to 0.115.0` |
| `ci` | CI/CD changes | `ci(github): add Docker build action` |
| `chore` | Maintenance tasks | `chore(cleanup): remove deprecated files` |
| `revert` | Revert previous commit | `revert: feat(auth): add OAuth2 login` |

#### Scopes (Project-Specific)

Common scopes for call centre agent project:
- `routing` - Ticket routing logic
- `classifier` - ML classification model
- `api` - REST API endpoints
- `ui` - Streamlit/frontend interface
- `db` - Database layer
- `auth` - Authentication/authorization
- `tests` - Test infrastructure
- `docs` - Documentation

#### Examples

**Good Commits** ✅
```
feat(classifier): add Gemini Pro model integration
fix(routing): handle empty department field
docs(api): add OpenAPI specification
test(classifier): add unit tests for priority detection
refactor(ui): extract ticket display component
perf(classifier): cache model embeddings
```

**Bad Commits** ❌
```
updated stuff
fix bug
WIP
checkpoint
asdf
Fixed the thing John mentioned
```

#### Commit Body Guidelines

For complex changes, add a body explaining **why** (not what):

```
feat(routing): implement priority-based queue assignment

Current FIFO queue causes high-priority tickets to wait unnecessarily.
New algorithm assigns tickets based on:
- Customer tier (premium/standard)
- Issue severity (critical/high/medium/low)
- SLA deadlines

Reduces P1 ticket resolution time by ~40% in testing.

Closes #234
```

#### Breaking Changes

Use `BREAKING CHANGE:` footer for incompatible API changes:

```
feat(api): redesign ticket creation endpoint

BREAKING CHANGE: /api/tickets/create now requires `department_id` 
instead of `department_name`. Update all client integrations.
```

---

## 4. Pull Request Workflow

### Creating a Pull Request

#### Step 1: Create Feature Branch

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/ticket-priority-routing

# Make changes, commit frequently
git add src/routing/priority.py
git commit -m "feat(routing): add priority calculation logic"

# Push to remote
git push -u origin feature/ticket-priority-routing
```

#### Step 2: Open Pull Request

**PR Title Format**: Same as commit message (Conventional Commits)

```
feat(routing): implement priority-based queue assignment
```

**PR Description Template**:

```markdown
## Summary
Briefly describe what this PR does and why.

## Changes
- Added priority calculation logic
- Updated routing engine to use priority scores
- Added unit tests for edge cases

## Testing
- ✅ Unit tests pass (98% coverage)
- ✅ Integration tests with 1000+ sample tickets
- ✅ Manual testing with production-like data

## Screenshots (if UI changes)
[Attach before/after screenshots]

## Checklist
- [x] Code follows style guidelines
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes (or documented)
- [x] Ready for review

## Related Issues
Closes #234
```

#### Step 3: Request Review

**For Feature PRs**:
- Assign to team lead or peer developer
- Add relevant labels (`enhancement`, `bug`, `documentation`)
- Link related issues

**For Hotfix PRs**:
- Mark as `urgent`
- Assign to senior engineer + DevOps
- Notify on team chat

### Reviewing a Pull Request

#### Reviewer Responsibilities

1. **Code Quality**
   - Follows coding standards (`../standards/coding_styleguide.md`)
   - No security vulnerabilities (`../standards/secure_coding_checklist.md`)
   - Proper error handling
   - Type hints present (Python projects)

2. **Functionality**
   - Logic is correct and efficient
   - Edge cases handled
   - No regressions introduced

3. **Tests**
   - Adequate test coverage (≥80%)
   - Tests actually validate the changes
   - Tests are maintainable

4. **Documentation**
   - README updated if needed
   - API docs updated
   - Comments for complex logic

#### Review Outcomes

- **Approve**: Code is production-ready, merge anytime
- **Request Changes**: Issues must be fixed before merge
- **Comment**: Suggestions for improvement (non-blocking)

### Merging Pull Requests

**Merge Criteria** (ALL must pass):
- ✅ At least 1 approving review
- ✅ All CI checks passing
- ✅ No merge conflicts
- ✅ Branch is up-to-date with base branch

**Merge Methods**:

| Method | Use Case | Git Command |
|--------|----------|-------------|
| **Merge Commit** (default) | Feature branches with meaningful history | `git merge --no-ff` |
| **Squash and Merge** | Feature branches with messy WIP commits | `git merge --squash` |
| **Rebase and Merge** | Small changes, want linear history | `git rebase` then `git merge --ff-only` |

**Post-Merge**:
```bash
# Delete remote branch
git push origin --delete feature/ticket-priority-routing

# Delete local branch
git branch -d feature/ticket-priority-routing

# Update local develop
git checkout develop
git pull origin develop
```

---

## 5. Merge Strategies

### When to Use Each Strategy

#### Merge Commit (`--no-ff`)
**Use For**: Multi-commit feature branches with clear development history

**Advantages**:
- Preserves complete feature development history
- Easy to revert entire feature (single merge commit)
- Clear visualization in git graph

**Example**:
```bash
git checkout develop
git merge --no-ff feature/priority-routing
git push origin develop
```

**Git History**:
```
*   Merge branch 'feature/priority-routing' into develop
|\
| * feat(routing): add priority scoring tests
| * feat(routing): implement priority calculation
| * docs(routing): add priority algorithm explanation
|/
* Previous develop commit
```

---

#### Squash and Merge
**Use For**: Feature branches with many WIP/checkpoint commits

**Advantages**:
- Clean, linear history on develop
- Single commit represents entire feature
- Easier code archaeology

**Example**:
```bash
git checkout develop
git merge --squash feature/priority-routing
git commit -m "feat(routing): implement priority-based queue assignment"
git push origin develop
```

**Git History**:
```
* feat(routing): implement priority-based queue assignment
* Previous develop commit
```

---

#### Rebase and Merge
**Use For**: Small bug fixes or single-commit changes

**Advantages**:
- Perfectly linear history
- No merge commits
- Cleanest git log

**Example**:
```bash
git checkout feature/small-fix
git rebase develop
git checkout develop
git merge --ff-only feature/small-fix
git push origin develop
```

**Git History**:
```
* fix(routing): handle null department gracefully
* Previous develop commit
```

---

## 6. AI Agent Compliance

### 🤖 AI Assistant Workflow Requirements

**CRITICAL**: AI assistants (GitHub Copilot, Tabnine, Cursor, etc.) MUST follow these rules:

#### Pre-Commit Validation Checklist

Before executing ANY git commit, AI agents MUST:

1. **Check Current Branch**
   ```bash
   git branch --show-current
   ```
   - ❌ If on `main` or `develop`: **STOP** and alert user
   - ✅ If on `feature/*`, `hotfix/*`, `bugfix/*`: Proceed

2. **Verify Workflow Context**
   - Check if project has branching strategy document (e.g., `BRANCHING_IMPLEMENTATION_GUIDE.md`)
   - Read and understand the project's specific workflow requirements
   - Identify project type (production vs. toy project)

3. **Alert User if Workflow Deviation Detected**
   ```
   ⚠️ WARNING: You are on the 'main' branch (protected).
   
   Recommended action:
   1. Create a feature branch: git checkout -b feature/descriptive-name
   2. Make your changes there
   3. Create a PR to merge back to develop/main
   
   For toy projects, you can bypass this with: "this is a toy project, proceed"
   ```

4. **Get Explicit Bypass Permission for Toy Projects**
   - AI must ask: "This appears to bypass the documented workflow. Is this a toy project?"
   - Only proceed after user confirms: "yes, toy project" or "this is a toy project"

#### AI Agent Code Generation Rules

When generating git commands:

**❌ NEVER Generate**:
```bash
git commit -m "updates"
git push origin main  # Without checking if on feature branch
git commit -am "WIP"
git push --force
```

**✅ ALWAYS Generate**:
```bash
# Check status first
git status
git branch --show-current

# Meaningful commit messages
git commit -m "feat(routing): add priority-based assignment logic"

# Push to feature branch (after validation)
git push -u origin feature/priority-routing

# Remind user to create PR
echo "Next step: Create Pull Request from feature/priority-routing to develop"
```

#### AI Agent Education Role

AI assistants should **educate users** about workflow:

```
💡 Best Practice: Instead of committing directly to main, let's:

1. Create a feature branch:
   git checkout -b feature/add-priority-routing

2. Make your changes and commit:
   git commit -m "feat(routing): add priority-based assignment"

3. Push and create PR:
   git push -u origin feature/add-priority-routing

This enables code review and maintains production stability.

For toy projects, you can bypass this process if needed.
```

---

## 7. Emergency Procedures

### Hotfix Workflow (Production Issues)

**When to Use**: Critical production bug requiring immediate fix

**Timeline**: Maximum 2 hours from detection to deployment

#### Step 1: Create Hotfix Branch from Main

```bash
git checkout main
git pull origin main
git checkout -b hotfix/fix-payment-timeout
```

#### Step 2: Make Minimal Fix

- **Only fix the critical issue** (no refactoring, no new features)
- Add regression test
- Update version number (patch increment)

```bash
git commit -m "fix(payment): increase gateway timeout to 30s"
```

#### Step 3: Fast-Track PR Review

- Create PR to `main`
- Label as `urgent`, `hotfix`
- Notify team lead immediately
- Expedited review (30 minutes max)

#### Step 4: Merge to Main and Develop

```bash
# Merge to main
git checkout main
git merge --no-ff hotfix/fix-payment-timeout
git tag -a v1.2.1 -m "Hotfix: Payment gateway timeout"
git push origin main --tags

# Merge to develop
git checkout develop
git merge --no-ff hotfix/fix-payment-timeout
git push origin develop

# Cleanup
git branch -d hotfix/fix-payment-timeout
git push origin --delete hotfix/fix-payment-timeout
```

#### Step 5: Post-Deployment Validation

- Monitor production metrics for 30 minutes
- Update incident report
- Schedule post-mortem review

---

### Rolling Back a Bad Deployment

**Scenario**: A merged PR causes production issues

#### Option 1: Revert Merge Commit (Safest)

```bash
git checkout main
git pull origin main

# Find the merge commit
git log --oneline --graph -10

# Revert the merge (creates new commit)
git revert -m 1 <merge-commit-hash>
git push origin main
```

#### Option 2: Emergency Rollback Tag

```bash
# Deploy previous stable version
git checkout <previous-stable-tag>
# Trigger deployment from this tag
```

---

## 8. Project Type Variations

### Production Projects (STRICT)

**Characteristics**: Customer-facing, revenue-impacting, regulated

**Requirements**:
- ✅ All workflow rules MANDATORY
- ✅ Branch protection enforced
- ✅ Signed commits required
- ✅ Multiple approvers for main (2+)
- ✅ Full CI/CD pipeline with security scans
- ✅ Deployment gates (manual approval)

**Example Projects**: E-commerce platform, banking API, healthcare system

---

### Internal Tools (BALANCED)

**Characteristics**: Internal use only, moderate risk

**Requirements**:
- ✅ Branch protection on main
- ✅ PR reviews required (1 approver)
- ⚠️ Signed commits optional
- ✅ CI/CD pipeline (automated tests)
- ⚠️ Manual deployment approval for production

**Example Projects**: Internal dashboard, admin tools, analytics platform

---

### Toy/Learning Projects (FLEXIBLE)

**Characteristics**: Educational, experimental, no production use

**Requirements**:
- ⚠️ Branch protection optional
- ⚠️ PR workflow recommended but not enforced
- ⚠️ Can commit directly to main (with awareness)
- ✅ Commit message standards still apply (good practice)
- ⚠️ CI/CD optional

**Example Projects**: Tutorials, proof-of-concepts, personal projects

**AI Agent Behavior**: Ask for confirmation before bypassing workflow

---

## 📚 Additional Resources

### Recommended Reading
- [Git Flow Original Article](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)

### Project-Specific Guides
- `telco-domain/BRANCHING_IMPLEMENTATION_GUIDE.md` - Project-specific implementation
- `agentic-framework/standards/coding_styleguide.md` - Code quality standards
- `agentic-framework/master-agent.md` - Master agent orchestration

### Tools
- **Git GUI**: GitKraken, SourceTree, GitHub Desktop
- **Commit Message Validation**: commitlint, pre-commit hooks
- **Branch Protection**: GitHub, GitLab, Bitbucket native features
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins

---

## ✅ Compliance Checklist

Use this checklist to ensure your project follows git workflow standards:

### Repository Setup
- [ ] `main` branch protection enabled
- [ ] `develop` branch created and protected
- [ ] Branch naming conventions documented
- [ ] Commit message template added (`.gitmessage`)
- [ ] PR template created (`.github/PULL_REQUEST_TEMPLATE.md`)

### AI Assistant Configuration
- [ ] Workflow rules added to `.github/copilot-instructions.md`
- [ ] Pre-commit validation enabled for AI agents
- [ ] Project type identified (production/internal/toy)

### Team Onboarding
- [ ] Team trained on Git Flow workflow
- [ ] Commit message standards shared
- [ ] PR review guidelines documented
- [ ] Emergency hotfix procedure documented

### Automation
- [ ] CI/CD pipeline configured
- [ ] Automated tests run on every PR
- [ ] Linting/formatting checks enabled
- [ ] Security scanning integrated

---

**Version History**:
- **v1.0** (2025-10-03): Initial version based on retrospective analysis of branching oversight

**Maintained By**: Agentic Framework Core Team  
**Questions?**: Open an issue in the framework repository
