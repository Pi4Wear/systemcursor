import sys
import os
import time
import signal
import logging
import threading
import subprocess
import shutil
from datetime import datetime
from io import BytesIO

# Third-party libraries
try:
    from pynput import keyboard
    from pynput.keyboard import Key, Listener, Controller
    import pyscreenshot as ImageGrab
    from PIL import Image
    import google.generativeai as genai
    import pytesseract
except ImportError as e:
    print(f"❌ A required library is not installed: {e}")
    print("Please run the `run.sh` script to install dependencies.")
    sys.exit(1)

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProAICompleter:
    def __init__(self):
        # State
        self.is_running = True
        self.key_buffer = []
        self.ctrl_pressed = False
        
        # Suggestion State
        self.current_suggestion = ''
        self.is_suggestion_active = False
        self.is_inserting_suggestion = False

        # Timers & Controllers
        self.completion_timer = None
        self.keyboard_controller = Controller()
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)

        # Statistics
        self.completions_shown = 0
        self.total_inputs = 0
        
        # --- AI Configuration ---
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logging.error("❌ GEMINI_API_KEY environment variable not set.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def _cancel_completion_timer(self):
        if self.completion_timer:
            self.completion_timer.cancel()
            self.completion_timer = None

    def on_press(self, key):
        if self.is_inserting_suggestion:
            return

        # --- Hotkey: Ctrl+L for context reset ---
        if key in {Key.ctrl_l, Key.ctrl_r}:
            self.ctrl_pressed = True
            return
        
        if self.ctrl_pressed and hasattr(key, 'char') and key.char == 'l':
            logging.info('🔄 Context manually cleared with Ctrl+L')
            self.key_buffer.clear()
            self._cancel_completion_timer()
            if self.is_suggestion_active:
                self._remove_suggestion()
            return

        self._cancel_completion_timer()
        self.total_inputs += 1
        
        try:
            # --- Suggestion Handling ---
            if self.is_suggestion_active:
                if key == Key.tab:
                    self._accept_suggestion()
                    return
                elif key == Key.esc:
                    self._remove_suggestion()
                    return
                else:
                    self.is_suggestion_active = False
                    self.current_suggestion = ''
            
            # --- Buffer Management ---
            if hasattr(key, 'char') and key.char:
                self.key_buffer.append(key.char)
            elif key == Key.space:
                self.key_buffer.append(' ')
            elif key == Key.backspace:
                if self.key_buffer: self.key_buffer.pop()
            elif key == Key.enter:
                self.key_buffer.clear()
                return

            # --- Trigger Completion ---
            text = ''.join(self.key_buffer)
            if len(text.strip()) > 4:
                self.completion_timer = threading.Timer(0.7, self._trigger_ai_completion)
                self.completion_timer.start()

        except Exception as e:
            logging.error(f"Error on key press: {e}", exc_info=True)

    def on_release(self, key):
        if key in {Key.ctrl_l, Key.ctrl_r}:
            self.ctrl_pressed = False

    def _accept_suggestion(self):
        logging.info('✅ Suggestion accepted with Tab')
        self.is_inserting_suggestion = True
        try:
            self.keyboard_controller.press(Key.right)
            self.keyboard_controller.release(Key.right)
        finally:
            self.is_inserting_suggestion = False
        
        self.key_buffer.extend(list(self.current_suggestion))
        self.is_suggestion_active = False
        self.current_suggestion = ''

    def _trigger_ai_completion(self):
        if self.is_suggestion_active or self.is_inserting_suggestion:
            return
            
        text = ''.join(self.key_buffer[-1000:]) # Limit context size
        if len(text.strip()) < 5:
            return

        logging.info(f'🎯 User paused, checking for completion on: "{text}"')
        threading.Thread(target=self._generate_ai_completion, args=(text,), daemon=True).start()

    def _get_context(self):
        """Captures screenshot, extracts text with OCR, and gets window title."""
        context = {}
        # Get Window Title
        try:
            if shutil.which("xdotool"):
                context['window_title'] = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname']).decode('utf-8').strip()
            else:
                context['window_title'] = "Unknown"
        except Exception:
            context['window_title'] = "Unknown"

        # Get Screenshot and run OCR
        try:
            screenshot = ImageGrab.grab()
            context['ocr_text'] = pytesseract.image_to_string(screenshot)
        except Exception as e:
            if "Tesseract is not installed" in str(e):
                 logging.error("❌ Tesseract is not installed or not in your PATH. Please install it.")
            else:
                logging.warning(f"Could not grab screenshot or run OCR: {e}")
            context['ocr_text'] = ""
        
        return context

    def _generate_ai_completion(self, text):
        try:
            context = self._get_context()
            window_title = context['window_title']
            ocr_text = context.get('ocr_text', "")

            prompt_parts = [
                "You are an intelligent inline completion tool. This is your context.",
                f"The user is in an application with the window title: '{window_title}'.",
                "Sometimes you provide huge completion sometimes less. Behave appropriately.",
                "Here is the text context from the screen (via OCR):",
                "--- OCR CONTEXT ---",
                ocr_text,
                "--- END OCR CONTEXT ---",
                "Sometimes the user might be typing a new text altogether, you need to be careful about that.",
                "You need to be very careful about the user's context and the text they are typing.",
                "You need to be very careful about the user's context and the text they are typing.",
                "\nHere is the text the user is currently typing:",
                text
            ]

            logging.info('🔄 Generating completion with OCR context...')
            response = self.model.generate_content(prompt_parts)
            
            completion = response.text.strip()
            
            if completion:
                if completion.lower().startswith(text.lower()):
                    completion = completion[len(text):].strip()
                
                # Basic cleanup
                completion = completion.strip('"').strip("'").strip('*').strip('`')
                
                if not completion or len(completion) < 2:
                    logging.info("❌ AI returned an empty or too-short completion.")
                    return

                logging.info(f'🤖 AI Completion: {completion}')
                self.completions_shown += 1
                self._insert_suggestion(completion)
                
        except Exception as e:
            logging.error(f"❌ AI generation failed: {e}", exc_info=True)
    
    def _insert_suggestion(self, suggestion):
        self.is_inserting_suggestion = True
        try:
            if self.is_suggestion_active: return
            self.keyboard_controller.type(suggestion)
            
            # Select the suggestion for easy overwriting
            for _ in range(len(suggestion)):
                self.keyboard_controller.press(Key.shift)
                self.keyboard_controller.press(Key.left)
                self.keyboard_controller.release(Key.left)
                self.keyboard_controller.release(Key.shift)
                time.sleep(0.005)
            
            self.current_suggestion = suggestion
            self.is_suggestion_active = True
            logging.info(f'✨ Inserted suggestion: "{suggestion}"')
            
        except Exception as e:
            logging.error(f"Error inserting suggestion: {e}", exc_info=True)
        finally:
            self.is_inserting_suggestion = False
    
    def _remove_suggestion(self):
        if not self.is_suggestion_active: return
        self.is_inserting_suggestion = True
        try:
            # Clear the timer because we are actively dismissing.
            self._cancel_completion_timer() 
            suggestion_length = len(self.current_suggestion)
            for _ in range(suggestion_length):
                self.keyboard_controller.press(Key.backspace)
                self.keyboard_controller.release(Key.backspace)
                time.sleep(0.005)
        finally:
            self.is_inserting_suggestion = False
            self.is_suggestion_active = False
            self.current_suggestion = ''
            logging.info('🗑️ Removed suggestion.')

    def start(self):
        logging.info('🚀 Starting Pro AI Completer...')
        self.listener.start()
        logging.info('✨ AI Completion is now active!')
        logging.info('💡 Type and pause for suggestions.')
        logging.info('✅ Press Tab to accept, Esc to reject.')
        logging.info('🔄 Press Ctrl+L to clear context.')
        logging.info('🛑 Press Ctrl+C in the terminal to quit.')
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        logging.info('👋 Shutting down...')
        self.is_running = False
        if self.listener.is_alive():
            self.listener.stop()
        self._cancel_completion_timer()
        logging.info(f'📊 Session Stats: {self.total_inputs} inputs, {self.completions_shown} completions.')

def main():
    # Graceful shutdown handler
    def signal_handler(signum, frame):
        # This will be caught by the KeyboardInterrupt in start()
        raise KeyboardInterrupt
    
    signal.signal(signal.SIGINT, signal_handler)
    
    app = ProAICompleter()
    app.start()

if __name__ == "__main__":
    main() 