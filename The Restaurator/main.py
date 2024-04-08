import pygame as pg
from time import time
from math import sqrt

window = pg.display.set_mode((1300, 1000))
clock = pg.time.Clock()
pg.font.init()

'''Класс, который управляет'''


class Building:
    def __init__(self, x, y, width, height, price, rental_price, customers_per_day):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.cd = time()
        self.price = price
        self.rental_price = rental_price
        self.cpd = customers_per_day
        self.opened = False

    def update(self, gm):
        if gm:
            pg.draw.rect(window, (0, 255, 0), (self.x, self.y, self.w, self.h), 5)

        if time() - self.cd >= 0.5:
            if pg.mouse.get_pressed()[0]:
                mx, my = pg.mouse.get_pos()
                if self.x <= mx <= self.x+self.w:
                    if self.y <= my <= self.y+self.h:
                        self.opened = not self.opened
                        self.cd = time()

        if self.opened:
            pg.draw.rect(window, (120, 120, 120), (1010, 300, 270, 500))


'''MovingBackground - класс, управляющий красивым полётом камеры в меню'''


class MovingBackground:
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.x >= 1000 or self.rect.y <= -1000:
            self.rect.x = 0
            self.rect.y = 0

        window.blit(self.img, (self.rect.x, self.rect.y))
        window.blit(self.img, (self.rect.x-1000, self.rect.y))
        window.blit(self.img, (self.rect.x, self.rect.y+1000))
        window.blit(self.img, (self.rect.x-1000, self.rect.y+1000))
        window.blit(self.img, (self.rect.x, self.rect.y-1000))
        window.blit(self.img, (self.rect.x+1000, self.rect.y))
        window.blit(self.img, (self.rect.x+1000, self.rect.y-1000))
        self.rect.x += 2
        self.rect.y -= 2


'''Map - класс "экрана"'''


class Map:
    def __init__(self, img, name, coords, buildings):
        self.img = img
        self.name = name
        self.x = coords[0]
        self.y = coords[1]
        self.gx = self.x*1000
        self.gy = self.y*1000
        self.buildings = buildings
        for b in buildings:
            b.map = self

    def draw(self, x, y):
        window.blit(self.img, (x, y))


'''MapManager - класс, который управляет экранами'''


class MapManager:
    def __init__(self, maps, cur_map):
        self.maps = maps
        self.cur_map = cur_map

    '''Switch - функция для переключения экрана'''
    def switch(self, target_map):

        xspeed = (target_map.x - self.cur_map.x)*8
        yspeed = (target_map.y - self.cur_map.y)*8

        mx = self.cur_map.gx
        my = self.cur_map.gy
        while ((mx != target_map.gx) or (my != target_map.gy)):
            window.fill((255, 255, 255))

            for m in maps:
                if sqrt((m.gx-mx)**2 + (m.gy-my)**2) < 1300:
                    m.draw(m.gx-mx, m.gy-my)

            mx += xspeed
            my += yspeed

            pg.display.update()

        self.cur_map = target_map

    def draw_cur_map(self):
        self.cur_map.draw(0, 0)


class Button:
    def __init__(self, x, y, **kwargs):
        self.img = kwargs['kwargs']['img']
        self.width = kwargs['kwargs']['width']
        self.height = kwargs['kwargs']['height']
        self.active = True

        if self.img:
            self.rect = self.img.get_rect()
        else:
            self.rect = pg.Rect((self.rect.x, self.rect.y, self.width, self.height))

        self.rect.x = x
        self.rect.y = y

        self.time = time()
        self.cd = 0.2

    def update(self, gm):
        if self.img:
            window.blit(self.img, (self.rect.x, self.rect.y))
        else:
            if gm:
                pg.draw.rect(window, (0, 255, 0), (self.rect.x, self.rect.y, self.width, self.height))

        if self.active:
            if time() - self.time >= self.cd:
                if pg.mouse.get_pressed()[0]:
                    mx, my = pg.mouse.get_pos()
                    if self.rect.x <= mx <= self.rect.x + self.rect.width:
                        if self.rect.y <= my <= self.rect.y + self.rect.height:
                            self.time = time()
                            return True

            return False


'''Булевые переменные'''
game = False
menu = True
gm = True

map_x = 0
map_y = 0

FPS = 60

start_game = Button(100, 100, kwargs={'img': pg.image.load("images/start_game.png"), 'width': 0, 'height': 0})
exit_cd = time()
menu_bg = MovingBackground(0, 0, pg.image.load('images/home.png'))

district = 1
maps = []

