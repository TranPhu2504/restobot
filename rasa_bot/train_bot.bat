@echo off
echo =====================================
echo        TRAINING RASA BOT
echo =====================================
echo.

cd /d "%~dp0"

echo Checking if we're in rasa_bot directory...
if not exist "domain.yml" (
    echo Error: domain.yml not found. Make sure you're in the rasa_bot directory.
    pause
    exit /b 1
)

echo.
echo Starting Rasa training process...
echo This may take 5-15 minutes depending on your system.
echo.

echo Training with improved configuration...
rasa train --config config.yml --domain domain.yml --data data/

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================== 
    echo    ✅ TRAINING COMPLETED SUCCESSFULLY!
    echo =====================================
    echo.
    echo New model has been created in the models/ directory.
    echo You can now run the bot with: rasa run actions (in one terminal)
    echo                          and: rasa run --enable-api --cors "*" (in another terminal)
    echo.
) else (
    echo.
    echo =====================================
    echo    ❌ TRAINING FAILED!
    echo =====================================
    echo.
    echo Please check the error messages above and fix any issues.
    echo Common issues:
    echo - Missing required files (nlu.yml, rules.yml, stories.yml, domain.yml)
    echo - Syntax errors in YAML files
    echo - Missing actions in domain.yml
    echo.
)

pause