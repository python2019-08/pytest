import gradio as gr
 
with gr.Blocks() as demo:
    with gr.Row():
        text1 = gr.Textbox(label="t1")
        slider2 = gr.Textbox(label="s2")
        drop3 = gr.Dropdown(["a", "b", "c"], label="d3")
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            text1 = gr.Textbox(label="prompt 1")
            text2 = gr.Textbox(label="prompt 2")
            inbtw = gr.Button("Between")
            text4 = gr.Textbox(label="prompt 1")
            text5 = gr.Textbox(label="prompt 2")
        with gr.Column(scale=2, min_width=300):
            img1 = gr.Image("images/cheetah.jpg")
            btn = gr.Button("Go")


demo.launch()

# with gr.Blocks() as demo:
#     a = gr.Number(label="a")
#     b = gr.Number(label="b")
#     with gr.Row():
#         add_btn = gr.Button("Add")
#         sub_btn = gr.Button("Subtract")
#     c = gr.Number(label="sum")

#     def add(num1, num2):
#         return num1 + num2
#     add_btn.click(add, inputs=[a, b], outputs=c)

#     def sub(data):
#         return data[a] - data[b]
#     sub_btn.click(sub, inputs={a, b}, outputs=c)
# 
# demo.launch()