# MySQL DB Query Editor

A simple Tkinter-based GUI application for browsing MySQL databases and executing SQL queries.

## Features

- List all available MySQL databases
- Select a database from the GUI
- Enter and run arbitrary SQL queries
- Display query results in a table view
- Show affected row count for non-select queries
- Basic health status check for the selected database connection

## Requirements

- Python 3.8+
- MySQL server reachable from the machine
- `mysql-connector-python`
- `python-dotenv` (optional, only if using `.env` for configuration)

## Installation

1. Clone or download the project.
2. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependency:

```bash
pip install mysql-connector-python python-dotenv
```

## Configuration

Copy `.env.example` to `.env` and update the database credentials as needed:

```bash
cp .env.example .env
```

Edit `.env` values:

```ini
DB_HOST=localhost
DB_PORT=
DB_USER=xxxxx
DB_PASSWORD=XXXXXXXX
DB_NAME=kiosk
```

If `.env` is unavailable, the app will fall back to environment variables.

## Usage

Run the GUI application:

```bash
python mysqldbqueryeditor.py
```

- Use the `Reload Databases` button to refresh the database list.
- Select a database from the list.
- Enter a SQL query and click `Run Query`.
- Results are shown in the grid below the query editor.

## Notes

- The default connection uses `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and optional `DB_PORT`.
- If no database is selected, the app defaults to using `kiosk`.
- Queries that return rows display the result set; other statements display affected row count.

## File Structure

- `mysqldbqueryeditor.py` — main GUI application
- `.env.example` — example environment configuration

## License

Use and modify this project as needed.
