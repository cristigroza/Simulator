from Test import app

@app.route('/robot')
def robot():
    return "Hello, robot!"