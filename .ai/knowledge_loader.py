#!/usr/bin/env python3
"""
AI Knowledge Loader - Quick context retrieval for new AI sessions
Provides formatted context summary for AI handoff
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_context_files():
    """Load all AI context files"""
    context = {}
    
    # Load main context
    ai_context_file = 'AI_CONTEXT.md'
    if os.path.exists(ai_context_file):
        with open(ai_context_file, 'r') as f:
            context['main_context'] = f.read()
    
    # Load session history
    history_file = '.ai/session_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            context['session_history'] = json.load(f)
    
    # Load project memory
    memory_file = '.ai/project_memory.md'
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            context['project_memory'] = f.read()
    
    return context

def get_recent_activity():
    """Get recent project activity from git and file changes"""
    activity = {}
    
    try:
        import subprocess
        
        # Get recent commits
        commits = subprocess.check_output([
            'git', 'log', '--oneline', '-3', '--pretty=format:%h %s (%ad)', 
            '--date=short'
        ], text=True).strip().split('\n')
        activity['recent_commits'] = commits
        
        # Get current status
        status = subprocess.check_output(['git', 'status', '--porcelain'], 
                                       text=True).strip()
        activity['modified_files'] = status.split('\n') if status else []
        
        # Get current branch
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                       text=True).strip()
        activity['current_branch'] = branch
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        activity['error'] = 'Git information unavailable'
    
    return activity

def analyze_current_state():
    """Analyze current project state"""
    state = {
        'timestamp': datetime.now().isoformat(),
        'files_status': {},
        'features_available': []
    }
    
    # Check key files
    key_files = [
        'package.json', 'requirements.txt', 'iphone.py', 'ipad.py', 
        'mac.py', 'convert_to_json.py', 'src/main.js', 'src/index.html'
    ]
    
    for file in key_files:
        state['files_status'][file] = {
            'exists': os.path.exists(file),
            'size': os.path.getsize(file) if os.path.exists(file) else 0,
            'modified': datetime.fromtimestamp(
                os.path.getmtime(file)
            ).isoformat() if os.path.exists(file) else None
        }
    
    # Detect available features
    if state['files_status']['iphone.py']['exists']:
        state['features_available'].append('iPhone scraping')
    if state['files_status']['ipad.py']['exists']:
        state['features_available'].append('iPad scraping')
    if state['files_status']['mac.py']['exists']:
        state['features_available'].append('Mac scraping')
    if state['files_status']['src/main.js']['exists']:
        state['features_available'].append('Web interface')
    
    return state

def generate_handoff_summary():
    """Generate a complete handoff summary for new AI session"""
    context = load_context_files()
    activity = get_recent_activity()
    state = analyze_current_state()
    
    summary = {
        'generated_at': datetime.now().isoformat(),
        'project_overview': {
            'name': 'Apple Store Scraper',
            'type': 'Web scraping and price comparison tool',
            'languages': ['Python', 'JavaScript'],
            'frameworks': ['Vite', 'Bootstrap 5']
        },
        'current_state': state,
        'recent_activity': activity,
        'context_available': list(context.keys()),
        'session_count': len(context.get('session_history', {}).get('sessions', [])),
        'last_session': None
    }
    
    # Get last session info
    if context.get('session_history') and context['session_history'].get('sessions'):
        last_session = context['session_history']['sessions'][-1]
        summary['last_session'] = {
            'id': last_session.get('id'),
            'timestamp': last_session.get('timestamp'),
            'summary': last_session.get('summary'),
            'key_changes': last_session.get('key_changes', [])
        }
    
    return summary

def format_for_ai():
    """Format context information for AI consumption"""
    summary = generate_handoff_summary()
    
    output = []
    output.append("# AI Session Handoff Summary")
    output.append(f"Generated: {summary['generated_at']}")
    output.append("")
    
    # Project overview
    output.append("## Project Overview")
    overview = summary['project_overview']
    output.append(f"- **Name**: {overview['name']}")
    output.append(f"- **Type**: {overview['type']}")
    output.append(f"- **Languages**: {', '.join(overview['languages'])}")
    output.append(f"- **Frameworks**: {', '.join(overview['frameworks'])}")
    output.append("")
    
    # Current state
    output.append("## Current State")
    state = summary['current_state']
    output.append(f"- **Available Features**: {', '.join(state['features_available'])}")
    output.append(f"- **Key Files Status**: {sum(1 for f in state['files_status'].values() if f['exists'])}/{len(state['files_status'])} files present")
    output.append("")
    
    # Recent activity
    activity = summary['recent_activity']
    if 'recent_commits' in activity:
        output.append("## Recent Activity")
        output.append("### Recent Commits")
        for commit in activity['recent_commits']:
            output.append(f"- {commit}")
        
        if activity.get('modified_files'):
            output.append("### Modified Files")
            for file in activity['modified_files']:
                output.append(f"- {file}")
        output.append("")
    
    # Last session
    if summary['last_session']:
        output.append("## Last AI Session")
        last = summary['last_session']
        output.append(f"- **ID**: {last['id']}")
        output.append(f"- **Date**: {last['timestamp']}")
        output.append(f"- **Summary**: {last['summary']}")
        if last['key_changes']:
            output.append("- **Key Changes**:")
            for change in last['key_changes']:
                output.append(f"  - {change}")
        output.append("")
    
    # Instructions
    output.append("## Next Steps for AI")
    output.append("1. Review AI_CONTEXT.md for detailed project knowledge")
    output.append("2. Check .ai/project_memory.md for technical patterns")
    output.append("3. Review recent git commits for latest changes")
    output.append("4. Use .ai/context_updater.py to record session activities")
    
    return "\n".join(output)

def main():
    """Main execution function"""
    if len(os.sys.argv) > 1 and os.sys.argv[1] == '--json':
        # Output JSON format
        summary = generate_handoff_summary()
        print(json.dumps(summary, indent=2))
    else:
        # Output formatted text
        print(format_for_ai())

if __name__ == '__main__':
    main()