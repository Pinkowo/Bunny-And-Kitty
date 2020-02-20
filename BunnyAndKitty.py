import pyxel
from enum import Enum, unique, auto

bul_num=15
bul_dis=62
bul_speed=1.8

way = [8,32,56,80,104]

@unique
class GameState(Enum):
    INIT = auto()
    START = auto()
    KITTY_WON = auto()
    BUNNY_WON = auto()

class App:
    def __init__(self):
        self.play_music = True
        self.state = GameState.INIT
        self.bunny_speed=2
        self.bunny_y=56
        self.kitty_y=56
        self.kitty_x=150
        
        self.bullet_x = [10]*bul_num
        self.bullet_y = [11]*bul_num
        self.bul_act=[False]*bul_num
        
        pyxel.init(160, 120, caption="Bunny and Kitty")
        pyxel.load("asset/bg.pyxres")
        pyxel.run(self.update, self.draw)
       

    def update(self):       
        if pyxel.btnp(pyxel.KEY_L): #Leave
            pyxel.quit()
                       
        if self.state == GameState.START:
            self.update_bunny()
            self.update_kitty()
            self.update_bullet()
            
        if self.kitty_x <= 25:
            self.state = GameState. KITTY_WON
            if self.play_music == True:
               pyxel.play(0,4,loop=False) 
               self.play_music = False
           
        for i in range(bul_num):
            if (self.bullet_x[i] >= self.kitty_x-5 and self.bullet_x[i] <= self.kitty_x+5) and (self.bullet_y[i] == self.kitty_y+3):
                self.state = GameState.BUNNY_WON
                if self.play_music == True:
                    pyxel.play(0,4,loop=False) 
                    self.play_music = False
                
        if pyxel.btnp(pyxel.KEY_SPACE) and (self.state != GameState.START):
            self.state = GameState.START
            self.bunny_y=56
            self.kitty_y=56
            self.kitty_x=150            
            self.bullet_x = [10]*bul_num
            self.bullet_y = [11]*bul_num
            self.bul_act=[False]*bul_num
            self.play_music = True
            
 
#############################################################
    def update_kitty(self):
        if pyxel.btnr(pyxel.KEY_UP):
            pyxel.play(1,1,loop=False)
            self.kitty_y = max(self.kitty_y - 24, 8)

        if pyxel.btnr(pyxel.KEY_DOWN):
            pyxel.play(1,2,loop=False)
            self.kitty_y = min(self.kitty_y + 24, 104)
            
        if pyxel.btn(pyxel.KEY_LEFT):
            self.kitty_x -= 1
#############################################################
    def update_bunny(self):
        if pyxel.btn(pyxel.KEY_W):
            self.bunny_y = max(self.bunny_y - self.bunny_speed, 6)

        if pyxel.btn(pyxel.KEY_S):
            self.bunny_y = min(self.bunny_y + self.bunny_speed, 104)
#############################################################
    def update_bullet(self):
        for i in range(5):
    #first bullet
            if self.bullet_x[i] > 160:
                self.bul_act[i] = False
            if  self.bunny_y ==  way[i] and self.bul_act[i] == False and self.bul_act[i+10] == True and self.bullet_x[i+10] >= bul_dis:
                self.bullet_reset(i,i)
            elif self.bunny_y ==  way[i] and self.bul_act[i] == False and self.bul_act[i+10] == False:
                self.bullet_reset(i,i)
            if self.bul_act[i] == True:
                self.bullet_x[i] += bul_speed
    #second bullet            
            if  self.bul_act[i+5] == False and self.bul_act[i] == True and self.bunny_y ==  way[i] and self.bullet_x[i] >= bul_dis :
                self.bullet_reset(i+5,i)
            if self.bul_act[i+5] == True:
                self.bullet_x[i+5] += bul_speed
            if self.bullet_x[i+5] > 160:
                self.bul_act[i+5] = False
                
    #third bullet
            if  self.bul_act[i+10] == False and self.bul_act[i+5] == True and self.bunny_y ==  way[i] and self.bullet_x[i+5] >= bul_dis :
                self.bullet_reset(i+10,i)
            if self.bul_act[i+10] == True:
                self.bullet_x[i+10] += bul_speed
            if self.bullet_x[i+10] > 160:
                self.bul_act[i+10] = False
            
            
    def bullet_reset(self,i,way_num):
        pyxel.play(0,0,loop=False)
        if way_num >= 5:
            way_num = way_num - 5 
        self.bullet_x[i] = 10     
        self.bullet_y[i] = way[way_num]+3
        self.bul_act[i]=True
##############################################################  
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 0, 160, 120)
        pyxel.blt(5, self.bunny_y, 2, 0, 0, 8, 11,6)
        pyxel.blt(self.kitty_x, self.kitty_y, 1, 0, 0, 8, 9,6)
        
        for i in range(bul_num):
            if self.bul_act[i] == True:
                pyxel.blt(self.bullet_x[i], self.bullet_y[i], 2, 16, 0, 23, 5,6)
                
        if self.state == GameState.INIT:
            pyxel.rect(30, 30, 100, 60, 3)
            pyxel.rectb(30, 30, 100, 60, 11)
            pyxel.text(50, 50, "Bunny And Kitty", 7)
            pyxel.text(41, 70, "Press Space To Start", 11)
            
        if self.state == GameState.KITTY_WON:
            pyxel.rect(30, 30, 100, 60, 4)
            pyxel.rectb(30, 30, 100, 60, 9)
            pyxel.text(60, 50, "Kitty Win", 7)
            pyxel.text(36, 70, "Press Space To Restart", 9)
            
        if self.state == GameState.BUNNY_WON:
            pyxel.rect(30, 30, 100, 60, 8)
            pyxel.rectb(30, 30, 100, 60, 14)
            pyxel.text(60, 50, "Bunny Win", 7)
            pyxel.text(36, 70, "Press Space To Restart", 14)
            
        

        
App()