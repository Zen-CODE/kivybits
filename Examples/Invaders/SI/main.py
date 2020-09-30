from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.properties import ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

from math import sqrt
from random import randint

#______________________________________________________________________________
#  Dimensions of the alien invasion
AliensPerRow = 11
AlienRows = 5

#______________________________________________________________________________
# Sounds are loaded globally on startup, and referenced where needed
Sounds = dict(explosion     = SoundLoader.load('sounds/explosion.wav'),
              fastinvader1  = SoundLoader.load('sounds/fastinvader1.wav'),
              fastinvader2  = SoundLoader.load('sounds/fastinvader2.wav'),
              fastinvader3  = SoundLoader.load('sounds/fastinvader3.wav'),
              fastinvader4  = SoundLoader.load('sounds/fastinvader4.wav'),
              invaderkilled = SoundLoader.load('sounds/invaderkilled.wav'),
              shoot         = SoundLoader.load('sounds/shoot.wav'),
              ufo_lowpitch  = SoundLoader.load('sounds/ufo_lowpitch.wav'),
              ufo_highpitch = SoundLoader.load('sounds/ufo_highpitch.wav'))

#______________________________________________________________________________
#  Run time parameters; kept here for easy reference in the code
GlobalParams = dict(  HiScore      = 0,
                      GunCount     = 0,
                      RestartDelay = 5.0,
                      ReadyDelay   = 3.0,
                      SinglePlayer = 1,
                      config       = None)

def saveGlobalParams():
    config = GlobalParams['config']
    if config:
        for option, value in GlobalParams.items():
            if value != config:
                config.set('Invaders', option, value)
        config.write()

class Graphic(Widget):
    """ A generic graphic paints the source using the current colour.  This makes
        it really easy to control fading in and out by simply changing the alpha.
        Where a widget has multiple states, we can select the appropriate source
        by incrementing the state and wrapping the number when it exceeds
        len(sources).  The state is an index into sources.
        <lumina> controls the brightness, and the paint colour is plain white.
    """
    sources = ListProperty(None)
    state   = NumericProperty(0)
    alpha   = NumericProperty(1)
    lumina  = NumericProperty(1)

    def stateEvent(self):
        ''' We call this whenever we update our state.  Children can override this. '''

    def incState(self):
        self.state = (self.state + 1) % len(self.sources)
        self.stateEvent()
        return self

class Projectile(Graphic):
    ''' Bombs and bullets are instances of graphics which update with every clock tick.
        They have very specific functionality; in particular, they can collide with
        other objects.
        <delta> controls the speed of travel, and points applies to bullets, which
        carries the score of the object they collided with.  Defined in si.kv
    '''
    sources = ["atlas://images/vaders/b1", "atlas://images/vaders/b2"]
    expired = False
    delta   = NumericProperty(0)
    points  = NumericProperty(0)

    def expiryCheck(self):
        ''' An event place holder '''

    def update(self, dt):
        if self.expired: return True
        pos = Vector(self.pos)
        pos.y = pos.y + self.delta * dt
        self.pos = pos.x, pos.y
        self.incState()
        self.expiryCheck()
        return self.expired

class Bullet(Projectile):
    ''' A kind of projectile that moves vertically upward and kills aliens
    '''
    def expiryCheck(self):
        if Vector(self.pos).y > self.parent.height:
            self.expired = True

class Bomb(Projectile):
    ''' A type of projectile that moves vertically downward and kills guns.
    '''
    def expiryCheck(self):
        if Vector(self.pos).y < 5:
            self.expired = True

class Invader(Graphic):
    ''' A generic invader appears within a specific row and column in a grid.  We maintain
        two states of validity, one for each player.  The <invalid> property reflects whether
        or not the invader has been shot for a specific player.
        An invader may have a bomb in the air; bombs are limited to one active bomb per invader.
    '''
    layer   = NumericProperty(0)
    column  = NumericProperty(0)
    invalid = False
    bomb    = None
    invalid1 = invalid2 = False

    def __init__(self, layer, column, **kwargs):
        super(Invader, self).__init__(**kwargs)
        self.layer  = layer
        self.column = column

    def switchPlayer(self, current):
        if current:
            self.invalid2 = self.invalid
            self.invalid = self.invalid1
        else:
            self.invalid1 = self.invalid
            self.invalid = self.invalid2

    def stateEvent(self):
        if not self.bomb and not self.invalid and self.alpha==1:  # no bomb out there
            perc = randint(0,500)
            if perc < 8:
#            if perc < 0:   # Debug- disable bombs
                bomb = Bomb()
                bomb.center_x = self.center_x
                bomb.y = self.y - bomb.height
                self.parent.parent.parent.parent.add_widget(bomb)
                self.bomb = bomb

    def beenShot(self, bullets, dt):
        for bullet in bullets:
            if bullet.expired: continue
            if self.alpha>0 and self.collide_point(bullet.x, bullet.y):
                sound = Sounds['invaderkilled']
                if sound is not None:
                    sound.stop()
                    sound.play()
                bullet.expired = True
                bullet.points = (6-self.layer) * 10
                self.invalid = True
        if self.invalid and self.alpha > 0:       # fade out
            self.alpha = self.alpha - dt
            if self.alpha < 0:
                self.alpha = 0
        if not self.invalid and self.alpha < 1:   # fade in
            self.alpha = self.alpha + dt
            if self.alpha > 1:
                self.alpha = 1
        if self.bomb:
            if self.bomb.expired:
                self.bomb.parent.remove_widget(self.bomb)
                self.bomb = None
        return self.invalid and self.alpha==0

class Ship(Invader):
    ''' A ship is a special kind of invader that travels independently from left to right
        or from right to left across the screen.
    '''
    counter   = NumericProperty(0)
    speed     = NumericProperty(10)
    direction = NumericProperty(0)
    sound     = None

    def __init__(self, parent):
        super(Ship,self).__init__(0,0)
        self.counter = 0
        self.direction = randint(0,1)
        self.x = self.direction * (parent.width - self.width)
        self.y = parent.x + parent.boxHeight + parent.boxGap + self.height
        self.direction = (self.direction * 2 - 1) * -1

    def getSound(self):
        return None

    def update(self, dt):
        self.counter = self.counter + dt
        if self.counter > 0.015:
            self.counter = 0
            self.x = self.x + self.direction * dt/0.015
            if self.sound is None:
                self.sound = self.getSound()
                if self.sound is not None:
                    self.sound.stop()
                    self.sound.play()

            if self.x < 0 or self.x > self.parent.width:
                self.parent.remove_widget(self)
                if self.sound is not None:
                    self.sound.stop()
                    self.sound = None
                return False
        return True
    def getPoints(self):
        ''' Virtual method to be specialised '''
        return 0
    def beenShot(self, bullet):
        if bullet.expired: return False
        if self.collide_widget(bullet):
            sound = Sounds['explosion']
            if sound is not None:
                sound.stop()
                sound.play()
            self.parent.remove_widget(self)
            if self.sound is not None:
                self.sound.stop()
            bullet.expired = True
            bullet.points = self.getPoints()
            return True
        return False

class bigShip(Ship):
    sources = ["atlas://images/vaders/bigshp"]
    speed   = 20
    loopAdj = 0.3220
    def getPoints(self):
        return randint(7, 18)*10
    def getSound(self):
        return Sounds['ufo_lowpitch']

class lilShip(Ship):
    sources = ["atlas://images/vaders/lilshp"]
    speed   = 15
    loopAdj = 0.1425
    def getPoints(self):
        return randint(15, 25)*10
    def getSound(self):
        return Sounds['ufo_highpitch']

class Alien0(Invader):
    sources = ["atlas://images/vaders/a00", "atlas://images/vaders/a01"]

class Alien1(Invader):
    sources = ["atlas://images/vaders/a10", "atlas://images/vaders/a11"]

class Alien2(Invader):
    sources = ["atlas://images/vaders/a20", "atlas://images/vaders/a21"]

class Alien3(Invader):
    sources = ["atlas://images/vaders/a30", "atlas://images/vaders/a31"]

class Alien4(Invader):
    sources = ["atlas://images/vaders/a40", "atlas://images/vaders/a41"]

class AlienBox(BoxLayout):
    ''' The AlienBox embeds an alien and handles padding differences per row of aliens
    '''
    alien  = ObjectProperty(None)
    column = NumericProperty(0)
    row    = NumericProperty(0)

    def __init__(self, alien, row, column):
        super(AlienBox,self).__init__()
        self.alien = alien
        self.row = row
        self.column = column
        self.add_widget(alien)

