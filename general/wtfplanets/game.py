import random
import sys
import pygame
from pygame.locals import *
from lib.commonmath import mmval
from lib.events import EventPublisher, EventSubscriber
from lib.states import State, StateManager
from lib.font import Font

# Simple, synchronous pub/sub system.
events = EventPublisher()

# Game settings.
WIN_SIZE = (600, 600)
# Game score.
score = 0
top_score = 0



def collisions(one, others):
    """Collide one against a group, and avoid colliding with self.
    """
    for other in others:
        if one.rect.colliderect(other.rect) and one is not other:
            return True
    return False



class Entity(object):
    def process(self):
        pass
    
    def draw(self, surface):
        surface.blit(self.surface, self.rect)
    
    def destroy(self):
        pass

class Baddie(Entity):
    # Pixels square (for height and width).
    size_minmax = (10, 40)
    # Pixels per frame.
    speed_minmax = (1, 8)
    # Reserved for the varied image surfaces.
    images = None
    
    def __new__(cls):
        if cls.images is None:
            # Allow lazy loading of image surface after pygame has been init'd.
            cls.images = [pygame.image.load('assets/moon0.png').convert_alpha(),
                          pygame.image.load('assets/moon1.png').convert_alpha(),
                          pygame.image.load('assets/moon2.png').convert_alpha(),
                          pygame.image.load('assets/moon3.png').convert_alpha()]
            #cls.image.set_colorkey((0, 0, 0))
        return super(Baddie, cls).__new__(cls)
    def __init__(self):
        self.size = random.randint(*self.size_minmax)
        # Start at the top of the screen, just outside.
        self.rect = pygame.Rect(random.randint(0, WIN_SIZE[0]-self.size), 0 - self.size, self.size, self.size)
        self.speed = random.randint(*self.speed_minmax)
        self.surface = pygame.transform.scale(random.choice(self.images), (self.size, self.size))

    def process(self):
        # Move down the screen.
        self.rect.move_ip(0, self.speed)
        if self.rect.top > WIN_SIZE[1]:
            return "dead"

class Player(Entity, EventSubscriber):
    # Number of delta pixels applied by keypress.
    move_rate = 5
    # Reserved for image surface.
    image = None

    def __new__(cls):
        if cls.image is None:
            # Allow lazy loading of image surface after pygame has been init'd.
            # Example of taking a sprite from a spritesheet.
            # (left, top), (width, height) of sprite on sprite sheet.
            player_ship = pygame.Rect((6, 68), (25, 22))
            # Take just the player ship we want.
            cls.image = pygame.image.load('assets/ships.gif').convert().subsurface(player_ship)
        return super(Player, cls).__new__(cls)

    def __init__(self):
        # Init EventSubscriber.
        super(Player, self).__init__()

        self.rect = self.image.get_rect()
        # Center bottom.
        self.rect.topleft = (WIN_SIZE[0]/2, WIN_SIZE[1]-50)
        self.surface = self.image
        
        # Velocity for keyboard based movement (x, y).
        self.velocity = [0, 0]
        
        # Subscribe to events.
        # Probably only do key or mouse motion, not both.
        self.subto(events, KEYDOWN, self.keydown_listener)
        self.subto(events, KEYUP, self.keyup_listener)
        self.subto(events, MOUSEMOTION, self.mousemotion_listener)
    
    def keydown_listener(self, ev):
        # ev is a pygame event wrapped in EventObject.
        ev = ev.data["ev"]
        # Pressing opposing keys will override previous behavior.
        if ev.key == K_LEFT or ev.key == ord('a'):
            self.velocity[0] = -self.move_rate
        if ev.key == K_RIGHT or ev.key == ord('d'):
            self.velocity[0] = self.move_rate
        if ev.key == K_UP or ev.key == ord('w'):
            # Screen pixels: negative is up.
            self.velocity[1] = -self.move_rate
        if ev.key == K_DOWN or ev.key == ord('s'):
            # Screen pixels: positive is down.
            self.velocity[1] = self.move_rate

    def keyup_listener(self, ev):
        # ev is a pygame event wrapped in EventObject.
        ev = ev.data["ev"]
        if ev.key == K_LEFT or ev.key == ord('a'):
            if self.velocity[0] < 0: self.velocity[0] = 0
        if ev.key == K_RIGHT or ev.key == ord('d'):
            if self.velocity[0] > 0: self.velocity[0] = 0
        if ev.key == K_UP or ev.key == ord('w'):
            if self.velocity[1] < 0: self.velocity[1] = 0
        if ev.key == K_DOWN or ev.key == ord('s'):
            if self.velocity[1] > 0: self.velocity[1] = 0

    def mousemotion_listener(self, ev):
        # ev is a pygame event wrapped in EventObject.
        ev = ev.data["ev"]
        if ev.type == MOUSEMOTION:
            # If the mouse moves, move the player where the cursor is.
            self.rect.center = ev.pos
            # Move the mouse cursor to match the player.
            pygame.mouse.set_pos(self.rect.centerx, self.rect.centery)

    def process(self):
        # Move player within boundaries.
        self.rect.left = mmval(self.rect.left+self.velocity[0], WIN_SIZE[0])
        self.rect.bottom = mmval(self.rect.bottom+self.velocity[1], WIN_SIZE[1])

    def destroy(self):
        # Remove event listeners.
        self.unsubfrom()



