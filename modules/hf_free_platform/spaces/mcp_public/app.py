import gradio as gr


def normalize_block(text: str) -> str:
    text = text or ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "STATUS=EMPTY"

    normalized = "\n".join(lines)
    return (
        f"STATUS=OK\n"
        f"LINES={len(lines)}\n"
        f"FIRST={lines[0]}\n\n"
        f"NORMALIZED\n{normalized}"
    )


demo = gr.Interface(
    fn=normalize_block,
    inputs=gr.Textbox(lines=12, label="Paste a machine-first block"),
    outputs=gr.Textbox(lines=10, label="Normalized output"),
    title="OT MCP Public Starter",
    description="Minimal public callable utility. No secrets. No privileged operations.",
)


if __name__ == "__main__":
    demo.launch()
