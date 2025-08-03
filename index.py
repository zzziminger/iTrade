from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "iTrade is working!", "status": "success"}

@app.route('/health')
def health():
    return {"status": "healthy"}

@app.route('/test')
def test():
    return """
    <html>
    <head>
        <title>iTrade</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <h1>🚀 iTrade</h1>
        <p class="success">✅ Successfully deployed on Vercel!</p>
        <p>Your stock trading platform is live.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run() 