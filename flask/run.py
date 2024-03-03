import logging

from app import create_app

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        logging.error("run.py: An error occurred while running the app: %s", str(e))
