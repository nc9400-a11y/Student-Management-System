"""CONTROLLER - connects View events to Model operations.
Every button in the View is bound to one of these event handlers."""
from model import Student


class StudentController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.bind_controller(self)
        self.refresh()

    # ----- event handlers -----
    def on_add(self):
        name, reg = self.view.get_form()
        error = self.model.validate(name, reg)
        if error:
            self.view.show_error(error)
            return
        try:
            self.model.add(Student(name, reg))
        except Exception as e:
            self.view.show_error(f"Could not add student.\n(Duplicate registration number?)\n\n{e}")
            return
        self.view.set_status(f"Added: {name.strip()}")
        self.view.clear_form()
        self.refresh()

    def on_update(self):
        sid = self.view.selected_id()
        if sid is None:
            self.view.show_error("Select a student from the table first.")
            return
        name, reg = self.view.get_form()
        error = self.model.validate(name, reg)
        if error:
            self.view.show_error(error)
            return
        try:
            self.model.update(Student(name, reg, sid))
        except Exception as e:
            self.view.show_error(f"Could not update.\n\n{e}")
            return
        self.view.set_status(f"Updated record #{sid}")
        self.view.clear_form()
        self.refresh()

    def on_delete(self):
        sid = self.view.selected_id()
        if sid is None:
            self.view.show_error("Select a student from the table first.")
            return
        if self.view.confirm("Delete this student record?"):
            self.model.delete(sid)
            self.view.set_status(f"Deleted record #{sid}")
            self.view.clear_form()
            self.refresh()

    def on_search(self, event=None):
        text = self.view.get_search()
        self.view.show_students(self.model.search(text) if text else self.model.get_all())

    def on_clear(self):
        self.view.clear_form()
        self.view.set_search("")
        self.refresh()

    def refresh(self):
        students = self.model.get_all()
        self.view.show_students(students)
        self.view.set_count(len(students))
