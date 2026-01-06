#!/bin/bash
# Script to train Rasa model

echo "Training Rasa model..."
rasa train

if [ $? -eq 0 ]; then
    echo "✅ Training completed successfully!"
else
    echo "❌ Training failed!"
    exit 1
fi
