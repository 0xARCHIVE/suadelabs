"""A simple script to run the app using Flask's server (debug mode)."""

from app.app import create_app

app = create_app()
app.run(port=8080, debug=True)
