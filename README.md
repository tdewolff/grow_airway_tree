# Install

    sudo apt-get install qtcreator python-pyqt5 pyqt5-dev-tools
    pip install PySide

# Run

    python run.py

# Guide

Start QtCreator and open `grow/qt/view.ui`. This is the file that defines the GUI and can be edited through QtCreator. You can add and move around widgets, but remember the `objectName` (right-click on widget -> Change objectName) as that is how the widget is referenced in the code. When done, save and run the following command to generate the Python files in `grow/ui_*.py`.

    grow/build.sh

In `grow/view.py` you can edit the code that handles any interaction with the GUI. It performs actions when buttons are pressed for example.

In `grow/scene.py` we handle interactions with the Zinc scene to which we can add new models from `grow/model.py`.
