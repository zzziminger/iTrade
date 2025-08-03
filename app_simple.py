from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "iTrade API is working!",
        "status": "success",
        "version": "simple"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "iTrade"
    })

@app.route('/test')
def test():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>iTrade Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; }
            .success { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>iTrade Test Page</h1>
            <p class="success">✅ Flask app is working!</p>
            <p>This is a simple test page to verify the deployment.</p>
            <ul>
                <li>Flask: ✅ Working</li>
                <li>Routes: ✅ Working</li>
                <li>JSON Response: ✅ Working</li>
                <li>HTML Template: ✅ Working</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True) 