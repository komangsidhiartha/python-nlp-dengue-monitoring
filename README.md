# Python NLP Dengue Fever Monitoring System

This repository contains contributions to an academic Tesis project from Universitas Gadjah Mada. The system is a public health surveillance tool designed to monitor Dengue Fever outbreaks by processing unstructured text data.

The core of this project is a **Natural Language Processing (NLP)** pipeline that uses a **Maximum Entropy** model for **Named Entity Recognition (NER)** to extract key information (locations, dates, victim counts) from news articles or social media posts. The extracted data is then visualized on a web-based dashboard built with **Flask** and **Google Maps**.

My role was to assist a friend by debugging, enhancing, and fine-tuning this complex system to improve its accuracy and functionality.

## Core Features & Technology

* **AI/ML Pipeline:** Utilizes a custom-trained NER model to extract structured data from unstructured text.
* **Web Dashboard:** A Flask-based web application provides an interface for users to query data by time period and view outbreak hotspots on an interactive Google Map.
* **Data Processing:** A series of Python scripts handle data preprocessing, cleaning, model training, and database interaction.
* **Database:** (Specify the database if you know it, e.g., MongoDB, PostgreSQL).

## How It Works: The Pipeline

The system operates through a multi-stage data processing pipeline:

1.  **Preprocessing (`preprocessor.py`):** Raw text data is cleaned, tokenized, and prepared for analysis.
2.  **Named Entity Recognition (`ner_maxent/`):** The core ML model processes the text to identify and tag entities like locations, dates, and incident counts.
3.  **Data Structuring & Storage (`dbmodel.py`):** The extracted entities are saved as structured documents in a database.
4.  **Visualization (`Flask-GoogleMaps/monitor.py`):** The Flask web server queries the database based on user input and plots the geolocated data points on a map.

## Instructions for Use (from original project documentation)

The following commands describe how to run the data processing pipeline for a given month and year (e.g., April 2015).

```bash
# 1. Preprocess the raw text data
# Format: p.execute("<month_shortcode>", "ner")
python -c 'import preprocessor as p; p.execute("apr", "ner")'

# 2. Run the NER model to extract entities
# Format: ner.execute("<month_shortcode>")
python -c 'import ner; ner.execute("apr")'

# 3. Group the extracted data by year
# Format: np.execute("<month_shortcode>", "<year>")
python -c 'import ner_pasing_to_month as np; np.execute("apr", "2015")'

# 4. Prepare data for forward-chaining rules
# Format: fwc.execute("<month_shortcode>", "<year>")
python -c 'import fwc_data_preparation as fwc; fwc.execute("apr", "2015")'

# --- OR ---

# Run the entire pipeline for one month
# Format: m.execute("<month_shortcode>", "<year>")
python -c 'import monitoring as m; m.execute("apr", "2015")'

# To run the web server for visualization
python Flask-GoogleMaps/monitoring/monitor.py
# Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
