

from typing import Any, Optional

import MySQLdb
from flask import Flask, g


def init_db(
    app: Flask,
    *,
    user: str,
    password: str,
    host: str,
    database: str,
    port: int = 3306,
    **connect_kwargs: Any,
):
    """Initialize DB settings and register teardown.

    Stores connection parameters in app.config and ensures the connection
    is closed at the end of each request.
    """
    app.config.setdefault(
        "MYSQLDB_SETTINGS",
        {
            "user": user,
            "password": password,
            "host": host,
            "database": database,
            "port": port,
            **connect_kwargs,
        },
    )

    app.teardown_appcontext(close_db)

    # Optional: create an eager connection once (mostly for early failure).
    # Requests will still get their own connection via get_db().
    return MySQLdb.connect(
        user=user,
        password=password,
        host=host,
        database=database,
        port=port,
        **connect_kwargs,
    )


def get_db() -> MySQLdb.Connection:
    """Get (or create) the per-request MySQL connection."""
    if "db" not in g:
        settings = getattr(g, "_mysql_settings", None)
        if settings is None:
            # app_context must exist here; use current_app via Flask's context.
            from flask import current_app

            settings = current_app.config.get("MYSQLDB_SETTINGS")
            if not settings:
                raise RuntimeError(
                    "Database is not initialized. Call db.init_db(app, ...) first."
                )

        g.db = MySQLdb.connect(**settings)

    return g.db


def get_cursor():
    """Convenience: dict cursor for the current request."""
    return get_db().cursor(cursorclass=MySQLdb.cursors.DictCursor)


# Backward-compatible typo in your original draft
fet_cursor = get_cursor


def close_db(exception: Optional[BaseException] = None):
    """Close the per-request connection."""
    db_conn = g.pop("db", None)
    if db_conn is not None:
        try:
            db_conn.close()
        except Exception:
            # Avoid masking the original exception during teardown
            pass
