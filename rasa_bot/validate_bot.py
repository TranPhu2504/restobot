"""
Rasa Bot Validation Script
Kiểm tra và validate các file cấu hình trước khi train
"""
import os
import yaml
import json
from pathlib import Path

def validate_yaml_file(file_path):
    """Validate YAML file syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True, None
    except Exception as e:
        return False, str(e)

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'domain.yml',
        'config.yml',
        'data/nlu.yml',
        'data/stories.yml', 
        'data/rules.yml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    return missing_files

def validate_domain():
    """Validate domain.yml structure"""
    try:
        with open('domain.yml', 'r', encoding='utf-8') as f:
            domain = yaml.safe_load(f)
        
        issues = []
        
        # Check required sections
        required_sections = ['intents', 'responses', 'actions']
        for section in required_sections:
            if section not in domain:
                issues.append(f"Missing section: {section}")
        
        # Check if actions are properly defined
        if 'actions' in domain:
            for action in domain['actions']:
                # Forms and built-in actions don't need action_ or utter_ prefix
                if (not action.startswith('action_') and 
                    not action.startswith('utter_') and 
                    not action.endswith('_form') and 
                    action not in ['action_listen', 'action_restart', 'action_session_start', 'action_default_fallback']):
                    issues.append(f"Action name '{action}' should start with 'action_' or 'utter_' (or be a form ending with '_form')")
        
        return issues
    except Exception as e:
        return [f"Error parsing domain.yml: {str(e)}"]

def validate_nlu():
    """Validate NLU data"""
    try:
        with open('data/nlu.yml', 'r', encoding='utf-8') as f:
            nlu_data = yaml.safe_load(f)
        
        issues = []
        
        if 'nlu' not in nlu_data:
            issues.append("Missing 'nlu' section in nlu.yml")
            return issues
        
        # Check for intents with examples
        intent_count = 0
        for item in nlu_data['nlu']:
            if 'intent' in item:
                intent_count += 1
                if 'examples' not in item or not item['examples']:
                    issues.append(f"Intent '{item['intent']}' has no examples")
        
        if intent_count == 0:
            issues.append("No intents found in NLU data")
        
        return issues
    except Exception as e:
        return [f"Error parsing nlu.yml: {str(e)}"]

def main():
    print("🔍 RASA BOT VALIDATION SCRIPT")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('domain.yml').exists():
        print("❌ Error: Not in rasa_bot directory. Please cd to rasa_bot folder.")
        return False
    
    print("📁 Checking required files...")
    missing_files = check_required_files()
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    print("✅ All required files present")
    
    print("\n📝 Validating YAML syntax...")
    yaml_files = ['domain.yml', 'config.yml', 'data/nlu.yml', 'data/stories.yml', 'data/rules.yml']
    
    for yaml_file in yaml_files:
        valid, error = validate_yaml_file(yaml_file)
        if not valid:
            print(f"❌ {yaml_file}: {error}")
            return False
        else:
            print(f"✅ {yaml_file}: Valid syntax")
    
    print("\n🎯 Validating domain.yml structure...")
    domain_issues = validate_domain()
    if domain_issues:
        print("❌ Domain validation issues:")
        for issue in domain_issues:
            print(f"   - {issue}")
        return False
    print("✅ Domain structure is valid")
    
    print("\n🧠 Validating NLU data...")
    nlu_issues = validate_nlu()
    if nlu_issues:
        print("❌ NLU validation issues:")
        for issue in nlu_issues:
            print(f"   - {issue}")
        return False
    print("✅ NLU data is valid")
    
    print("\n" + "=" * 50)
    print("🎉 ALL VALIDATIONS PASSED!")
    print("Ready to train with: rasa train")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)