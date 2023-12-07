from Null import NullObject
import asyncio
import threading
import aiohttp


class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class SendToOpenAICommand(Command):
    def __init__(self, receiver, data):
        self._receiver = receiver
        self._data = data
        print('called')

    async def execute(self):
        print('called')
        await self._receiver.async_send_to_openai(self._data)


class ModifyPromptCommand(Command):
    def __init__(self, receiver, new_prompt):
        self._receiver = receiver
        self._new_prompt = new_prompt
        self._old_prompt = None

    def execute(self):
        self._old_prompt = self._receiver.prompt
        self._receiver.modify_prompt(self._new_prompt)

    def undo(self):
        if self._old_prompt is not None:
            self._receiver.modify_prompt(self._old_prompt)

# Additional commands can be defined following the same pattern


class CommandInvoker:
    def __init__(self):
        self._commands = []
        self._current = -1

    def store_and_execute(self, command):
        self._commands.append(command)
        command.execute()
        self._current += 1

    async def async_store_and_execute(self, command):
        print('Invoker async_store_and_execute called')
        self._commands.append(command)
        if asyncio.iscoroutinefunction(command.execute):
            
            await command.execute()
        else:
            
            command.execute()
            self._current += 1

    def undo(self):
        if self._current >= 0:
            self._commands[self._current].undo()
            self._current -= 1

    def redo(self):
        if self._current + 1 < len(self._commands):
            self._current += 1
            self._commands[self._current].execute()



class Receiver:
    def __init__(self, api_key):
        self.prompt = ""
        self.api_key = api_key
        self.response = None  # Store the response

    async def async_send_to_openai(self, user_input):
        print('async send to openai called.')
        async with aiohttp.ClientSession() as session:
            url = "https://api.openai.com/v1/engines/davinci/completions"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {"prompt": user_input, "max_tokens": 150}
            
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    self.response = await response.json()  # Assuming JSON response
                else:
                    self.response = {"error": "Error in API response"}









'''
    # Client code
    if __name__ == "__main__":
        receiver = Receiver()
        invoker = CommandInvoker()

        send_command = SendToOpenAICommand(receiver, "Data to send")
        modify_command = ModifyPromptCommand(receiver, "New prompt text")

        invoker.store_and_execute(send_command)
        invoker.store_and_execute(modify_command)
    
    
 ''' 