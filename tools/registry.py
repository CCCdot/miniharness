class ToolRegistry():
    def __init__(self):
        #注册一个空字典用来存储工具
        self.registry={}

    def register(self,name,description,parameters,function):
        #检查name合法性
        name=name.strip()
        if not isinstance(name,str):
            raise TypeError(f"{name}数据类型不是字符串")
        if not name.strip():
            raise ValueError(f"{name}内容不能为空")
        if name in self.registry:
            raise ValueError("工具名称重复")

        #检查description合法性
        if not isinstance(description,str):
            raise TypeError(f"{description}数据类型不是字符串")
        if not description.strip():
            raise ValueError(f"{description}内容不能为空")

        #检查parameters数据结构合法性
        if not isinstance(parameters,dict):
            raise TypeError(f"{parameters}数据类型错误，不是字典")
        if not parameters:
            raise ValueError(f"{parameters}内容为None")
        
        #检查function调用合法性
        if not callable(function):
            raise TypeError(f"{function}不是可调用对象")

        self.registry[name] = {
        "name": name,
        "description": description,
        "parameters": parameters,
        "function": function
        }

    def get_tool(self,name):
        if not isinstance(name,str):
            raise TypeError(f"{name}不是字符串类型")
        name=name.strip()
        if not name:
            raise ValueError(f"{name}是空字符串")
        if not name in self.registry:
            raise KeyError(f"{name}不是已注册工具")
        return self.registry[name]
    
    def get_tools_schema(self):
        tools_schema=[]
        for name,tool in self.registry.items():
            tool_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        }

        tools_schema.append(tool_schema)
        return tools_schema