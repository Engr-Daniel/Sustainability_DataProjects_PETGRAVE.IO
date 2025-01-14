# Recycling Business Locator and Data Analysis

## Overview
This project aims to identify and analyze recycling businesses in specified locations, with a focus on their geographic distribution, materials handled, and operational details. It leverages Google Maps API for location data and web scraping to extract additional information, providing structured insights to enhance recycling efforts.

---

## Features

### Business Search
- Locate recycling businesses in a specified location.

### Data Collection
- Gather detailed business information:
  - **Name and Address**
  - **Geographic Coordinates**
  - **Contact Details** (Phone, Website)
  - **Operating Hours**
  - **Google Ratings**
  - **Materials Handled** and Recycling Capabilities
  - **Detailed Address Components**

### Website Analysis
- Analyze business websites to extract additional information on recycling materials and services.

### Data Export
- Export all collected data to a structured JSON format for easy analysis and visualization.

### Data Visualization
- Visualize data using tools like Power BI or Python libraries to:
  - Map the geographic distribution of businesses.
  - Analyze material focus and operational gaps.

---

## Prerequisites

### System Requirements
- **Python**: Version 3.x
- **Virtual Environment**: Recommended for managing dependencies

### Required Python Packages
Install the following packages using `pip install`:
- `beautifulsoup4`
- `googlemaps`
- `requests`
- `pyodbc`
- `unixodbc`

### API Key
- Obtain a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/).

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - Add your Google Maps API key to the `.env` file or directly in the script.

---

## Usage

1. **Run the Business Locator**
   ```bash
   python main.py
   ```

2. **Input Location**
   - Specify the location to search for recycling businesses.

3. **Export Data**
   - Collected data is automatically exported to `output/recycling_data.json`.

4. **Visualize Data**
   - Import the JSON data into visualization tools like Power BI or Python libraries (e.g., Plotly).

---

## Methodology

### Data Collection
- **Web Scraping**: Identify recycling businesses and gather data on their services.
- **Google Maps API**: Retrieve geographic and operational details.

### Data Cleaning
- Filter out non-recycling businesses and incomplete entries.
- Format the data into a clean JSON structure.

### Data Visualization
- Use Power BI or Python to:
  - Create maps, bar charts, and pie charts.
  - Highlight underserved areas and materials.

---

## Insights from Delta State Report

### Key Findings
1. Recycling businesses are concentrated in Warri (95%), with minimal presence in Agbor (5%).
2. Focus is primarily on recycling plastics and metals, leaving textiles, hazardous waste, and general waste underserved.

### Recommendations
1. Expand facilities to underserved areas like Asaba.
2. Diversify recycling efforts to include textiles and hazardous waste.
3. Foster partnerships with governments and NGOs to enhance recycling activities.
4. Conduct broader data collection to include all recycling businesses in Delta State.

---

## Acknowledgments

- **Google Maps Platform**: For providing location and business data.
- **Beautiful Soup**: For web scraping capabilities.
- **Power BI**: For data visualization tools.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

