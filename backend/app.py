from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "project": "Warehouse Management System",
        "status": "running"
    }

if __name__ == "__main__":
    app.run(debug=True)
