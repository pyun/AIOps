import json
import anthropic
import boto3
import time


# Set up a Bedrock runtime client for model invocation
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

#print(bedrock_client.list_foundation_models())
#model_id = "anthropic.claude-3-haiku-20240307-v1:0"
#model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

def genPrompt(text):
    basePrompt = """
你是一个aws高级开发人员，对aws python sdk非常熟悉，你会根据用户在<text>标签中输入的需求，编写python程序，实现用户的需求。代码按照<require>标签中的要求生成。
<text>
{msg}
</text>
<require>
1、代码不要有异常捕获try catch
2、本程序是针对aws资源的相关查询代码，请根据aws python sdk使用合适的api和参数
3、程序中无需打印输出结果，直接返回程序的运行结果
4、要求程序的最后输出数据格式为pandas的DataFrame格式
5、程序运行结果赋值给一个固定的变量result。
6、所有数组按索引取值，map根据key取值，都做需要先做越界和存在判断。
7、生成的代码不要定义函数，请直接在主程序里实现全部功能。
8、如果需求是删除或修改资源，请生成的程序用dryrun方式运行，一定在aws的sdk调用中增加dryrun参数。
</require>
#生成的程序放在一个<programe>标签中,请跳过前言，直接输出结果
#根据用户的提示，判断输出结果是否适合生成图表，如果适合，请在<chart>标签中输出Pandas.plot图表类型，如果不适合生成图表，请保留空<chart>标签
#将生成的程序的依赖组成一个list，放到<package>标签中
"""
    fullPrompt = basePrompt.format(msg=text)
    return fullPrompt

def bedrock_invoke_model(prompt):
    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "messages": prompt,
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    # Invoke the model with the request.
    response = bedrock.invoke_model(modelId=model_id, body=request)
    print("--------------------2.model response----------------")
    print(response)
    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    return response_text

def invokeModel(prompt):
    print("--------------------1.prompt------------------")
    print(prompt)
    retry_count = 2
    result = ""
    while retry_count>0:
        try:
            result = bedrock_invoke_model(prompt)
            retry_count = 0
        except Exception as e:
            retry_count -= 1
            if retry_count>0:
                time.sleep(60)  
    print("--------------------3.prompt result----------------------")
    print(result)
    programe = result.split('<programe>')[1].split('</programe>')[0]
    chart = result.split('<chart>')[1].split('</chart>')[0]
    package = result.split('<package>')[1].split('</package>')[0]
    return programe,chart,package