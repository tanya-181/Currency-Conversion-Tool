from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests
from dotenv import load_dotenv

load_dotenv()

#create tool
#conversion factor tool
from langchain_core.tools import InjectedToolArg
from typing import Annotated

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """
    This function fetches the currency conversion factor between a given base currency and a target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/6406415841ae46dca8061b90/pair/{base_currency}/{target_currency}'

    response = requests.get(url)

    return response.json() #the api sends json back

# result = get_conversion_factor.invoke({"base_currency" : "SGD", "target_currency" : "INR"})
# print(result)


@tool
def convert(base_currency_value: int, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
    """
    Given a currency conversion rate this function calculates the target currency value from a given base currency value
    """

    return base_currency_value * conversion_rate

#final_result = convert.invoke({"base_currency_value" : 10, "conversion_rate" : 75.3762})  


#tool binding 
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash")

llm_with_tools = llm.bind_tools([get_conversion_factor, convert])


messages = [HumanMessage('what is the conversion factor between SGD and INR, and based on that can you convert 20 SGD to INR')]

ai_message = llm_with_tools.invoke(messages)


print(ai_message.tool_calls)

import json
for tool_call in ai_message.tool_calls:  #go through every tool call gemini requested
    #execute the 1st tool and get the value of conversion rate 
    if tool_call['name'] == 'get_conversion_factor':   #checking which tool gemini requested, if gemini requested get_conversion_factor then execute the same
        tool_message1 = get_conversion_factor.invoke(tool_call)  # where tool actually runs
        print(tool_message1)
        #fetch this conversion rate

        conversion_rate = json.loads(tool_message1.content)['conversion_rate']
        #append this tool to messages list

        messages.append(ai_message)  #save gemini previous response in the convo
        messages.append(tool_message1)  #save the result returned by the tool

    #execute the 2nd tool using the conversion rate from tool
    if tool_call['name'] == 'convert':
        #fetch the current arg
        tool_call['args']['conversion_rate'] = conversion_rate
        tool_message2 = convert.invoke(tool_call)
        messages.append(tool_message2)

result = llm_with_tools.invoke(messages).content     
print(result)
