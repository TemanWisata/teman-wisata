# Teman Wisata

## Requirements

- Python version >= 3.12
- uv >= 0.7.14
- Node.js (for UI development)

## Setup

Clone the repository and install dependencies:

```sh
uv sync
```

For development tools (linting, testing):

```sh
uv sync
uv run pre-commit install
```

## Running the Backend

To start the FastAPI backend:

```sh
uv run python app/main.py
```

Or, using Uvicorn directly:

```sh
uv run uvicorn app.main:app --reload
```

## Running the Frontend (UI)

Navigate to the `ui` directory and install dependencies:

```sh
cd ui
npm install
```

Start the development server:

```sh
npm run dev
```

The UI will be available at [http://localhost:5173](http://localhost:5173) by default.

## Development

- **Lint Python code:**
  ```sh
  uv run ruff check .
  uv run mypy .
  ```

- **Lint and format UI code:**
  ```sh
  cd ui
  npm run lint
  npm run format
  ```

- **Run tests:**
  ```sh
  uv run pytest
  ```

- **Clean project:**
  ```sh
  uv run cleanpy .
  ```

## Project Structure

- `app/` — Backend FastAPI application
- `ui/` — Frontend (Vite + TypeScript + TailwindCSS)
- `tests/` — Tests for backend
- `deployment/` — Deployment scripts and Dockerfiles
- `supabase/` — Supabase configuration

See the Makefile for

## Supabase Setup

### Local Supabase

1. **Install Supabase CLI**
   Follow the [official guide](https://supabase.com/docs/guides/cli) or run:
   ```sh
   npm install -g supabase
   ```

2. **Start Supabase locally**
   In the project root (where `supabase/` exists):
   ```sh
   supabase start
   ```

3. **Access Supabase Studio**
   Visit [http://localhost:54323](http://localhost:54323) for the dashboard.

4. **Apply migrations**
   ```sh
   supabase db push
   ```

### Online Supabase (Hosted)

1. **Create a project**
   Go to [Supabase Dashboard](https://app.supabase.com/), sign in, and create a new project.

2. **Configure environment variables**
   - Get your Supabase URL and anon/public key from the project settings.
   - Add them to your backend `.env` file:
     ```
     SUPABASE_URL=your-supabase-url
     SUPABASE_KEY=your-supabase-key
     ```

3. **Apply migrations**
   Push your schema to the hosted project:
   ```sh
   supabase db push --db-url "postgresql://<username>:<password>@<host>:<port>/dbname"
   ```

4. **Connect your app**
   Use the provided URL and key in your backend and frontend configuration.

---
