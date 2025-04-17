# fth-receipt-processor
Python Fast-API application that processes a JSON purchase receipt and calculates reward points.

## Installation

### 1. Clone the repository
```
git clone https://github.com/smk-dev20/fth-receipt-processor.git
cd fth-receipt-processor
```
### 2. Dev Environment Setup
#### Setup a virtual environment - Unix/Linux
```
python3 -m venv .venv
source .venv/bin/activate
```

#### Setup a virtual environment - Windows - Command Prompt
```
python -m venv .venv
.venv\Scripts\activate
```

#### Install dependencies
```
pip install -r requirements.txt
```

#### Setup Environment Variables
Create a .env file and configure database credentials:
```
DB_NAME=receipt_points_db
```

#### Run the application
```
python app/main.py
```

Application will start on http://localhost:8000

### 3. Running on Docker
#### Setup Environment Variables
Create a .env file in app folder and configure database credentials:
```
DB_NAME=receipt_points_db
```

#### Build the docker image
```
docker build -t receipt_processor .
```

#### Run the application
```
docker run -p 8000:8000 receipt_processor
```
Application will start on http://127.0.0.1:8000/

## APIS

### 1. Process Receipt
```
URL: http://127.0.0.1:8000/receipts/process
Method: POST
Header: Content-Type: application/json
Body:
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}

Expected Response:
(JSON containing an id for the receipt.)
{
    "id": "5e1f28ce-3b39-4861-ac94-3a084ed4f410"
}
```

### 2. Get Points
```
URL: http://127.0.0.1:8000/receipts/{id}/points
Method: GET
Header: Content-Type: application/json
Body: None

Expected Response:
(A JSON object containing the number of points awarded.)
{
    "points": 109
}

```


