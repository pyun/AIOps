import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import io
import json
import anthropic
import boto3
import code

def process_input(text):
    # 这里你可以添加你想要的逻辑来处理输入的文本
    # 例如,你可以返回一个字符串、一个DataFrame或一个图像
    #output_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    result,chart = code.execCode(text)
    pd.DataFrame(result).to_csv('file/temp.csv', index=False)


    #data = json.loads(result)
    #output_df = pd.DataFrame(result)
    #output_df = code
    #return  [output_df,"temp.png" if len(chart.strip())>0 else None]
    visible = False
    image_file = None
    if len(chart.strip())>0:
        visible = True
        image_file = "file/temp.png"
    
    return {
            output_df: gr.DataFrame(value=pd.DataFrame(result)),
            output_img: gr.Image(visible=visible,value=image_file)
        }

def clear_input():
    #return None
    return {
            inputs: gr.Textbox(value=None),
            output_df: gr.DataFrame(value=None),
            output_img: gr.Image(visible=False)
        }

with gr.Blocks() as demo:
    with gr.Row():
        inputs = gr.Textbox(label="输入文本")
    with gr.Row():
        submit_btn = gr.Button("提交")
        clear_btn = gr.Button("清除")
        gr.Button(value="导出",link="file=file/temp.csv")
    with gr.Row():
        output_df = gr.DataFrame(label="输出表格")
    with gr.Row() as img_block:
        output_img = gr.Image(label="输出图片",visible=False)
    submit_btn.click(fn=process_input, inputs=inputs, outputs=[output_df,output_img])
    clear_btn.click(fn=clear_input, outputs=[inputs,output_df,output_img])
    #clear_btn.click(lambda: None, None, inputs, queue=False)

demo.launch(share=True,allowed_paths=["./file/"])
