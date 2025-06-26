from DAL.DAL_crud import AgentDB
from model.agents import Agent

def menu():
    db = AgentDB()
    while True:
        print("\n--- Eagle Eye Agent Management ---")
        print("1. Add agent")
        print("2. View agent by ID")
        print("3. Update agent")
        print("4. Delete agent")
        print("5. List all agents")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            codeName = input("Code Name: ")
            realName = input("Real Name: ")
            location = input("Location: ")
            status = input("Status (Active/Injured/Missing/Retired): ")
            missionsCompleted = int(input("Missions Completed: "))
            agent = Agent(codeName, realName, location, status, missionsCompleted)
            db.create(agent)
            print("Agent added with ID:", agent.id)

        elif choice == '2':
            id = int(input("Enter Agent ID: "))
            agent = db.read_agent(id)
            if agent:
                print(agent)
            else:
                print("Agent not found")

        elif choice == '3':
            id = int(input("Enter Agent ID to update: "))
            agent = db.read_agent(id)
            if agent:
                agent.codeName = input(f"Code Name [{agent.codeName}]: ") or agent.codeName
                agent.realName = input(f"Real Name [{agent.realName}]: ") or agent.realName
                agent.location = input(f"Location [{agent.location}]: ") or agent.location
                agent.status = input(f"Status [{agent.status}]: ") or agent.status
                missions = input(f"Missions Completed [{agent.missionsCompleted}]: ")
                if missions:
                    agent.missionsCompleted = int(missions)
                db.update_agent(agent)
                print("Agent updated")
            else:
                print("Agent not found")

        elif choice == '4':
            id = int(input("Enter Agent ID to delete: "))
            db.delete_agent(id)
            print("Agent deleted if existed")

        elif choice == '5':
            agents = db.get_all_agents()
            print("id   code name    real name    location   status       3"
                  "mission complete")
            for agent in agents:
                print(agent)
                print("-" * 20)

        elif choice == '0':
            db.close()
            break

        else:
            print("Invalid option, try again.")

if __name__ == '__main__':
    menu()

