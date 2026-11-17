class AgentState:
    def __init__(self,session_id):
        self.messages=[]
        self.iterations=0
        self.session_id=session_id

    def add_message(self,message):
        self.messages.append(message)

    def reset(self):
        self.messages=[]
        self.iteration=0