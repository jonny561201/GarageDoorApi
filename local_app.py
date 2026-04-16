from svc.manager import create_app, start_services

app = create_app()
start_services(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
