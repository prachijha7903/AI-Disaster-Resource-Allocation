****AI Disaster Resource Allocation Management System****

Project Overview

The **AI Disaster Resource Allocation Management System** is a web-based application designed to help visualize disaster-affected areas and support resource prioritization. It displays affected zones on an interactive map and provides a dashboard to monitor disaster-related information.

The system helps users understand which areas may require attention by considering factors such as disaster severity, affected population, and resource availability.

## Objectives

- Visualize disaster-affected zones on an interactive map.
- Display disaster-related information through a dashboard.
- Add and manage affected zones.
- Calculate priority scores to help identify areas that may require urgent assistance.
- Support better planning and allocation of disaster relief resources.

## Features

- **Interactive Map:** Displays affected zones using map markers.
- **Disaster Zone Management:** Supports viewing and adding affected zones.
- **Dashboard:** Displays an overview of affected people and available resources.
- **Priority Scoring:** Uses disaster severity, affected population, and resource shortage to calculate a priority score.
- **API Integration:** Provides backend endpoints for dashboard and zone data.
- **Local Database:** Uses SQLite for storing project data.

## Technologies Used

- **Python** — Backend programming
- **Flask** — Web application framework
- **SQLite** — Database
- **HTML, CSS, JavaScript** — Web interface
- **Interactive Map Library** — Map visualization, depending on the library used in the project

## Project Structure

AI-Disaster-Resource-Allocation/
│
├── .venv/                          # Python virtual environment (not uploaded to GitHub)
│
├── ai_module/
│   ├── __pycache__/                 # Python cache files
│   ├── priority_engine.py           # Disaster priority calculation
│   └── resource_allocator.py        # Resource allocation logic
│
├── backend/
│   ├── app.py                       # Backend application and API routes
│   └── requirements.txt             # Python dependencies
│
├── database/
│   ├── disaster.db                  # SQLite database
│   ├── init_db.py                   # Database initialization script
│   └── schema.sql                   # Database table definitions
│
├── docs/                            # Project documentation
│
├── frontend/
│   ├── index.html                   # Web application interface
│   ├── script.js                    # Frontend functionality
│   └── style.css                    # Frontend styling
│
└── README.md                        # Project documentation

## How to Run the Project

1. Open the project folder in VS Code.
2. Open the terminal.
3. Install the required dependencies:
   `pip install -r backend/requirements.txt`
4. Start the Flask application:
   `python backend/app.py`
5. Open http://127.0.0.1:5000 in your browser.

## Disaster Priority Calculation

The application uses a rule-based priority score based on factors such as:

- Disaster severity
- Number of affected people
- Resource shortage

This score can help prioritize zones for review and resource allocation. It should be treated as decision-support information, not as a substitute for official emergency assessments.

## Testing

The application can be tested by:

1. Starting the Flask server.
2. Opening the dashboard in a browser.
3. Checking that affected zones appear on the map.
4. Adding a disaster zone and verifying that it appears.
5. Checking that dashboard and zone data load correctly.
6. Verifying the priority score for different input values.

## Future Enhancements

- Integrate verified real-time weather and disaster data.
- Develop and evaluate a machine-learning model for disaster impact prediction.
- Add user authentication and role-based access.
- Improve resource allocation recommendations.
- Add notifications for high-priority zones.
- Deploy the application to a cloud platform.

These are proposed enhancements and are not necessarily implemented in the current version.

## Limitations

- The displayed information may include sample or manually entered data.
- Priority scores depend on the implemented scoring rules and the accuracy of the input data.
- The application should not be used as the sole basis for real-world emergency decisions.

## Author

**Prachi Kumari**

GitHub: https://github.com/prachijha7903

## License

This project is developed for educational and demonstration purposes. A license can be added if the project is intended for public reuse.
