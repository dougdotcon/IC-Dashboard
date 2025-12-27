# IC Dashboard

An interactive dashboard designed to analyze the impacts of the 6x1 work schedule (6 days on, 1 day off) on workers' lives. The application visualizes statistics and interactive charts based on a SQLite database, organized into three main tabs: Occupational Data, Personal Data, and Impact Perception.

![Dashboard Preview](https://via.placeholder.com/800x450?text=Dashboard+Preview)

## 📋 Index

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contribution](#contribution)
- [License](#license)

## 🔍 Overview

This dashboard was developed to visualize and analyze data regarding the impacts of the 6x1 work schedule. It allows users to explore interactive charts and KPIs based on data stored in a SQLite database. The interface is divided into three primary sections to facilitate deep analysis of occupational trends, personal demographics, and the perceived physical and mental health impacts of the schedule.

## ✨ Features

- **Occupational Data Visualization**: Interactive charts displaying information regarding time spent on the 6x1 schedule, contract types, working hours, job occupations, CNAE (economic activity code), and work location (state).
- **Personal Data Visualization**: Interactive charts showing the distribution of age, gender, race/color, marital status, dependents, income, and education level.
- **Impact Perception Visualization**: Interactive charts visualizing the impacts of the 6x1 schedule on family life, physical health, and mental health.
- **KPIs (Key Performance Indicators)**: Crucial metrics highlighting important statistics, such as the percentage of workers on the 6x1 schedule, gender distribution, and most frequent impacts.
- **Data Refresh**: Functionality to update charts with new data directly from the database.
- **Responsive Design**: A professional, organized interface with a cohesive color scheme and responsive layout suitable for various screen sizes.

## 📋 Requirements

### Local Installation
- Python 3.9+
- Pip (Python package manager)
- Python Libraries: dash, pandas, plotly, spacy, nltk

### Docker Installation
- Docker
- Docker Compose

## 🚀 Installation

### Local Installation

1. Clone the repository or download the project files:

bash
git clone https://github.com/your-username/ic-dashboard.git
cd ic-dashboard


2. Install the dependencies:

bash
pip install -r requirements.txt


3. Download necessary NLP models and resources:

bash
python -m spacy download pt_core_news_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"


4. Convert the source Excel file to SQLite (if not already done):

bash
python excel_to_sqlite.py


5. Run the application:

bash
python app.py


6. Access the dashboard in your browser:


http://127.0.0.1:8050/


### Docker Installation

1. Clone the repository or download the project files.

2. Ensure you have Docker and Docker Compose installed and running.

3. Build and start the containers:

bash
docker-compose up --build


4. Access the dashboard in your browser:


http://localhost:8050


## 📂 Project Structure


ic-dashboard/
├── app.py                 # Main application file (Dash app logic)
├── excel_to_sqlite.py     # Script to convert Excel data to SQLite
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── data/
│   ├── source_data.xlsx   # Raw Excel data (Input)
│   └── database.db        # SQLite database generated from Excel
└── assets/
    └── style.css          # Custom stylesheets


## 🛠 Technologies Used

- **Framework**: Dash (Python)
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **NLP**: SpaCy, NLTK (for potential text analysis features)
- **Database**: SQLite
- **Containerization**: Docker

## 🤝 Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
