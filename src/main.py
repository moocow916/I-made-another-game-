import pygame
from random import randint
from math import floor
 
class Dolla:
    def __init__(self):
        pygame.init()
 
        self.load_images()
 
        self.window_width = 1280
        self.window_height = 720
        self.window = pygame.display.set_mode((self.window_width,self.window_height))
        pygame.display.set_caption("C.R.E.A.M")
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.SysFont("Arial", 40)
        self.timer_font = pygame.font.SysFont("Arial", 120)
 
        self.game_state = "menu"        
 
        self.new_game()
 
        self.main_loop()
 
    def new_game(self):
         
 
        self.start_ticks=pygame.time.get_ticks() #restart timer
 
        self.robot_x = self.window_width/2-self.images[3].get_width()/2
        self.robot_y = self.window_height/2-self.images[3].get_height()/2
                        
        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False
 
        self.robot_speed = 5
 
        self.spawn_left = [0,self.window_height/2-self.images[1].get_height()/2]
        self.spawn_right = [self.window_width-self.images[1].get_width(),self.window_height/2-self.images[1].get_height()/2]
 
        self.monsters_count = 0
        self.monsters_list = []
        self.monsters_speed = 3
        
 
        self.spawn_coin()
 
        
 
    def load_images(self):
        self.images = []
        for name in ["coin","door","monster","robot"]:
            self.images.append(pygame.image.load(name + ".png"))
 
    def main_loop(self):
        while True:
            self.seconds= 10-floor(self.monsters_count/5)-((pygame.time.get_ticks()-self.start_ticks)/1000) # timer starts at 10, reduces by 1 every 5 points
            if self.seconds <= 0 and self.game_state == "active":
                self.game_state = "dead"
            self.check_events()
            self.draw_window()
 
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True
                if event.key == pygame.K_SPACE:
                    self.new_game()
                    self.game_state = "active"                   
 
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False
                if event.key == pygame.K_UP:
                    self.to_up = False
 
            if event.type == pygame.QUIT:
                exit()
                
 
    def draw_window(self):
 
        self.window.fill((255,255,255))
 
        if self.game_state == "active":
 
            self.coin_collision()
            self.monster_collision()
            self.move_monsters()
            self.move_robot()
 
            score_text = self.score_font.render(f"Current Score: {self.monsters_count}",True,(255,0,0))
            time_text = self.timer_font.render(f"{int(self.seconds)}",True,(255,0,0))
            self.window.blit(score_text,(0,0))
            self.window.blit(time_text,((self.window_width/2)-(time_text.get_width()/2),(self.window_height/2)-time_text.get_height()/2))
 
 
            self.window.blit(self.images[1],(self.spawn_left[0],self.spawn_left[1])) #draw door
            self.window.blit(self.images[1],(self.spawn_right[0],self.spawn_right[1])) #draw door
            self.window.blit(self.images[3],(self.robot_x,self.robot_y)) #draw robot
            for i in range(self.monsters_count): #draw monsters
                self.window.blit(self.images[2],(self.monsters_list[i][0],self.monsters_list[i][1]))
            self.window.blit(self.images[0],(self.coin_x, self.coin_y))  #draw coin
        
        if self.game_state == "menu":
            menu_text = self.timer_font.render("Press SPACE To Begin!",True,(255,0,0))
            self.window.blit(menu_text,((self.window_width/2)-(menu_text.get_width()/2),(self.window_height/2)-menu_text.get_height()/2))
 
        if self.game_state == "dead":
            if self.monsters_count == 1:
                menu_text = self.timer_font.render(f"You got {self.monsters_count} point!",True,(255,0,0))
            else:
                menu_text = self.timer_font.render(f"You got {self.monsters_count} points!",True,(255,0,0))
            self.window.blit(menu_text,((self.window_width/2)-(menu_text.get_width()/2),(self.window_height/2)-menu_text.get_height()))
            menu_text = self.timer_font.render(f"Press SPACE To Try Again!",True,(255,0,0))
            self.window.blit(menu_text,((self.window_width/2)-(menu_text.get_width()/2),(self.window_height/2)))
        pygame.display.flip()
 
        self.clock.tick(60)
        
    def move_robot(self):
        if self.to_right:
            self.robot_x += self.robot_speed
        if self.to_left:
            self.robot_x -= self.robot_speed
        if self.to_down:
            self.robot_y += self.robot_speed
        if self.to_up:
            self.robot_y -= self.robot_speed
 
        self.robot_x = min(self.robot_x,self.window_width-self.images[3].get_width())
        self.robot_x = max(self.robot_x,0)
        self.robot_y = min(self.robot_y,self.window_height-self.images[3].get_height())
        self.robot_y = max(self.robot_y,0)
 
    def spawn_monster(self):
        self.monsters_count += 1
 
        if self.robot_x > self.window_width/2-self.images[3].get_width()/2:
            self.monsters_list.append([self.spawn_left[0],self.spawn_left[1]])
        else:
            self.monsters_list.append([self.spawn_right[0],self.spawn_right[1]])
 
    def move_monsters(self):
        for i in range(self.monsters_count):
            if self.monsters_list[i][0] < self.robot_x:
                self.monsters_list[i][0] += self.monsters_speed
            if self.monsters_list[i][0] > self.robot_x:
                self.monsters_list[i][0] -= self.monsters_speed
            if self.monsters_list[i][1] < self.robot_y:
                self.monsters_list[i][1] += self.monsters_speed
            if self.monsters_list[i][1] > self.robot_y:
                self.monsters_list[i][1] -= self.monsters_speed
 
    def spawn_coin(self):
        self.coin_x = randint(0,self.window_width-self.images[0].get_width())
        self.coin_y = randint(0,self.window_height-self.images[0].get_height())
 
    def coin_collision(self):
        self.coin_middle_x = self.coin_x + self.images[0].get_width()/2
        self.coin_middle_y = self.coin_y + self.images[0].get_height()/2
 
        self.robot_middle_x = self.robot_x + self.images[3].get_width()/2
        self.robot_middle_y = self.robot_y + self.images[3].get_height()/2
 
        if abs(self.robot_middle_x-self.coin_middle_x) <= (self.images[3].get_width()+self.images[0].get_width())/2:
            if abs(self.robot_middle_y-self.coin_middle_y) <= (self.images[3].get_height()+self.images[0].get_height())/2:
                self.spawn_coin()
                self.spawn_monster()
                self.start_ticks=pygame.time.get_ticks()
 
    def monster_collision(self):
        for i in range(self.monsters_count):
            monster_middle_x = self.monsters_list[i][0] + self.images[1].get_width()/2
            monster_middle_y = self.monsters_list[i][1] + self.images[1].get_height()/2
 
            if abs(self.robot_middle_x-monster_middle_x)+30 <= (self.images[3].get_width()+self.images[1].get_width())/2:
                if abs(self.robot_middle_y-monster_middle_y)+30 <= (self.images[3].get_height()+self.images[1].get_height())/2:
                    self.game_state = "dead"
 
 
Dolla()