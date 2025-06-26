from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QMessageBox
)
from model.agents import Agent

class AgentDialog(QDialog):
    def __init__(self, parent=None, agent=None):
        super().__init__(parent)
        self.setWindowTitle("Add / Edit Agent")
        self.agent = agent
        self.build_form()

    def build_form(self):
        self.form = QFormLayout(self)

        self.code = QLineEdit(self.agent.codeName if self.agent else "")
        self.real = QLineEdit(self.agent.realName if self.agent else "")
        self.loc = QLineEdit(self.agent.location if self.agent else "")
        self.status = QComboBox()
        self.status.addItems(["Active", "Injured", "Missing", "Retired"])
        if self.agent:
            index = self.status.findText(self.agent.status)
            if index >= 0:
                self.status.setCurrentIndex(index)

        self.missions = QLineEdit(str(self.agent.missionsCompleted if self.agent else "0"))

        self.form.addRow("Code Name:", self.code)
        self.form.addRow("Real Name:", self.real)
        self.form.addRow("Location:", self.loc)
        self.form.addRow("Status:", self.status)
        self.form.addRow("Missions:", self.missions)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)
        self.form.addRow(buttons)

    def validate(self):
        if not self.code.text().strip() or not self.real.text().strip():
            QMessageBox.warning(self, "Error", "Code and Real name are required.")
            return
        if not self.missions.text().isdigit() or int(self.missions.text()) < 0:
            QMessageBox.warning(self, "Error", "Missions must be a non-negative number.")
            return
        self.accept()

    def get_agent(self):
        return Agent(
            codeName=self.code.text().strip(),
            realName=self.real.text().strip(),
            location=self.loc.text().strip(),
            status=self.status.currentText(),
            missionsCompleted=int(self.missions.text())
        )
