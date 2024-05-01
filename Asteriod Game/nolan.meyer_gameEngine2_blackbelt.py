import pygame,simpleGE,random
"""
Extension of previous asteriod
game. In this game the space
movement is more realistic
to real space. You can also
shoot bullets at angles. Don't
let the earth get hit three times.
Your spaceship also has three health.
Get a score of 50 and you win!

Spaceship Image: https://opengameart.org/content/spaceship-8
Thruster Image: https://opengameart.org/content/lpc-flames
Spaceship with thrusters: Created and edited by me
Asteriod Image:  https://opengameart.org/content/brown-asteroid
Space Background: https://opengameart.org/content/space-bg-planets
Game Over Image: https://pngimg.com/image/83334
Earth Image: https://opengameart.org/content/earth
Explosion Image: https://opengameart.org/content/pixel-explosion-12-frames
Laser Bullets Image: https://opengameart.org/content/bullet-collection-1-m484
Trophy: https://www.vecteezy.com/png/9315016-winner-trophy-in-flat-style
Explosion Sound: https://opengameart.org/content/explosion-0
Game over Sound: https://opengameart.org/content/lose-game-short-music-clip
Laser Sound: https://opengameart.org/content/shots
Win and lose life Sound: https://opengameart.org/content/oldschool-win-and-die-jump-and-run-sounds

Nolan Meyer

November 6, 2023
"""
#Game class that sets up the playground
class Game(simpleGE.Scene):

    def __init__(self):
        super().__init__()

        #Set up background
        self.setCaption("Asteriod Game 2")
        self.background = pygame.image.load("spaceBackground.png")
        self.background = self.background.convert_alpha()
        self.background = pygame.transform.scale(self.background,((self.screen.get_size())))

        #Create asteriod,spaceship, bullet
        self.spaceship = Spaceship(self)

        self.asteriod = Asteriod(self)
        
        self.bullet = Bullet(self)

        #Score Label
        self.scoreLabel = simpleGE.Label()
        self.scoreLabel.text = "Score: 0"
        self.scoreLabel.bgColor = (0,0,0)
        self.scoreLabel.fgColor = (255,255,255)
        self.scoreLabel.center = (50,20)
        self.score = 0

        #Spaceship health bar
        self.spaceshipHeart1 = simpleGE.SuperSprite(self)
        self.spaceshipHeart1.setImage("spaceship_heart.png")
        self.spaceshipHeart1.setSize(30,30)
        self.spaceshipHeart1.setBoundAction(self.spaceshipHeart1.CONTINUE)
        self.spaceshipHeart1.x = 530
        self.spaceshipHeart1.y = 20

        self.spaceshipHeart2 = simpleGE.SuperSprite(self)
        self.spaceshipHeart2.setImage("spaceship_heart.png")
        self.spaceshipHeart2.setSize(30,30)
        self.spaceshipHeart2.setBoundAction(self.spaceshipHeart2.CONTINUE)
        self.spaceshipHeart2.x = 565
        self.spaceshipHeart2.y = 20

        self.spaceshipHeart3 = simpleGE.SuperSprite(self)
        self.spaceshipHeart3.setImage("spaceship_heart.png")
        self.spaceshipHeart3.setSize(30,30)
        self.spaceshipHeart3.setBoundAction(self.spaceshipHeart3.CONTINUE)
        self.spaceshipHeart3.x = 600
        self.spaceshipHeart3.y = 20

        #Earth image that can't be hit
        self.earth = simpleGE.BasicSprite(self)
        self.earth.setImage("earth.png")
        self.earth.setSize(300,300)
        self.earth.x = 300
        self.earth.y = 480

        #Earth health bar
        self.earthHealth = 3
        self.earthHealth1 = simpleGE.SuperSprite(self)
        self.earthHealth1.setImage("earth.png")
        self.earthHealth1.setSize(30,30)
        self.earthHealth1.setBoundAction(self.earthHealth1.CONTINUE)
        self.earthHealth1.x = 530
        self.earthHealth1.y = 60

        self.earthHealth2 = simpleGE.SuperSprite(self)
        self.earthHealth2.setImage("earth.png")
        self.earthHealth2.setSize(30,30)
        self.earthHealth2.setBoundAction(self.earthHealth2.CONTINUE)
        self.earthHealth2.x = 565
        self.earthHealth2.y = 60

        self.earthHealth3 = simpleGE.SuperSprite(self)
        self.earthHealth3.setImage("earth.png")
        self.earthHealth3.setSize(30,30)
        self.earthHealth3.setBoundAction(self.earthHealth3.CONTINUE)
        self.earthHealth3.x = 600
        self.earthHealth3.y = 60

        #Explosion Image
        self.explosion = simpleGE.SuperSprite(self)
        self.explosion.setImage("explosion.png")
        self.explosion.setBoundAction(self.explosion.CONTINUE)
        self.explosion.setSize(50,50)
        self.explosion.x = -150
        self.explosion.y = -150

        #Game over image
        self.gameOver = simpleGE.SuperSprite(self)
        self.gameOver.setImage("gameOver.png")
        self.gameOver.setBoundAction(self.gameOver.CONTINUE)
        self.gameOver.x = -150
        self.gameOver.y = -150
        self.gameOver.setSize(200,200)

        #Win image
        self.win = simpleGE.SuperSprite(self)
        self.win.setImage("win.png")
        self.win.setSize(200,200)
        self.win.setBoundAction(self.win.CONTINUE)
        self.win.x = -150
        self.win.y = -150

        #Game over and win sounds
        self.winSound = simpleGE.Sound("round_end.wav")
        self.gameOverSound = simpleGE.Sound("gameOverSoud.wav")
        self.playSoundTimes = 1

        #Restart button
        self.restartButton = simpleGE.Button()
        self.restartButton.center = (320,375)
        self.restartButton.text = "Restart"
        self.restartButton.fgColor = (0,0,0)
        self.restartButton.bgColor = (225,225,0)
        self.restartButton.hide()

        #Quit button
        self.quitButton = simpleGE.Button()
        self.quitButton.center = (320,420)
        self.quitButton.text = "Quit"
        self.quitButton.fgColor = (0,0,0)
        self.quitButton.bgColor = (225,225,0)
        self.quitButton.hide()

        #Starting label/button that gives instructions
        self.startButton = simpleGE.MultiLabel()
        self.startButton.textLines =  ["Don't let earth get hit 3 times",
                          "Don't let spaceship get hit 3 times",
                          "shoot the asteriods and score 50 to win",
                          "Use the arrows to move, and SPACE to shoot",
                          "Click me to start! Have fun!"]
        self.startButton.center = ((325,240))
        self.startButton.size = ((500,200))
        self.startButton.fgColor = (0,0,0)
        self.startButton.bgColor = (225,225,0)

        self.sprites = [self.earth,self.scoreLabel,self.spaceshipHeart1,self.spaceshipHeart2,self.spaceshipHeart3,self.spaceship,self.asteriod,
                        self.earthHealth1,self.earthHealth2,self.earthHealth3,self.bullet,self.explosion,self.win,self.gameOver,self.restartButton,
                        self.quitButton,self.startButton]
    
    #Checks for buttons being clicked
    def update(self):
        """
        Checks if the start,quit, or restart
        button is clicked.
        """

        if self.quitButton.clicked:
            
            self.stop()
        
        if self.restartButton.clicked:

            self.spaceship.canMove = True
            self.spaceship.x = 300
            self.spaceship.y = 300
            
            self.asteriod.fall = True

            self.win.x = -100
            self.win.y = -100

            self.gameOver.x = -100
            self.gameOver.y = -100

            self.explosion.x = -100
            self.explosion.y = -100

            self.earthHealth = 3

            self.earthHealth1.x = 530
            self.earthHealth1.y = 60

            self.earthHealth2.x = 565
            self.earthHealth2.y = 60

            self.earthHealth3.x = 600
            self.earthHealth3.y = 60

            self.spaceship.health = 3

            self.spaceshipHeart1.x = 530
            self.spaceshipHeart1.y = 20

            self.spaceshipHeart2.x = 565
            self.spaceshipHeart2.y = 20

            self.spaceshipHeart3.x = 600
            self.spaceshipHeart3.y = 20

            self.restartButton.hide()
            self.quitButton.hide()

            self.scoreLabel.text = "Score: 0"
            self.score = 0

            self.playSoundTimes = 1
        
        if self.startButton.clicked:

            self.spaceship.canMove = True
            self.asteriod.fall = True
            self.startButton.hide()


