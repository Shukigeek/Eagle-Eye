from DAL.sqlConnection import connect_db
from model.agents import Agent
class AgentDB():
    def __init__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
    def create(self,agent: Agent):
        query = """INSERT INTO agents (codeName, realName, location, status, missionsCompleted)
                 VALUES (%s, %s, %s, %s, %s)"""
        self.cursor.execute(query, (agent.codeName, agent.realName, agent.location, agent.status, agent.missionsCompleted))
        self.conn.commit()
        agent.id = self.cursor.lastrowid
        return agent.id


    def read_agent(self, agent_id):
        query = "SELECT * FROM agents WHERE id = %s"
        self.cursor.execute(query, (agent_id,))
        row = self.cursor.fetchone()
        if row:
            return Agent(*row[1:], id=row[0])
        return None

    def update_agent(self, agent: Agent):
        if agent.id is None:
            print("Cannot update agent without ID.")
            return False
        try:
            sql = """UPDATE agents
                     SET codeName=%s, realName=%s, location=%s, status=%s, missionsCompleted=%s
                     WHERE id=%s"""
            self.cursor.execute(sql, (
                agent.codeName,
                agent.realName,
                agent.location,
                agent.status,
                agent.missionsCompleted,
                agent.id
            ))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False
            return True
        except Exception as e:
            print("Error updating agent:", e)
            return False

    def delete_agent(self, agent_id):
        sql = "DELETE FROM agents WHERE id=%s"
        self.cursor.execute(sql, (agent_id,))
        self.conn.commit()
    def get_all_agents(self):
        sql = "SELECT * FROM agents"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [Agent(codeName=row[1],realName=row[2],
                      location=row[3],status=row[4],missionsCompleted=row[5],id=row[0]) for row in rows]
    def close(self):
        self.cursor.close()
        self.conn.close()

