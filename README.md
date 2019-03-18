# Following instructions are valid only for Win10 platform 

To install the app:

- Activate virtualenv

- Install requirements

        $ pip install -r requirements.txt
    
- Install wxPython for your platform
        
        Win10:
            $ pip install -U wxPython

- Run installation script
        
        $ pyinstaller app.spec -n Light Controller
        
        - To create .spec file run: 
            $ pyi-makespec your_app_name.py
            
        
- Proceed to dist directory and run .exe file