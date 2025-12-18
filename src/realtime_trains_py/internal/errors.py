# Custom exception classes for Realtime Trains Py

# API Response Error
class APIResponseError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nAPI response error: {message}")

# Authentication Error
class AuthenticationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nAPI authentication failed. Check your credentials and try again. \n{message}")

# File Write Error
class FileWriteError(Exception):
    def __init__(self, file: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nFailed to write to file. Perhaps the file already exists? \nFile: {file}")

# Invalid Complexity
class InvalidComplexity(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nInvalid complexity level. Please select a valid complexity level. \nGiven: \"{invalid_item}\" \nExpected: One of [\"a\", \"a.n\", \"a.p\", \"c\", \"s\",\"s.n\", \"s.p\"]")

# Invalid Date Provided
class InvalidDateProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe date you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: YYYY/MM/DD format.")

# Invalid Mode Provided
class InvalidModeProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe mode you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: One of [\"DMI.Y\", \"DMI.W\", \"LCD\"]")

# Invalid Time Provided
class InvalidTimeProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe time you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: HHMM format.")

# Invalid UID Provided
class InvalidUIDProvided(Exception):
    def __init__(self, invalid_item: str) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nThe Service UID you provided didn't meet the requirements or fall into a valid range. \nGiven: \"{invalid_item}\" \nExpected: A string starting with a capital letter followed by 5 digits (e.g., A12345).")

# No Data Found
class NoDataFound(Exception):
    def __init__(self) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nNo data found for the request made. Please check your parameters and try again.")

# Unexpected Response Error
class UnexpectedResponseError(Exception):
    def __init__(self) -> None:
        super().__init__(f"\nRealtime Trains Py error:\nAn unexpected error occurred handling your request. Try again in a few minutes. \nIf this issue persists, please open an issue on the GitHub repository.")