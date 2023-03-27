FORMATTED_DATE = "%d:%M:%Y"
MAX_FILE_SIZE_IN_MB = 30 * 1024 * 1024
MAX_PICTURE_SIZE_IN_MB = 3 * 1024 * 1024

NAME_REGEX = "^[a-zA-Z][a-zA-Z\-\s]*$"
PASSWORD_REGEX = "^.{8,64}$"


class ValidationMessage:
    NAME = "Name not valid: name must start and ends with letter and can contain only ' ' or '-' special characters "
    EMAIL = "Please provide valid email address"
    PASSWORD = "Password must be between 8-64 characters, can include upper/lower cases, digits and special characters"