class Level(BoxLayout):
    ''' A level is a box layout containing AlienBox's which in turn
        contain invaders.  Each level calculates the amount of padding
        for it's AlienBox's according to: 2*((4-row)/2) (si.kv), so for
            row:0, padding is 4
            row:1, padding is 2
            row:2, padding is 2
            row:3, padding is 0
            row:4, padding is 0
        This is consistent with the alien size scaling for the original
        game, and makes it more difficult to shoot the top aliens.
        Levels have a min_col and max_col which are None when all aliens
        in a row have been shot.  Each level maintains a count of valid
        aliens, and a list of bombs in the air for it's aliens.
    '''
    row           = NumericProperty(0)
    min_col       = 0
    max_col       = 0
    count         = 0
    bombs         = []

    def __init__(self, Alien, row, **kwargs):
        super(Level, self).__init__(**kwargs)
        self.row = row
        for column in range(AliensPerRow):
            w = Alien(row, column, **kwargs)
            box = AlienBox(w, row, column)
            self.add_widget(box, -column)

    def checkState(self, bullets, dt):
        min_col, max_col = (None, None)
        count = 0
        self.bombs = []
        bullets = [bullet for bullet in bullets if self.collide_widget(bullet)]  # optimisation
        for vader in self.getAllVaders():
            if not vader.beenShot(bullets, dt):
                if min_col is None or min_col > vader.column: min_col = vader.column
                if max_col is None or max_col < vader.column: max_col = vader.column
                count = count + 1
            if vader.bomb is not None:
                self.bombs.append(vader.bomb)
        self.min_col, self.max_col = min_col, max_col
        self.count = count

    def step(self):
        for vader in self.getValidVaders():
            vader.incState()

    def gameOver(self):
        for vader in self.getValidVaders():
            vader.alpha = 0.3
            vader.invalid = True

    def switchPlayer(self, current):
        for vader in self.getAllVaders():
            vader.switchPlayer(current)

    def resetGame(self):
        for vader in self.getAllVaders():
            vader.invalid = vader.invalid1 = vader.invalid2 = False
            vader.alpha = 0

    def hideVaders(self):
        for vader in self.getValidVaders():
            vader.alpha = 0.3

    def showVaders(self):
        for vader in self.getValidVaders():
            vader.alpha = 1

    def getAllVaders(self):
        return (box.alien for box in self.children if box.alien is not None)

    def getValidVaders(self):
        return (vader for vader in self.getAllVaders() if not vader.invalid)

class Levels(BoxLayout):
    ''' A collection of levels is a BoxLayout containing Level instances.  This
        BoxLayout has a limited width and height, allowing the widget to be moved
        as a whole, first across the screen and then down when horizontal limits
        are reached.
        The speed of movement is controlled by the <velocity> which is calculated
        dynamically.  The <current> position determines where the invader grid appears
        and the <direction> determines horizontal direction.
        Each step (clock tick) adds the elapsed time to a counter, which is reset when
        the counter exceeds <maxDelta>.  When this occurs, we recalculate the position
        and redisplay the widget, causing all the invaders to move together.  This is
        slightly inconsistent with the original game.
        Whether or not a <ship> (UFO) is travelling across the screen is held in a variable,
        ensuring that no more than one UFO is on screen at any stage.  Ships are spawned randomly.
        The current position and direction of travel is stored per player, allowing us to
        easily switch between players.
        When there are <noMoreInvaders>, the level is restarted.
        The list of bombs is totalled for each individual level, and accessed for processing later.
    '''
    aliens         = [Alien0, Alien1, Alien2, Alien3, Alien4]

    velocity_x     = NumericProperty(5.0)
    velocity_y     = NumericProperty(23.0)
    velocity       = ReferenceListProperty(velocity_x, velocity_y)
    current_x      = NumericProperty(0)
    current_y      = NumericProperty(10)
    current        = ReferenceListProperty(current_x, current_y)
    direction      = NumericProperty(1)
    counter        = NumericProperty(0.0)
    maxDelta       = NumericProperty(0.5)
    bombs          = []
    ship           = None
    noMoreInvaders = False
    player1 = dict(x=0, y=10, direction=1)
    player2 = dict(x=0, y=10, direction=1)

    def __init__(self, **kwargs):
        super(Levels, self).__init__(**kwargs)
        for row in range(len(self.aliens)):
            w = Level(self.aliens[row], row, **kwargs)
            self.add_widget(w, -row)

    def calcVelocity(self):
        self.velocity_x = self.parent.width  / 160.0
        self.velocity_y = self.parent.height / 30.0

    def calcPos(self, current):
        current = Vector(current)
        dx, dy = current.x * self.velocity_x, current.y * self.velocity_y
        return Vector(dx, dy)+Vector(self.parent.pos)

    def resize(self):
        self.calcVelocity()
        self.pos = self.calcPos(self.current)
#        print("width=%s; height=%s" % (self.x, self.y))

    def speed(self, completion):
        return (1+completion)*self.direction

    def step(self, dt, levelsGap, bullets):
