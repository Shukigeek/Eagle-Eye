from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from DAL.DAL_crud import AgentDB
from UI.add_update_dialog import AgentDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eagle Eye - Agent Manager")
        self.resize(800, 500)

        self.db = AgentDB()
        self.init_ui()
        self.load_agents()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Code name", "Real name", "Location", "Status", "Missions"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add Agent")
        self.edit_btn = QPushButton("✏️ Edit")
        self.del_btn = QPushButton("❌ Delete")

        self.add_btn.clicked.connect(self.add_agent)
        self.edit_btn.clicked.connect(self.edit_agent)
        self.del_btn.clicked.connect(self.delete_agent)

        for b in (self.add_btn, self.edit_btn, self.del_btn):
            btn_layout.addWidget(b)

        layout.addLayout(btn_layout)
        central.setLayout(layout)

    def load_agents(self):
        agents = self.db.get_all_agents()
        self.table.setRowCount(len(agents))

        for row, agent in enumerate(agents):
            self.table.setItem(row, 0, QTableWidgetItem(str(agent.id)))
            self.table.setItem(row, 1, QTableWidgetItem(agent.codeName))
            self.table.setItem(row, 2, QTableWidgetItem(agent.realName))
            self.table.setItem(row, 3, QTableWidgetItem(agent.location))
            self.table.setItem(row, 4, QTableWidgetItem(agent.status))
            self.table.setItem(row, 5, QTableWidgetItem(str(agent.missionsCompleted)))

    def add_agent(self):
        dialog = AgentDialog(self)
        if dialog.exec_():
            agent = dialog.get_agent()
            self.db.create(agent)
            self.load_agents()

    def edit_agent(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Choose agent to edit.")
            return
        agent_id = int(self.table.item(selected, 0).text())
        agent = self.db.read_agent(agent_id)
        dialog = AgentDialog(self, agent)
        if dialog.exec_():
            updated_agent = dialog.get_agent()
            updated_agent.id = agent_id
            self.db.update_agent(updated_agent)
            self.load_agents()

    def delete_agent(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "Choose agent to delete.")
            return
        agent_id = int(self.table.item(selected, 0).text())
        confirm = QMessageBox.question(self, "Confirm", f"Delete agent ID {agent_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_agent(agent_id)
            self.load_agents()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    with open("C:\\Users\\shuki\\Desktop\\Eagle-Eye\\UI\\style.qss", "r",encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
