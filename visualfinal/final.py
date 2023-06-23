
#Final project 심예훈 20191111 


import pygame
import math
import random
import os

pygame.init()

SCREEN_W = 800
SCREEN_H = 600
def main():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('tower defence final project 20191111 ')

    clock = pygame.time.Clock()
    FPS = 60

    level = 1
    high_score = 0
    difficulty = 0
    targetdiff = 1000
    DIFF_MULT = 1.1
    game_over = False
    next_level = False
    ENEMYTIME = 1000
    last_enemy = pygame.time.get_ticks()
    enemies_alive = 0
    max_towers = 4
    CANNONPRICE = 5000
    tower_positions = [
    [SCREEN_W - 250, SCREEN_H - 200],
    [SCREEN_W - 200, SCREEN_H - 200],
    [SCREEN_W - 150, SCREEN_H - 200],
    [SCREEN_W - 100, SCREEN_H - 200],
    ]


    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as file:
            high_score = int(file.read())

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    font = pygame.font.SysFont('Arial', 30)
    font_60 = pygame.font.SysFont('Arial', 60)


    bg = pygame.image.load('bg1.png').convert_alpha()
    health_castle100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
    health_castle50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
    health_castle25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()
    health_tower100 = pygame.image.load('img/tower/tower_100.png').convert_alpha()
    health_tower50 = pygame.image.load('img/tower/tower_50.png').convert_alpha()
    health_tower25 = pygame.image.load('img/tower/tower_25.png').convert_alpha()
    tower_img_200 = pygame.image.load('img/tower/tower_200.png').convert_alpha()

    bullet_shot = pygame.mixer.Sound('img/snd/bulletshot.wav')
    level_clear = pygame.mixer.Sound('img/snd/clearstage.wav')
    gamedone = pygame.mixer.Sound('img/snd/gameover.wav')
    enemy_kill = pygame.mixer.Sound('img/snd/killenemy.wav')
    enemy_attk = pygame.mixer.Sound('img/snd/attack.wav')
    power_up = pygame.mixer.Sound('img/snd/powerup.wav')




    bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
    b_w = bullet_img.get_width()
    b_h = bullet_img.get_height()
    bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

    enemy_animations = []
    enemy_types = ['mushroom', 'frog', 'troll']
    enemy_health = [60,20,120]

    animation_types = ['walk', 'attack', 'death']
    for enemy in enemy_types:
        animation_list = []
        for animation in animation_types:
            temp_list = []
            num_of_frames = 5
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
                e_w = img.get_width()
                e_h = img.get_height()
                img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
                temp_list.append(img)
            animation_list.append(temp_list)
        enemy_animations.append(animation_list)

    repair_img = pygame.image.load('img/repair.png').convert_alpha()
    armour_img = pygame.image.load('img/armour.png').convert_alpha()


    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    def show_info():
        draw_text('GOLD: ' + str(castle.money), font, GREEN, 10, 10)
        draw_text('SCORE: ' + str(castle.score), font, GREEN, 250, 10)
        draw_text('High Score: ' + str(high_score), font, GREEN, 10, 45)
        draw_text('Level: ' + str(level), font, GREEN, 440, 10)
        draw_text('HP: ' + str(castle.health) + " / " + str(castle.max_health), font, GREEN, SCREEN_W - 350, SCREEN_H - 50)
        draw_text('1000', font, GREEN, SCREEN_W - 260 , 70)
        draw_text(str(CANNONPRICE), font, GREEN, SCREEN_W - 160, 70)
        draw_text('500', font, GREEN, SCREEN_W - 70 , 70)

    class Fort():
        def __init__(self, image100, image50, image25, x, y, scale):
            self.health = 1000
            self.max_health = self.health
            self.fired = False
            self.money = 0
            self.score = 0

            width = image100.get_width()
            height = image100.get_height()

            self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
            self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
            self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
            self.rect = self.image100.get_rect()
            self.rect.x = x
            self.rect.y = y


        def shoot(self):
            pos = pygame.mouse.get_pos()
            x_dist = pos[0] - self.rect.midleft[0]
            y_dist = -(pos[1] - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_dist, x_dist))
            if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
                bullet_shot.play()
                self.fired = True
                bullet = Ammo(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False



        def draw(self):
            if self.health <= 250:
                self.image = self.image25
            elif self.health <= 500:
                self.image = self.image50
            else:
                self.image = self.image100
                
            screen.blit(self.image, self.rect)
            
        def repair(self):
            if self.money >= 1000 and self.health < self.max_health:
                self.health += 500
                self.money -= 1000
                if castle.health > castle.max_health:
                    castle.health = castle.max_health

        def armour(self):
            if self.money >= 500:
                self.max_health += 250
                self.money -= 500

    class Ammo(pygame.sprite.Sprite):
        def __init__(self, image, x, y, angle):
            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.angle = math.radians(angle)
            self.speed = 10
            self.dx = math.cos(self.angle) * self.speed
            self.dy = -(math.sin(self.angle) * self.speed)


        def update(self):
            if self.rect.right < 0 or self.rect.left > SCREEN_W or self.rect.bottom < 0 or self.rect.top > SCREEN_H:
                self.kill()			

            self.rect.x += self.dx
            self.rect.y += self.dy

    class Cannon(pygame.sprite.Sprite):
            def __init__(self, image100, image50, image25, x, y, scale):
                pygame.sprite.Sprite.__init__(self)

                self.got_target = False
                self.angle = 0
                self.last_shot = pygame.time.get_ticks()

                width = image100.get_width()
                height = image100.get_height()

                self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
                self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
                self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
                self.image = self.image100
                self.rect = self.image100.get_rect()
                self.rect.x = x
                self.rect.y = y


            def update(self, enemy_group):
                self.got_target = False

                for e in enemy_group:
                    if e.alive:
                        target_x, target_y = e.rect.midbottom
                        self.got_target = True
                        break

                if self.got_target:
                    x_dist = target_x - self.rect.midleft[0]
                    y_dist = -(target_y - self.rect.midleft[1])
                    self.angle = math.degrees(math.atan2(y_dist, x_dist))

                    shot_cooldown = 1000
                    if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                        self.last_shot = pygame.time.get_ticks()
                        bullet = Ammo(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                        bullet_group.add(bullet)
                        bullet_shot.play()

                if castle.health <= 250:
                    self.image = self.image25
                elif castle.health <= 500:
                    self.image = self.image50
                else:
                    self.image = self.image100

    class Crosshair():
        def __init__(self, scale):
            image = pygame.image.load('img/crosshair.png').convert_alpha()
            width = image.get_width()
            height = image.get_height()

            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()

            pygame.mouse.set_visible(False)


        def draw(self):
            mx, my = pygame.mouse.get_pos()
            self.rect.center = (mx, my)
            screen.blit(self.image, self.rect)

    class Button():
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

        def draw(self, surface):
            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            surface.blit(self.image, (self.rect.x, self.rect.y))

            return action



    class Enemy(pygame.sprite.Sprite):
        def __init__(self, health, animation_list, x, y, speed):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.speed = speed
            self.health = health
            self.last_attack = pygame.time.get_ticks()
            self.attack_cooldown = 1000
            self.animation_list = animation_list
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = pygame.Rect(0, 0, 25, 40)
            self.rect.center = (x, y)


        def update(self, surface, target, bullet_group):
            if self.alive:
                if pygame.sprite.spritecollide(self, bullet_group, True):
                    self.health -= 25

                if self.rect.right > target.rect.left:
                    self.update_action(1)
                    

                if self.action == 0:
                    self.rect.x += self.speed

                
                if self.action == 1:
                    enemy_attk.play()
                    if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                        target.health -= 25
                        if target.health < 0:
                            target.health = 0
                        self.last_attack = pygame.time.get_ticks()


                if self.health <= 0:
                    target.money += 100
                    target.score += 100
                    self.update_action(2)
                    enemy_kill.play()
                    self.alive = False

            self.update_animation()

            surface.blit(self.image, (self.rect.x - 10, self.rect.y - 15))


        def update_animation(self):
            ANIMATION_COOLDOWN = 50
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0


        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_date = pygame.time.get_ticks()
                
    castle = Fort(health_castle100, health_castle50, health_castle25, SCREEN_W - 250, SCREEN_H - 300, 0.2)

    crosshair = Crosshair(0.025)

    repair_button = Button(SCREEN_W - 240, 10, repair_img, 0.5)
    tower_button = Button(SCREEN_W - 160, 10, tower_img_200, 0.1)
    armour_button = Button(SCREEN_W - 75, 10, armour_img, 1.5)

    tower_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)

    run = True
    while run:

        clock.tick(FPS)

        if game_over == False:
            screen.blit(bg, (0, 0))

            castle.draw()
            castle.shoot()
            tower_group.draw(screen)
            tower_group.update(enemy_group)

            crosshair.draw()

            bullet_group.update()
            bullet_group.draw(screen)


            enemy_group.update(screen, castle, bullet_group)

            show_info()

            if repair_button.draw(screen):
                castle.repair()
                power_up.play()
            if tower_button.draw(screen):
                power_up.play()
                if castle.money >= CANNONPRICE and len(tower_group) < max_towers:
                    tower = Cannon(
                        health_tower100,
                        health_tower50,
                        health_tower25,
                        tower_positions[len(tower_group)][0],
                        tower_positions[len(tower_group)][1],
                        0.2
                        )
                    tower_group.add(tower)
                    castle.money -= CANNONPRICE
            if armour_button.draw(screen):
                castle.armour()
                power_up.play()

            if difficulty < targetdiff:
                if pygame.time.get_ticks() - last_enemy > ENEMYTIME:
                    e = random.randint(0, len(enemy_types) -1)
                    enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_H - 100, 1)
                    enemy_group.add(enemy)
                    last_enemy = pygame.time.get_ticks()
                    difficulty += enemy_health[e]


            if difficulty >= targetdiff:
                enemies_alive = 0
                for e in enemy_group:
                    if e.alive == True:
                        enemies_alive += 1
                if enemies_alive == 0 and next_level == False:
                    next_level = True
                    level_reset_time = pygame.time.get_ticks()

            if next_level == True:
                draw_text('LEVEL COMPLETE!', font_60, WHITE, 200, 300)
                level_clear.play()
                if castle.score > high_score:
                    high_score = castle.score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                if pygame.time.get_ticks() - level_reset_time > 1500:
                    next_level = False
                    level += 1
                    last_enemy = pygame.time.get_ticks()
                    targetdiff *= DIFF_MULT
                    difficulty = 0
                    enemy_group.empty()

            if castle.health <= 0:
                game_over = True

        else:
            draw_text('YOU LOSE!', font, GREEN, 300, 300)
            gamedone.play()
            draw_text('PRESS "R" TO PLAY AGAIN!', font, GREEN, 250, 360)
            pygame.mouse.set_visible(True)
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                game_over = False
                level = 1
                targetdiff = 1000
                difficulty = 0
                last_enemy = pygame.time.get_ticks()
                enemy_group.empty()
                tower_group.empty()
                castle.score = 0
                castle.health = 1000
                castle.max_health = castle.health
                castle.money = 0
                pygame.mouse.set_visible(False)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()
