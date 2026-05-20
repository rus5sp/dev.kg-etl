# DEV.KG ETL Pipeline
 
Asynchronous ETL pipeline that extracts job vacancies from [dev.kg](https://devkg.com) API, transforms the data and loads it into a SQLite database.

## Installation
 
### 1. Clone the repository
 
```bash
git clone https://github.com/your/dev.kg-etl.git
cd dev.kg-etl
```
 
### 2. Create a virtual environment
 
```bash
python -m venv .venv
```
 
### 3. Activate the virtual environment
 
**Windows:**
```bash
.venv\Scripts\activate
```
 
**Mac/Linux:**
```bash
source .venv/bin/activate
```
 
### 4. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 5. Run
 
```bash
python main.py
```