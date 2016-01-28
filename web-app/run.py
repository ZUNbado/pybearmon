# Run a test server.
from app import app
if __name__ == '__main__':
    app.config.from_object('config.Development')
    app.run(host='0.0.0.0', port=5000, debug=True)
