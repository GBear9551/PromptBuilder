# Program Title: Prompt Builder
# Program description: A simple program designed to manage prompts.
# Date: 11/17/2023
# Recent Update: 12/6/2023

# Headers
import tkinter as tk
import asyncio
import threading
from UI import UserInterface

# Function to start the asyncio event loop in a separate thread
def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Main loop
def main():
    # Create a new asyncio event loop
    loop = asyncio.new_event_loop()
    
    # Start the asyncio event loop in a separate thread
    loop_thread = threading.Thread(target=start_asyncio_loop, args=(loop,), daemon=True)
    loop_thread.start()

    # Initialize and run the Tkinter application with the event loop reference
    root = tk.Tk()
    app = UserInterface(root, asyncio_loop=loop)
    app.run()

if __name__ == "__main__":
    main()