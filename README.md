
# Introduction

This enhanced Math Alarm Clock application is designed to intercept alarm notifications from the Windows Clock app. To dismiss the alarm, users must solve math problems. This version includes the ability to play a music file of the user's choice until the math problems are solved.
Prerequisites

    Windows 10 or higher
    Python 3.6 or higher
    win11toast, winsdk, vlc, and tkinter packages

# Setup

# Installation

    Python Installation:
    Ensure Python 3.6 or higher is installed on your system. You can download it from the official Python website.

    Dependencies Installation:
    Install the required Python packages using pip:

    shell

    pip install win11toast winsdk python-vlc tk

# Configuration

No extensive configuration is needed. However, make sure that your Windows settings allow Python scripts to access notifications:

    Go to Settings in Windows.
    Navigate to Privacy & Security.
    Go to Notifications.
    Ensure that the option to let apps access your notifications is enabled.

# Running the Application

    Start the Script:
        Run the script using Python:

        open shell

        python math_alarm_clock.py

        Upon startup, you'll be prompted to select a music file to play when the alarm triggers.

    Set an Alarm:
        Use the Windows Clock app to set an alarm.

    Alarm Interaction:
        When the alarm triggers, the selected music will play, and a notification with math problems will appear.
        Solve the problems by entering the answers in the notification's input field, separated by commas, and click "Submit" to dismiss the alarm and stop the music.

# Usage

    The script must be running for the math problem interception and music playback to work.
    The music will continue to play until the math problems are correctly solved.

# Customization

    The number of math problems (default is 3) can be adjusted in the code.
    The difficulty of the math problems can be modified by changing the parameters in the generate_problem function.

# Troubleshooting

    If the application does not intercept the alarm notifications, verify that it has the necessary permissions to access notifications in Windows settings.
    Ensure that all required packages (win11toast, winsdk, vlc, tk) are installed correctly
