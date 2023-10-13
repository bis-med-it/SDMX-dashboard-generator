# Walkthrough

## Introduction

SDMX Dashboard Generator is an open-source [Dash](https://dash.plotly.com) application that generates dynamic dashboards by pulling data and metadata from SDMX Rest API.
It has been developed for the [SDMX Hackathon Global Conference 2023](https://www.sdmx2023.org/hackathon).

## Main features

<div style="display: flex;">
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/sdmx.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;";><summary style="margin: 10px;text-align: center;">SDMX integration</summary>

  Version 2.1 supported

  Reading of settings file (`.yaml`) for data and metadata retrieval

  </details></div>
  
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/bars.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Interactive graphs</summary>
  
  Plotly for interactive visualization

  Multiple charts supported: KPIs, line, pie and bar charts

  </details></div>

  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/python.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Open source code</summary>

  Apache 2.0 licence

  Open-source libraries

  </details></div>

</div>

<div style="display: flex">
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/pen.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Flexible design</summary>

  Position and size automatically adjusted

  Bootstrap components to modify themes, icons and incorporate HTML5 elements

  </details></div>
  
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/cpu.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Optimized performance</summary>

  Data and metadata asynchronous retrieval

  Caching methods for better user navigation

  </details></div>

  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/download.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Dynamic data filtering and download</summary>

  Data accessible with table format supported by dynamic filters and download export (CSV)

  </details></div>

</div>

<div style="display: flex;">
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/language.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Multilingual support</summary>

  Multi-lingual metadata to access titles, labels and info buttons in the desired language, when supported by SDMX

  Automatic titles and subtitles in multiple languages, when specified by the user

  </details></div>
  
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/search.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Searchable documentation</summary>

  Sphinx documentation automatically updated to support the exploration of the material

  Documentation deployment via GitHub Actions

  </details></div>

  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/valid.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Settings validation</summary>

  Text messages are displayed when exceptions are encountered, to guide with the right configuration of the settings

  Software engineering components (i.e. unit tests using pytest, coverage reporting, continuous integration using tox, automated license monitoring, code linting using pylint and flake8)

  </details></div>

</div>

<div style="display: flex">
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/security.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Security components</summary>

  Security testing using bandit

  Software composition analysis using GitHub Dependabot

  Secret scanning using Github Advanced Security

  </details></div>
  
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/team.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Collaboration</summary>

  User-independent access within the same company and across countries

  Worldwide contribution (feedback and pull requests via Github) are welcome

  </details></div>

  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/work-in-progress.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px;"><summary style="margin: 10px;text-align: center;">Future enhancements</summary>

  Settings in a new tab or dropdown menu

  Interactivity (search, simulation)

  Add support for other chart types (mix, map, dual-axis, flows, network, outlier)

  </details></div>

</div>

## High-level architecture

<div style="display: flex;">
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/dashboard.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px; text-align: left";><summary style="margin: 10px;text-align: center;">The Dash application</summary>

  source code contained in the file `app.py`

  can run both on locally or shared across the domain

  follows the guidelines provided in the [SDMX Hackathon Global Conference 2023 Terms of Reference](https://sdmx.org/wp-content/uploads/SDMX-Hackathon-2023-ToRrev.pdf) (e.g. a maximum of three charts per row is allowed)

  </details></div>
  
</div>

<div style="display: flex">

  <div style="flex: 1; text-align: right;">
  <img src="_static/left-arrow.png" style="max-height: 60px;"/>
  </div>
  
  <div style="flex: 1; text-align: center;">
  <img src="_static/down-arrow.png" style="max-height: 60px;"/>
  </div>

  <div style="flex: 1; text-align: left;">
  <img src="_static/right-arrow.png" style="max-height: 60px;"/>
  </div>

</div>

<div style="display: flex">
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/sdmx.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px; text-align: left";><summary style="margin: 10px;text-align: center;">SDMX</summary>

  Leveraging two classes, `SDMXData` and `SDMXMetadata`, built on top of [SDMXThon](https://github.com/Meaningful-Data/sdmxthon)

  Metadata (e.g. codelist for the legend or multilingual support) retrieval through a metadata url (`dataflow`)

  When supported by SDMX, the metadata is retrieved through DSD url (`datastructure`) to increase the speed performance

  </details></div>
  
  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/configuration.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px; text-align: left";><summary style="margin: 10px;text-align: center;">The specification file</summary>

The SDMX Dashboard Generator requires a `.yaml` file contained in `/yaml` folder with the settings for the dashboard.

Example of `.yaml` structure:

![Yaml sample](_static/yaml_sample.png "This is a yaml sample.")

- `DashID`: dashboard identifier using any string composed of numbers, letters, and underscores (_), which can be used to compose the URL to display the dashboard. For example, if the base URL of the application is `http://127.0.0.1:5000` and the `DashID` is `eurostat`, the dashboard might be displayed at [http://127.0.0.1:5000/eurostat](http://127.0.0.1:5000/eurostat)

- `Row`: row position of the visual indicated as an integer value 0…3. Up to three charts can share the same row and they are distributed left-right in the order they appear in the specification file. Title, subtitle and footnotes are identified with `Row=0` and `chartType=TITLE` and `chartType=FOOTER` respectively

- `Title`: title description of the chart. If no title is specified, the dashboard shows automatically the name of the requested dataflow, supported by multilingual translation

- `Subtitle`: a string to complement the title description of the chart. If `auto` is provided, the subtitle takes the code name from `legendConcept`. If more than one code name is available, then it will take the first one and append to it `...`. If the subtitle node is empty, no subtitle will be shown

- `Unit`: a string to describe the unit which can be show in the chart if `UnitShow` is set to `Yes`

- `UnitIcon`: a bootstrap icon to be show on top of the KPI. Full list available at: [https://icons.getbootstrap.com/](https://icons.getbootstrap.com)

- `Decimals`: the number of decimals to display

- `chartType`: it can be KPI (i.e. VALUE) or charts (i.e. PIE, LINE and BAR)

- `legendConcept`: indicates the dimension that defines multiple series to be displayed in the visualization (e.g. sectors of the pie chart, each of the lines in a lines chart or each cluster in a bar chart)

- `legendloc`: indicates the legend location which can be TOP, BOTTOM, LEFT, RIGHT or HIDE for no legend. Not applicable to the KPI

- `LabelsYN`: indicates ("Yes"/"No") whether the description of each category is to be displayed on the chart. Not applicable to the KPI

- `xAxisConcept`: indicates the concept to be allocated on the x-axis (e.g. TIME_PERIOD for LINES)

- `yAxisConcept`: indicates the concept to be allocated to the y-axis (e.g. OBS_VALUE)

- `downloadYN`: indicates ("Yes"/"No") whether the download of the data behind the chart

- `dsdLink`: an URL of an application or file containing related the datastructure data

- `metadataLink`: an URL of an application or file containing reference metadata (e.g. used in the info button)

- `DATA`: an URL of an application or file containing data

  </details></div>

  <div style="flex: 1; text-align: center; margin: 10px; background-color: rgba(200, 200, 200, 0.15);">
  <img src="_static/chart.png" style="max-height: 60px; margin: 10px;"/>
  <details close style="margin: 10px; text-align: left";><summary style="margin: 10px;text-align: center;">The ChartGenerator</summary>

  The ChartGenerator is a class contained in the file `src/draw.py`, allowing the user to select the `chartType` from the `.yaml` file:

  - `chartType:VALUE` returns a Key Performance Indicator (KPI), a value corresponding to an observation value at a given point in time displayed in the visual placeholder

  - `chartType:PIE` returns a pie chart composed by the values returned by the query(ies) specified in DATA which sum represents the full circle (360°). Each value defines a sector of x°, proportional to the fraction of the total it represents

  - `chartType:LINES` returns a lines chart including one or multiple series, either time series or cross-sectional

  - `chartType:BARS` returns a vertical bars chart including one or multiple series (clustered bars), either time series or cross-sectional

  Each function, with the exception of the one returning the KPI, makes use of `decorator` elements for enriching the chart with style elements (e.g. legendlocation).

  </details></div>

</div>