#Spaceship class
class Spaceship(simpleGE.SuperSprite):
    
    def __init__(self,scene):
        super().__init__(scene)
        self.images = {
            
            "off_thruster": pygame.image.load("spaceship.png"),
            "all_thrusters": pygame.image.load("spaceship_allThrusters.png"),
            "left_thrusters": pygame.image.load("spaceship_leftThrusters.png"),
            "right_thrusters": pygame.image.load("spaceship_rightThrusters.png")
        }
        self.imageMaster = self.images["off_thruster"]
        self.sound = simpleGE.Sound("death.wav")
        self.setSpeed(0)
        self.setAngle(0)
        self.x = 300
        self.y = 300
        self.health = 3
        self.setAngle(90)
        self.canMove = False

    def checkEvents(self):
        """
        Checks if the spaceship can moved. If it can based
        off what buttons they click it will set that to certain
        images, rotate it, and add forces. Also checks for if you
        want to shoot a bullet, and runs the checkHealth, checkEarthHealth,
        and checkScore methods. 
        """

        if self.canMove:

            self.imageMaster = self.images["off_thruster"]
            if self.scene.isKeyPressed(pygame.K_LEFT):
                self.rotateBy(5)
                self.imageMaster = self.images["right_thrusters"]
            
            if self.scene.isKeyPressed(pygame.K_RIGHT):
                self.rotateBy(-5)
                self.imageMaster = self.images["left_thrusters"]

            if self.scene.isKeyPressed(pygame.K_UP):
                self.addForce(.2, self.rotation)
                self.imageMaster = self.images["all_thrusters"]

            if self.scene.isKeyPressed(pygame.K_SPACE):

                self.scene.bullet.shoot()

        
        self.checkHealth()
        self.checkEartHealth()
        self.checkScore()
    
   
    def checkHealth(self):
        """
        Checks what health the spaceship is at 
        and moves the health images off the screen
        based off how many hearts you have. 
        """

        if self.health == 2:
            self.scene.spaceshipHeart1.x = -100
            self.scene.spaceshipHeart1.y = -100
        
        if self.health == 1:
            self.scene.spaceshipHeart2.x = -100
            self.scene.spaceshipHeart2.y = -100
        
        if self.health == 0:
            self.scene.spaceshipHeart3.x = -100
            self.scene.spaceshipHeart3.y = -100
            self.scene.asteriod.fall = False
            self.scene.spaceship.canMove = False
            self.scene.spaceship.setDX(0)
            self.scene.spaceship.setDY(0)
            self.scene.gameOver.x = 320
            self.scene.gameOver.y = 240
            self.scene.restartButton.show((320,375))
            self.scene.quitButton.show((320,420))

            if self.scene.playSoundTimes == 1:
                self.scene.gameOverSound.play()
                self.scene.playSoundTimes += 1 

    
    def checkEartHealth(self):
        """
        Checks what the earth's health is at 
        and moves the health images off how many
        times the earth has been hit.
        """
        

        if self.scene.earthHealth == 2:

            self.scene.earthHealth1.x = -100
            self.scene.earthHealth1.y = -100
        
        if self.scene.earthHealth == 1:

            self.scene.earthHealth2.x = -100
            self.scene.earthHealth2.y = -100
        
        if self.scene.earthHealth == 0:

            self.scene.earthHealth3.x = -100
            self.scene.earthHealth3.y = -100
            self.scene.asteriod.fall = False
            self.scene.spaceship.canMove = False
            self.scene.spaceship.setDX(0)
            self.scene.spaceship.setDY(0)
            self.scene.gameOver.x = 320
            self.scene.gameOver.y = 240
            self.canMove = False
            self.scene.restartButton.show((320,375))
            self.scene.quitButton.show((320,420))

            if self.scene.playSoundTimes == 1:
                self.scene.gameOverSound.play()
                self.scene.playSoundTimes += 1
        
    def checkScore(self):
        """
        Checks what the score is and ends the game
        if it is equal to 50. 
        """

        if self.scene.score == 50:
            self.scene.win.x = 320
            self.scene.win.y = 240
            self.canMove = False
            self.scene.asteriod.fall = False
            self.scene.restartButton.show((320,375))
            self.scene.quitButton.show((320,420))
            self.scene.spaceship.setDX(0)
            self.scene.spaceship.setDY(0)
            
            if self.scene.playSoundTimes == 1:
                self.scene.winSound.play()
                self.scene.playSoundTimes += 1



