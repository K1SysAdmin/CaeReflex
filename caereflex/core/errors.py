class CaeReflexError(Exception):
    """Base CaeReflex exception."""

class DependencyMissingError(CaeReflexError):
    """Raised when an optional dependency is required but unavailable."""

class PathSafetyError(CaeReflexError):
    """Raised for unsafe paths or workspace violations."""

class UnsupportedFormatError(CaeReflexError):
    """Raised when no supported artefact is detected."""
