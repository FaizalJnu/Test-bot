from gradio import Interface
import mistral

model = mistral.__path__(model_name="Mistral-7B-v0.1")


def chat_with_mistral(message):
  response = model.predict(message)["text"]
  return response

interface = Interface(chat_with_mistral, "text", "text")

if __name__ == "__main__":
  interface.launch()


