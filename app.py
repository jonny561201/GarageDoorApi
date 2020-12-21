from svc.manager import create_app

app = create_app(__name__)
app.run(host='0.0.0.0', port=5001)
