import gradio as gr
from rag_server import ask_amul  # import your existing function

def chat_with_amul(message, history):
    """Wrapper for Gradio to use ask_amul with conversation history."""
    response = ask_amul(message)
    history.append((message, response))
    return "", history   # "" clears the textbox, history updates chatbot

# Gradio Chat UI
with gr.Blocks(css=".chatbot {height: 600px}") as demo:
    gr.Markdown("## 🧈 AmulGPT - Chat with Amul (RAG + Ollama + Pinecone)")

    chatbot = gr.Chatbot(elem_classes="chatbot")
    msg = gr.Textbox(label="Ask AmulGPT a question:", placeholder="Type your question here...")
    clear = gr.Button("Clear Chat")

    msg.submit(chat_with_amul, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=True)
