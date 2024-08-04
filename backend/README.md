
## initial setup
```
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```


## How to run development
```
.\venv\Scripts\activate
uvicorn src.main:app --port 8081
```


## update requirements
```
pip freeze > requirements.txt
```