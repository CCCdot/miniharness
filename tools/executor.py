import json
import logging

from jsonschema import ValidationError, validate
from tools.registry import ToolRegistry
logger=logging.getLogger(__name__)
class ToolExectuor():
    def __init__(self, registry: ToolRegistry):
        #后续 Executor 不仅需要访问工具数据，还需要使用 Registry 提供的 get_tool() 方法，保存实例
        self.registry = registry

    def execute(self,tool_name,arguments):
        
        # 判断 arguments 类型
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError as e:
                logger.warning("Tool '%s' received invalid JSON: %s",tool_name,e.msg)
                raise

        elif not isinstance(arguments, dict):
            logger.warning(tool_name)
            raise TypeError("arguments必须是字符串或字典")

        # 检查JSON解析后的结果
        if not isinstance(arguments, dict):
            logger.warning(tool_name)
            raise TypeError("JSON解析结果必须是字典")

        #获取参数schema
        tool_use=self.registry.get_tool(tool_name)
        arguments_schema=tool_use["parameters"]
        
        #这个顺序应该是instance,schema，成功返回None，失败直接会ValidationError
        try:
            validate(
            instance=arguments,
            schema=arguments_schema
        )
        except ValidationError as e:
            logger.warning("Tool '%s' argument validation failed: %s",tool_name,e.message)
            raise
        """
        它需要完成：
        1. 根据 tool_name 找到对应工具。
        2. 从工具记录中提取 Python function。
        3. 将 arguments 传递给 function。
        4. 获取函数执行结果并返回。
        """
        try:
            return tool_use["function"](**arguments)
        except Exception:
            logger.exception("Tool '%s' execution failed", tool_name)
            raise