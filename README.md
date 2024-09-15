# Screenshot Monitoring App with LINE Notifications

This application allows users to monitor a specific area of the screen by periodically taking screenshots. The app detects changes in the selected area and sends a notification to the user’s LINE account when the process completes. Additionally, users can manually take a screenshot for preview purposes or clear the displayed screenshot from the app.

## Features
- Monitor Screen Area: Select a specific area of the screen to monitor for changes.
- LINE Notifications: Get notified via LINE when the monitoring process detects no changes in the selected area.
- User Input for LINE API Key: Enter your LINE API key directly in the app (masked with asterisks) or load it from an .env file.
- Manual Screenshot: Take a preview screenshot to help set the cropping area before starting the monitoring.
- Clear Screenshot: Clear the current screenshot display from the app screen.

## Usage
Run the following commands in your terminal:

``` 
git clone https://github.com/MySweetEden/automonita.git
cd automonita
uv sync
python app.py
```

The app provides the following functionalities:
- Start Monitoring: Enter the coordinates and size for the selected area, and press the Start button to begin periodic monitoring. Screenshots will be taken at the interval specified.
- Stop Monitoring: Press the Stop button to halt the monitoring process.
- Take Screenshot (Preview): Click this button to manually capture a screenshot of the specified area for preview purposes.
- Remove Screenshot: Clear the currently displayed screenshot by pressing the Remove Screenshot button.
- Enter LINE API Key: Enter your LINE API key directly in the app’s textbox (the input will be masked with asterisks), or the app will use the .env key if the textbox is left empty.

## macOS Setup

You need to grant screen access permissions for the environment you’re using.
- If running in the terminal, allow terminal access.
- If using VS Code, grant access to VS Code.
