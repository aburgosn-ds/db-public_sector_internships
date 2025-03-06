import sys

def error_message_details(error, error_detail:sys):
    '''
    Customize the error message to be shown by Exception object
    '''
    _, _, exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename

    error_message = f"Error occured in python script name [{filename}] - line number [{exc_tb.tb_lineno}] - error message: {str(error)}"

    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail:sys):
        super().__init__(error)
        self.error_message = error_message_details(error=error, error_detail=error_detail)

    def __str__(self):
        return self.error_message