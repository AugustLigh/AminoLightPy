from time import sleep
from AminoLightPy import Client, SubClient
# Your help message
help_message = """
Welcome!
This is help page.
"""
# Create Client object
client = Client()
# Login into account
client.login("example_mail@gmail.com", "example_password")
# And display the help !
@client.event("on_text_message")
def on_message(data):
    comId = data.comId
    chatId = data.message.chatId

    if data.message.author.userId != client.profile.userId:  # Do not answer to myself
        # Create SubClient object
        sub_client = SubClient(comId=comId, profile=client.profile)
        if data.message.content.startswith('/help'):
            # typing
            with client.typing(chatId=chatId, comId=comId):
                # imitation of work
                sleep(3)
                sub_client.send_message(chatId=chatId, message=help_message)