#Class that controls the asteriod 
class Asteriod(simpleGE.BasicSprite):

    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("asteroid.png")
        self.setSize(30,30)
        self.fall = False
        self.sound = simpleGE.Sound("explosion.wav")
        self.reset()

    
    def reset(self):
        """
        Resets the asteriod's x,y, and fallSpeed.
        """
        self.x = random.randint(0,640)
        self.y = 20
        self.fallSpeed = 5


    def checkEvents(self):
        """
        If the asteriod can fall subtract the Y
        from the fall speed allowing it to fall
        and check for collision. 
        """

        if self.fall == True:
            self.y += self.fallSpeed
        
        self.checkCollision()

    
    def checkCollision(self):
        """
        Checks if the asteriod collides with the 
        spaceship 
        """

        if self.collidesWith(self.scene.spaceship):
            self.scene.spaceship.health -= 1
            self.scene.spaceship.sound.play()
            self.reset()
        
        if self.collidesWith(self.scene.earth):
                self.scene.earthHealth -= 1
                self.scene.spaceship.sound.play()
                self.reset()

    def checkBounds(self):
        """
        If the asteriod is off the screen it resets it.
        """

        if self.rect.bottom > self.scene.background.get_height():
            self.reset()


#Bullet Class that allows you to shoot
class Bullet(simpleGE.SuperSprite):

    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("bullet2.png")
        self.setSize(30,15)
        self.x = -100
        self.y = -100
        self.rotateBy(self.scene.spaceship.rotation)
        self.reset()
        self.setBoundAction(self.HIDE)
        self.sound = simpleGE.Sound("laserSound.wav")
        

    def shoot(self):
        """
        Shoots the bullet by first checking if hte bullet is off the screen.
        If it is it will play the fire sound, set the position to the spaceships
        position. Set the speed to 10, and lastly, set the rotation angle to the
        spacehsips rotation angle. 
        """
        
        if self.x < 0:
            if self.y < 0:
                self.sound.play()
                self.setPosition((self.scene.spaceship.x,self.scene.spaceship.y))
                self.setSpeed(10)
                self.setAngle(self.scene.spaceship.rotation)
                
            
    def reset(self):
        """
        Resets the bullet by settings is position off the screen,
        and setting its speed to zero. 
        """
        self.setPosition((-100,-100))
        self.setSpeed(0)

    def checkEvents(self):
        """
        Runs the collision checker 30 times
        every frame. 
        """

        self.checkCollision()
    
    def checkCollision(self):
        """
        Checks if the bullet collides with something. If it 
        does it will reset the bullet, put an explosion image
        to where the collision took place, and update the score. 
        """

        if self.collidesWith(self.scene.asteriod):
            self.scene.explosion.x = self.scene.asteriod.x
            self.scene.explosion.y = self.scene.asteriod.y
            self.scene.asteriod.sound.play()
            self.scene.asteriod.reset()
            self.reset()
            self.scene.score += 10
            self.scene.scoreLabel.text = f"Score: {self.scene.score}"




#Main that controls create the instance of the game and runs the code
def main():

    scene = Game()
    scene.start()

#Calls main
if __name__ == "__main__":
    main()
                                      