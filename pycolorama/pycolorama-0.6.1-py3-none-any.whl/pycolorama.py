


"""################################################################################
"""

PYGAME = 0
OPENCV = 1

print("IMPORTED my_color_module", PYGAME)


class COLOR:

    BLACK = (0, 0, 0)

    WHITE  = (255, 255, 255)
    ORANGE = (255, 165, 0)
    RED    = (255, 0, 0)
    BLUE   = (0, 0, 255)
    GREEN  = (0, 255, 0)
    YELLOW = (255, 255, 0)

    CYAN        = (0,255,255)
    MAGENTA     = (255,0,255)
    PINK        = (255,105,180)
    DARK_GREEN  = (0,128,0)
    DARK_BLUE   = (0,0,128)
    DARK_RED    = (128,0,0)
    GOLD        = (255,215,0)
    TURQUOISE   = (64,224,208)
    DODGER_BLUE = (30,144,255)
    HOT_PINK    = (255,105,180)
    DARK_GRAY   = (64,64,64)


    COLORS = [ CYAN, MAGENTA, DARK_GREEN, DARK_BLUE, GOLD, TURQUOISE, DODGER_BLUE, HOT_PINK ]    




    def __init__( self, type=PYGAME):
        self.type = type
        
        self.InitializeColors()
    
    
    def InitializeColors( self ):
        if self.type == PYGAME:
            pass
        elif self.type == OPENCV:
            
            # opencv is in BGR format
            self.BLACK = (0,0,0)
            
            self.WHITE  = (255,255,255)
            self.ORANGE = (0,165,255)
            self.RED    = (0,0,255)
            self.BLUE   = (255,0,0)
            self.GREEN  = (0,255,0)
            self.YELLOW = (0,255,255)

            self.CYAN        = (255,255,0)
            self.MAGENTA     = (255,0,255)
            self.PINK        = (180,105,255)
            self.DARK_GREEN  = (0,128,0)
            self.DARK_BLUE   = (128,0,0)
            self.DARK_RED    = (0,0,128)
            self.GOLD        = (0,215,255)
            self.TURQUOISE   = (208,224,64)
            self.DODGER_BLUE = (255,144,30)
            self.HOT_PINK    = (180,105,255)
            self.DARK_GRAY   = (64,64,64)
        
        else:
            print("### ERROR ###, unsupported color mode")
            
            
            


"""################################################################################
"""