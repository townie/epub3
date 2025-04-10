# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Test: `python -m unittest discover`
- Run single test: `python -m unittest tests.test_example`
- install package: `pip install -e .`


## Code Style
- Python: PEP 8 style with docstrings (Google style)
- Type hints required for all function parameters and return values
- Use dataclasses for data models
- Class names: CamelCase
- Functions/methods: snake_case
- Imports: stdlib first, then third-party, then local
- Error handling: Use specific exceptions with clear messages
- JavaScript: ES6+ modules, 2-space indentation
- All code should be well-documented and include unit tests


# General Instructions

## Priorities

1. Produce correct, idomatic code in the language you are producing code for.
2. Prefer minimally elaborate solutions to the given problem.
3. Prefer backwards compatability over re-writes.
4. Produce testable code that is factored into appropriate units of functionality
5. Never produce a solution by removing the feature - unless feature removal is the task at hand.
6. If in doubt, ask for clarification.
7. When possible, match the style of adjacent or similar code within a codebase.

## Naming Conventions and Code Style

- Whether classes or functions prefer good metaphors over overly_verbose_function_names_that_go_on_and_on.
- Prefer free functions or static methods if it is appropriate to do so.
- Prefer small, purposeful files/modules over "god modules".
- If writing tests, prefer to never hard code values unless it is extremely clear what those values are.
- Use code commments to explain the implementation.
- Do not use code comments that are related to the "instructions" - assume they will be read by future developers or agents, and they are present to provide relevant context or explanation. They are NOT for the current developer or agent session unless it is extremely relevant or practical for that purpose.
- No magic numbers/strings. Use Enums, types, or constants, defined in an appropriate module or at the top of a given file.
- Use underscores or other idomatic conventions for differentiating between "private" and "public" functions, variables, classes, etc.


## Testing and Validation

- Use proper testing and autoformatting and code building tooling whenever possible.
- If the tooling or setup are project specific, document it in an appropriate CLAUDE.md for future reference.
- Always check appropriate CLAUDE.md files for development instructions.
