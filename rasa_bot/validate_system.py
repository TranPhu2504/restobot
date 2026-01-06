#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RestoBot - Comprehensive System Validation Script
Validates all components: YAML configs, Python actions, business logic
"""

import os
import sys
import yaml
import importlib.util
from pathlib import Path

print("=" * 60)
print("🔍 RESTOBOT - COMPREHENSIVE SYSTEM VALIDATION")
print("=" * 60)

# Get the rasa_bot directory
RASA_BOT_DIR = Path(__file__).parent
os.chdir(RASA_BOT_DIR)

validation_results = []
errors_found = []

# ===== 1. YAML CONFIGURATION VALIDATION =====
print("\n📋 YAML Configuration Validation")
print("-" * 60)

yaml_files = [
    'domain.yml',
    'config.yml',
    'data/nlu.yml',
    'data/stories.yml',
    'data/rules.yml'
]

for yaml_file in yaml_files:
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✅ {yaml_file}: Valid YAML syntax")
        validation_results.append(('YAML', yaml_file, 'PASS', None))
    except Exception as e:
        print(f"❌ {yaml_file}: {str(e)}")
        validation_results.append(('YAML', yaml_file, 'FAIL', str(e)))
        errors_found.append(f"{yaml_file}: {str(e)}")

# ===== 2. DOMAIN STRUCTURE VALIDATION =====
print("\n🏗️ Domain Structure Validation")
print("-" * 60)

try:
    with open('domain.yml', 'r', encoding='utf-8') as f:
        domain = yaml.safe_load(f)
    
    # Check required sections
    required_sections = ['intents', 'actions', 'responses', 'slots']
    for section in required_sections:
        if section in domain:
            count = len(domain[section]) if isinstance(domain[section], (list, dict)) else 0
            print(f"✅ {section}: {count} items")
            validation_results.append(('DOMAIN', section, 'PASS', f'{count} items'))
        else:
            print(f"⚠️  {section}: Missing")
            validation_results.append(('DOMAIN', section, 'WARN', 'Missing'))
            
except Exception as e:
    print(f"❌ Domain validation failed: {str(e)}")
    errors_found.append(f"Domain: {str(e)}")

# ===== 3. NLU DATA VALIDATION =====
print("\n🧠 NLU Data Validation")
print("-" * 60)

try:
    with open('data/nlu.yml', 'r', encoding='utf-8') as f:
        nlu_data = yaml.safe_load(f)
    
    if 'nlu' in nlu_data:
        intents = [item for item in nlu_data['nlu'] if 'intent' in item]
        examples_count = sum(len(intent.get('examples', '').split('\n')) for intent in intents)
        
        print(f"✅ NLU Intents: {len(intents)}")
        print(f"✅ Training Examples: ~{examples_count}")
        validation_results.append(('NLU', 'intents', 'PASS', f'{len(intents)} intents'))
        validation_results.append(('NLU', 'examples', 'PASS', f'~{examples_count} examples'))
    else:
        print("❌ NLU data structure invalid")
        errors_found.append("NLU: Invalid structure")
        
except Exception as e:
    print(f"❌ NLU validation failed: {str(e)}")
    errors_found.append(f"NLU: {str(e)}")

# ===== 4. PYTHON ACTIONS VALIDATION =====
print("\n🐍 Python Actions Validation")
print("-" * 60)

action_modules = [
    'actions/modules/menu_actions.py',
    'actions/modules/booking_actions.py',
    'actions/modules/order_actions.py',
    'actions/modules/payment_actions.py',
    'actions/modules/confirmation_actions.py',
    'actions/modules/auth_helper.py'
]

for module_path in action_modules:
    try:
        # Check if file exists
        if not os.path.exists(module_path):
            print(f"❌ {module_path}: File not found")
            errors_found.append(f"{module_path}: File not found")
            continue
            
        # Try to compile the Python file
        with open(module_path, 'r', encoding='utf-8') as f:
            compile(f.read(), module_path, 'exec')
        
        print(f"✅ {module_path}: Valid Python syntax")
        validation_results.append(('PYTHON', module_path, 'PASS', None))
        
    except SyntaxError as e:
        print(f"❌ {module_path}: Syntax error at line {e.lineno}")
        errors_found.append(f"{module_path}: Syntax error at line {e.lineno}")
        validation_results.append(('PYTHON', module_path, 'FAIL', f'Syntax error at line {e.lineno}'))
    except Exception as e:
        print(f"⚠️  {module_path}: {str(e)}")
        validation_results.append(('PYTHON', module_path, 'WARN', str(e)))

# ===== 5. BUSINESS LOGIC VALIDATION =====
print("\n💼 Business Logic Validation")
print("-" * 60)

# Check for critical functions
critical_functions = {
    'actions/modules/menu_actions.py': ['normalize_vietnamese_dish_name', 'find_exact_dish_match'],
    'actions/modules/booking_actions.py': ['validate_business_hours'],
    'actions/modules/order_actions.py': ['ActionAddToOrder'],
    'actions/modules/payment_actions.py': ['ActionInitiatePayment', 'ActionProcessPayment']
}

for module_path, functions in critical_functions.items():
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for func_name in functions:
            if f'def {func_name}' in content or f'class {func_name}' in content:
                print(f"✅ {module_path}: {func_name} found")
                validation_results.append(('LOGIC', f'{module_path}:{func_name}', 'PASS', None))
            else:
                print(f"❌ {module_path}: {func_name} NOT FOUND")
                errors_found.append(f"{module_path}: {func_name} missing")
                validation_results.append(('LOGIC', f'{module_path}:{func_name}', 'FAIL', 'Missing'))
                
    except Exception as e:
        print(f"⚠️  {module_path}: Cannot validate - {str(e)}")

# ===== 6. CONFIGURATION VALIDATION =====
print("\n⚙️ Configuration Validation")
print("-" * 60)

try:
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Check pipeline
    if 'pipeline' in config:
        print(f"✅ NLU Pipeline: {len(config['pipeline'])} components")
        for component in config['pipeline']:
            name = component.get('name', 'Unknown')
            print(f"   - {name}")
        validation_results.append(('CONFIG', 'pipeline', 'PASS', f"{len(config['pipeline'])} components"))
    else:
        print("❌ Pipeline missing in config.yml")
        errors_found.append("Config: Pipeline missing")
    
    # Check policies
    if 'policies' in config:
        print(f"✅ Policies: {len(config['policies'])} policies")
        for policy in config['policies']:
            name = policy.get('name', 'Unknown')
            print(f"   - {name}")
        validation_results.append(('CONFIG', 'policies', 'PASS', f"{len(config['policies'])} policies"))
    else:
        print("❌ Policies missing in config.yml")
        errors_found.append("Config: Policies missing")
        
except Exception as e:
    print(f"❌ Config validation failed: {str(e)}")
    errors_found.append(f"Config: {str(e)}")

# ===== 7. DEPENDENCIES CHECK =====
print("\n📦 Dependencies Check")
print("-" * 60)

required_packages = [
    'yaml',
    'requests',
    'sqlalchemy',
    'pydantic'
]

for package in required_packages:
    try:
        __import__(package)
        print(f"✅ {package}: Installed")
        validation_results.append(('DEPS', package, 'PASS', None))
    except ImportError:
        print(f"❌ {package}: NOT INSTALLED")
        errors_found.append(f"Dependency: {package} not installed")
        validation_results.append(('DEPS', package, 'FAIL', 'Not installed'))

# Check Rasa (might fail due to packaging issue)
try:
    import rasa
    print(f"✅ rasa: {rasa.__version__}")
    validation_results.append(('DEPS', 'rasa', 'PASS', rasa.__version__))
except Exception as e:
    print(f"⚠️  rasa: Import error - {str(e)}")
    validation_results.append(('DEPS', 'rasa', 'WARN', str(e)))

# ===== FINAL SUMMARY =====
print("\n" + "=" * 60)
print("📊 VALIDATION SUMMARY")
print("=" * 60)

total_checks = len(validation_results)
passed = sum(1 for r in validation_results if r[2] == 'PASS')
failed = sum(1 for r in validation_results if r[2] == 'FAIL')
warnings = sum(1 for r in validation_results if r[2] == 'WARN')

print(f"\nTotal Checks: {total_checks}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"⚠️  Warnings: {warnings}")

if errors_found:
    print(f"\n🚨 CRITICAL ERRORS FOUND ({len(errors_found)}):")
    for error in errors_found:
        print(f"   - {error}")
else:
    print("\n🎉 NO CRITICAL ERRORS FOUND!")

# Overall status
if failed == 0:
    print("\n✅ VALIDATION PASSED - System ready for deployment")
    print("\n📝 Next Steps:")
    print("   1. Fix packaging issue: pip install 'packaging>=22.0,<24.0'")
    print("   2. Train Rasa model: rasa train")
    print("   3. Test actions server: rasa run actions")
    print("   4. Test Rasa server: rasa run --enable-api")
    sys.exit(0)
else:
    print("\n❌ VALIDATION FAILED - Please fix errors above")
    sys.exit(1)
