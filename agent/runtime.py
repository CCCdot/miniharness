
import logging

logger = logging.getLogger(__name__)


class AgentRuntime:
    def __init__(self, llm, registry, executor,state):
        # 注入三个依赖对象
        self.llm = llm
        self.tool_registry = registry
        self.tool_executor = executor
        self.agentstate=state

    def run(self, user_input, max_iterations=10):
        # 检查最大迭代次数
        if not isinstance(max_iterations, int) or isinstance(max_iterations, bool) or max_iterations < 1:
            raise ValueError("max_iterations必须是正整数")

        # 记住之前的信息
        messages = self.agentstate.messages
        new_message={"role": "user", "content": user_input}
        messages.append(new_message)

        # 获取所有工具的Schema
        tools_schema = self.tool_registry.get_tools_schema()

        # 第一次调用LLM
        response = self.llm.chat(messages, tools_schema)

        iteration = 0

        # Agent Loop
        while response.get("tool_calls"):

            # 检查最大迭代次数
            if iteration >= max_iterations:
                logger.error("Agent exceeded maximum iterations: %s", max_iterations)
                raise RuntimeError("Agent超过最大迭代次数")

            # 保存Assistant的工具调用消息
            messages.append(response)

            # 遍历当前轮次的所有工具调用
            for tool_call in response["tool_calls"]:

                tool_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                tool_call_id = tool_call["id"]

                # 执行工具，捕获异常
                try:
                    result = self.tool_executor.execute(
                        tool_name,
                        arguments
                    )

                    tool_content = str(result)

                except Exception as e:
                    logger.warning(
                        "Tool '%s' failed: %s: %s",
                        tool_name,
                        type(e).__name__,
                        e
                    )

                    # 将错误信息反馈给LLM
                    tool_content = (
                        f"Tool execution failed: "
                        f"{type(e).__name__}: {e}"
                    )

                # 无论成功还是失败，都生成Tool Message
                tool_result = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_content
                }

                messages.append(tool_result)

            # 完成一轮工具调用，迭代次数加一
            iteration += 1

            # 将本轮所有工具执行结果反馈给LLM
            response = self.llm.chat(messages, tools_schema)

        # 没有新的工具调用，返回最终回答
        final_content = response.get("content")

        if final_content is None:
            raise RuntimeError("模型没有返回最终文本内容")
        
        # 保存最终 Assistant Message
        messages.append(response)
        return final_content

    def reset(self):
        self.agentstate.reset()