import logging

from core.llm import DeepSeekLLM
from tools.registry import ToolRegistry
from tools.executor import ToolExectuor
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def add(a,b):
    return a+b
def division(a,b):
    if not b:
        raise ZeroDivisionError
    if not isinstance(a,int):
        raise TypeError("schema验证失败")
    return a/b
tools=ToolRegistry()
#name,description,parameters,function
parameters = {
    "type": "object",
    "properties": {
        "a": {
            "type": "integer",
            "description": "第一个加数"
        },
        "b": {
            "type": "integer",
            "description": "第二个加数"
        }
    },
    "required": ["a", "b"],
    "additionalProperties": False
}
parameters1 = {
    "type": "object",
    "properties": {
        "a": {
            "type": "integer",
            "description": "被除数"
        },
        "b": {
            "type": "integer",
            "description": "除数"
        }
    },
    "required": ["a", "b"],
    "additionalProperties": False
}
tools.register("calculator","两数相加",parameters,add)
tools.register("division","两数相除",parameters1,division)
print(tools.get_tools_schema())
arguments = '{"a": 10, "b": }'
executor=ToolExectuor(tools)
print(executor.execute("division",arguments))
#tools.register("calculator","两数相加",parameters,add)
#tools.get_tool("minus")
#tools.get_tool(add)