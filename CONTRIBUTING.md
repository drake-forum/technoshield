# Contributing to TECHNOSHIELD

Thank you for your interest in contributing to TECHNOSHIELD! This document provides guidelines and instructions for contributing to this project.

We at rooter are committed to providing a safe and secure environment for all users.

Our Contributers

- [drake-forum](https://drakefolio.netlify.app/)
- [hiteshi-vishwakarma](https://github.com/hiteshi-vishwakarma)
- [gourav-likhitkar](https://github.com/gourav-likhitkar)
- [darshani-sharma](https://github.com/darshani-sharma)
- [hema-11k](https://github.com/hema-11k)

## Code of Conduct

By participating in this project, you agree to uphold our Code of Conduct, which expects all contributors to be respectful, inclusive, and considerate of others.

## How to Contribute

### Reporting Bugs

Bugs are tracked as GitHub issues. When you create an issue, please include:

- A clear and descriptive title
- A detailed description of the issue
- Steps to reproduce the behavior
- Expected behavior
- Screenshots if applicable
- Your environment information (OS, browser, etc.)

### Suggesting Enhancements

Enhancement suggestions are also tracked as GitHub issues. When suggesting an enhancement, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Any specific implementation details you have in mind
- Why this enhancement would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

### Pull Request Guidelines

- Update the README.md with details of changes if applicable
- Update the documentation if necessary
- The PR should work for all supported platforms
- Follow the coding style and conventions used in the project
- Include appropriate tests for your changes

## Development Setup

### Prerequisites

- Node.js 16.x or higher
- Python 3.9 or higher
- PostgreSQL 13 or higher
- Docker (optional, for containerized deployment)

### Local Development

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/technoshield.git
   cd technoshield
   ```

2. Set up the backend
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Update with your configuration
   python -m app.main
   ```

3. Set up the frontend
   ```bash
   cd frontend
   npm install
   cp .env.example .env  # Update with your configuration
   npm run dev
   ```

## Testing

Before submitting a pull request, please ensure all tests pass:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use docstrings for functions and classes
- Use type hints where appropriate

### JavaScript/React Code

- Follow the ESLint configuration in the project
- Use functional components with hooks
- Use proper PropTypes or TypeScript for type checking

## License

By contributing to TECHNOSHIELD, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

If you have any questions or need help with the contribution process, please open an issue or contact the project maintainers.

Thank you for contributing to TECHNOSHIELD!
