class Popup():
    def __init__(self, width_ratio, height_ratio):
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        self.active = False
    
    def show(self):
        self.active = True
    
    def hide(self):
        self.active = False
    
    def is_active(self):
        return self.active
    
    

# DISCONNECTED POPUP
# COULD NOT CONNECT TO SERVER POPUP