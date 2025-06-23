# Pro AI Completer

This is an experimental, system-wide, context-aware AI text completion tool. It's designed to explore how AI can be present everywhere on your PC, providing intelligent suggestions in any application you use.

It uses Google's Gemini 1.5 Flash model to understand not just your text, but also your visual context through screenshots, to provide more accurate and relevant completions.

## Features

- **Visual Context**: Takes a screenshot of the active screen to provide rich context to the AI for more accurate suggestions.
- **Application Awareness**: Detects the title of the active window (e.g., "VS Code", "Firefox") to further refine the AI's understanding of your task.
- **Dynamic Suggestions**: The AI is prompted to provide suggestions of variable length based on the application context (e.g., longer snippets for code, shorter phrases for chat).
- **Manual Context Reset**: Press `Ctrl+L` at any time to clear the AI's text buffer if you feel the context is stale.
- **Intelligent Triggering**: Only provides suggestions after you pause typing, preventing frantic and distracting popups.

## Dependencies

- **Python 3.10+**
- **xdotool**: A command-line utility for window manipulation. Install it on Debian/Ubuntu with:
  ```bash
  sudo apt-get update && sudo apt-get install xdotool
  ```
- **tesseract-ocr**: A command-line utility for OCR. Install it on Debian/Ubuntu with:
  ```bash
  sudo apt-get update && sudo apt-get install tesseract-ocr
  ```

## Setup & Usage

1.  **Clone the repository**.

2.  **Set up your API Key**: Create a file named `.env` in this directory and add your Gemini API key to it:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

3.  **Run the application**: Execute the provided run script. It will automatically create a virtual environment and install the required packages.
    ```bash
    ./run.sh
    ```
    You will be prompted for your `sudo` password, which is required for the global keyboard listener to function.

## How to Use

- **Start Typing**: Begin typing in any application.
- **Pause**: Briefly pause your typing. A suggestion will appear, highlighted.
- **Accept**: Press `Tab` to accept the suggestion.
- **Reject**: Press `Esc` to dismiss the suggestion.
- **Overwrite**: Simply keep typing to ignore the suggestion.

## Known Limitations

- **Complex Web Applications**: Simulating keyboard input in some complex web applications (e.g., in-browser IDEs) can be unreliable.
- **Wayland Support**: This tool relies on X11 capabilities and will not function correctly in a Wayland session without modification. 