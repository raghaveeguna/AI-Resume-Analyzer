# AI Resume Analyzer using NLP Techniques

![Project Banner](https://via.placeholder.com/1200x400?text=AI+Resume+Analyzer+Banner) <!-- Placeholder for a project banner image -->

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
  - [4. Firebase Hosting Deployment (Optional)](#4-firebase-hosting-deployment-optional)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Live Demo](#live-demo) <!-- Placeholder for live demo link -->
- [Screenshots](#screenshots) <!-- Placeholder for screenshots -->

## Project Overview

This project is an AI-powered Resume Analyzer designed to streamline the recruitment process by efficiently parsing resumes, extracting key information using Natural Language Processing (NLP) techniques, and ranking candidates against job descriptions. The system features a React-based frontend for user interaction and a FastAPI backend for handling resume processing, NLP tasks, and database operations.

## Features

- **User Authentication**: Secure email and password login/registration using Firebase Authentication.
- **Resume Upload**: Supports PDF, DOCX, and plain text resume formats for easy submission.
- **Resume Parsing**: Extracts raw text content from various resume formats using `PyMuPDF` and `Python-Docx`.
- **Text Processing**: Cleans and preprocesses extracted text by converting to lowercase, removing stop words, special characters, and numbers using `NLTK` and regular expressions.
- **Keyword Extraction**: Identifies and extracts relevant keywords, skills, technologies, and degrees from resumes and job descriptions using a combination of:
    - **Rule-Based Matching**: Predefined keywords based on industry sectors and company requirements.
    - **TF-IDF (Term Frequency-Inverse Document Frequency)**: Ranks the importance of terms within documents.
    - **NER (Named Entity Recognition)**: Utilizes `SpaCy` to identify and categorize entities like skills, technologies, and educational degrees.
- **Job Description Analysis**: Parses and extracts critical keywords and requirements from job descriptions to create a target profile.
- **Candidate Ranking**: Ranks uploaded resumes based on their relevance and match against a specific job description, providing a score for each candidate.
- **MongoDB Integration**: Persistently stores processed resumes, job descriptions, and user data in a MongoDB Atlas cloud database.

## Tech Stack

### Frontend
- **React**: A declarative, component-based JavaScript library for building dynamic user interfaces.
- **Firebase**: Provides robust backend services, specifically Firebase Authentication for user management and Firebase Hosting for deployment.
- **React Router DOM**: Manages navigation and routing within the single-page application.
- **Axios**: A promise-based HTTP client for making requests to the FastAPI backend.

### Backend
- **Python**: The core language for all backend logic, NLP processing, and API development.
- **FastAPI**: A modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints, ensuring fast development and robust code.
- **PyMuPDF**: A Python library for working with PDF documents, used for extracting text from PDF resumes.
- **Python-Docx**: A library for creating and updating Microsoft Word (.docx) files, used here for extracting text from DOCX resumes.
- **SpaCy**: An industrial-strength natural language processing library for Python, utilized for advanced text processing, tokenization, and Named Entity Recognition.
- **NLTK (Natural Language Toolkit)**: A leading platform for building Python programs to work with human language data, used for tasks like stop word removal and tokenization.
- **Scikit-learn**: A comprehensive machine learning library for Python, employed for TF-IDF vectorization and other data processing utilities.
- **PyMongo**: The official Python driver for MongoDB, enabling seamless interaction with the MongoDB Atlas database.
- **Passlib**: A password hashing library for Python, used for securely hashing and verifying user passwords.
- **Python-Jose**: A JOSE (JSON Object Signing and Encryption) implementation in Python, used for handling JSON Web Tokens (JWT) for API authentication.
- **python-dotenv**: A module that loads environment variables from a `.env` file, crucial for managing sensitive configurations.

### Database
- **MongoDB Atlas**: A global cloud database service for MongoDB, providing a scalable, secure, and highly available NoSQL database solution for storing application data.

## Project Structure

```
/ai-resume-analyzer
├── /src
│   ├── /backend
│   │   ├── /api            # FastAPI application endpoints (main.py, auth.py)
│   │   ├── /core           # Core functionalities (e.g., database connection)
│   │   ├── /models         # Pydantic models for data validation and serialization
│   │   ├── /nlp            # NLP-related modules (resume parsing, text processing, keyword extraction)
│   │   └── /utils          # Utility functions (e.g., security, password hashing)
│   └── /frontend
│       ├── /public         # Public assets for React app
│       └── /src            # React source code
│           ├── /components # Reusable React components
│           ├── /context    # React Context API for global state (e.g., AuthContext)
│           ├── /hooks      # Custom React hooks
│           ├── /pages      # Main application pages
│           ├── /services   # API service integrations (e.g., Firebase, Backend API)
│           └── /assets     # Static assets like images
├── /docs                   # Project documentation (e.g., design docs, API docs)
├── /tests                  # Unit and integration tests for both frontend and backend
├── README.md               # Project description, setup instructions, and usage guide
├── LICENSE                 # License file (e.g., MIT, GPL)
├── .gitignore              # Specifies intentionally untracked files to ignore by Git
├── requirements.txt        # Python backend dependencies
└── .env.example            # Template for environment variables
```

## Setup and Installation

Follow these steps to get your AI Resume Analyzer project up and running locally.

### 1. Clone the Repository

First, clone the project repository from GitHub to your local machine:

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Backend Setup

Navigate to the root directory of your cloned project (`ai-resume-analyzer`).

#### 2.1. Create and Activate a Python Virtual Environment

It's highly recommended to use a virtual environment to manage Python dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `.\venv\Scripts\activate`
```

#### 2.2. Install Backend Dependencies

Install all required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

#### 2.3. Configure Environment Variables (`.env` file)

Create a `.env` file in the root directory (`ai-resume-analyzer/`) by copying the provided `.env.example`:

```bash
cp .env.example .env
```

Now, open the newly created `.env` file and fill in your MongoDB Atlas connection string and a strong secret key for JWT. Refer to the [MongoDB Atlas Setup Guide](#mongodb-atlas-setup-guide) below for detailed instructions on obtaining your `MONGO_URI`.

```dotenv
MONGO_URI="your_mongodb_atlas_connection_string"
DB_NAME="resume_analyzer_db" # You can change this to your preferred database name
SECRET_KEY="your_super_secret_jwt_key_here" # Generate a strong, random key
```

**Important**: The `SECRET_KEY` should be a long, random string. You can generate one using Python:
```python
import os
import secrets
print(secrets.token_urlsafe(32))
```

#### 2.4. Run the FastAPI Application

Start the FastAPI server. The `--reload` flag enables auto-reloading on code changes, which is useful for development:

```bash
uvicorn src.backend.api.main:app --reload
```

The backend API will be accessible at `http://localhost:8000`.

### 3. Frontend Setup

Navigate to the frontend directory:

```bash
cd src/frontend
```

#### 3.1. Install Frontend Dependencies

Install all Node.js packages required for the React application:

```bash
npm install
# or if you use Yarn:
yarn install
```

#### 3.2. Configure Firebase

1.  **Create a Firebase Project**: Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2.  **Register Your App**: In your Firebase project, add a new web app. Follow the instructions to get your Firebase configuration object.
3.  **Enable Email/Password Authentication**: In the Firebase Console, navigate to `Authentication` -> `Sign-in method` and enable `Email/Password`.
4.  **Update `firebase.js`**: Open `src/frontend/src/services/firebase.js` and replace the placeholder `firebaseConfig` with your actual Firebase project configuration:

    ```javascript
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_AUTH_DOMAIN",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_STORAGE_BUCKET",
      messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
      appId: "YOUR_APP_ID",
      measurementId: "YOUR_MEASUREMENT_ID"
    };
    ```

#### 3.3. Run the React Development Server

Start the React application in development mode:

```bash
npm start
# or yarn start
```

The frontend application will typically open in your browser at `http://localhost:3000` (or another available port).

### 4. Firebase Hosting Deployment (Optional)

If you wish to deploy your React frontend to Firebase Hosting for a live demo:

#### 4.1. Install Firebase CLI

If you haven't already, install the Firebase Command Line Interface (CLI) globally:

```bash
npm install -g firebase-tools
```

#### 4.2. Log in to Firebase

From your terminal, log in to your Firebase account:

```bash
firebase login
```

#### 4.3. Initialize Firebase in your Frontend Project

Navigate to your frontend project directory (`ai-resume-analyzer/src/frontend`) and initialize Firebase:

```bash
cd src/frontend
firebase init
```

During the initialization process:
- Select `Hosting: Configure files for Firebase Hosting and (optionally) set up GitHub Action deploys`.
- Choose your Firebase project.
- For `What do you want to use as your public directory?`, enter `build`.
- For `Configure as a single-page app (rewrite all URLs to /index.html)?`, type `Y`.
- For `Set up automatic builds and deploys with GitHub?`, type `N` (unless you want to set up CI/CD).

This will create a `firebase.json` file in your `src/frontend` directory.

#### 4.4. Build the React Application

Before deploying, you need to create a production build of your React app:

```bash
npm run build
```

This command will create a `build` folder containing the optimized static assets for your application.

#### 4.5. Deploy to Firebase Hosting

Finally, deploy your application:

```bash
firebase deploy --only hosting
```

After a successful deployment, Firebase will provide you with a Hosting URL (e.g., `https://your-project-id.web.app`). You can then add this link to the `Live Demo` section of your `README.md`.

## Usage

Once both the backend and frontend servers are running:

1.  **Register/Login**: Access the frontend application (e.g., `http://localhost:3000`), register a new user account, or log in with existing credentials.
2.  **Upload Resume**: Navigate to the "Upload Resume" page. Select a PDF, DOCX, or plain text resume file to upload. The backend will parse, process, and store the resume data in MongoDB.
3.  **Analyze Job Description**: Go to the "Analyze Job Description" page. Paste the text of a job description into the provided textarea and click "Analyze JD". The backend will extract keywords and store the job description.
4.  **Rank Candidates**: Visit the "Rank Candidates" page. Click "Refresh Ranking" to see a list of uploaded resumes ranked by their relevance to the most recently analyzed job description. The ranking is based on keyword matching.

## Contributing

We welcome contributions to improve this project! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Live Demo

[Link to Live Demo (Once Deployed)](https://your-firebase-hosting-url.web.app) <!-- Update this after deploying to Firebase Hosting -->

## Screenshots

Add screenshots of your application here to showcase its features. Create a `screenshots` directory in the root of your project and link images like this:

![Dashboard Screenshot](./screenshots/dashboard.png)
![Upload Resume Screenshot](./screenshots/upload-resume.png)
![Ranking Page Screenshot](./screenshots/ranking-page.png)

<!-- Placeholder for actual screenshots -->

