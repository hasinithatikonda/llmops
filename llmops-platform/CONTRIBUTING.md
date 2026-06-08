# Contributing to LLMOps Monitoring Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

See [QUICKSTART.md](QUICKSTART.md) for local development setup.

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow React best practices
- Use functional components
- Keep components small and reusable

### General
- Write clear commit messages
- Add comments for complex logic
- Keep code DRY (Don't Repeat Yourself)

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Guidelines

1. **Description**: Clearly describe what your PR does
2. **Testing**: Include test results
3. **Screenshots**: For UI changes, include screenshots
4. **Breaking Changes**: Clearly mark any breaking changes
5. **Documentation**: Update docs if needed

## Feature Requests

- Open an issue with [Feature Request] tag
- Describe the feature and use case
- Explain why it would be valuable

## Bug Reports

- Open an issue with [Bug] tag
- Include steps to reproduce
- Describe expected vs actual behavior
- Include error messages and logs
- Specify your environment

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## Questions?

Feel free to open an issue with [Question] tag.

Thank you for contributing!
