from tkinter import font
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.power_ups.power_up_manager import Powerupmanager
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.score import Score

from dino_runner.utils.constants import BG, DEATH, DEFAULT_TYPE, FONT_STYLE, HAMMER_TYPE, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD, SHIELD_TYPE, TITLE, FPS




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()       
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.sound_menu = pygame.mixer.Sound("y2mate.com-Rosalía-fans-be-like.wav")
        self.sound_game = pygame.mixer.Sound("ba_ba_ba_ba_bababa_meme_full_version.wav")
        self.sound_death = pygame.mixer.Sound("Great_Grey_Wolf_Sif_-_Dark_Souls_Soundtrack.wav")

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = Powerupmanager()
        self.heart_manager = PlayerHeartManager()

        self.death_count = 0
        self.score = Score()

    def execute(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
    
        pygame.quit()
    
    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset_game(self):
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        self.score.reset_score()
        self.power_up_manager.reset_power_ups()
        self.heart_manager.reset_hearts()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.score.update(self) 
        self.power_up_manager.update(self.game_speed, self.player, self.score.score)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.heart_manager.draw(self.screen)
        self.draw_power_up_active()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0 :
            #and self.playing == False 
            self.sound_game.play()
            font = pygame.font.Font(FONT_STYLE, 30)
            text_component = font.render("Press any key to start", True, (0, 0, 0))
            text_rect = text_component.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text_component, text_rect)
            self.screen.blit(RUNNING[0], (half_screen_width - 30, half_screen_height - 140))
            self.sound_game.set_volume(0.02)
 #       elif self.playing == True:
  #          print("hola")
   #         self.sound_menu.play()-----------> Una idea para musica de inicio
    #        self.sound_game.stop()       
     #       self.sound_menu.set_volume(0.02)
        else:
            self.sound_game.stop()
      #      self.sound_game.stop()
            self.sound_death.play()
            font = pygame.font.Font(FONT_STYLE, 30)
            text_component = font.render("Try again", True, (0, 0, 0))
            text_rect = text_component.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text_component, text_rect)
            self.screen.blit(DEATH[0], (half_screen_width - 30, half_screen_height - 140))
            text_component = font.render(f"You death: {self.death_count} times", True, (0, 0, 0))
            text_rect = text_component.get_rect()
            text_rect.midbottom = (half_screen_width, half_screen_height + 100)
            self.screen.blit(text_component, text_rect)
            text_component = font.render(f"Your score was: {self.score.score}", True, (0, 0, 0))
            text_rect = text_component.get_rect()
            text_rect.midbottom = (half_screen_width, half_screen_height + 150)
            self.screen.blit(text_component, text_rect)
            self.sound_death.set_volume(0.02)




        pygame.display.update()
        self.handle_key_events_on_menu()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def on_death(self):
        has_shield = self.player.type == SHIELD_TYPE
        has_hammer = self.player.type == HAMMER_TYPE
        is_invicible = has_shield or self.heart_manager.heart_count > 0
        is_invicible = has_hammer or self.heart_manager.heart_count > 0
        if not has_shield:
            self.heart_manager.reduce_heart()

  #      if  has_hammer:
   #         self.obstacles.remove(obstacle)

        if not is_invicible:
            pygame.time.delay(500)
            self.playing = False
            self.death_count += 1

        return is_invicible

    def draw_power_up_active(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks()) / 1000)
            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 18)
                text_component = font.render(f"{self.player.type.capitalize()} enable for {time_to_show} seconds.", True, (0, 0, 0))
                text_rect = text_component.get_rect()
                text_rect.center = (half_screen_width , half_screen_height - 200)
                self.screen.blit(text_component, text_rect)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
