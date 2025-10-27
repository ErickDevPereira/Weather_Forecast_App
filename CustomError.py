class InvalidDateError(Exception):

    def __init__(self, date):
        self.date = date
        self.msg = f"The input {date} is not a valid date format\nEvery date should have the format YYYY-MM-DD"
        super().__init__(self.msg)

class RangeError(Exception):

    def __init__(self, first_val, second_val):
        self.first_val = first_val #Minimum allowed value
        self.second_val = second_val #Maximum allowed value
        self.msg = f"The value is out of the range {first_val} to {second_val}"
        super().__init__(self.msg)