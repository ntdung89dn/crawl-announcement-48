
Install in local
```bash
 $python3 -m venv venv
# On Linux/macOS
 $source venv/bin/activate
# On Windows
 $venv\Scripts\activate
 #Install package by file:
 pip install -r requirements.txt
 #OR 
 $pip install playwright asyncio
 $playwright install

## Running file:
```bash
python main.py

## Build Docker Image

From the project root directory (where the `Dockerfile` and your Python script are located), run:

```bash
docker build -t playwright-python-scraper .