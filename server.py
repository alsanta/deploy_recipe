from flask_app import app
from flask_app.controllers import mainsite
from flask_app.controllers import login_register

if __name__=="__main__":
    app.run(debug=True)