# Local setup on D:

Run these commands from the project root:

```powershell
cd D:\23BCE5104\7SEM\vsss\mmm
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run extraction from either the project root or the `ingestion` folder:

```powershell
.\.venv\Scripts\python.exe ingestion\extract.py
```

The extracted text is written to `data\mahabharatham_raw.txt`. The script resolves
the PDF and output paths from its own location, so the current directory does not
change where project data is read or written.