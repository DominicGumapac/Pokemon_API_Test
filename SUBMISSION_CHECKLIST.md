# Submission Checklist (do these yourself)

The code, data, and README are done. Here's what's left, in order.

## 1. Run it on your own machine
```bash
cd pokemon-api
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Leave that terminal running — it's your server. Open a **second** terminal
for the curl commands below (or use Postman instead if you prefer).

## 2. Take one screenshot per HTTP method
Run each command and screenshot the terminal showing the command AND its
JSON response (or do the equivalent in Postman: request + response body).

**GET**
```bash
curl -s -w "\nStatus: %{http_code}\n" http://127.0.0.1:5000/pokemon/1
```

**POST**
```bash
curl -s -w "\nStatus: %{http_code}\n" -X POST http://127.0.0.1:5000/pokemon \
  -H "Content-Type: application/json" \
  -d '{"name":"Charizard","type":"Fire/Flying","hp":78,"attack":84,"defense":78,"speed":100}'
```

**PUT** (use whatever id your POST above returned, e.g. 16)
```bash
curl -s -w "\nStatus: %{http_code}\n" -X PUT http://127.0.0.1:5000/pokemon/16 \
  -H "Content-Type: application/json" \
  -d '{"hp": 85}'
```

**DELETE**
```bash
curl -s -w "\nStatus: %{http_code}\n" -X DELETE http://127.0.0.1:5000/pokemon/16
```

Optional bonus screenshots (not required but shows thoroughness): a 400
from POSTing with a missing field, and a 404 from GETting a bad id.

Compile all screenshots into a single doc or image set for Canvas.

## 3. Push to GitHub
```bash
cd pokemon-api
git init
git add .
git commit -m "Pokemon REST API - full CRUD with Flask and SQLite"
git branch -M main
git remote add origin https://github.com/<your-username>/pokemon-api.git
git push -u origin main
```
Make sure the repo is set to **Public** on GitHub so it can be graded.

## 4. Submit
- GitHub repo link (public)
- The screenshot document/image set (4 methods, GET/POST/PUT/DELETE)
