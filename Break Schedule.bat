@ECHO OFF

:: Pass my script to python, along with the html file passed to it.
:: For the 32bit version
::WPy32-3850\\python-3.8.5\\python src\\break_schedule_generator.py "%~f1"

:: For the 64bit version
WPy64-3850\\python-3.8.5.amd64\\python src\\break_schedule_generator.py "%~f1"

:: We had an error, so hang to keep the terminal open.
IF %ERRORLEVEL% NEQ 0 (
   echo "--------------"
   echo "It broke..."
   echo "Contact Simon to get it fixed."
   pause
)
