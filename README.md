<a name="readme-top"></a>
<br />
<div align="center">
  <img src="images/favicon.png" alt="Logo" width="100" height="80">
</div>
<br/>
<p align="center">
  <img src="images/coverage.svg" alt="Coverage">
  <img src="images/pylint.svg" alt="pylint">
  <img src="images/apache20.svg" alt="Apache 2.0">
  <img src="images/active.svg" alt="Active repo">
  <a href="https://github.com/SNStatComp/awesome-official-statistics-software">
    <img src="https://awesome.re/mentioned-badge.svg" alt="Mentioned in Awesome">
  </a>
</p>

## About the SDMX Dashboard Generator

The SDMX Dashboard Generator (SDMX-DG) is an open-source [Dash](https://dash.plotly.com) application that generates dynamic dashboards by pulling data and metadata from SDMX Rest API. It supports the version 2.1 of the standard. It leverages the open-source library SDMXthon to retrieve and parse data and metadata in SDMX. Data and metadata are supported by asynchronous retrieval. A dashboard is composed of several visualizations as defined by the specifications provided in a .yaml file. The specifications are interpreted by a ChartGenerator class containing instructions to define the Plotly charts. It has been developed for the [SDMX Hackathon Global Conference 2023](https://www.sdmx2023.org/hackathon).

## Documentation

A quick introduction to the SDMX Dashboard Generator is available at [sdmx.io](https://www.sdmx.io/tools/sdmx-dg/). The full documentation for this app is available at [GitHub Pages](https://bis-med-it.github.io/SDMX-dashboard-generator/).
## License

The source code in this repository is licensed under Apache-2.0. See [LICENSE](LICENSE) for more information.

## Acknowledgments

This app has been developed by Cristina Leonte, Pietro Patelli, Stephan Probst and Olivier Sirello (Bank for International Settlements). The views expressed are those of the authors and do not necessarily reflect those of the Bank for International Settlements. All errors are our own.

## Infographics

<p align="center">
  <img src="images/sdmx-dg-pic1.png" alt="How it works" width="350">
</p>

<p align="center">
  <img src="images/sdmx-dg-pic2.png" alt="What it does" width="350">
</p>