#        160 x 25 (parent in velocity units)
#        128 x 16 (invader grid)
#       If our current Y position starts at 25 - 16 = 9, then we iterate until that
#       position is zero (adjusted for max_row).
#       We can decrement Ypos only when we reach the sides (adjusted for max_col/min_col
#
        min_col, max_col = None, None
        count = 0
        self.bombs = []
        max_row = None
        for level in self.children:
            level.checkState(bullets, dt)
            count = count + level.count
            if level.min_col is not None:
                if min_col is None or min_col > level.min_col: min_col = level.min_col
            if level.max_col is not None:
                if max_col is None or max_col < level.max_col: max_col = level.max_col

            if min_col is not None and max_col is not None:
                if max_row is None or level.row > max_row:
                    max_row = level.row
            self.bombs.extend(level.bombs)  # building list of known valid bombs

        self.noMoreInvaders = False
        if min_col is None or max_col is None:
            self.noMoreInvaders = True
            return False   # Invaders are all shot up.  Restart level

        self.min_col, self.max_col = min_col, max_col
        self.counter = self.counter + dt

        if self.ship:
            if not self.ship.update(dt):
                self.ship = None
            else:
                for bullet in bullets:
                    if self.ship.beenShot(bullet):
                        self.ship = None  # already removed from parent
                        break
        else:
            if randint(0,10000) < 10:     # Do we spawn a ship? one in a thousand
                if randint(0,20) < 4:     # yes, which kind? big is 80% of the time
                    self.ship = lilShip(self.parent)
                else:
                    self.ship = bigShip(self.parent)
                self.parent.add_widget(self.ship)

        if self.counter > self.maxDelta:
            completion = 1-(count / (AliensPerRow*AlienRows+1.0))
            self.counter = 0

            invaderWidth  = self.width / AliensPerRow         #  invaders per level
            invaderHeight = self.height / AlienRows           #  invader row count

            min_pos = min_col * -invaderWidth    # adjust for invaders that have been shot
            max_pos = levelsGap + (AliensPerRow-1-max_col) * invaderWidth # width (40) + half spacing(20) = 50

            current = Vector(self.current)
            current = Vector(current.x+self.speed(completion), current.y)        # Add one to current
            pos = self.calcPos(current)                                 # Convert to position

            if pos.x > max_pos :
                self.direction = self.direction * -1                     # toggle direction
                current = Vector(current.x+self.speed(completion), current.y-1)  # Reduce Y
            if pos.x < min_pos:
                self.direction = self.direction * -1                     # toggle direction
                current = Vector(current.x+self.speed(completion), current.y-1)  # Reduce Y

            pos = self.calcPos(current)                                 # Convert to position
            self.current = current.x, current.y
            # Adjust the speed based on a few things
            sensitivity = 20                    # controls speedup for closeness to ground level
            factor=(sensitivity+current.y)/(sensitivity+25.0)
            self.maxDelta = 0.05 + 0.45 * (1-completion)   # speed depends on number of remaining aliens
            self.maxDelta = 0.05 + self.maxDelta * factor      # and closeness to completion

            self.pos = pos.x, pos.y
            for level in self.children:
                level.step()

            height_adj = (AlienRows-1-max_row) * (invaderHeight/self.velocity_y)

            if int(current.y + height_adj) < 0:
                return True  # Game over; invaders progressed past end
            else:
                ofs = int(completion * 4)
                speeds = ['fastinvader1', 'fastinvader2', 'fastinvader3', 'fastinvader4']
                soundFile = speeds[ofs]
                sound = Sounds[soundFile]
                if sound is not None:
                    sound.stop()
                    sound.play()
        return False

    def gameOver(self):
        self.maxDelta = 0.5
        for level in self.children:
            level.gameOver()

    def resetGame(self):
        self.maxDelta = self.maxDelta * 0.8
        self.direction = 1
        self.current = (0, 10)
        self.resize()
        self.player1 = dict(x=0, y=10, direction=1)
        self.player2 = dict(x=0, y=10, direction=1)
        self.calcVelocity()
        for level in self.children:
            level.resetGame()

    def switchPlayer(self, current):
        if current:
            p = self.player2
            self.player1 = dict(x=self.current_x, y=self.current_y, direction=self.direction)
            self.current_x, self.current_y, self.direction = p['x'],p['y'],p['direction']
        else:
            p = self.player1
            self.player2 = dict(x=self.current_x, y=self.current_y, direction=self.direction)
            self.current_x, self.current_y, self.direction = p['x'],p['y'],p['direction']
        self.calcVelocity()
        for level in self.children:
            level.switchPlayer(current)
    def hideVaders(self):
        for level in self.children:
            level.hideVaders()
    def showVaders(self):
        for level in self.children:
            level.showVaders()

