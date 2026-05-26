# Custom exception classes for Realtime Trains Py

class APIResponseError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nAPI response error: {message}")

class AuthenticationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nAPI authentication failed. Check your credentials and try again. \n{message}")

class FileWriteError(Exception):
    def __init__(self, file: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nFailed to write to file. Perhaps the file already exists? \nFile: {file}")

class InvalidComplexity(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nInvalid complexity level. Please select a valid complexity level. \nGiven: \"{invalid_item}\" \nExpected: One of [\"a\", \"a.n\", \"a.p\", \"c\", \"s\",\"s.n\", \"s.p\"]")

class InvalidDateProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe date you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: YYYY-MM-DD format.")

class InvalidModeProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe mode you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: One of [\"DMI.Y\", \"DMI.W\", \"LCD\"]")

class InvalidTimeProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe time you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: HHMM format.")

class InvalidUIDProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe Service UID you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: A string starting with a capital letter followed by 5 digits (e.g., A12345).")

class NoDataFound(Exception):
    def __init__(self) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nNo data found for the request made. Please check your parameters and try again.")
