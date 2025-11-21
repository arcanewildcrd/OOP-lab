# exceptions.py

class DataFormatError(Exception):
    """Raised when data format is invalid."""
    pass

class DomainRuleError(Exception):
    """Raised when a domain-specific rule is violated."""
    pass
