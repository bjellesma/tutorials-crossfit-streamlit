---
description: Guidelines for writing docstrings in Python code.
applyTo: **/*.py
---
# Docstring Instructions

When writing docstrings for Python functions, classes, or modules, please follow these guidelines to ensure consistency and clarity:

- Please include a blank line between the summary line and the rest of the docstring.
- Use triple double quotes (`"""`) for docstrings.
- The first line should be a brief summary of the function, class, or module.
- Follow the summary with a blank line.
- Provide a detailed description of the function, class, or module.
- List all parameters and their types.
- Describe the return value and its type.
- Include any exceptions that the function might raise.
- End with a blank line before closing the triple double quotes.

The format should look like this:

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief summary of the function.

    Detailed description of the function.

    Args:
        param1 (int): Description of param1.
        param2 (str): Description of param2.

    Returns:
        bool: Description of the return value.

    Raises:
        ValueError: If an error occurs.
    """
```