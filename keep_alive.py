from flask import Flask
from threading import Thread
import os
import time
import logging

# Configuration du logging pour Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Discord</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 3em; margin: 0; }
            p { font-size: 1.2em; margin: 10px 0; }
            .status { 
                display: inline-block;
                width: 12px;
                height: 12px;
                background: #00ff00;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Bot Discord</h1>
            <p><span class="status"></span> Bot en ligne et opérationnel</p>
            <p>Préfixe des commandes : <strong>+</strong></p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "bot": "running",
        "service": "discord-bot"
    }, 200

@app.route('/ping')
def ping():
    return "pong", 200

def run():
    # Render utilise la variable PORT
    port = int(os.environ.get('PORT', 10000))
    
    print("=" * 60)
    print(f"🌐 DÉMARRAGE FLASK")
    print(f"   Host: 0.0.0.0")
    print(f"   Port: {port}")
    print(f"   URL: http://0.0.0.0:{port}")
    print("=" * 60)
    
    try:
        # Démarrer Flask sans reloader ni debug (important pour Render)
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE FLASK : {e}")
        import traceback
        traceback.print_exc()

def keep_alive():
    """Démarre Flask dans un thread séparé"""
    print("\n🚀 Initialisation du serveur Flask...")
    
    t = Thread(target=run, daemon=True, name="FlaskThread")
    t.start()
    
    # Attendre que Flask démarre
    time.sleep(3)
    
    port = int(os.environ.get('PORT', 10000))
    print(f"✅ Flask devrait être accessible sur le port {port}")
    print(f"   Testez : http://localhost:{port}\n")
    
    return t