class Fragment(Widget):
    ''' Houses/shields are broken down during the course of play by bombs dropping on them, or
        eventually, by aliens running all over them when they drop low enough. How to display
        this visually, and deal with collision tests efficiently becomes a rather big question.
        What we do, is map an 8x8 grid of 64 fragments over each house.  The alpha of each
        fragment is initially set to zero, so the fragment is not painted. The color is set to
        the same as the background colour of the game, so when the alpha is 1, it looks like
        there is a hole in the house.
        For collision tests, we first check if a bomb or bullet has collided with the house
        itself.  If so, we then proceed to perform collision tests for each of the 64
        fragments having zero alpha.  This approach means that we limit the number of overall
        collision tests, and are guaranteed a successful collision unless the alpha was non-zero.

        We maintain two sets of fragment alpha per house, one set per player.  So we don't actually
        duplicate the fragment to support two players, we only need to duplicate the alpha.
    '''
    alpha     = NumericProperty(0)
    alpha1    = 0
    alpha2    = 0
    current   = 0

    def collision_test(self, widget):
        if self.alpha < 1 and self.collide_widget(widget):
            self.alpha = 1   # blot out a part of the house
            return True
        return False
    def switchPlayer(self, current):
        if current:
            self.alpha1 = self.alpha
            self.alpha  = self.alpha2
        else:
            self.alpha2 = self.alpha
            self.alpha  = self.alpha1

    def reset(self):
        self.current = 0
        self.alpha = self.alpha1 = self.alpha2 = 0

class House(Graphic):
    ''' A house, or bunker, protects the player's shooter from bombs falling, and
        takes damage from both bullets and bombs, eventually losing it's protective
        capacity.
        See the comments for a Fragment for how this is implemented.
    '''
    sources   = ["atlas://images/vaders/house"]
    offset    = NumericProperty(0)
    fragments = ObjectProperty(None)

    def __init__(self, offset, **kwargs):
        super(House, self).__init__(**kwargs)
        self.offset = offset
        self.fragments = GridLayout()
        for r in range(64):
            self.fragments.add_widget(Fragment(), -r)
        self.fragments.rows, self.fragments.cols = (8,8)
        self.add_widget(self.fragments)

    def resize(self, dx):
        self.y = self.parent.y
        self.center_x = dx * self.offset
        self.fragments.center_x = self.center_x
        self.fragments.size = self.size
        self.fragments.y = self.y

    def collision(self, projectile):
        if projectile.expired: return False
        collided = False
        if self.collide_widget(projectile):         # if the projectile collides with the house
            for frag in self.fragments.children:    # only then would it collide with the fragments
                if frag.collision_test(projectile):
                    projectile.expired = True
                    return True
        return collided

    def checkAlienDamage(self, levels):
        damage = False
        for level in levels.children:
            if level.max_col is not None and level.min_col is not None:  # valid level
                if self.collide_widget(level):      # only test if level collides with house
                    for frag in self.fragments.children:
                        if frag.collision_test(level):
                            damage = True
        return damage

    def switchPlayer(self, current):
        for frag in self.fragments.children:
            frag.switchPlayer(current)

    def reset(self):
        for frag in self.fragments.children:
            frag.reset()

class Gun(Graphic):
    ''' A gun (or shooter) is a source of bullets.  We maintain a maximum of
        three bullets in the air at any given time.  These bullets are spawned
        at the current gun position, and travel vertically upward.
        Bullets expire after hitting either a house or an invader, or after
        travelling beyond a vertical limit.  When they hit and invader, bullets
        receive a positive score attribute which is added to a total before the
        bullet is removed from the game.  getPoints() clears this total, and
        is called just before adding to the player score.
        Guns are destroyed by bombs (<invalid> becomes True).
    '''
    sources = ["atlas://images/vaders/gun"]
    bullets = ListProperty([])
    lastPoint = None
    points = NumericProperty(0)
    invalid = False

    def fire(self, point):
        if self.lastPoint:  # Calc distance between mouse down and mouse up
            dx = self.lastPoint.x - point.x
            dy = self.lastPoint.y - point.y
            distance = sqrt(dx*dx + dy*dy)
            self.lastPoint = None
            if distance and distance > 3:
                return None   # Just moving the gun

        if len(self.bullets) < 3:
            bullet = Bullet()
            bullet.center_x = self.center_x
            bullet.y = self.y+self.height
            self.bullets.append(bullet)
            sound = Sounds['shoot']
            if sound is not None:
                sound.stop()
                sound.play()
            return bullet
        return None

    def resize(self):
        self.y = self.parent.y

    def collision(self, projectile):
        if projectile.expired: return False
        if self.collide_widget(projectile):
            sound = Sounds['explosion']
            if sound is not None:
                sound.stop()
                sound.play()
            projectile.expired = True
            self.alpha = 0.5
            return True
        return False

    def reset(self):
        self.alpha = 1
        self.invalid = True

    def touch_down(self, point):
        if not self.lastPoint: self.lastPoint = Vector(point.x,point.y)

    def move(self, point):
        self.center_x = point.x

    def getPoints(self):
        points = self.points
        self.points = 0
        return points

    def update(self, dt):
        for bullet in self.bullets:
            expired = bullet.update(dt)
            if expired:
                bullet.parent.remove_widget(bullet)
                self.points += bullet.points
        self.bullets = [b for b in self.bullets if not b.expired]

        if self.invalid:
            self.alpha = self.alpha - dt
            if self.alpha < 0:
                self.invalid = False
                self.alpha = 0
                self.x = 0
            return False
        if self.alpha < 1:
            self.alpha = self.alpha + dt
            if self.alpha > 1:
                self.alpha = 1
            return False
        return True

