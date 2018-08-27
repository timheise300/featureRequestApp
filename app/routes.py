from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    clients = [
        {
            'clientName' : 'Client A'
        },
        {
            'clientName' : 'Client B'
        },
        {
            'clientName' : 'Client C'
        }
    ]
    
    return render_template('index.html', title='Feature Requests', clients=clients)