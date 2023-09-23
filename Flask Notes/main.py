from website import create_app

app = create_app()

#Only start our web server if we run this file directly
if __name__ == '__main__':
    #Start our flask app (debug=True means any change we make restarts the server)
    #Change to False once app is running in production
    app.run(debug=True)