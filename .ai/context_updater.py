#!/usr/bin/env python3
"""
AI Context Updater - Automated context capture for AI knowledge transfer
Captures project state changes and updates AI context files
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

def get_git_status():
    """Get current git status and recent commits"""
    try:
        # Get current branch
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                       text=True).strip()
        
        # Get recent commits (last 5)
        commits = subprocess.check_output([
            'git', 'log', '--oneline', '-5', '--pretty=format:%h|%s|%ad', 
            '--date=short'
        ], text=True).strip().split('\n')
        
        # Get modified files
        modified = subprocess.check_output(['git', 'status', '--porcelain'], 
                                         text=True).strip().split('\n')
        modified = [f.strip() for f in modified if f.strip()]
        
        return {
            'branch': branch,
            'recent_commits': [c.split('|') for c in commits if c],
            'modified_files': modified
        }
    except subprocess.CalledProcessError:
        return None

def analyze_project_structure():
    """Analyze current project structure and identify key components"""
    structure = {}
    
    # Check for key files
    key_files = [
        'package.json', 'requirements.txt', 'README.md', 'TECHNICAL_SPEC.md',
        'iphone.py', 'ipad.py', 'mac.py', 'convert_to_json.py'
    ]
    
    for file in key_files:
        structure[file] = os.path.exists(file)
    
    # Check src directory structure
    if os.path.exists('src'):
        src_files = list(Path('src').rglob('*'))
        structure['src_files'] = [str(f) for f in src_files if f.is_file()]
    
    return structure

def update_session_history(summary, changes, decisions, priorities):
    """Update session history with new information"""
    history_file = '.ai/session_history.json'
    
    # Load existing history
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            data = json.load(f)
    else:
        data = {'sessions': [], 'current_context': {}}
    
    # Create new session entry
    session_id = f"session_{len(data['sessions']) + 1:03d}"
    new_session = {
        'id': session_id,
        'timestamp': datetime.now().isoformat() + 'Z',
        'summary': summary,
        'key_changes': changes,
        'decisions_made': decisions,
        'next_priorities': priorities,
        'git_state': get_git_status()
    }
    
    data['sessions'].append(new_session)
    
    # Update current context
    data['current_context'].update({
        'last_session': session_id,
        'last_updated': datetime.now().isoformat() + 'Z',
        'project_structure': analyze_project_structure()
    })
    
    # Save updated history
    os.makedirs('.ai', exist_ok=True)
    with open(history_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return session_id

def generate_context_summary():
    """Generate a summary of current project context"""
    git_info = get_git_status()
    structure = analyze_project_structure()
    
    summary = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'git_branch': git_info['branch'] if git_info else 'unknown',
        'modified_files': git_info['modified_files'] if git_info else [],
        'key_components_status': structure,
        'active_features': [],
        'known_issues': []
    }
    
    # Detect active features based on file existence
    if structure.get('iphone.py'):
        summary['active_features'].append('iPhone scraping')
    if structure.get('ipad.py'):
        summary['active_features'].append('iPad scraping')
    if structure.get('mac.py'):
        summary['active_features'].append('Mac scraping (development)')
    if structure.get('src_files') and any('main.js' in f for f in structure['src_files']):
        summary['active_features'].append('Web interface')
    
    return summary

def main():
    """Main execution function"""
    if len(os.sys.argv) < 2:
        print("Usage: python context_updater.py <summary> [changes] [decisions] [priorities]")
        return
    
    summary = os.sys.argv[1]
    changes = os.sys.argv[2].split(',') if len(os.sys.argv) > 2 else []
    decisions = os.sys.argv[3].split(',') if len(os.sys.argv) > 3 else []
    priorities = os.sys.argv[4].split(',') if len(os.sys.argv) > 4 else []
    
    session_id = update_session_history(summary, changes, decisions, priorities)
    context = generate_context_summary()
    
    print(f"Updated AI context - Session ID: {session_id}")
    print(f"Current context: {len(context['active_features'])} active features")
    
    if context['modified_files']:
        print(f"Modified files: {', '.join(context['modified_files'])}")

if __name__ == '__main__':
    main()