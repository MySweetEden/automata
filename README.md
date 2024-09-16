# Screen Monitoring App with LINE Notifications

This application enables users to monitor specific areas of their screen for changes. It periodically checks the designated region and sends a notification to the user’s LINE account when changes are detected or when the monitoring process completes. While the primary focus is on monitoring, the app also allows users to preview and clear screenshots as needed.

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
python main.py
```

The app provides the following functionalities:
- Start Monitoring: Enter the coordinates and size for the selected area, and press the Start button to begin periodic monitoring. Screenshots will be taken at the interval specified.
- Stop Monitoring: Press the Stop button to halt the monitoring process.
- Take Screenshot (Preview): Click this button to manually capture a screenshot of the specified area for preview purposes.
- Remove Screenshot: Clear the currently displayed screenshot by pressing the Remove Screenshot button.
- Enter LINE API Key: Enter your LINE API key directly in the app’s textbox (the input will be masked with asterisks), or the app will use the .env key if the textbox is left empty.

## Build

You can find more details on publishing here:
https://flet.dev/docs/publish

After setting up your environment, you can use the following command to build the app for your specific operating system:
flet build <os name>

Replace <os name> with your target operating system (e.g., windows, macos, or linux). This will package the app and create an executable file tailored for your OS, allowing it to be distributed without the need for manual installation of dependencies.

## macOS Setup

You need to grant screen access permissions for the environment you’re using.
- If running in the terminal, allow terminal access.
- If using VS Code, grant access to VS Code.
