# Getting started

This page contains useful tips to install and run the app.
Make sure that your environment is correctly set up to execute Python code and that your `pip` and `Python` are up-to-date.
The app has been successfully tested with Python versions equal or higher to 3.9.13.

## Installation

1. Clone the repo

   ```sh
   git clone https://github.com/bis-med-it/SDMX-dashboard-generator.git
   ```

2. (Recommended) Create virtual environment using `virtualenv`

   ```sh
   python.exe -m pip install --upgrade pip
   pip install virtualenv
   cd SDMX-dashboard-generator/
   virtualenv venv --system-site-packages
   .\venv\Scripts\activate
   ```

   or if you use `virtualenvwrapper`

   ```sh
   python.exe -m pip install --upgrade pip
   pip install virtualenvwrapper
   cd SDMX-dashboard-generator/
   mkvirtualenv SDMX-dashboard-generator
   workon SDMX-dashboard-generator
   ```

3. Install dependencies

   ```sh
   python.exe -m pip install --upgrade pip
   cd SDMX-dashboard-generator
   pip install -r requirements.txt
   ```

   If you wish to contribute, you can install the optional development requirements:

   ```sh
   pip install -r requirements/dev_requirements.txt
   ```

4. From the root folder, run the app

   ```sh
   python app.py
   ```

5. Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000) if you use Flask or [http://127.0.0.1:8050](http://127.0.0.1:8050)

## How to with examples

The application comes with examples stored in the `/yaml` folder which can be used in two ways:

- by uploading one `.yaml` file in the interface via drag and drop or
- by typing the `DashID` of the dashboard in the URL (i.e. [http://127.0.0.1:5000/eurostat](http://127.0.0.1:5000/eurostat) for the `eurostat_sample.yaml` file which contains `DashID: eurostat`).

The application will scan the existing content in the `yaml` subfolder of the project and load the `.yaml` file containing the requested `DashID`. If none is found, the app will raise a `PreventUpdate`.
