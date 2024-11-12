# Open Source Software Licence Compliance Note

The BIS has independently authored the software program: SDMX Dashboard Generator. It relies on multiple third-party software modules listed in `requirements.txt`.

SDMX Dashboard Generator is licensed under the Apache License Version 2.0 and is therefore provided with no warranty. To comply with the terms of the licences covering the third-party components, SDMX Dashboard Generator must be installed with the considerations below, any other installation method may not be compliant with the relevant third-party licences.

# Installation considerations

For a licence compliant installation, SDMX Dashboard Generator must be installed using the package installer for Python (pip) using the --no-binary flag. An example installation command is:

`pip install -r requirements.txt--no-binary :all:`