# Contributing to DataCentral Cloud LLC

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## Development Workflow

### Branch Naming Conventions

Use descriptive branch names:
- `feature/description` - for new features
- `fix/description` - for bug fixes
- `docs/description` - for documentation
- `refactor/description` - for refactoring
- `test/description` - for test improvements

### Commit Messages

Write clear commit messages following this format:

```
Type: Brief description (50 chars max)

Detailed explanation if needed (72 chars per line)

- Bullet point 1
- Bullet point 2

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

### Pull Requests

1. Create a PR with a descriptive title
2. Include a summary of changes
3. Reference related issues
4. Ensure all tests pass
5. Request review from maintainers

## Code Quality Standards

### JavaScript/TypeScript
- Use ESLint configuration provided
- Follow consistent formatting with Prettier
- Write meaningful variable and function names
- Add comments for complex logic

### Python
- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for functions and classes
- Run pylint/black for code formatting

## Testing Requirements

- Write tests for new features
- Ensure all existing tests pass
- Aim for 80%+ code coverage
- Include both unit and integration tests

## Documentation

- Update README.md for user-facing changes
- Add JSDoc/docstring comments for public APIs
- Include examples in documentation
- Keep CHANGELOG.md up to date

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

## Review Process

- At least one maintainer review required
- All CI/CD checks must pass
- Address feedback and suggestions
- Rebase and merge when approved

## Questions?

- Check existing issues and discussions
- Ask in PR comments or issues
- Contact maintainers directly

Thank you for contributing!