class StartStage(State):
    name = "start"
    
    def __init__(self, game_engine):
        self.font = game_engine.font
        # Used to signal end of our stage.
        self.next_stage = None
    
    def enter(self):
        self.next_stage = None
    
    def handle_event(self, event):
        if event.type == KEYUP:
            self.next_stage = "game"
    
    def process(self):
        return self.next_stage
    
    def draw(self, surface):
        self.font.draw('WTF Planets?\nPress a key to start.', surface, centerx=True, centery=True)

class GameStage(State):
    name = "game"
    add_new_baddie_rate = 6
    
    def __init__(self, game_engine):
        self.font = game_engine.font
        # Reserved settings, initialized on stage entry.
        self.baddie_add_counter = None
        self.entities = None
        
    def enter(self):
        # Reset game settings.
        global score
        score = 0
        
        self.baddie_add_counter = 0
        # All entities for processing.
        self.entities = []
        # Keep separate reference to player for collision tests.
        self.player = Player()
        self.entities.append(self.player)

        # Play the game music.
        pygame.mixer.music.play(-1, 0.0)

    def exit(self):
        for ent in self.entities:
            ent.destroy()

        # Stop the game music.
        pygame.mixer.music.stop()

    def process(self):
        global score
        # Increase the score every frame.
        score += 1 
        
        # Add new baddies at the top of the screen, if needed.
        self.baddie_add_counter += 1
        if self.baddie_add_counter >= self.add_new_baddie_rate:
            self.baddie_add_counter = 0
            self.entities.append(Baddie())

        self.entities = filter(lambda ent: ent.process() != "dead", self.entities)

        # Check if any of the baddies have hit the player.
        if collisions(self.player, self.entities):
            return "end"
    
    def handle_event(self, event):
        pass
    
    def draw(self, surface):
        self.font.draw('Score: %s\nTop Score: %s' % (score, top_score), surface, x=10)
        for ent in self.entities:
            ent.draw(surface)

class EndStage(State):
    name = "end"
    
    def __init__(self, game_engine):
        self.font = game_engine.font
        self.sound = pygame.mixer.Sound('assets/gameover.wav')
        self.next_stage = None
    
    def handle_event(self, event):
        if event.type == KEYUP:
            self.next_stage = "game"
    
    def enter(self):
        # Play game over music.
        self.sound.play()
        self.next_stage = None
    
    def exit(self):
        # Cleanup.
        global score, top_score
        if score > top_score:
            # Set the new high score.
            top_score = score

        # Stop game over music.
        self.sound.stop()
        
    def process(self):
        return self.next_stage

    def draw(self, surface):
        message = 'GAME OVER\nYour Score: %s\nPress a key to play again.' % score
        if score > top_score:
            message = "You got a high score!\n\n" + message
        self.font.draw(message, surface, centerx=True, centery=True)



class GameEngine(StateManager):
    fps = 40
    def __init__(self):
        super(GameEngine, self).__init__()

        # set up pygame, the window, and the mouse cursor
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption('WTF Planets?')
        pygame.mouse.set_visible(False)
        
        self.background = pygame.image.load("assets/starfield.png").convert()
        self.background = pygame.transform.scale(self.background, (WIN_SIZE[0]*2, WIN_SIZE[1]*2))
        self.background_rotation = 0
        
        # sounds
        pygame.mixer.music.load('assets/background.ogg')
        
        # Main game font.
        self.font = Font()
        
        self.add_state(StartStage(self))
        self.add_state(GameStage(self))
        self.add_state(EndStage(self))
        self.set_state("start")

    def run(self):        
        """The game loop. Call this to get things running.
        """
        while True:
            # Handle/pass on device events caught by pygame.
            for event in pygame.event.get():
                if event.type == QUIT or\
                            (event.type == KEYUP and event.key == K_ESCAPE):
                    # We're done, quit.
                    pygame.quit()
                    sys.exit()
                
                # Pass events to each stage.
                self.active_state.handle_event(event)
        
                # Pass events as their type through the event system.
                events.pub(event.type, ev=event)
            
            # Normal game processing.
            potential_next_stage = self.active_state.process()
            if potential_next_stage is not None:
                self.set_state(potential_next_stage)
            
            # Clear previous view with new, modified background.
            self.background_rotation += 1
            rotated_bg = pygame.transform.rotate(self.background, self.background_rotation)
            self.window.blit(rotated_bg, (WIN_SIZE[0]/2-rotated_bg.get_width()/2, 
                                          WIN_SIZE[1]/2-rotated_bg.get_height()/2))
            # Draw items over memory surface.
            self.active_state.draw(self.window)
            # Redraw the screen. This is not optimised, but could be by passing
            # in a sequence of dirty rects that need updating.
            pygame.display.update()
        
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = GameEngine()
    game.run()
