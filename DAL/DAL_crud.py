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
            print("⚠️ Cannot update agent without ID.")
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
                print("⚠️ Agent not found in DB.")
                return False

            print("✅ Agent updated successfully.")
            return True
        except Exception as e:
            print("❌ Error updating agent:", e)
            return False

    def delete_agent(self, agent_id):
        sql = "DELETE FROM agents WHERE id=%s"
        self.cursor.execute(sql, (agent_id,))
        self.conn.commit()
    def get_all_agents(self):
        sql = "SELECT * FROM agents"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [Agent(*row) for row in rows]
    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    a = Agent('r','chaim','now york','live',6,2)
    s = AgentDB()
    # s.create(a)
    # s.delete_agent(3)
    print(s.read_agent(2))
    s.update_agent(a)

    s.get_all_agents()
    s.close()