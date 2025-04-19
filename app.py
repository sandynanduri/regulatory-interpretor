import os
import gradio as gr
from datetime import datetime

# Allowed extensions
def allowed_ext(filename):
    return os.path.splitext(filename)[1].lower() in [".pdf", ".txt", ".docx"]

# Mock chatbot function (replace this with your LLM logic)
def chatbot_function(user_input, reg_files, tech_files, history):
    """
    user_input: the user's prompt
    reg_files: list of uploaded regulatory document file objects
    tech_files: list of uploaded technical spec file objects
    history: list of dicts with 'role' and 'content'
    """
    # Build response body
    response = f"Processed: '{user_input}'"
    reg_names = ", ".join(os.path.basename(f.name) for f in reg_files) if reg_files else None
    tech_names = ", ".join(os.path.basename(f.name) for f in tech_files) if tech_files else None
    if reg_names or tech_names:
        refs = ", ".join(filter(None, [reg_names, tech_names]))
        response += f"\n\n(Referencing: {refs})"

    # Append to history
    new_history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response}
    ]
    return new_history, new_history

# Custom CSS to hide built-in footer
custom_css = """
body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; }
.gr-chatbot { border: 1px solid #bdc3c7; border-radius: 5px; padding: 10px; background-color: #ffffff; }
footer {visibility: hidden}
"""

with gr.Blocks(
    title="Regulatory Interpretation Interface",
    css=custom_css
) as demo:
    # App header
    gr.HTML(
        """
        <div style='text-align: center; margin-bottom: 1em;'>
          <h1>💼 Regulatory Interpretation</h1>
          <p>Upload your <strong>📄 Regulatory Requirement</strong> and <strong>📑 Technical Specification</strong> files, then chat below.</p>
        </div>
        """
    )

    with gr.Row():
        # File upload panel
        with gr.Column(scale=1, min_width=200):
            reg_files = gr.File(
                label="Regulatory Requirement",
                file_types=[".pdf", ".txt", ".docx"],
                file_count="multiple"
            )
            tech_files = gr.File(
                label="Technical Specification",
                file_types=[".pdf", ".txt", ".docx"],
                file_count="multiple"
            )
            file_display = gr.HTML("")

            def show_uploaded(rf, tf):
                invalid = []
                for f in (rf or []):
                    if not allowed_ext(f.name): invalid.append(f.name)
                for f in (tf or []):
                    if not allowed_ext(f.name): invalid.append(f.name)
                if invalid:
                    msgs = [f"<span style='color:red'>Invalid file type: {name}</span>" for name in invalid]
                    return '<br>'.join(msgs)
                regs = '<br>'.join(f"{i+1}. {os.path.basename(f.name)}" for i,f in enumerate(rf)) if rf else 'None'
                techs = '<br>'.join(f"{i+1}. {os.path.basename(f.name)}" for i,f in enumerate(tf)) if tf else 'None'
                return (
                    f"<b>Regulatory ({len(rf) if rf else 0}):</b><br>{regs}<br><br>"
                    f"<b>Technical ({len(tf) if tf else 0}):</b><br>{techs}"
                )

            reg_files.change(show_uploaded, [reg_files, tech_files], file_display)
            tech_files.change(show_uploaded, [reg_files, tech_files], file_display)

        # Chat interface
        with gr.Column(scale=2, min_width=400):
            chatbot = gr.Chatbot(label="Chat with Regulatory GPT", type="messages")
            chat_history = gr.State([])

            # Input area: textbox and send button
            with gr.Column(elem_id="input-area"):
                user_input = gr.Textbox(
                    placeholder="Ask about requirements...", lines=3, elem_id="chat-input"
                )
                send_btn = gr.Button("Send", interactive=False)

            # Toggle send button interactivity
            user_input.change(
                lambda txt: gr.update(interactive=bool(txt.strip())),
                inputs=user_input,
                outputs=send_btn
            )

            # Submission events
            submit = user_input.submit(
                fn=chatbot_function,
                inputs=[user_input, reg_files, tech_files, chat_history],
                outputs=[chatbot, chat_history],
                queue=True
            )
            submit.then(lambda: "", None, user_input)

            click = send_btn.click(
                fn=chatbot_function,
                inputs=[user_input, reg_files, tech_files, chat_history],
                outputs=[chatbot, chat_history],
                queue=True
            )
            click.then(lambda: "", None, user_input)

    # Custom settings button
    gr.HTML(
        """
        <div style='position: fixed; bottom: 10px; right: 10px;'>
          <button id='custom-settings' style='background:none;border:none;cursor:pointer;'>
            <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'>
              <path fill='currentColor' d='M12 8a4 4 0 100 8 4 4 0 000-8zm8.94 4a6.98 6.98 0 00-.78-3.08l2.12-2.12-1.5-1.5-2.12 2.12A6.98 6.98 0 0012 3.06V1h-2v2.06a6.98 6.98 0 00-3.08.78L4.8 1.72l-1.5 1.5 2.12 2.12A6.98 6.98 0 003.06 12H1v2h2.06a6.98 6.98 0 00.78 3.08L1.72 19.2l1.5 1.5 2.12-2.12a6.98 6.98 0 003.08.78V23h2v-2.06a6.98 6.98 0 003.08-.78l2.12 2.12 1.5-1.5-2.12-2.12a6.98 6.98 0 00.78-3.08H23v-2h-2.06z'/>
            </svg>
          </button>
        </div>
        """
    )

    demo.launch(share=True)
