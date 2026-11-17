import logging
from datetime import date,timedelta
from agent import AgentRuntime
from core.llm import DeepSeekLLM
from tools.registry import ToolRegistry
from tools.executor import ToolExectuor
from agent.state import AgentState

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
tools_executor=ToolExectuor(tools)
t=date.today()
agent_state=AgentState(t)
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
agent=AgentRuntime(DeepSeekLLM(),tools,tools_executor,agent_state)
print(agent_state.session_id)
user_input = """
请严格按以下顺序使用工具：

第一步：调用 division 计算 100 除以 5。
第二步：获取第一步结果，再调用 calculator 将结果加上 20。

必须分两轮完成工具调用，不要直接心算，也不要省略任何一步。
"""


print(agent.run("把刚才的结果再加上20"))
