# AI Knowledge Transfer System

This directory contains the AI-to-AI knowledge transfer system for the Apple Store Scraper project.

## Purpose
Preserve context and knowledge between AI sessions to eliminate the need for repeated explanations and project re-discovery.

## Files Overview

### Core Context Files
- **`../AI_CONTEXT.md`** - Main project context and handoff information
- **`project_memory.md`** - Technical patterns, decisions, and gotchas
- **`session_history.json`** - Historical record of AI sessions and changes

### Automation Scripts
- **`context_updater.py`** - Automated context capture tool
- **`knowledge_loader.py`** - Quick context retrieval for new sessions

## Usage for AI Sessions

### Starting a New Session
```bash
# Get quick project overview
python .ai/knowledge_loader.py

# Or get detailed JSON data
python .ai/knowledge_loader.py --json
```

### During Development
```bash
# Update context after major changes
python .ai/context_updater.py "Feature implementation" "Added new component,Fixed bug" "Use pattern X,Avoid pattern Y" "Test feature,Deploy to production"
```

### Key Information Sources
1. **AI_CONTEXT.md** - Start here for project overview
2. **TECHNICAL_SPEC.md** - Detailed technical documentation
3. **README.md** - User-facing documentation and setup
4. **Git history** - Recent changes and development patterns

## AI Session Protocol

### Initial Assessment (First 5 minutes)
1. Run `python .ai/knowledge_loader.py` for quick context
2. Review AI_CONTEXT.md for project state
3. Check git status for recent changes
4. Review any pending issues or todos

### During Session
- Use existing patterns documented in project_memory.md
- Follow established conventions (English comments, consistent error handling)
- Update context when making significant changes

### Session Completion
- Update session_history.json with key accomplishments
- Note any new patterns or decisions in project_memory.md
- Update AI_CONTEXT.md if project scope changed

## Context File Maintenance

### Automatic Updates
- `context_updater.py` handles session history and git state
- File modification timestamps tracked automatically
- Project structure analysis on each update

### Manual Updates Required
- AI_CONTEXT.md for major architectural changes
- project_memory.md for new patterns or gotchas
- This README for system improvements

## Benefits

1. **Faster Onboarding** - New AI sessions start with full context
2. **Consistent Patterns** - Preserved coding conventions and decisions
3. **Reduced Redundancy** - No repeated explanations of project background
4. **Better Continuity** - Seamless handoff between sessions
5. **Knowledge Accumulation** - Learning builds up over time

## Integration with Development Workflow

### Package.json Scripts (Recommended additions)
```json
{
  "scripts": {
    "ai:context": "python .ai/knowledge_loader.py",
    "ai:update": "python .ai/context_updater.py"
  }
}
```

### Git Hooks (Optional)
- Pre-commit: Capture context before significant commits
- Post-commit: Update session history with commit information

## Future Enhancements

- Automatic context updates on git commits
- Integration with issue tracking
- Code pattern detection and documentation
- Performance metrics and optimization tracking
- Automated testing of knowledge transfer effectiveness