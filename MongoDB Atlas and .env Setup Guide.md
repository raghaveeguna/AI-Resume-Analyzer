# MongoDB Atlas and .env Setup Guide

This guide will walk you through the process of setting up a free MongoDB Atlas cluster, obtaining your connection string, and configuring your `.env` file for the AI Resume Analyzer backend.

## 1. Create a MongoDB Atlas Account and Cluster

1.  **Sign Up/Log In**: Go to the [MongoDB Atlas website](https://www.mongodb.com/cloud/atlas) and sign up for a free account or log in if you already have one.
2.  **Create a New Project**: Once logged in, you'll be prompted to create a new project. Give it a meaningful name (e.g., `AI-Resume-Analyzer-Project`).
3.  **Build a Database**: Choose `Build a Database`.
4.  **Select a Free Tier**: Select the `Shared` cluster option (M0 Sandbox is free). Choose a cloud provider and region closest to you for optimal performance.
5.  **Cluster Name**: Give your cluster a name (e.g., `ResumeAnalyzerCluster`) and click `Create Cluster`.

## 2. Configure Security Settings

After your cluster is provisioned (this might take a few minutes):

1.  **Create a Database User**: In the `Security` section of your cluster overview, go to `Database Access`. Click `Add New Database User`.
    -   Choose `Password` as the Authentication Method.
    -   Enter a strong `Username` and `Password`. **Remember these credentials**, as you will need them for your connection string.
    -   Set `Database User Privileges` to `Read and write to any database` (for simplicity in development, you can refine this later).
    -   Click `Add User`.
2.  **Add IP Access List Entry**: Go to `Network Access` under the `Security` section. Click `Add IP Address`.
    -   For development, you can select `Allow Access from Anywhere` (this is less secure but easiest for testing). **For production, you should restrict access to specific IP addresses of your backend server.**
    -   Click `Confirm`.

## 3. Get Your Connection String

1.  **Connect to Your Cluster**: From your cluster overview, click the `Connect` button.
2.  **Choose a Connection Method**: Select `Connect your application`.
3.  **Select Driver and Version**: Choose `Python` as your driver and the latest version (e.g., `4.0 or later`).
4.  **Copy the Connection String**: Copy the provided connection string. It will look something like this:

    ```
    mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
    ```

## 4. Configure Your `.env` File

Now that you have your MongoDB Atlas connection string, you need to update the `.env` file in your project root directory (`ai-resume-analyzer/`).

1.  **Locate `.env`**: Ensure you have created the `.env` file from the `.env.example` template (if not, run `cp .env.example .env` in your project root).
2.  **Edit `.env`**: Open the `.env` file and replace the placeholder values with your actual MongoDB URI and a strong `SECRET_KEY`.

    ```dotenv
    MONGO_URI="mongodb+srv://YOUR_ATLAS_USERNAME:YOUR_ATLAS_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME="resume_analyzer_db"
    SECRET_KEY="your_super_secret_jwt_key_here"
    ```

    -   **`MONGO_URI`**: Paste the connection string you copied from MongoDB Atlas. **Crucially, replace `<username>` and `<password>` with the database username and password you created in Step 2.1.**
    -   **`DB_NAME`**: This is the name of the database your application will use. You can keep `resume_analyzer_db` or change it.
    -   **`SECRET_KEY`**: This is used for signing JWT tokens in your FastAPI backend. Generate a strong, random string for this. You can use Python to generate one:
        ```python
        import secrets
        print(secrets.token_urlsafe(32))
        ```

3.  **Save the `.env` file.**

Your backend is now configured to connect to your MongoDB Atlas cluster. Remember that the `.env` file should **never** be committed to version control (it's already included in `.gitignore`).