class Score(Widget):
    ''' We maintain a score for each player, and a high score which
        persists beyond the lifetime of the application.
    '''
    s1txt = StringProperty('0000')
    s2txt = StringProperty('0000')
    hstxt = StringProperty('0000')

    scores = ReferenceListProperty(s1txt, hstxt, s2txt)

    s1Score = NumericProperty(0)
    s2Score = NumericProperty(0)
    hiScore = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Score, self).__init__()
        self.hiScore = GlobalParams['HiScore']
        self.hstxt = "%04i" % self.hiScore

    def reset(self):
        self.s1Score = self.s2Score = 0
        self.s1txt = self.s2txt = '0000'
        if GlobalParams['SinglePlayer']:
            self.s2txt = ''

    def add(self, player, score):
        if score > 0:
            if player==0:
                score = self.s1Score = self.s1Score+score/2
                self.s1txt = "%04i" % self.s1Score
            else:
                score = self.s2Score = self.s2Score+score/2
                self.s2txt = "%04i" % self.s2Score
            if score > self.hiScore:
                self.hiScore = score
                GlobalParams['HiScore'] = score
                self.hstxt = "%04i" % self.hiScore

class LevelsBox(Widget):
    ''' The <Levels> BoxLayout which contains the aliens moves around within a LevelsBox
        parent.
        We adjust the size of <levels> to the width and height of the LevelsBox, to
        try to ensure that the game remains playable.  Mileage will vary- landscape
        orientation is pretty much required.
        <boxGap> is the relative size of the vertical and horizontal gap to the
        left and right or above/below the aliens grid.
    '''
    levels        = ObjectProperty(None)
    gapSize       = 4     # Multiplied by pixels per step to get box width/height
    boxHeight     = NumericProperty(40*AlienRows)
    boxWidth      = NumericProperty(40*AliensPerRow)
    boxGap        = NumericProperty(40*gapSize)
    hSteps        = 15     # Horizontal steps required
    vSteps        = 10     # vertical movement steps required

    def __init__(self, **kwargs):
        super(LevelsBox, self).__init__(**kwargs)
        self.levels  = Levels()
        self.add_widget(self.levels)
    def on_size(self, box, size):
        w, h = size
        self.boxGap      = self.gapSize * (w * 1.0 / self.hSteps + h * 1.0 / self.vSteps) / 2
        self.boxHeight   = AlienRows * self.boxGap / self.gapSize
        self.boxWidth    = w - self.boxGap
        self.levels.size = (self.boxWidth,  self.boxHeight)
        self.levels.resize()
    def reset(self):
        self.levels.resetGame()
    def step(self, dt, bullets):
        return self.levels.step(dt, self.boxGap, bullets)
    def hideVaders(self):
        self.levels.hideVaders()
    def showVaders(self):
        self.levels.showVaders()
    def noMoreInvaders(self):
        return self.levels.noMoreInvaders
    def switchPlayer(self, current):
        return self.levels.switchPlayer(current)

class GameOver(AnchorLayout):
    alpha = NumericProperty(0)

class GetReady(AnchorLayout):
    alpha = NumericProperty(0)

class HousesBox(Widget):
    ''' This widget contains four houses or bunkers, and defines
        the positioning for the house widgets.
    '''
    def on_size(self, box, size):
        w, h = size #@UnusedVariable
        dx = w / 5
        for house in self.children:
            house.resize(dx)

class ShooterBox(Widget):
    ''' The shooter moves within the bounds of this box.
    '''
    def on_size(self, box, size):
        for shooter in self.children:
            shooter.resize()

class FooterBox(Widget):
    '''  The footer shows the number of shooters left for either player
    '''
    def __init__(self, **kwargs):
        super(FooterBox, self).__init__(**kwargs)

