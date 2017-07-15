import datetime
from avasdk.plugins.python_model import PythonModel

class what(PythonModel):
    """
        What plugin
    """

    def __init__(self, name="what"):
        super(what, self).__init__(name)
        self.set_commands_list({**PythonModel._commands, **{\
        "time" : self.time, \
        "date" : self.date, \
        }})

    def time(self, command):
        print(datetime.datetime.now().strftime("%H:%M:%S"))

    def date(self, command):
        print(datetime.datetime.now().strftime("%A %d %B %Y"))
