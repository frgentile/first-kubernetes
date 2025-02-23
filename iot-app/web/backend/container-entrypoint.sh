#!/bin/bash

/app/venv/bin/python3 -m uvicorn apis:app --host 0.0.0.0 --port 8000
