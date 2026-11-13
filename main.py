"""Entry point: creates Model, View and Controller and starts the event loop."""
from model import StudentModel
from view import StudentView
from controller import StudentController


def main():
    model = StudentModel()
    view = StudentView()
    StudentController(model, view)
    view.mainloop()          # main event loop (waits for user events)
    model.close()


if __name__ == "__main__":
    main()
