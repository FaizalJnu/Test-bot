import streamlit as st
# Load model directly
from mistral import Client
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi there! How can I help you?"}]

def mistral_inference(user_query, conversation_history=[]):
  # Tokenize the query
  input_ids = tokenizer(user_query, return_tensors="pt").input_ids

  # Generate response with past conversation context (if applicable)
  if conversation_history:
    past = tokenizer(conversation_history, return_tensors="pt").input_ids
    past = past[:, :-1]  # Remove last token for causal generation
    outputs = model.generate(input_ids, past=past)
  else:
    outputs = model.generate(input_ids)

  # Decode the generated response
  generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
  return generated_text


st.title(" Chatbot")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.text_input(""):
    if not prompt:
        st.info("Please type a message to chat.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate response using Mistral
    response = mistral_inference(prompt, conversation_history=st.session_state.messages[-2:])
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