class GunList(FloatLayout):
    ''' A gun layout displays a list of <nShooters> shooters, positioned either
        to the left or to the right depending on the player
    '''
    nShooters = NumericProperty(0)
    gunLayout = ObjectProperty(None)

    def setShooters(self, nShooters):
        self.nShooters = nShooters
        for gun in self.gunLayout.children[:]:
            self.gunLayout.remove_widget(gun)
        for n in range(self.nShooters):
            self.gunLayout.add_widget(Gun(), n)

class Invaders(Widget):
    ''' The main application.  We try to reproduce the original game of Space Invaders.
    '''
    scores        = ObjectProperty(None)

    levelsBox    = ObjectProperty(None)
    housesBox    = ObjectProperty(None)
    shooterBox   = ObjectProperty(None)
    footerBox    = ObjectProperty(None)

    house1  = ObjectProperty(None)
    house2  = ObjectProperty(None)
    house3  = ObjectProperty(None)
    house4  = ObjectProperty(None)
    houses  = ReferenceListProperty(house1, house2, house3, house4)

    gun     = ObjectProperty(None)

    leftGunList  = ObjectProperty(None)
    rightGunList = ObjectProperty(None)

    players       = ReferenceListProperty(leftGunList, rightGunList)

    currentPlayer = 0
    gameOver      = None
    getReady      = None

    def __init__(self, **kwargs):
        super(Invaders, self).__init__(**kwargs)

        self.gun = Gun()
        self.shooterBox.add_widget(self.gun)

        self.house1 = House(1)
        self.house2 = House(2)
        self.house3 = House(3)
        self.house4 = House(4)
        for house in self.houses:
            self.housesBox.add_widget(house)
        self.reset()

    def switchPlayer(self):
        nPlayers = 1 if GlobalParams['SinglePlayer'] else 2
        if nPlayers > 1:
            self.currentPlayer = (self.currentPlayer + 1) % nPlayers
            self.levelsBox.switchPlayer(self.currentPlayer)
            for house in self.houses:
                house.switchPlayer(self.currentPlayer)
        return self.players[self.currentPlayer]

    def on_touch_move(self, touch):
        self.gun.move(touch)

    def on_touch_down(self, touch):
        self.gun.touch_down(touch)

    def on_touch_up(self, touch):
        bullet = self.gun.fire(touch)
        if bullet: self.add_widget(bullet)

    def setGunCount(self):
        gunCount = GlobalParams['GunCount']
        self.leftGunList.setShooters(gunCount)
        if GlobalParams['SinglePlayer']:
            self.rightGunList.setShooters(0)
        else:
            self.rightGunList.setShooters(gunCount)

    def reset(self):
        self.levelsBox.reset()
        self.gun.reset()
        self.scores.reset()
        for house in self.houses: house.reset()
        self.currentPlayer = 0
        self.setGunCount()
        self.ready()

    def ready(self):
        if self.getReady is not None:
            return
        self.getReady = GetReady()
        self.getReady.pos = 0,0
        self.getReady.size = self.width, self.height
        self.add_widget(self.getReady)
        self.levelsBox.hideVaders()
        anim = Animation(alpha=1, duration=GlobalParams['ReadyDelay'])
        anim.start(self.getReady)
        saveGlobalParams()

    def restartGame(self):
        if self.gameOver is not None:
            return
        self.levelsBox.levels.gameOver()
        self.gameOver = GameOver()
        self.gameOver.pos = 0,0
        self.gameOver.size = self.width, self.height
        self.add_widget(self.gameOver)
        self.levelsBox.hideVaders()
        anim = Animation(alpha=1, duration=GlobalParams['RestartDelay'])
        anim.start(self.gameOver)
        saveGlobalParams()

    def on_size(self, box, sz):
        if self.getReady is not None:
            self.getReady.pos = 0,0
            self.getReady.size = self.width, self.height
        if self.gameOver is not None:
            self.gameOver.pos = 0,0
            self.gameOver.size = self.width, self.height

    def update(self, dt):
        ''' We come here quite often- around once every 12th of a second, with the
            elapsed time in <dt>.

            This is a sort of finite state machine, with the processing done here
            dependent on the state of the game:
                If the game is over, we reset the game
                Else, if we are ready for the new game,
                    call gun.update;
                    if true,
                        we were bombed:
                            invalidate all further bombs
                            return  (carries on with re-entry)
                    gameOver = value of Restarting
                    reset[Restarting]
                    With all bombs
                        update bomb
                        if the bomb collided with shooter
                            switch player
                            if no player guns left
                                switch player
                                if no player guns left
                                    gameOver is true
                            if gameOver is not true
                                init ready sequence for continuation
                        else bomb did not collide
                            for each house,
                                if the bomb collided with the house,
                                    expire the bomb
                    With all houses
                        with all bullets
                            if bullet collided with the house,
                                expire the bullet
                        check if aliens collided with the house
                    if the game is not over
                        if levels step returned true, the aliens reached the bottom
                            set player shooter count to zero
                            switch player
                            if no player shooters remain
                                gameOver
                    if gameOver
                        restart the game
                    else if all the invaders have been shot
                        increment the number of shooters
                        restart the level
        '''
        player = self.players[self.currentPlayer]
        if self.gameOver is not None:
            if self.gameOver.alpha==1:
                self.remove_widget(self.gameOver)
                self.gameOver = None
                self.reset()
            return
        if self.getReady is not None:
            if self.getReady.alpha==1:
                self.remove_widget(self.getReady)
                self.getReady = None
