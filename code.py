import model
import boto3
import pandas as pd
from datetime import datetime, timedelta,timezone
import time
import io
from botocore.exceptions import ClientError
import matplotlib.pyplot as plt
import utils
import traceback

def execCode(text):
    message_chat = [{
                "role": "user",
                "content": [{"type": "text", "text": model.genPrompt(text)}],
            }]

    retry_count = 3
    quit_flag = True
    result = ""
    chart = ""
    error = ""
    while retry_count>0 and quit_flag:
        if error!="":
            print(error)
            print("生成代码有问题，正在重新生成……")
            time.sleep(30)
        programe,chart,package = model.invokeModel(message_chat)

        print("--------------------4.install package-----------------------")
        utils.install_package(package)
        
        local_vars = {}
        error = ""
        try:
            exec(programe, globals(), local_vars)
            error=""
            result = local_vars['result']
            print("--------------------5. program run result--------------------")
            print(result)
        except Exception as e:
            error = traceback.format_exc()
        if (not isinstance(result,pd.DataFrame)) and error!="":
            assistant_message = {"role": "assistant",
                    "content": [{"type": "text", "text": programe}],
                }
            new_user_message = {
                    "role": "user",
                    "content": [{"type": "text", "text": f"程序运行发生如下错误：{error}"}],
                }
            message_chat.append(assistant_message)
            message_chat.append(new_user_message)
            retry_count -= 1
        else:
            quit_flag = False
    #print("chart:",chart)
    if len(chart.strip())>0:
        # 设置Timestamp为索引
        df = pd.DataFrame(result)
        df.set_index(df.columns[0], inplace=True)
        df.sort_index(inplace=True)

        # 绘制折线图
        plt.figure(figsize=(12, 6))
        #print("-------df-----")
        #print(df)
        for item in df.columns:
            #print(item)
            plt.plot(df.index, df[item], label=item)
    
        #plt.xlabel('Timestamp')
        #plt.ylabel('Network Traffic')
        #plt.title('Network Traffic Over Time')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)

        # 保存图像
        plt.savefig('file/temp.png', dpi=300, bbox_inches='tight')
    return result,chart