class MoreInfo:

    def describe(self):
        self.file = open('ERROR_files/info.txt', 'r')
        self.txt = self.file.read()
        return self.txt

class InvalidDateError(MoreInfo, Exception):

    def __init__(self, date):
        self.date = date
        self.msg = f"The input {date} is not a valid date format\nEvery date should have the format YYYY-MM-DD"
        super().__init__(self.msg)

class InvalidDateTimeError(MoreInfo, Exception):

    def __init__(self, datetime):
        self.datetime = datetime
        self.msg = f"{datetime} presents incorrect format for datetime data\nEvery datetime should have the format YYYY-MM-DD HH:MM:SS"
        super().__init__(self.msg)

class RangeError(MoreInfo, Exception):

    def __init__(self, first_val, second_val):
        self.first_val = first_val #Minimum allowed value
        self.second_val = second_val #Maximum allowed value
        self.msg = f"The value is out of the range {first_val} to {second_val}"
        super().__init__(self.msg)

class NotAscendingError(MoreInfo, Exception):

    def __init__(self, list):
        self.list = list
        self.msg = f"The list {self.list} must be crescent"
        super().__init__(self.msg)

class NotDistinctError(MoreInfo, Exception):

    def __init__(self, list):
        self.list = list
        self.msg = f"The list {self.list} must have distinct elements"
        super().__init__(self.msg)