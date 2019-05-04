import os

from tea_site import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT')) 
    app.run(host='0.0.0.0', port=port, debug=False)