d1 = Button(1000, 0, kwargs={'img': pg.image.load("images/d1.png"), 'width': 0, 'height': 0})
d2 = Button(1100, 0, kwargs={'img': pg.image.load("images/d2.png"), 'width': 0, 'height': 0})
d3 = Button(1200, 0, kwargs={'img': pg.image.load("images/d3.png"), 'width': 0, 'height': 0})
d4 = Button(1000, 50, kwargs={'img': pg.image.load("images/d4.png"), 'width': 0, 'height': 0})
d5 = Button(1100, 50, kwargs={'img': pg.image.load("images/d5.png"), 'width': 0, 'height': 0})
d6 = Button(1200, 50, kwargs={'img': pg.image.load("images/d6.png"), 'width': 0, 'height': 0})
d7 = Button(1000, 100, kwargs={'img': pg.image.load("images/d7.png"), 'width': 0, 'height': 0})
d8 = Button(1100, 100, kwargs={'img': pg.image.load("images/d8.png"), 'width': 0, 'height': 0})
d9 = Button(1200, 100, kwargs={'img': pg.image.load("images/d9.png"), 'width': 0, 'height': 0})

maps.append(Map(pg.image.load('images/left-top.png'), 'left-top', (0, 0), [Building(35, 140, 310, 100, 3000, 300, 170),
                                                                           Building(540, 120, 295, 145, 6000, 500, 200),
                                                                           Building(0, 490, 145, 210, 1000, 150, 80),
                                                                           Building(490, 490, 160, 250, 1100, 160, 85),
                                                                           Building(710, 490, 75, 65, 550, 55, 60),
                                                                           Building(5, 870, 220, 95, 3000, 300, 60)]))

maps.append(Map(pg.image.load('images/mid-top.png'), 'mid-top', (1, 0), [Building(330, 485, 440, 180, 3000, 300, 170)]))

maps.append(Map(pg.image.load('images/right-top.png'), 'right-top', (2, 0), [Building(205, 495, 200, 125, 1000, 130, 80)]))

maps.append(Map(pg.image.load('images/left-mid.png'), 'left-mid', (0, 1), [Building(695, 95, 285, 200, 1200, 100, 300),
                                                                           Building(375, 185, 250, 115, 1300, 120, 300)]))

maps.append(Map(pg.image.load('images/mid-mid.png'), 'mid-mid', (1, 1), [Building(650, 0, 260, 135, 1000, 70, 40)]))

maps.append(Map(pg.image.load('images/right-mid.png'), 'right-mid', (2, 1), [# Building(650, 0, 260, 135, 1000, 70, 40)
                                                                             ]))

maps.append(Map(pg.image.load('images/left-bot.png'), 'left-bot', (0, 2), [Building(520, 250, 395, 80, 1600, 150, 120)]))

maps.append(Map(pg.image.load('images/mid-bot.png'), 'mid-bot', (1, 2), [Building(900, 115, 80, 165, 1800, 200, 150)]))

maps.append(Map(pg.image.load('images/right-bot.png'), 'right-bot', (2, 2), [Building(365, 180, 75, 270, 1400, 150, 90)]))

font = pg.font.SysFont('Arial', 24, False, False)

day = 0
day_time = time()

k_cd = time()

mm = MapManager(maps, maps[0])

while menu:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            menu = False
            game = False

    menu_bg.update()

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE] and time() - exit_cd >= 0.3:
        menu = False
        exit_cd = time()

    if start_game.update(gm):
        game = True
        menu = False

    pg.display.update()

    while game:
        '''Сменяется день'''
        if time() - day_time >= 300:
            day += 1
            day_time = time()

        '''Заливка окна'''
        window.fill((255, 255, 255))

        '''Проверка событий'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE] and time() - exit_cd >= 0.3:
            game = False
            exit_cd = time()

        '''Смена картинки'''
        keys = pg.key.get_pressed()
        if keys[pg.K_1] or d1.update(gm):
            mm.switch(maps[0])

        elif keys[pg.K_2] or d2.update(gm):
            mm.switch(maps[1])

        elif keys[pg.K_3] or d3.update(gm):
            mm.switch(maps[2])

        elif keys[pg.K_4] or d4.update(gm):
            mm.switch(maps[3])

        elif keys[pg.K_5] or d5.update(gm):
            mm.switch(maps[4])

        elif keys[pg.K_6] or d6.update(gm):
            mm.switch(maps[5])

        elif keys[pg.K_7] or d7.update(gm):
            mm.switch(maps[6])

        elif keys[pg.K_8] or d8.update(gm):
            mm.switch(maps[7])

        elif keys[pg.K_9] or d9.update(gm):
            mm.switch(maps[8])

        elif keys[pg.K_k] and time() - k_cd >= 0.5:
            k_cd = time()
            print(pg.mouse.get_pos())

        '''Отрисовка текущей карты'''
        mm.draw_cur_map()

        '''Обновление зданий'''
        for b in mm.cur_map.buildings:
            b.update(gm)

        '''Отрисовка текущего дня'''
        window.blit(font.render(f'Day: {day}', False, (0, 0, 0)), (1010, 170))

        pg.display.update()

