class CotacoesNotFoundException(Exception):
    """Exception raised when no quotes are found."""
    def __init__(self, message="No quotes found."):
        self.message = message
        super().__init__(self.message)
        
class SAPCotacoesNotSavedException(Exception):
    """Exception raised when SAP quotes are not saved."""
    def __init__(self, message="SAP quotes were not saved."):
        self.message = message
        super().__init__(self.message)