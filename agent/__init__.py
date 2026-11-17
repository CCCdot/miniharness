class AgentRuntime:
    def __init__(self, llm, registry, executor):
        # 保存三个依赖对象
        self.llm=llm
        self.tool_registry=registry
        self.tool_executor=executor

    def run(self,user_input):
        messages=[{"role":"user",
                 "content":user_input}]
        tools_schema=self.tool_registry.get_tools_schema()
        response=self.llm.chat(messages, tools_schema)
        if response.get("tool_calls"):
            messages.append(response)
            #这里应该是个列表，然后这个列表里有很多工具，暂时只考虑一个工具的存在
            tool_call = response["tool_calls"][0]

            tool_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            result = self.tool_executor.execute(tool_name, arguments)
            tool_result={"role":"tool",
                         "tool_call_id":tool_call["id"],
                         "content":str(result)}
            messages.append(tool_result)
            #信息返回llm,保存第二次回答
            response=self.llm.chat(messages, tools_schema)
            if not response.get("tool_calls"):
                return response["content"]

        else:
            return response["content"]