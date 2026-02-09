# Neon PostgreSQL Setup Instructions

## Step 1: Create Neon Database

1. Go to https://neon.tech and sign up/login
2. Click "Create Project"
3. Choose a project name (e.g., "evolution-of-todo")
4. Select a region (choose closest to you)
5. Click "Create Project"

## Step 2: Get Connection String

1. In your Neon dashboard, click on your project
2. Go to "Connection Details" or "Dashboard"
3. Copy the connection string that looks like:
   ```
   postgresql://[user]:[password]@[host]/[database]?sslmode=require
   ```
4. Example format:
   ```
   postgresql://myuser:mypassword@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## Step 3: Update Backend Configuration

1. Open `e:\phasell\backend\.env`
2. Replace the DATABASE_URL line with your Neon connection string:
   ```
   DATABASE_URL=postgresql://[your-connection-string-here]
   ```
3. Save the file

## Step 4: Install PostgreSQL Driver (if needed)

The `psycopg2-binary` package is already in requirements.txt, but verify it's installed:

```bash
cd e:\phasell\backend
pip install -r requirements.txt
```

## Step 5: Start Backend and Verify

```bash
cd e:\phasell\backend
uvicorn app.main:app --reload
```

The backend will:
- Connect to Neon PostgreSQL
- Automatically create tables on startup
- Log connection details (check console output)

## Step 6: Verify Database Migration

1. Start the backend server
2. Check console logs for "CREATE TABLE" statements
3. Run the test suite:
   ```bash
   pytest test_api.py -v
   ```
4. If tests pass, data is persisting in Neon!

## Troubleshooting

**Connection Error**: Verify connection string is correct and includes `?sslmode=require`

**Authentication Failed**: Check username/password in connection string

**Tables Not Created**: Check console logs for SQLModel errors

**SSL Error**: Ensure connection string ends with `?sslmode=require`

## Verify Persistence

1. Create a todo via the API or frontend
2. Stop the backend server (Ctrl+C)
3. Restart the backend server
4. Check if the todo still exists
5. ✅ If yes, Neon persistence is working!
