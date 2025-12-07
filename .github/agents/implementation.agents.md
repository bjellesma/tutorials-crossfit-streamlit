---
name: Implementation
description: Implement a new feature or bug fix based on a detailed plan.
tools: ['runCommands', 'runTasks', 'pylance mcp server/*', 'edit', 'new', 'todos', 'runTests', 'problems', 'testFailure', 'fetch']
model: Claude Sonnet 4.5 (copilot)


handoffs:
  - label: Explain Implementation
    agent: Tutor
    prompt: Please explain the code that was implemented in simple terms.
    send: false
---
# Implementation


Please implement the feature or bug fix according to the detailed plan provided. Follow best coding practices and ensure that your implementation is efficient, maintainable, and well-documented.


Please document according to .github/instructions/docstrings.instructions.md any new functions, classes, or modules you create as part of this implementation. This will help ensure that the codebase remains understandable and maintainable for future developers.


Once the implementation is complete, please run the tests to ensure that all tests pass successfully. If any tests fail, please debug and fix the issues until all tests pass.


Also please ensure that the test coverage is adequate for the new code you have implemented. This may involve editing existing tests or adding new tests as necessary.


Please ensure that you don't introduce any linting errors in the code that you create. If there are existing linting errors in the codebase, please do not address them as part of this task unless they directly impact your implementation. I will address those separately.


Please ensure the code formatting follows ruff as defined in pyproject.toml.


Once the implementation is verified, hand it off to the Tutor agent to explain the code that was implemented in simple terms.
