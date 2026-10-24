# 🏗️ Multimodal Construction Intelligence Platform

An AI-powered construction intelligence platform designed to support construction professionals with site safety monitoring, structural crack analysis, real estate valuation, project planning, and daily site assistance.

## 📌 Overview

Traditional construction management often relies on manual inspections, static documentation, and experience-based decisions. This project aims to make construction workflows more efficient by combining text inputs, construction images, and structured project data with AI-assisted analysis.

The platform uses a React frontend and a Python FastAPI backend, with optional integration with Google's Gemini AI for multimodal analysis.

## ✨ Key Features

- **Construction Site Safety Monitoring:** Analyze site-related inputs and generate safety observations and recommended actions.
- **Structural Crack Detection and Analysis:** Submit construction images for crack-related observations and inspection guidance.
- **Real Estate Valuation:** Estimate property value using area, price per square foot, property age, and condition.
- **Construction Project Planning:** Organize project phases, milestones, and potential risks.
- **Daily Site Assistance:** Get construction-related guidance, checklists, and weather-aware recommendations.
- **Image Upload:** Submit construction images for supported analysis workflows.
- **Analysis History:** Store and review previous analysis results.
- **AI Integration:** Support for connecting Google's Gemini AI through an API key.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| React.js | Frontend user interface |
| HTML5 and CSS3 | Structure and styling |
| Python | Backend programming |
| FastAPI | REST API development |
| Pydantic | Data validation |
| SQLite | Local data storage |
| Google Gemini API | Optional AI-powered analysis |
| Git and GitHub | Version control and source code hosting |

## 🏛️ System Architecture

```text
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  +---- Input Validation
  |
  +---- AI Integration
  |       |
  |       v
  |    Gemini API
  |
  +---- Analysis Logic
  |
  +---- SQLite Database
  |
  v
Results displayed in React
```

## 📂 Project Structure

```text
multimodal-construction-intelligence-platform/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── index.html
│
├── .gitignore
└── README.md
```

*Note: The folder structure above is illustrative. Refer to the actual files in the repository if your project differs.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git
- A Google Gemini API key if you want to enable Gemini-powered features

### 1. Clone the repository

```bash
git clone https://github.com/irounak14/multimodal-construction-intelligence-platform.git
cd multimodal-construction-intelligence-platform
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The backend API should be available at:

`http://127.0.0.1:8000`

Explore the API documentation at:

`http://127.0.0.1:8000/docs`

### 3. Set up the frontend

Open a second terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local frontend URL printed in the terminal, commonly:

`http://localhost:5173`

### 4. Configure AI integration

To enable Gemini-powered analysis, configure your API key using the backend's environment configuration.

1. Create a `.env` file in the appropriate backend directory.
2. Add the Gemini API key using the environment variable name expected by the application.
3. Restart the backend server.

**Important:** Never commit your `.env` file or expose your API key publicly. Check the project code for the exact environment variable name before configuring it.

## 🔒 Safety and Limitations

- AI-generated observations are intended to support, not replace, qualified construction professionals.
- Structural crack observations are not certified structural assessments.
- Safety recommendations should be verified by qualified personnel.
- Property valuations are estimates and are not professional appraisals.
- Live weather information requires an actual weather data integration.
- AI-powered functionality depends on the configured provider, API access, and usage limits.

## 🚀 Future Enhancements

- Real-time weather API integration
- Advanced computer vision for construction site monitoring
- Improved crack measurement and image analysis
- User authentication and role-based access control
- Downloadable PDF inspection reports
- Project dashboards and progress tracking
- Cloud deployment and persistent database hosting

## 🎯 Project Objective

The objective of this project is to explore how multimodal artificial intelligence can assist construction professionals in analyzing site information, identifying potential risks, planning projects, and making better-informed decisions.

## 👨‍💻 Author

**Rounak**

GitHub: [@irounak14](https://github.com/irounak14)

## 📄 License

This project is available for educational and portfolio purposes. A specific open-source license has not yet been assigned.
