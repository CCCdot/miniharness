import os
import logging

from dotenv import load_dotenv
from openai import OpenAI

from tools.registry import ToolRegistry
load_dotenv()
logger = logging.getLogger(__name__)
class DeepSeekLLM():
    def __init__(self):
        self.model=os.getenv("DEEPSEEK_MODEL","deepseek-flash")
        if self.model:
            logger.info(f"Using model:{self.model}")
        self.base_url="https://api.deepseek.com"
        self.api_key=os.getenv("DEEPSEEK_API_KEY")
        if self.api_key:
            logger.info("api_key正确读取")
        else:
            logger.error("api_key错误")
            raise ValueError("DEEPSEEK_API_KEY is not configured")
        self.client=OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def chat(self,messages,tools=None):
        if tools:
            response=self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
        else:
            response=self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
        if response.choices:
            logger.error("api返回choices为空")
            raise IndexError("api返回choices为空")
        message = response.choices[0].message

        if message is None:
            logger.error("assistant message为空")
            raise RuntimeError("assistant message为空")
        #这里返回的是 OpenAI SDK 的 ChatCompletionMessage 对象，而不是普通 Python 字典。
        #最好修改成python字典，将模型返回的 assistant message 加入 messages 对话历史，再将整个 messages 传回 DeepSeek。
        return message.model_dump(exclude_none=True)