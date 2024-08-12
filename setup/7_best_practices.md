## Best Practices

Following the best practices of software development, I have created a `Makefile` to automate the quality checks and other tasks.

Quality Checks includes the following:
- `black`: Code Formatter
- `pylint`: Static Code Analyser 
- `isort`: Import Sorter
- `trailingspaces`: Trailing Whitespace Remover
- `end-of-file-fixer`: End of File Fixer
- `check-yaml`: YAML Linter

To run the quality checks, run the following command:

```bash
make quality_checks
```

We have also incorporated `pre-commit` hooks to run the quality checks before every commit. To install the `pre-commit` hooks, run the following command:

```bash
make run_pre_commit
```

## Tests

We have written `unit tests` and `integration tests` located in the `tests` directory. To run the these tests, run the following command:

```bash
make tests
```
