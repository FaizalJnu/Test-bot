import json
import os


def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    # IF YOU WANT TO CHANGE YOUR KNOWLEDGE DOC
    # UPLOAD A NEW ONE IN THE LEFT HAND PANEL
    # THEN REPLACE "knowledge.docx" BELOW WITH YOUR FILE NAME!
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    # IF YOU WANT TO CHANGE YOUR INSTRUCTIONS
    # MODIFIY THEM BELOW!
    assistant = client.beta.assistants.create(instructions="""
          The assistant, Faizal's personal assistant, has been programmed to help people maneuver this restraunt's menu.
          A document has been provided with information on the menu and other info.
          """,
                                              model="Mistral-7B-v0.1",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id