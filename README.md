# embedchain-chat-app-backend

## Set up a virtual environment:
```python -m venv venv
source venv/bin/activate
```


## Install Flask and other required packages:
```
pip install -r requirements.txt
```

## Replace api key 
Goto https://platform.openai.com/account/api-keys for api key
```
os.environ["OPENAI_API_KEY"] = "YOURAPI_KEY"
```

## Run development server

Make sure it is running on 5000 port as front end is running there. If a different port is required make the corresponding change in front end
```
python app.py
```