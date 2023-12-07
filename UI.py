import tkinter as tk
from tkinter import messagebox
import openai
from Command import SendToOpenAICommand, ModifyPromptCommand, CommandInvoker, Receiver
from Null import NullObject
import asyncio

class UserInterface:
    def __init__(self, root, asyncio_loop):
        self.root = root
        self.root.title("GSL Drag & Drop")
        self.receiver = Receiver("api-key")
        self.invoker = CommandInvoker()
        self.asyncio_loop = asyncio_loop
        #Prototype design pattern for variable: self.send_button
        self.setup_ui()

        # ... You can set up OpenAI API key here, or load from configuration
        openai.api_key = "your-api-key" # Please use an enivornment 

    def createLLMOutputFrame(self,parentFrame):
        # Declare and initialize variables
        target_text_frame = tk.Frame(parentFrame, bd=2, relief="solid", width=500, height=600)
        target_text_frame.pack(side="left", padx=5, pady=5, expand=True, fill="both")

        # Text Frame
        # Create a Text widget to input target text
        # The target text is in the local scope and needs to beable to be accessed and mutated by the UI class. 
        self.target_text = tk.Text(target_text_frame, wrap="word")
        self.target_text.pack(expand=True, fill="both", padx=10, pady=10)

        # return
        return target_text_frame


    def createPromptFrame(self, parentFrame):
        # Declare and initialize variables
        # Bottom frame
        prompt_frame = tk.Frame(parentFrame, bd=2, relief="solid", height=50)
        prompt_frame.pack(padx=10, pady=5, fill="x")

        # Modify this line and add the `height` option
        self.prompt_text = tk.Text(prompt_frame, height=5, wrap="word")  # Adjust the height as needed
        # This should fill only the x direction and leave room for the button on the right.
        self.prompt_text.pack(side="left", expand=True, fill="x", padx=10, pady=10)

        # No return
        return prompt_frame

    def createSendButton(self, parentFrame):
        # Button frames container on the right
        button_frames_container = tk.Frame(parentFrame)
        # This should be packed to the right of the prompt_text which is packed to the left.
        button_frames_container.pack(side="right", padx=5, pady=5)

        self.send_button = tk.Button(button_frames_container, text="Send", command=self.on_send_click)
        # The button should be packed inside the button_frames_container.
        self.send_button.pack()
        return button_frames_container  


    def setup_ui(self):
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=100, pady=100, expand=True, fill="both")


        # Create a Command instances SendButtonCommand instance only when the send button is pressed.
          #cmd_send_prompt = SendPromptCommand(self.receiver,data)


        # ... Add other UI setup here, like creating text areas, buttons, etc.

        # The Main Frame contains all the widgets

          # Display LLM output frame, this is a text frame, because it will show text. 
            # Create the frame for the LLM output frame such that it is the child of the main frame.
              # function: createLLMOutputFrame(parentFrame)
        tf = self.createLLMOutputFrame(self.main_frame)

          # Display Prompt frame
            # Create the Prompt, text frame, child of main frame or child of LLMOutput frame.
        promptFrame = self.createPromptFrame(tf) 


          # Buttons (includes prompt-send button and more)
            # Create Button Frame, child of main frame, and to the right of the LLMOutput frame. 

            # Send Button
        self.createSendButton(promptFrame)
        # Bind the send button to a command instance
        

              # Create Button 

            # Edit Prompts Button

            # Prompt Buttons





        # Example: Create a Text widget for input

        # Example: Create a Send button





    def enable_send_button(self):
        self.send_button.config(state='normal')  # Re-enable the button


    def on_send_click(self):
        self.send_button.config(state='disabled')  # Disable the button
        user_input = self.prompt_text.get("1.0", tk.END).strip()

        send_command = SendToOpenAICommand(self.receiver, user_input) 
           
        future = asyncio.run_coroutine_threadsafe(
                self.invoker.async_store_and_execute(send_command),
                self.asyncio_loop
            )
        future.add_done_callback(lambda f: self.root.after(0, self.update_target_text))
         

    def update_target_text(self):
        # Safely update the target_text widget with the response
        print("Future returned.")
        if hasattr(self.receiver, 'response'):
            response_text = self.receiver.response.get('choices', [{}])[0].get('text', '')
            self.target_text.insert(tk.END, response_text + '\n')
            self.send_button.config(state='normal')  # Re-enable the button
            print("Future goal.")




    def get_response_from_api(self, user_input):
        # ... Implement the API call and response handling here
        pass

    # ... Add other methods as needed, such as for performing thought compression





    # Start the application
    def run(self):
        self.root.mainloop()