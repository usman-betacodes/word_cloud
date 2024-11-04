#!/bin/bash

# Define paths
VENV_PATH="myenv"  # Path to your virtual environment
English_PATH="english"  # Path to your social directory

# Function to kill specific Python scripts using their PIDs based on ports
kill_specific_python_scripts() {
    echo "Killing specific Python scripts..."
    

    # Get the PID of the Python script running on port 2002
    ENGLISH_PID=$(lsof -t -i:8000)
    if [ -n "$ENGLISH_PID" ]; then
        kill "$ENGLISH_PID" && echo "Killed social script with PID: $ENGLISH_PID"
    fi
}

# Function to run the scripts
run_scripts() {
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"  # Activate the virtual environment
    # Change to the social directory and run main.py in the background
    cd "$English_PATH" || exit  # Change to social directory
    python main.py &  # Run in the background

    echo "Started social scripts."
    cd ..
}

# Infinite loop to keep the process running every hour
while true; do
    kill_specific_python_scripts  # Kill only the specific running Python scripts
    run_scripts                   # Run the scripts
    sleep 3600                    # Wait for 1 hour (3600 seconds)
done
