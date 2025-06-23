# System Cursor

This is an experimental, system-wide, context-aware AI text completion tool. It's designed to explore how AI can be present everywhere on your PC, providing intelligent suggestions in any application you use.

It uses Google's Gemini 1.5 Flash model to understand not just your text, but also your visual context through screenshots, to provide more accurate and relevant completions.

## 🚀 The Vision: AI That Follows You

**This project represents a fundamental shift in how we interact with AI.**

Instead of users constantly switching tabs to follow AI (ChatGPT, Claude, etc.), **AI should follow the user** wherever they are working. This is a seed-level experiment to demonstrate that AI can be contextually aware of your entire digital environment, not just isolated chat windows.

**This is the first step in Pi4Wear's vision of "One AI. Just for you."**

### Why This Matters
- **Current paradigm**: Open AI tab → Copy/paste → Switch back → Repeat
- **Our vision**: AI seamlessly integrated into your natural workflow
- **The goal**: Make AI assistance as ubiquitous as autocorrect, but infinitely smarter
- **Pi4Wear's mission**: Personal, private AI that sees, hears, and works with you naturally

### 🔮 The Bigger Picture
Pi4Wear is building the future where AI feels as personal as the devices we hold dear:

1. **🖥️ It starts on your PC** (this project!) - AI that works wherever you are
2. **📱 Expands to all devices** - Seamless experience across everything
3. **👓 Comes as eyewear** - Lightweight, ambient AI presence
4. **🔒 Becomes truly private** - Your data stays with you, always

**Ready for the full vision?** → **[Join Pi4Wear's Waitlist](https://pi4wear.com)** to be part of building truly personal, private AI.

This open source project is just the beginning. We're open-sourcing this experiment to invite the community to expand this direction and make AI more contextually aware across all platforms and use cases.

## 🌟 Join the Movement

**This is seed-level software that needs your help to grow.** We're looking for contributors to help us:

### 🖥️ **Cross-Platform Support**
- **Windows** implementation using Win32 APIs
- **macOS** support with Accessibility APIs  
- **Wayland** support for modern Linux desktops
- **Mobile** platforms (Android/iOS) for true everywhere AI

### 🤖 **AI Model Diversity**
- **Local models** (Ollama, GPT4All) for privacy-conscious users
- **Multiple providers** (OpenAI, Anthropic, Cohere, local LLMs)
- **Specialized models** for different contexts (code, writing, data)
- **Model switching** based on application context

### 🎯 **Enhanced Accuracy & Context**
- **Better OCR** integration and text extraction
- **Application-specific** prompting and behavior
- **File context** awareness (current document, project structure)
- **Temporal context** (understanding user's recent actions)
- **Privacy controls** and local processing options

### 🔧 **Core Improvements**
- **Performance optimization** for real-time suggestions
- **Better UI/UX** for suggestion display and interaction
- **Configuration system** for user preferences
- **Plugin architecture** for extensibility
- **Accessibility** improvements

## 💡 The Ultimate Goal

Imagine AI that:
- Knows you're writing an email and suggests professional completions
- Detects you're coding and provides contextual snippets
- Sees you're in a terminal and suggests commands
- Understands your screen content and provides relevant help
- Works seamlessly across every application you use

**We're not just building a completion tool—we're prototyping the future of human-AI interaction.**

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

---

## 🤝 Contributing

**This project is a call to action for the open source community.** We believe the future of AI interaction shouldn't be locked behind proprietary walls—it should be open, extensible, and shaped by the community.

### 🚀 Quick Start for Contributors
1. **Fork the repository**
2. **Pick an area** from our roadmap above
3. **Create an issue** to discuss your approach
4. **Submit a PR** with your improvements

### 🎯 High-Impact Contribution Areas

**Immediate Impact:**
- **Cross-platform ports** (Windows/macOS/Wayland)
- **Local AI model** integration (Ollama, GPT4All)
- **Better UI/UX** for suggestion display
- **Performance optimizations**

**Research & Innovation:**
- **Novel context extraction** methods
- **Application-specific AI** behavior
- **Privacy-preserving** AI techniques
- **Accessibility** improvements

**Community Building:**
- **Documentation** and tutorials
- **Demo videos** and examples
- **Blog posts** about the vision
- **Conference talks** and presentations

### 💬 Get Involved
- **Issues**: Report bugs, suggest features, discuss ideas
- **Discussions**: Share your vision for contextual AI
- **Discord/Matrix**: [Coming soon] Real-time collaboration
- **Twitter**: Share your experiments with #ContextualAI

### 🌍 Our Belief
**AI assistance should be:**
- **Universal** - Available everywhere you work
- **Contextual** - Understanding your environment
- **Open** - Not controlled by big tech alone
- **Privacy-conscious** - Your data, your choice
- **Community-driven** - Built by users, for users
- **Personal** - One AI that knows you, follows you, works for you

**Pi4Wear believes in "One AI. Just for you"** - where artificial intelligence feels as personal as the devices we hold dear. This project is step one in that journey.

**Want to be part of the full vision?** Join the movement at **[pi4wear.com](https://pi4wear.com)** and help us build AI that's truly personal and private.

**Together, we can make AI that truly follows the user, not the other way around.**

---

*This is just the beginning. Help us build the future of human-AI interaction.*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This software is provided for educational and productivity purposes.** Pi4Wear does not endorse, support, or assume responsibility for any malicious, illegal, or unethical use of this software. Users are solely responsible for ensuring their use complies with applicable laws and regulations.

**Responsible Use Guidelines:**
- Respect privacy and consent when using screen capture features
- Follow workplace policies regarding AI assistance tools
- Ensure compliance with local data protection laws
- Use the software ethically and responsibly

**Pi4Wear expressly disclaims any liability for misuse of this software.** 
