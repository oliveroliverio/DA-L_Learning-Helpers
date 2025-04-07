"""
Settings for the transcription app.
"""

# Default model size to use
DEFAULT_MODEL_SIZE = "base"

# Available model sizes
MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]

# Default output format
DEFAULT_OUTPUT_FORMAT = "txt"

# Environment settings
ENVIRONMENTS = {
    "dev": {
        "debug": True,
        "log_level": "DEBUG",
    },
    "test": {
        "debug": True,
        "log_level": "INFO",
    },
    "prod": {
        "debug": False,
        "log_level": "WARNING",
    }
}

# Default environment
DEFAULT_ENVIRONMENT = "dev"

# Get current environment settings
def get_environment_settings(env=DEFAULT_ENVIRONMENT):
    """
    Get settings for the specified environment.
    
    Args:
        env (str): Environment name (dev, test, prod)
        
    Returns:
        dict: Environment settings
    """
    return ENVIRONMENTS.get(env, ENVIRONMENTS[DEFAULT_ENVIRONMENT])
