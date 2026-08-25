class OplabError(RuntimeError):
    """Base class for expected application failures."""


class NetworkPermissionError(OplabError):
    """Raised when a caller did not explicitly enable network access."""


class SnapshotConflictError(OplabError):
    """Raised when immutable snapshot bytes do not match their recorded hash."""


class RecordValidationError(OplabError):
    """Raised when an upstream record cannot be normalized safely."""


class ConfigurationError(OplabError):
    """Raised when ranking configuration is invalid."""


class IntegrityError(OplabError):
    """Raised when tracked artifacts fail integrity validation."""
