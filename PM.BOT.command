#!/bin/bash

# Optional: Log start time
echo "Launching Chrome bot at $(date)" >> ~/Selenium/bot.log

# Activate your Python virtual environment
source /Users/anmacair/Selenium/myenv/bin/activate

# Run the Python script
python /Users/anmacair/Selenium/bMAIN.PS.EM.py >> ~/Selenium/bot.log 2>&1

# Optional: Log end
echo "Bot finished at $(date)" >> ~/Selenium/bot.log

# Keep Terminal window open (optional for debugging)
echo "Press any key to close this window..."
read -n 1
