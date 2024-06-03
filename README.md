# NestleNutriEcoDashboard
## NestleNutriEcoDashboard is an interactive visualization tool designed to analyze Nestlé food products' NutriScore and EcoScore. This dashboard allows users to explore nutritional and ecological data through various interactive charts, including scatter plots, histograms, and radar charts.

### You can find the app up and running here: https://nestlenutritionecodashboard.onrender.com/

## Features

### Nutritional Analysis Tab:
Scatter plot showing clustering by NutriScore grade.
Histogram displaying the distribution of NutriScore grades.
Boxplot comparing fat values based on selected NutriScore grades.
Interactive filtering by clicking on scatter plot points or histogram bars.

### Eco Analysis Tab:
Histogram showing the distribution of EcoScore grades.
Radar chart visualizing packaging materials in relation to EcoScore grades.
Interactive filtering by clicking on histogram bars.

## Technologies Used
Dash: Web application framework for Python.
Plotly: Graphing library to create interactive plots.
Pandas: Data manipulation and analysis library.

## Getting Started
Prerequisites
Python 3.6 or later
Pip (Python package installer)

## Installation
Clone the repository from GitHub.
Install the required packages using pip.
Run the application.
Open your web browser and go to the local host URL to view the dashboard.

## Project Structure
app.py: Main application file containing the Dash app and callbacks.
assets/: Directory containing logo images used in the dashboard.
nestle_es_cleaned.csv: Dataset containing nutritional and ecological information for Nestlé products.
data_cleaning.ipynb: Jupyter notebook for data cleaning and preparation.

## Usage
Navigate to the Nutritional Analysis tab to explore NutriScore-related data.
Navigate to the Eco Analysis tab to explore EcoScore-related data.
Use the reset buttons to clear any applied filters.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
