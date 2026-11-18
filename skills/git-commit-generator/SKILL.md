---
name: git-commit-generator
description: Generate clear, standardized Git commit messages following the Conventional Commits specification from git diffs, file change lists, or plain-language descriptions. Use whenever the user asks to create, write, generate, draft, or format a git commit message, shares a git diff or patch, or describes code changes they want to commit.
---

# Git Commit Generator

Generate concise, meaningful, and standardized Git commit messages based on Conventional Commits from staged repository changes, code diffs, or plain-language descriptions.

## When to Use

- The user asks to generate a commit message for current repository changes.
- The user shares a `git diff`, patch, or list of changed files and asks for a commit message.
- The user describes features, bug fixes, refactors, or chores in plain language and needs a formatted commit message.
- The user asks to rewrite, shorten, or standardize an existing commit message.

## Workflow

1. **Gather Changes Safely (Read-Only)**
   - If the user did not paste a diff or description, inspect the repository using read-only Git commands.
   - Check the **staging area first** (`git diff --staged`). If staged changes exist, generate the commit message exclusively from those staged changes and ignore unstaged working tree edits.
   - If the staging area is empty, inspect the **working area** (`git status` and `git diff`) to draft the message, and remind the user to stage the files (`git add`) before committing.
   - **Never** run `git commit`, `git add`, or any state-modifying Git command unless the user explicitly asks you to execute the commit.

2. **Analyze the Input**
   - Identify the primary intent of the change (new feature, bug fix, refactoring, documentation, dependency update, etc.).
   - Determine the affected module, component, or directory to use as an optional `scope`.
   - Check if the change introduces backward-incompatible behavior (`BREAKING CHANGE`).

3. **Select the Commit Type**
   Use standard Conventional Commits types:
   - `feat`: A new feature or user-facing capability.
   - `fix`: A bug fix.
   - `refactor`: Code restructuring that neither fixes a bug nor adds a feature.
   - `perf`: Changes that improve performance.
   - `docs`: Documentation-only changes.
   - `style`: Formatting, whitespace, or linting changes with no logic impact.
   - `test`: Adding or updating tests.
   - `build`: Changes affecting the build system or external dependencies.
   - `ci`: Changes to CI/CD configuration files or scripts.
   - `chore`: Maintenance tasks, tooling updates, or routine housekeeping.

4. **Format the Output**
   Follow this structure:

   ```text
   <type>(<optional-scope>): <imperative subject>

   <optional body explaining why and what changed>

   <optional footer, e.g., BREAKING CHANGE: ... or Refs: #123>
   ```

   - **Subject line**: Keep under 72 characters. Use lowercase imperative mood (e.g., `add`, `fix`, `update`, `remove`) with no trailing period.
   - **Body**: Include only when the diff involves multiple distinct changes, non-obvious reasoning, or architectural trade-offs. Wrap lines at 72 characters and use bullet points for multi-part changes.
   - **Language**: Default to English for commit messages unless the user explicitly asks for Indonesian or another language.
   - **Presentation**: Output the primary commit message inside a fenced `text` code block so the user can copy it immediately. If inspected changes mix unrelated concerns, suggest splitting them into atomic commits and provide one message per logical unit.

## Examples

### Single Focused Change

**Input**: Fixed null pointer exception when user profile avatar URL is empty in `UserController.php`.

**Output**:

```text
fix(profile): handle null avatar URL in user controller
```

### Multi-Part Feature with Body

**Input**: Added JWT refresh token rotation, updated auth middleware to validate token family, and added unit tests for expired tokens.

**Output**:

```text
feat(auth): implement JWT refresh token rotation

- Add token family tracking to invalidate compromised refresh tokens
- Update auth middleware to verify token rotation state
- Add unit tests covering expired and reused refresh tokens
```

## Gotchas

- **Mixing staged and unstaged changes**: Never combine unstaged working tree edits into a commit message when staged changes are already present.
- **Describing implementation instead of intent**: Focus on *what* the change achieves and *why*, rather than listing every edited variable or line.
- **Vague subjects**: Avoid generic subjects like `fix bug` or `update code`. Specify the behavior or component affected.
- **Bundling unrelated changes**: If the input contains both a feature and an unrelated bug fix, point this out and provide separate commit messages so the user can stage them cleanly.
