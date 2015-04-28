import pygame

# Text drawing.
class Font(object):
    """Light wrapper for pygame text drawing.
    """
    def __init__(self, default_surface=None, size=48, face=None, color=(255, 255, 255),
                 aa=True, linespacing=5):
        """main_surface is the default surface we will draw on.
        """
        self.size = size
        self.face = face
        self.color = color
        self.font = pygame.font.SysFont(face, size)
        self.default_surface = default_surface
        # anti-aliasing flag
        self.aa = aa
        # Default spacing between multiple lines.
        self.linespacing = linespacing
        
    def draw(self, text, surface=None, x=0, y=0, centerx=False, centery=False, linespacing=None):
        """Draw text on the screen, multiline friendly.
        
        x, y indicate upperleft anchor of text.
        
        centerx=True will override any x value provided and horizontally 
        center text, relative to the surface.
        centery=True will override any y value provided and vertically
        center the text, relative to the surface.
        
        linespacing is an additional number of pixels added as a vertical
        separator between different lines of text. If provided, the default
        is overridden.
        """
        # Use provided or defaults.
        surface = surface or self.default_surface
        half_surface_width = surface.get_width()/2
        half_surface_height = surface.get_height()/2
        linespacing = linespacing or self.linespacing
        
        # Split into lines of text to process.
        lines = text.split("\n")
        
        if centery == True:
            # Calculate horizontal centering.
            # half_surface_height - (Total lines + spacing between lines)/2 
            y = half_surface_height - (len(lines)*self.size + (len(lines)-1)*linespacing)/2

        for line in lines:
            t = self.font.render(line, self.aa, self.color)
            trect = t.get_rect()
            if centerx == True:
                # Horizontal center.
                offsetx = trect.width/2
                trect.topleft = (half_surface_width-offsetx, y)
            else:
                # Absolute position.
                trect.topleft = (x, y)
            surface.blit(t, trect)
            # Move down a line.
            y += trect.height + linespacing
