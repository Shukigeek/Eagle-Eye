class Agent:
    def __init__(self,codeName,realName,location,status,missionsCompleted,id=None):
        self.id = id
        self.codeName = codeName
        self.realName = realName
        self.location = location
        self.status = status
        self.missionsCompleted = missionsCompleted
    def __str__(self):
        return (f"ID: {self.id}\n"
                f"code name: {self.codeName}\n"
                f"real name: {self.realName}\n"
                f"location: {self.location}\n"
                f"status: {self.status}\n"
                f"missions completed: {self.missionsCompleted}")