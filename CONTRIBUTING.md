# Contributing to Millennium Problem Formalizations

Thank you for considering contributing to this project! This document outlines guidelines and processes for contributing.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or suggest enhancements
- Include as much detail as possible: steps to reproduce, expected vs actual behavior
- For mathematical concerns, reference specific Lean definitions/theorems when possible

### Submitting Changes
1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes
4. Ensure Lean compiles successfully (`lake build`)
5. Submit a pull request with a clear description of your changes

## Development Setup

### Prerequisites
- Lean 4 (v4.11.0 or later)
- Lake build tool
- Git

### Building the Project
```bash
lake build
```

### Running Tests
Currently, verification is primarily through Lean type checking. Ensure all files compile without errors.

## Mathematical Contribution Guidelines

### Understanding the Reflection Map Framework
Before contributing mathematical content, please review:
- REFLECTION_MAP_FRAMEWORK.md for the core analogy
- SUMMARY.md for completed work and next steps
- Individual Lean files for specific implementations

### Making Mathematical Contributions
1. **Clarify Assumptions**: Clearly state what assumptions are being made in any new definition or theorem
2. **Literature Connections**: When possible, connect to established mathematical literature
3. **Avoid Trivial Restatements**: Aim for substantive mathematical content rather than definitional tautologies
4. **Document Mathematical Insight Needed**: When leaving `sorry` statements, clearly articulate what mathematical insight would be needed to complete the proof
5. **Maintain Consistency**: Ensure new contributions align with the existing reflection map framework patterns

### Specific Areas for Contribution
- Replacing `sorry` statements with actual mathematical insights
- Strengthening Q parameter definitions with literature connections
- Developing explicit connections between Q parameters and physical mass gap definitions
- Creating computational validation code in the companion directory
- Improving documentation and cross-referencing between files

## Code Style

### Lean 4
- Follow Mathlib conventions where applicable
- Use clear, descriptive names for definitions and theorems
- Provide comprehensive comments explaining mathematical intuition
- Keep individual definitions and theorems focused and modular

### Documentation
- Use clear, accessible language while maintaining mathematical precision
- Include examples where helpful
- Reference related work both within and outside the repository

## Community

### Communication
- Be respectful and constructive in all interactions
- Welcome questions from newcomers
- Acknowledge contributions appropriately

### Attribution
All contributions will be acknowledged appropriately. Major contributions may be recognized in the SUMMARY.md or similar documents.

## License
By contributing, you agree that your contributions will be licensed under the MIT License.