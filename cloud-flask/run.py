from src.app import app

if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_app = app