#                self.levelsBox.showVaders()
                player.setShooters(player.nShooters - 1)

        if not self.gun.update(dt):
            for bomb in self.levelsBox.levels.bombs:
                bomb.expired = True
            return

        gameOver = False
        if (GlobalParams['Restarting']):
            GlobalParams['Restarting'] = False
            gameOver = True

        self.scores.add(self.currentPlayer, self.gun.getPoints())

        for bomb in self.levelsBox.levels.bombs:
            bomb.update(dt)
            if not bomb.expired:
                if self.gun.collision(bomb):
                    player = self.switchPlayer()
                    if player.nShooters == 0:
                        player = self.switchPlayer()
                        if player.nShooters == 0:
                            gameOver = True
                    if not gameOver:
                        self.ready()
                        self.gun.reset()
                else:
                    for house in self.houses:
                        if house.collision(bomb):
                            bomb.expired = True

        for house in self.houses:
            for bullet in self.gun.bullets:
                if house.collision(bullet):
                    bullet.expired = True
            house.checkAlienDamage(self.levelsBox.levels)

        if not gameOver and self.levelsBox.step(dt, self.gun.bullets):
            player.setShooters(0)
            player = self.switchPlayer()
            if player.nShooters==0:
                gameOver = True
        if gameOver:
            self.restartGame()
        elif self.levelsBox.noMoreInvaders():
            ''' Restart level, increment retries '''
            self.levelsBox.reset()
            self.gun.reset()
            for house in self.houses: house.reset()
            player = self.players[self.currentPlayer]
            player.setShooters(player.nShooters + 2)
            self.ready()

class SIApp(App):
    icon = 'images/icon.png'
    title = 'Space Invaders!'

    def synchGlobalParams(self, config):
        GlobalParams['config']       = config
        GlobalParams['SinglePlayer'] = config.getint('Invaders', 'SinglePlayer')
        GlobalParams['HiScore']      = config.getint('Invaders', 'HiScore')
        GlobalParams['GunCount']     = config.getint('Invaders', 'GunCount')
        GlobalParams['ReadyDelay']   = config.getfloat('Invaders', 'ReadyDelay')
        GlobalParams['RestartDelay'] = config.getfloat('Invaders', 'RestartDelay')

    def build_config(self, config):
        config.setdefaults('Invaders',
                           {'SinglePlayer': 1,
                            'HiScore': 0,
                            'Restarting': 0,
                            'GunCount': 4,
                            'ReadyDelay': 3.0,
                            'RestartDelay':5.0})
        try:
            config.read(self.get_application_config())
        finally:
            self.synchGlobalParams(config)
    def build_settings(self, settings):
        settings.add_json_panel('Space Invaders', self.config, data='''[
            { "type": "bool", "title": "Single Player",
              "desc": "Off for alternating players",
              "section": "Invaders", "key": "SinglePlayer" },
            { "type": "numeric", "title": "Gun Count",
              "desc": "Number of guns to start with",
              "section": "Invaders", "key": "GunCount" },
            { "type": "numeric", "title": "Ready Delay",
              "desc": "How long to wait for new guns (seconds)",
              "section": "Invaders", "key": "ReadyDelay"
            },
            { "type": "numeric", "title": "Restart Delay",
              "desc": "Delay between game restarts (seconds)",
              "section": "Invaders", "key": "RestartDelay"
            }
        ]''')

    def on_config_change(self, config, section, key, value):
        print("setting %s to %s" % (key, value))
        GlobalParams[key] = value
        saveGlobalParams()
        GlobalParams['Restarting'] = True

    def on_stop(self):
        saveGlobalParams()

    def on_pause(self):
        ''' Used on Android to indicate the app has been paused '''
        return True

    def on_resume(self):
        ''' The application has been resumed '''
        pass

    def build(self):
        GlobalParams['Restarting'] = False
        game = Invaders()
        Clock.schedule_interval(game.update, 5.0/60.0)
        return game

if __name__ == '__main__':
    SIApp().run()
