import gradio as gr

def validate_index(text: str) -> str:
    text = text or ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "NO_INPUT"
    return f"LINES={len(lines)}\nFIRST={lines[0]}"

demo = gr.Interface(
    fn=validate_index,
    inputs=gr.Textbox(lines=12, label="Paste machine-first index or recovery block"),
    outputs=gr.Textbox(lines=8, label="Validation summary"),
    title="OT Private Tools Starter",
    description="Safe starter utility. No secrets. No external state."
)

if __name__ == "__main__":
    demo.launch()
