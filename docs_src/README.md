# Documentation hosting

To build the documentation, make sure sphinx and the required extensions are installed in the
active python environment and run the following command from the root of the repository:

```
sphinx-apidoc -o docs_src src/
sphinx-build -b html docs_src docs
```

For a clean build, please run from the root of the repository:

```
sphinx-build -E docs_src docs
```

The resulting 'docs' folder of the main branch will be published through GitHub pages.
