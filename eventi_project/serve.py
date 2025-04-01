from waitress import serve

from eventi_project.wsgi import application

if __name__ == '__main__':
    print("Starting server...")
    serve(application, port='8000', host='0.0.0.0')