# My Flask App

A simple Flask Blog App with Authorization
integrated docker

## To run the app:
### Requirements:
    - Docker
    - Python3

### To run in production with docker:
```bash
    $ git clone https://github.com/alaturqua/my_flask_app.git
    $ docker-compose up
    
    
```
    Visit http://localhost
    
It will be served on port 80

### To run locally in development:
```bash
    $ git clone https://github.com/alaturqua/my_flask_app.git
    $ pip3 install -r requirements.txt
    $ python3 app.py
```

    Visit http://localhost:5000