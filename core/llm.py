import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
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

    def chat(self,messages):
        response=self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        if response.choices:
            if response.choices[0].message.content:
                return response.choices[0].message.content
            else:
                logger.error("输出为None")
                raise RuntimeError("message.content为空")
        else: 
            raise RuntimeError("response.choices为空")