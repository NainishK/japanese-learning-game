@echo off
echo Starting Django server...
start cmd /k "cd backend && ..\env\Scripts\python manage.py runserver 8001"
timeout /t 5
echo Starting React server...
start cmd /k "cd frontend && npm start"
echo Servers started! Please check:
echo Backend: http://127.0.0.1:8001/api/list/
echo Frontend: http://localhost:3000
