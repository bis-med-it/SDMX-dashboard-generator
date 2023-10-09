# Troubleshooting

This page contains information on common issues users encounter when using
the app and how to avoid/fix them.

## Use virtual environments

Working in the global Python environment as opposed to project-specific virtual environments may cause a lot of problems.
We recommend to use [virtual environments](https://docs.python.org/3/library/venv.html>) for running this Python project with the correct package versions.

### SSL: CERTIFICATE_VERIFY_FAILED
A wrong configuration of the virtual environment with `venv` may lead to the error below or a white screen issue in the dashboard:
`[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1129)`

Please make sure you initiate your `venv` with the `--system-site-packages` flag such as:
   ```sh 
      virtualenv venv --system-site-packages
   ```
