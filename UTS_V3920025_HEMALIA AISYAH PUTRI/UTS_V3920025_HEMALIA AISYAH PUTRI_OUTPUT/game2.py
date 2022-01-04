# Judul dari permainan
TITLE = "Sky High"

# untuk mengakses kerangka kerja PyGame,os, sys, pickle.
import pygame, os, sys, pickle
#mengimpor semua modul pygame yang tersedia ke dalam paket pygame
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Player, Obstacle, Hat, Pet, TulangMeter, Text, Powerup, Particle, Shockwave, JetpackTrail
from data.scripts.scene import Scene, SceneManager
from data.scripts.config import *

#menginisialisasi semua modul yang diperlukan untuk PyGame
pygame.init()
pygame.mixer.init()

# Directories
# os.path.join()menggabungkan berbagai komponen jalur dengan tepat satu pemisah direktori
GAME_DIR = os.path.dirname(_file_)
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
IMG_DIR = os.path.join(DATA_DIR, "img")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

#menambahkan kelas GameData
class GameData:
    #mendekalarasikan variabel self
    def _init_(self):
        #memuat hewan peliharaan yang dilengkapi
        self.equipped_pet = "none"
        #memuat hewan peliharaan yang dimiliki
        self.owned_pets = []
        #memuat hewan peliharaan yang dilengkapi topi
        self.equipped_hat = "none"
        #memuat hewan peliharaan yang dimiliki topi
        self.owned_hats = []

        # Mulai untuk nerd
        #memuat koin 
        self.coins = 0
        #memuat skortertinggi
        self.highscore = 0
        #memuat waktu saat mati
        self.times_died = 0
        #memuat waktu saat memukul
        self.times_hit = 0
        #memuat waktu pengambilan bahan bakar
        self.times_fuelpickup = 0
        #memuat waktu shieldpickup
        self.times_shieldpickup = 0

        self.play_time = 0

# mendekalarasikan Muat data permainan
infile = open(os.path.join(DATA_DIR, "user_data.dat"), "rb")
game_data = pickle.load(infile)
infile.close()

# Functions
#mendekalarasikan fungsi load sound
def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd
#mendekalarasikan variabel self
def load_png(file, directory, scale, convert_alpha=False):
    try:
        # os.path.join()menggabungkan berbagai komponen jalur dengan tepat satu pemisah direktori
        path = os.path.join(directory, file)
        if not convert_alpha:
            #memuat gambar baru dari file
            img = pygame.image.load(path).convert_alpha()
        else:
            #memuat gambar baru dari file
            img = pygame.image.load(path).convert()
            #memuat warna pada gambar yang di dapat
            transColor = img.get_at((0,0))
            #mengatur kunci pada gambar
            img.set_colorkey(transColor)
        #memuat lebar pada gambar
        img_w = img.get_width()
         #memuat lebar pada gambar
        img_h = img.get_height()
        #memuat lebar pada gambar
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(e)
        exit()

# Load sounds ====================
select_sfx = load_sound("select.wav", SFX_DIR, 0.6)
enter_sfx = load_sound("enter.wav", SFX_DIR, 0.6)
buy_sfx = load_sound("buy.wav", SFX_DIR, 0.6)
denied_sfx = load_sound("denied.wav", SFX_DIR, 0.8)
explosion_sfx = load_sound("explosion.wav", SFX_DIR, 0.5)
#menambahkan kelas TitleScene
class TitleScene(Scene):
    #mendekalarasikan variabel self
    def _init_(self):
        # Memuat Booleans
        self.help_available = False
        self.stats_available = False

        # Memuat Permukaan
        self.menu_area = pygame.Surface((256, 280))
        self.menu_area_rect = self.menu_area.get_rect()
        self.menu_area_rect.centerx = WIN_SZ[0] / 2
        self.menu_area_rect.y = 200
        #memuat logo baru dari file
        self.logo_img = load_png("lo10.png", IMG_DIR, 1)
        self.help_area = pygame.Surface((300, 450))
        #memuat gambar baru dari file
        self.help_img = load_png("help.png", IMG_DIR, 4)
        self.stats_area = pygame.Surface((300, 450))
        self.stats_area = pygame.transform.scale(self.stats_area, (10,10))
        #memuat gambar pemain dari file
        self.dev_img = load_png("kitty3.png", IMG_DIR,1 )

        self.bg_layer1_x = 0
        self.bg_layer2_x = 0
        self.bg_layer3_x = 0
        #memuat backround pada layer 1 dari file
        self.bg_layer1_img = load_png("bgnaw.png", IMG_DIR, 1)     
        self.bg_layer1_rect = self.bg_layer1_img.get_rect()
        self.bg_layer1_img = pygame.transform.scale(self.bg_layer1_img, (1200,512))
        

        # Pemilih
        self.y_offset = 32
        self.selector_width = 6
        self.selector_y = -self.selector_width + self.y_offset
        self.cur_sel = 0

        # Sprite groups
        self.statstexts = pygame.sprite.Group()
        self.helptexts = pygame.sprite.Group()
        self.optiontexts = pygame.sprite.Group()

        # Memuat Teks untuk menu
        #self.text_title = Text(self.menu_area.get_width() / 2, self.menu_area.get_height () / 8, "CAFFEINE", GAME_FONT, 48, 'white')
        self.text_play = Text(self.menu_area.get_width() / 2, 0 + self.y_offset, "PLAY", GAME_FONT, 34, 'white')
        self.text_shop = Text(self.menu_area.get_width() / 2, 45 + self.y_offset, "SHOP", GAME_FONT, 32, 'yellow')
        self.text_stats = Text(self.menu_area.get_width() / 2, 90 + self.y_offset, "STATS", GAME_FONT, 32, 'white')
        self.text_help = Text(self.menu_area.get_width() / 2, 135 + self.y_offset, "HELP", GAME_FONT, 32, 'white')
        self.text_quit = Text(self.menu_area.get_width() / 2, 180 + self.y_offset, "QUIT", GAME_FONT, 32, 'white')
        #self.texts.add(self.text_title)
        self.optiontexts.add(self.text_play)
        self.optiontexts.add(self.text_shop)
        self.optiontexts.add(self.text_stats)
        self.optiontexts.add(self.text_help)
        self.optiontexts.add(self.text_quit)

        # Texts for help area
        self.text_help = Text(0, 0, "HELP", GAME_FONT, 32, 'white')
        self.text_help.rect = (16,16)
        self.helptexts.add(self.text_help)

        # Texts for stats area
        self.text_statslabel = Text(0, 0, "STATS", GAME_FONT, 32, 'white')
        self.text_statslabel.rect = (16,16)
        self.text_highscore = Text(0,0, f"Hi-score: {game_data.highscore}", GAME_FONT, 14, 'yellow')
        self.text_highscore.rect = (16,64)
        self.text_coins = Text(0,0, f"Coins: {game_data.coins}", GAME_FONT, 14, 'white')
        self.text_coins.rect = (16,94)
        self.text_timesdied = Text(0,0, f"Times died: {game_data.times_died}", GAME_FONT, 14, 'white')
        self.text_timesdied.rect = (16,124)
        self.text_timeshit = Text(0,0, f"Times hit: {game_data.times_hit}", GAME_FONT, 14, 'white')
        self.text_timeshit.rect = (16,154)
        self.text_timesfuel = Text(0,0, f"Fuel pickups: {game_data.times_fuelpickup}", GAME_FONT, 14, 'white')
        self.text_timesfuel.rect = (16,184)
        self.text_timesshield = Text(0,0, f"Shield pickups: {game_data.times_shieldpickup}", GAME_FONT, 14, 'white')
        self.text_timesshield.rect = (16,214)
        self.text_playtime = Text(0,0, f"Play time: {game_data.play_time}s", GAME_FONT, 14, 'white')
        self.text_playtime.rect = (16,244)
        self.statstexts.add(self.text_statslabel)
        self.statstexts.add(self.text_highscore)
        self.statstexts.add(self.text_coins)
        self.statstexts.add(self.text_timesdied)
        self.statstexts.add(self.text_timeshit)
        self.statstexts.add(self.text_timesfuel)
        self.statstexts.add(self.text_timesshield)
        self.statstexts.add(self.text_playtime)
        
    #mendekalarasikan variabel (self,events)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.cur_sel > 0:
                    self.selector_y -= 45
                    self.cur_sel -= 1
                    select_sfx.play()
                #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.cur_sel < len(self.optiontexts) - 1:
                    self.selector_y += 45
                    self.cur_sel += 1
                    select_sfx.play()
                 #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                if event.key == pygame.K_RETURN:
                    if self.cur_sel == 0:
                        self.manager.go_to(GameScene())
                    elif self.cur_sel == 1:
                        self.manager.go_to(ShopScene())
                    elif self.cur_sel == 2:
                        self.stats_available = not self.stats_available
                        self.help_available = False
                    elif self.cur_sel == 3:
                        self.stats_available = False
                        self.help_available = not self.help_available
                    elif self.cur_sel == 4:
                        # Memuat menyimpan data dan keluar
                        #game_data.coins = 3000
                        outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
                        pickle.dump(game_data, outfile)
                        outfile.close()
                        sys.exit()
                    enter_sfx.play()
    #mendekalarasikan untuk mengupdate
    def update(self):

        # Perbarui latar belakang dan posisi paralaks x
        self.bg_layer1_x -= 1

        self.statstexts.update()
        self.helptexts.update()
        self.optiontexts.update()
    #mendekalarasikan untuk menggambar
    def draw(self, window):
        window.fill((0,0,12))
        self.draw_background(window, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x)
    
        window.blit(self.logo_img, (65,115))
        window.blit(self.menu_area, (140,198))
        window.blit(self.dev_img, (490,128))
        if self.help_available:
            window.blit(self.help_area, (430, 32))
            self.help_area.fill('black')
            self.helptexts.draw(self.help_area)
            self.help_area.blit(self.help_img, (0,0))
            pygame.draw.rect(self.help_area, 'white', (0,0,self.help_area.get_width(),self.help_area.get_height()), 8)
        if self.stats_available:
            window.blit(self.stats_area, (430, 32))
            self.stats_area.fill('brown')
            self.statstexts.draw(self.stats_area)
            pygame.draw.rect(self.stats_area, 'white', (0,0,self.stats_area.get_width(),self.stats_area.get_height()), 8)
        #window.blit(self.menu_area, self.menu_area_rect)
        #window.blit(self.logo_img, (WIN_SZ[1] / 2 - (self.logo_img.get_width()/6), 48))
        self.menu_area.fill('brown')
        self.menu_area.set_colorkey('brown')
        self.optiontexts.draw(self.menu_area)
        pygame.draw.rect(self.menu_area, 'white', (3,self.selector_y,249,40), self.selector_width) # selector
    #mendekalarasikan untuk menggambar pada background
    def draw_background(self, surf, img, img_rect, pos):
        surf_w = surf.get_width()
        rel_x = pos % img_rect.width
        surf.blit(img, (rel_x - img_rect.width, 0))

        if rel_x < surf_w:
            surf.blit(img, (rel_x, 0))
#membuat class ShopScene
class ShopScene(Scene):
    #mendekalarasikan variabel self
    def _init_(self):
        #memuat game dengan highscore
        self.coins = 1000
        self.init_x = 16
        self.init_y = 16
        self.x_offset = 64 + self.init_x 
        self.y_offset = 64 + self.init_y
        #memuat pelihanran file
        self.pet_files = [
            'pet_cat.png', 
            'pet_chiki.png', 
            'pet_coffee.png', 
            'pet_dog.png', 
            'pet_fish.png', 
            'pet_skull.png', 
            'pet_stealbucks.png'
        ]
        #memuat topi file
        self.hat_files = [
            'hat_dimadome.png',
            'hat_howl.png',
            'hat_leprechaun.png',
            'hat_phony.png',
            'hat_santa.png',
            'hat_swag.png',
            'hat_ushanka.png'
        ]
        self.pet_imgs = self.load_items(self.pet_files)
        self.hat_imgs = self.load_items(self.hat_files)
        #print(self.hat_imgs)
        self.selector_x = 16
        self.selector_y = 16
        if game_data.equipped_pet != "none":
            self.pet_equipped_x = 16 + (80 * self.pet_files.index(game_data.equipped_pet))
            #self.row_break = len(self.all_pets) // 2
        if game_data.equipped_hat != "none":
            self.hat_equipped_x = 16 + (80 * self.hat_files.index(game_data.equipped_hat))
        self.cur_pet = 0
        self.cur_hat = 0
        self.item_cost = 20
        self.debug_mode = False
        
        # Surfaces
        self.pets_area = pygame.Surface((WIN_SZ[0] / 1.33, 96))
        self.hats_area = pygame.Surface((WIN_SZ[0] / 1.33, 96))
        self.cur_shop = self.pets_area
         #memuat backround pada layer 1 dari file
        self.bg_layer1_img = load_png("bgnaw.png", IMG_DIR, 1)     
        self.bg_layer1_rect = self.bg_layer1_img.get_rect()
        

        self.bg_layer1_x = 0
        self.bg_layer2_x = 0
        self.bg_layer3_x = 0

        # Sprite groups
        self.texts = pygame.sprite.Group()

        # Texts
        self.text_shoplabel = Text(WIN_SZ[0] / 5, 64, "Shop", GAME_FONT, 48, 'white')
        self.text_coins = Text(WIN_SZ[0] / 1.4, 75, f"C{game_data.coins}", GAME_FONT, 32, 'yellow')
        self.text_isbought = Text(WIN_SZ[0] / 1.5, 400, "Bought", GAME_FONT, 32, 'white', False)
        self.text_entbutton = Text(WIN_SZ[0] / 1.5, 360, "[ENT]", GAME_FONT, 32, 'white')
        self.text_cost = Text(WIN_SZ[0] / 1.5, 400, f"Cost {self.item_cost}", GAME_FONT, 32, 'white', False)
        self.text_exitbutton = Text(WIN_SZ[0] / 4.2, 400, "[ESC]", GAME_FONT, 32, 'white')
        self.texts.add(self.text_shoplabel)
        self.texts.add(self.text_coins)
        self.texts.add(self.text_isbought)
        self.texts.add(self.text_cost)
        self.texts.add(self.text_exitbutton)
        self.texts.add(self.text_entbutton)

    #mendekalarasikan variabel (self,events)
    def handle_events(self, events):
        # YandereDev-esque code here. Beware!
        for event in events:
            if event.type == pygame.KEYDOWN:

                if self.cur_shop == self.pets_area:
                    #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                    if event.key == pygame.K_d and self.cur_pet < len(self.pet_files) - 1:
                        self.selector_x += 64 + self.init_x
                        self.cur_pet += 1
                        select_sfx.play()
                        #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                    if event.key == pygame.K_a and self.cur_pet > 0:
                        self.selector_x -= 64 + self.init_x
                        self.cur_pet -= 1
                        select_sfx.play()
                elif self.cur_shop == self.hats_area:
                    #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                    if event.key == pygame.K_d and self.cur_hat < len(self.hat_files) - 1:
                        self.selector_x += 64 + self.init_x
                        self.cur_hat += 1
                        select_sfx.play()
                    #jika acara kunci saat  mengklik tombol tutup di sudut jendela
                    if event.key == pygame.K_a and self.cur_hat > 0:
                        self.selector_x -= 64 + self.init_x
                        self.cur_hat -= 1
                        select_sfx.play()

#event key pada shop 
                if event.key == pygame.K_RETURN: # mengatur key pada shop
                    if self.cur_shop == self.pets_area: # area shop
                        if self.pet_files[self.cur_pet] in game_data.owned_pets: #hewan merupakan data dari pemilik  hewan
                            if game_data.equipped_pet == self.pet_files[self.cur_pet]: # mendapatkan hewan 
                                game_data.equipped_pet = "none" # perlengkapan hewan dari pemain
                                enter_sfx.play() # running sfx
                            else: # percabangan
                                game_data.equipped_pet = self.pet_files[self.cur_pet]  #pengaturan perlengkapan hewan merupakan file dari cur_pet
                                self.pet_equipped_x = self.selector_x # pengatur untuk seleksi perlengkapan hewan
                                enter_sfx.play() # running sfx
                        else: #percabangan/kondisi
                            #jika data coins lebih dari sama dengan cost item
                            if game_data.coins >= self.item_cost: # pengaturan item koin
                                game_data.equipped_pet = self.pet_files[self.cur_pet] #pengaturan ketika hewan menyentuh item koin
                                self.pet_equipped_x = self.selector_x # seleksi hewan x
                                game_data.owned_pets.append(self.pet_files[self.cur_pet]) # pengaturan hewan yang sudah dipilih
                                #data coins dikurangi dengan item cost
                                game_data.coins -= self.item_cost 
                                #menampilkan hasil
                                self.text_coins.text = f"C{game_data.coins}"
                                buy_sfx.play()
                            else:
                                self.text_coins.color = 'black' # warna pada  koin
                                denied_sfx.play() # penolakan
                    #jika cur_shop sama dengan hats_area            
                    elif self.cur_shop == self.hats_area:
                        if self.hat_files[self.cur_hat] in game_data.owned_hats: #data topi pada game
                            if game_data.equipped_hat == self.hat_files[self.cur_hat]: # memiliki data topi
                                game_data.equipped_hat = "none" 
                                enter_sfx.play() # running dari topi tersebut
                            else:
                                game_data.equipped_hat = self.hat_files[self.cur_hat] #data topi
                                self.hat_equipped_x = self.selector_x # seleksi topi yang dipilih user
                                enter_sfx.play() # running
                        else:
                            #jika data coins lebih dari sama dengan item cost
                            if game_data.coins >= self.item_cost: 
                                game_data.equipped_hat = self.hat_files[self.cur_hat] # data dari topi
                                self.hat_equipped_x = self.selector_x # pemilihan topi
                                game_data.owned_hats.append(self.hat_files[self.cur_hat]) # topi yang dimiliki
                                game_data.coins -= self.item_cost # pengurangan koin 
                                self.text_coins.text = f"C{game_data.coins}" # data dari koin
                                buy_sfx.play() # pembelian running
                            else:
                                self.text_coins.color = 'red' # pewarnaan teks pada koin
                                denied_sfx.play() # running penolakan

                if event.key == pygame.K_w: # key K_w
                    self.cur_shop = self.pets_area #area shop
                    self.cur_pet = 0 # area hewan
                    self.selector_x = 16 # seleksi
                    select_sfx.play() # running seleksi

                if event.key == pygame.K_s: #key K_s
                    self.cur_shop = self.hats_area # area shop
                    self.cur_hat = 0 # area hewan 
                    self.selector_x = 16# seleksi
                    select_sfx.play() # runninng seleksi

                if event.key == pygame.K_ESCAPE: #key K_ESCAPE
                    self.manager.go_to(TitleScene()) # mengatur sendiri menuju title scene
                    enter_sfx.play() # running

                #print(self.pet_files[self.cur_pet]) # mencetak file hewan
                #print(self.pet_files[self.cur_pet] in Game_Data.owned_pets) #mencetak dalam pemilik file hewan
        #print("Pet Equipped: " + game_data.equipped_pet) # mencetak hewan yang dimiliki
        #print("Hat Equipped:" + game_data.equipped_hat) # mencetak topi yang dimiliki
        #print(self.cur_pet, self.cur_hat) # mencetak file dari nama ini

    def update(self): # melakukan pengupdatean

        # Update background and parallax x position pada shop
        self.bg_layer1_x -= 1

        if self.cur_shop == self.pets_area: # area shop = area hewan

            if self.pet_files[self.cur_pet] in game_data.owned_pets: # file hewan yang dimiliki user
                self.text_isbought.visible = True # yang dibeli akan terlihat kondisi benar
                self.text_cost.visible = False # untuk biaya akan terlihat kondisi salah
            else: # atau
                self.text_isbought.visible = False # yang dibeli akan terlihat kondisi salah
                self.text_cost.visible = True # biaya akan terlihat kondisi benar

            self.item_cost = 30 # item yang berbayar
            self.text_cost.text = f"C{self.item_cost}" #item cost ini mengambil dalam self.item_cost

        elif self.cur_shop == self.hats_area: #area shop merupakan area topi

            if self.hat_files[self.cur_hat] in game_data.owned_hats: # file topi merupakan data yang ada di user
                self.text_isbought.visible = True  # yang dibeli akan terlihat kondisi benar
                self.text_cost.visible = False # untuk biaya akan terlihat kondisi salah
            else:
                self.text_isbought.visible = False # yang dibeli akan terlihat kondisi salah
                self.text_cost.visible = True # biaya akan terlihat kondisi benar


            self.item_cost = 20 #item berbayar 
            self.text_cost.text = f"C{self.item_cost}" #item cost ini mengambil dalam self.item_cost

        self.texts.update() # melakukan pengupdatean dengan sendiri
    #def draw pada shop
    def draw(self, window): # pengambaran
        self.draw_items(self.pets_area, self.pet_imgs) #  mengambar area hewan menjadi gambar hewan
        self.draw_items(self.hats_area, self.hat_imgs) #  mengambar topi hewan menjadi gambar topi
        window.fill((0,0,12)) # layar
        self.draw_background(window, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x) #background untuk gambar
       
        window.blit(self.pets_area, (64,128)) # pengaturan skala/panjang dan lebar layar area hewan
        window.blit(self.hats_area, (64,256)) # pengaturan skala/panjang dan lebar layar topi area
        self.pets_area.fill('black') # pada area hewan mengisi warna hitam
        self.hats_area.fill('black') # pada area topi mengisi warna hitam
        pygame.draw.rect(self.pets_area, 'white', (0,0, self.pets_area.get_width(), self.pets_area.get_height()), 8, 8, 8, 8) # mengatur panjang, lebar, background pada area hewan
        pygame.draw.rect(self.hats_area, 'white', (0,0, self.hats_area.get_width(), self.hats_area.get_height()), 8, 8, 8, 8) # mengatur panjang, lebar, background pada area hewan
        pygame.draw.rect(self.cur_shop, 'white', (self.selector_x, self.selector_y, 64, 64), 8) # this is the selector
        if game_data.equipped_pet != "none": # data perlengkapan hewan
            pygame.draw.rect(self.pets_area, 'yellow', (self.pet_equipped_x, self.init_y, 64, 64), 8) # mengatur sumbu x dan y dan juga warna dalam area hewan
        if game_data.equipped_hat != "none": # data perlengkapan topi
            pygame.draw.rect(self.hats_area, 'yellow', (self.hat_equipped_x, self.init_y, 64, 64), 8) # mengatur sumbu x dan y dan juga warna dalam area topi

        self.texts.draw(window) # mulai mengambar pada layar

    def load_items(self, files): # memuat item
        images = list() # gambar masuk dalam daftar
        for f in files: # file
            images.append(load_png(f, IMG_DIR, 4)) # menambahkan gambar

        return images # kembali ke gambar

    def draw_items(self, surface, imgs): # mengambar item
        x = self.init_x # sumbu x
        y = self.init_y # sumbu y
        cur_col = 0 # dimulai dari 0,0

        for pet in imgs: # gambar hewan
            surface.blit(pet, (x,y)) # pengambaran sumbu x dan y
            x += self.x_offset # sumbu x
            cur_col += 1 # cur_col kurang lebih 1
            #if cur_col > self.row_break: # istirahat
                #cur_col = 0
                #x = self.init_x # ssumbu x
                #y += self.y_offset + self.init_y # sumbu x dan y

    def draw_background(self, surf, img, img_rect, pos): # mengambar background
        surf_w = surf.get_width() # pengaturan lebar
        rel_x = pos % img_rect.width # untuk mengepos gambar dalam pengaturan lebar
        surf.blit(img, (rel_x - img_rect.width, 0)) # pewujudan

        if rel_x < surf_w: # rel_x lebih kurang dari surf_w
            surf.blit(img, (rel_x, 0)) # pewujudan gambar rel_x dan 0

class GameScene(Scene): # kelas game scene
    def _init_(self): # penampilan
        # Settings
        self.offset = repeat((0,0)) # For screen shake
        self.orig_gxspeed = 0 # pengaturan original kecepatan
        self.global_xspeed = 3 # pengaturan kecepatan keseluruhan
        self.bg_layer1_x = 0 # background layar 1 x
        self.bg_layer2_x = 0 # background layar 2 x
        self.bg_layer3_x = 0 # background layar 3 x
        self.moon_x = 0 # pengaturan bulan
        self.score = 0 # pengaturan skor
        self.coins = 0 # pengaturan koin
        self.max_enemies = 2 # pengaturan musuh maksimal
        self.max_powerups = 1 # pengaturan kekuatan maksimal
        self.difficulty_ticks = 0 # pengaturan kesulitan 
        self.difficulty_increase_delay = 7500 # pengaturan kesulitan peningkatan penundaan
        self.difficulty_level = 0 # pengaturan kesulitan level
        self.debug_mode = False # pengaturan mode debug
        self.start_delay = 3000 # pengaturan mulai penundaan
        self.exit_ticks = 0 # pengaturan keluar ticks
        self.can_exit = False # pengaturan bisa keluar
        self.cur_playtime = 0 # pengaturan waktu bermain
        img_sc = 4  # gambar
        img_sc2=1 # gambar
        img_sc3=2 # gambar

        # Load Images =============================
        # Play area and stats area and other crap
        self.play_area = pygame.Surface((536, 440)) # area bermain
        self.stats_area = pygame.Surface((156, 440)) # area mulai bermain
        self.color_correction = pygame.Surface((self.play_area.get_width(), self.play_area.get_height())) # pengaturan warna koreksi dalam permukaan bermain panjang dan lebar
        self.color_correction.set_alpha(10) # pengaturan warna kereksi mengatur set_alpha
        self.border_img = load_png("border.png", IMG_DIR, img_sc) # mengatur batasan gambar

        # Background pada saat dijalankan
        self.bg_layer1_img = load_png("bgnaw.png", IMG_DIR, 1)
        self.bg_layer1_rect = self.bg_layer1_img.get_rect()
       

        # Player
        player_imgs = { # gambar pemain
            "NORMAL": { # secara normal
                "MOVRIGHT": load_png("kitty4.png", IMG_DIR, img_sc2), # perpindahan kanan
                "IDLE": load_png("kitty5.png", IMG_DIR, img_sc2), # tetap ditempat
                "MOVLEFT": load_png("kitty5.png", IMG_DIR, img_sc2) # perpindahan kiri
            },
            "SHIELDED": { # ketika terlindungi
                "MOVRIGHT": load_png("kitty8.png", IMG_DIR, img_sc2), # perindahan kanan
                "IDLE": load_png("kitty8.png", IMG_DIR, img_sc2), # tepat ditempat
                "MOVLEFT": load_png("kitty8.png", IMG_DIR, img_sc2) # perpindaha kiri
            }    
        }

        if game_data.equipped_pet != "none": # data perlengkapan hewan
            pet_ing = load_png(game_data.equipped_pet, IMG_DIR, 3) # gambar hewan
        if game_data.equipped_hat != "none": # data perlengkapan topi 
            hat_img = load_png(game_data.equipped_hat, IMG_DIR, img_sc) # gambar topi

        # Obstacles
        kid_obstacle_imgs = [ # memunculkan gambar
            load_png("obstacle_kid1.png", IMG_DIR, img_sc),
            load_png("obstacle_kid2.png", IMG_DIR, img_sc)
        ]
        heli_obstacle_imgs = [ # memunculkan gambar helikopter
            load_png("obstacle_heli1.png", IMG_DIR, img_sc),
            load_png("obstacle_heli2.png", IMG_DIR, img_sc)
        ]
        obstacle_bird_imgs = [ # memunculkan gambar burung
            load_png("obstacle_bird1.png", IMG_DIR, img_sc),
            load_png("obstacle_bird2.png", IMG_DIR, img_sc)
        ]
        barry_obstacle_imgs = [ #memunculkan gambar barry
            load_png("obstacle_barry1.png", IMG_DIR, img_sc),
            load_png("obstacle_barry2.png", IMG_DIR, img_sc)
        ]
        crate_obstacle_imgs = [ # memunculkan gambar crate
            load_png("obstacle_crate1.png", IMG_DIR, img_sc),
            load_png("obstacle_crate2.png", IMG_DIR, img_sc)
        ]
        parasol_obstacle_img = [load_png("obstacle_parasol1.png", IMG_DIR, img_sc)] # memunculkan gambar parasol
        self.obstacle_imgs = [kid_obstacle_imgs, heli_obstacle_imgs, obstacle_bird_imgs, barry_obstacle_imgs, parasol_obstacle_img, crate_obstacle_imgs]

        # TulangMeter
        tulang_meter_imgs = { # memunculkan gambar tulang_meter
            "100": load_png("ikan11.png", IMG_DIR, img_sc3),
            "90": load_png("ikan12.png", IMG_DIR, img_sc3),
            "80": load_png("ikan13.png", IMG_DIR, img_sc3),
            "70": load_png("ikan14.png", IMG_DIR, img_sc3),
            "60": load_png("ikan15.png", IMG_DIR, img_sc3),
            "50": load_png("ikan16.png", IMG_DIR, img_sc3),
            "40": load_png("ikan17.png", IMG_DIR, img_sc3),
            "30": load_png("ikan18.png", IMG_DIR, img_sc3),
            "20": load_png("ikan19.png", IMG_DIR, img_sc3),
            "10": load_png("ikan20.png", IMG_DIR, img_sc3),
        }

        # ShieldOMeter
        shield_meter_imgs = { # memunculkan gambar shield_meter
            "2": load_png("ShieldOMeter1.png", IMG_DIR, img_sc),
            "1": load_png("ShieldOMeter2.png", IMG_DIR, img_sc),
            "0": load_png("ShieldOMeter3.png", IMG_DIR, img_sc)
        }

        # Powerup
        self.powerup_imgs = { # memunculkan gambar kekuatan
            "fuel": load_png("ikan.png", IMG_DIR, img_sc2),
            "shield": load_png("powerup_shield.png", IMG_DIR, img_sc),
            "coin": load_png("powerup_coin.png", IMG_DIR, img_sc)
        }
        
        # Sprite groups
        self.sprites = pygame.sprite.Group() # pengaturan sprite
        self.enemies = pygame.sprite.Group() # pengaturan musuh
        self.texts = pygame.sprite.Group() # pengaturan tulisan
        self.texts_pa = pygame.sprite.Group() # pengaturan tulisan_pa
        self.powerups = pygame.sprite.Group() # pengaturan kekuatan
        self.particles = pygame.sprite.Group() # pengaturan partikel
        self.trails = pygame.sprite.Group() # pengaturan jalan setapak
        self.moving_stuff = pygame.sprite.Group() # this group is just for detecting overlapping sprites in the spawning functions

        # Player
        self.player = Player(player_imgs) # gambar pemain
        if game_data.equipped_pet != "none": # perlengkapan hewan
            self.pet = Pet(pet_ing, self.player) # hewan sama dengan pemain
        if game_data.equipped_hat != "none": # perlengkapan topi
            self.hat = Hat(hat_img, self.player, img_sc, img_sc * 6) # gambar topi sama dengan pemain juga sebagai aksesoris
        
        # Stats texts saat dikanan permainan
        self.text_stats = Text(self.stats_area.get_width() / 2, 40, "Stats", GAME_FONT, 25, 'white') # pengaturan lebar dari tulisan
        self.tulang_meter = TulangMeter(tulang_meter_imgs, (28, 70), "100", "10") # pengaturan tulang_meter
        self.text_scorelabel = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 3.5, "Score", GAME_FONT, 23, 'white') # pengaturan label skor
        self.text_score = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 2.8, f"{str(self.score).zfill(5)}", GAME_FONT, 23, 'white')  # pengaturan skor
        self.shield_o_meter = TulangMeter(shield_meter_imgs, (16, WIN_SZ[1] / 2.6), "2", "0", False) # pengaturan pelindung/ tulang_meter
        self.text_coinslabel = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 1.3, "Coins", GAME_FONT, 23, 'yellow') # pengaturan tulisan skor dalam koin 
        self.text_coins = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 1.18, f"{str(self.coins).zfill(5)}", GAME_FONT, 23, 'yellow') # pengaturan panjang lebar, dll untuk tulisan skor dalam koin
        self.texts.add(self.text_stats) # menambahkan tulisan stats
        self.texts.add(self.text_scorelabel) # menambahkan tulisan label skor
        self.texts.add(self.text_score) # menambahkan tulisan skor
        self.texts.add(self.text_coinslabel) # menambahkan tulisan skor
        self.texts.add(self.text_coins) # menambahkan tulisan koin

        # Play area text(s) saat gameover
        self.text_gameover = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 4, "GAME OVER!", GAME_FONT, 48, 'white', False) # pengaturan tulisan game_over panjang lebar, jenis font,dll
        self.text_finalscore = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 2.4, "SCORE 00000", GAME_FONT, 32, 'white', False) # pengaturam skor terakhir
        self.text_finalcoin = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 2, "COINS 00000", GAME_FONT, 32, 'white', False) # pengaturan koin terakhir
        self.text_exitbutton = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 1.4, "[X] Exit", GAME_FONT, 32, 'white', False) # pengaturan tombol keluar
        self.texts_pa.add(self.text_gameover) # menambahkan tulisan gameover
        self.texts_pa.add(self.text_finalscore) # menambahkan tulisan skor terakhir
        self.texts_pa.add(self.text_finalcoin) # menambahkan koin terakhir
        self.texts_pa.add(self.text_exitbutton) # menambahkan tombol keluar

    # handle pada gamescene
    def handle_events(self, events): # mengatur dalam game scene
        for event in events:
            if event.type == pygame.KEYDOWN: # tipe KEYDOWN
                # Debug only
                if event.key == pygame.K_e and self.debug_mode: # key pada mode K_e dan mode debug
                    self.global_xspeed += 0.25 # pengaturan kecepatan keseluruhan
                    #self.player.speedx = self.global_xspeed + 1 # pengaturan kecepatan keseluruhan ditambah 1
                    print(self.global_xspeed) # pencetakan kekuatan keseluruhan
                if event.key == pygame.K_q and self.debug_mode: # key pada mode K_q dan mode debug
                    self.orig_gxspeed = self.global_xspeed # pengaturan original kekuatan sama dengan kecepatan keseluruhan
                    self.global_xspeed = 1 # pengaturan kekuatan keseluruhan sama dengan 1 

                if event.key == pygame.K_x and self.can_exit: # key K_x dan bisa keluar
                    game_data.coins += self.coins # data koin
                    if round(self.score) > game_data.highscore: # data skor lebih dari skor tertinggi
                        game_data.highscore = round(self.score) # data skor tertinggi = round skor
                    game_data.times_died += 1 # waktu mati kurang lebih 1
                    game_data.play_time += round(self.cur_playtime / 1000) # pengaturan waktu main
                    self.manager.go_to(TitleScene()) # pengaturan manager diri sendiri dalam judul scene

                if event.key == pygame.K_ESCAPE: # key K_ESCAPE
                    self.manager.go_to(TitleScene())# menuju ke judul scene
                    game_data.play_time += round(self.cur_playtime / 1000) # pengaturan waktu bermain

                    if self.can_exit: # ketika bisa keluar
                        game_data.coins += self.coins # data koin
                        if round(self.score) > game_data.highscore: # skor > skor tertinggi
                            game_data.highscore = round(self.score) # skor tertinggi = skor
                        game_data.times_died += 1 #  pengaturan waktu mati
                        game_data.play_time += round(self.cur_playtime / 1000) # pengaturan waktu mati lanjutan

    def update(self):
        
        # Update crap
        self.cur_playtime += 10
        # Kondisi ketika player mulai game dan player masih hidup
        if self.player.has_started and not self.player.is_dead:
            self.update_difficulty()
            self.score += 0.1
            self.player.fuel -= 0.1 + (self.global_xspeed // 15)
            self.text_score.text = f"{str(round(self.score)).zfill(5)}"

        # Check for enemy collision(tabrakan)
        if self.player.fuel > 0 and not self.player.is_dead:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_rect_ratio(0.7))
            for hit in hits:
                self.offset = self.shake(20,5)
                self.spawn_particles(self.sprites, self.particles, hit.rect.centerx, hit.rect.centery, ['white'], 10)
                self.spawn_shockwave(hit.rect.centerx, hit.rect.centery, 'white')
                if self.player.shield <= 0:
                    self.player.is_dead = True
                else:
                    self.player.shield -= 1
                game_data.times_hit += 1
                
                hit.kill()
                explosion_sfx.play()

        # Kondisi Ketika Player Masih Hidup
        if not self.player.is_dead:
            hits = pygame.sprite.spritecollide(self.player, self.powerups, False, pygame.sprite.collide_rect_ratio(0.7))
            for hit in hits:
                #menampilkan partikel ketika menabrak powerup
                self.spawn_particles(self.sprites, self.particles, self.player.rect.centerx, self.player.rect.centery, [(124,231,20)], 10)
                self.spawn_shockwave(self.player.rect.centerx, self.player.rect.centery, (124,231,20))

                #jika fuel bertambah satu maka pada TulangMeter akan bertambah sebanyak 20
                if hit.type == "fuel":
                    game_data.times_fuelpickup += 1
                    self.player.fuel += 20
                    #jika fuel lebih dari 100 maka fuel tetap sama dengan 100
                    if self.player.fuel > 100:
                        self.player.fuel = 100
                
                elif hit.type == "shield":
                    game_data.times_shieldpickup += 1
                    self.player.shield += 1
                    if self.player.shield > 2:
                        self.player.shield = 2
                elif hit.type == "coin":
                    self.coins += 1
                    self.text_coins.text = f"{str(self.coins).zfill(5)}"
                hit.kill()
                buy_sfx.play()

        # Update background and parallax x position
        self.bg_layer1_x -= self.global_xspeed / 4

        if self.player.has_started:
            # Spawn enemies
            if len(self.enemies) < self.max_enemies:
                self.spawn_enemies()

            # Spawn powerups
            if len(self.powerups) < self.max_powerups:
                self.spawn_powerup()

        # Spawn trail
        if len(self.trails) < 64 and self.player.fuel > 0:
            self.spawn_trail(self.player.rect.left + 10, self.player.rect.centery, ['white'], 8)
        
        # Move enemies
        for sprite in self.enemies:
            sprite.rect.x -= self.global_xspeed

        # Move powerups
        for sprite in self.powerups:
            sprite.rect.x -= self.global_xspeed

        # Digunakan untuk membatasi pergerakan player
        if self.player.has_started:
            # Untuk membatasi pergerakan player ke atas
            if self.player.rect.top < 0:
                self.player.rect.top = 0
                self.player.speedy = 1
            # Untuk membatasi pergerakan player ke atas yang melebihi batas layar
            # Ketika pergerakan player melebihi batas layar, fuel lebih dari 0 dan dalam kondisi player masih hidup maka kondisi tersebut akan membuat player mati
            if self.player.rect.top > self.play_area.get_height() and self.player.fuel > 0 and not self.player.is_dead:
                self.player.is_dead = True
            # Untuk membatasi pergerakan player ke kiri
            if self.player.rect.left < 0:
                self.player.rect.left = 0
            # Untuk membatasi pergerakan player ke kanan melebihi batas layar
            if self.player.rect.right > self.play_area.get_width():
                self.player.rect.right = self.play_area.get_width()

        # Keadaan Ketika Player mati akan muncul teks game over dan exit_ticks
        if self.player.is_dead:
            self.exit_ticks += 10
            self.text_gameover.visible = True

            # Ketika player mati, maka score dan coin akan diperlihatkan.
            # Begitupun dengan button exit sehingga player bisakeluar dari game dan dapat memulai game yang baru dari awal
            if self.exit_ticks > 500:
                self.text_finalscore.visible = True # Menampilkan Score
                self.text_finalcoin.visible = True  # Menampilkan Coin
                self.text_finalscore.text = "Score " + str(round(self.score))
                self.text_finalcoin.text = "Coin " + str(self.coins)
                self.text_exitbutton.visible = True # Menampilkan exit button
                self.can_exit = True    # Player dapat exit game

        # Untuk update data sprites, player, texts, dan texts_pa
        self.sprites.update()
        self.player.update()
        self.texts.update()
        self.texts_pa.update()
        if game_data.equipped_pet != "none":
            self.pet.update()
        if game_data.equipped_hat != "none":
            self.hat.update()
        self.tulang_meter.update(self.player.fuel)
        self.shield_o_meter.update(self.player.shield)

    # Fungsi untuk menampilkan objek
    def draw(self, window):
        window.fill('#87CEEB')  # Memberi warna background
        window.blit(self.play_area, (32,32))    # Update area game
        window.blit(self.stats_area, (WIN_SZ[0] / 1.3, 30)) # Update Stats game
        self.stats_area.fill('#87CEEB') # Memberi warna pada stats area
        self.play_area.fill('black')      # Memberi warna pada play area
        window.blit(window, next(self.offset)) # Untuk update window
        
        # Untuk menampilkan background
        self.draw_background(self.play_area, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x, "horizontal")
        
        # Menampilkan play area dalam sprites
        self.sprites.draw(self.play_area)
        # Menampilkan play area dalam group player
        self.player.draw(self.play_area)
        if game_data.equipped_pet != "none":
            self.pet.draw(self.play_area)
        if game_data.equipped_hat != "none":
            self.hat.draw(self.play_area)
        self.play_area.blit(self.border_img, (0,0))
        self.play_area.blit(self.color_correction, (0,0))
        
        # Menampilkan tulang_meter, shield.o meter, texts dalam stats area
        self.tulang_meter.draw(self.stats_area)
        self.shield_o_meter.draw(self.stats_area)
        self.texts.draw(self.stats_area)
        # Menampilkan texts_pa dalam play area
        self.texts_pa.draw(self.play_area)
        pygame.draw.rect(self.color_correction, (0,0,255), (0,0,self.play_area.get_width(), self.play_area.get_height()))

    #musuh muncul
    def spawn_enemies(self):
        o = Obstacle(choice(self.obstacle_imgs), self.play_area)
        # Spawn only non-overlapping sprites
        if not pygame.sprite.spritecollide(o, self.moving_stuff, False, pygame.sprite.collide_rect_ratio(2)):
            self.sprites.add(o)
            self.enemies.add(o)
            self.moving_stuff.add(o)
        else:
            del o
    # Menampilkan Background
    def draw_background(self, surf, img, img_rect, pos, direction="vertical"):
        # Ketika arah vertical
        if direction == "vertical":
            surf_h = surf.get_height()
            rel_y = pos % img_rect.height
            surf.blit(img, (0, rel_y - img_rect.height))

            if rel_y < surf_h:
                surf.blit(img, (0, rel_y))
        # Ketika arah horizontal
        elif direction == "horizontal":
            surf_w = surf.get_width()
            rel_x = pos % img_rect.width
            surf.blit(img, (rel_x - img_rect.width, 0))

            if rel_x < surf_w:
                surf.blit(img, (rel_x, 0))

    def spawn_powerup(self):
        p = Powerup(self.powerup_imgs, self.play_area)
        # Spawn only non-overlapping sprites
        if not pygame.sprite.spritecollide(p, self.moving_stuff, False, pygame.sprite.collide_rect_ratio(2)):
            self.sprites.add(p)
            self.powerups.add(p)
            self.moving_stuff.add(p)
        else:
            del p

    def spawn_particles(self, sprites, particles, x, y, colors, amount):
        for _ in range(amount):
            p = Particle(x, y, colors)
            particles.add(p)
            sprites.add(p)

    def spawn_shockwave(self, x, y, color):
        s = Shockwave(x, y, color, 128)
        self.sprites.add(s)

    def shake(self, intensity, n):
        # Credits to sloth from StackOverflow, thanks buddy!
        shake = -1
        for _ in range(n):
            for x in range(0, intensity, 5):
                yield (x*shake, 0)
            for x in range(intensity, 0, 5):
                yield (x*shake, 0)
            shake *= -1
        while True:
            yield (0, 0)

    def update_difficulty(self):
        self.difficulty_ticks += 10
        if self.difficulty_ticks >= self.difficulty_increase_delay and self.difficulty_level != 15:
            self.difficulty_ticks = 0
            if self.difficulty_level < 5:
                self.max_enemies += 1
            if self.difficulty_level < 1:
                self.max_powerups += 1
            self.global_xspeed += 0.10
            self.player.speedx = self.global_xspeed
            self.difficulty_level += 1
            if self.difficulty_increase_delay > 2500:
                self.difficulty_increase_delay -= 500
            #print(self.difficulty_level, self.difficulty_increase_delay)

    def spawn_trail(self, x, y, colors, amount):
        for _ in range(amount):
            t = JetpackTrail(x, y, colors)
            self.trails.add(t)
            self.sprites.add(t)

# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_SZ)
    # Mengatur caption layar
    pygame.display.set_caption(TITLE)
    # Mengatur icon pada layar
    pygame.display.set_icon(load_png("kitty.png", IMG_DIR, 1))
    # Mengatur agar mouse tidak terlihat
    pygame.mouse.set_visible(False)

    # Load and play music
    # Mengatur musik
    pygame.mixer.music.load(os.path.join(SFX_DIR, "music.ogg"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    # Loop
    running = True
    manager = SceneManager(TitleScene())
    clock = pygame.time.Clock()
    FPS = 60

    while running:
        # waktu untuk menganimasikan sebesar FPS atau 60s
        clock.tick(FPS)
        
        if pygame.event.get(QUIT):
            running = False

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.draw(window)

        pygame.display.flip()
    
# Run the application loop
main()

# Exit pygame and application, and save user data
pygame.quit()

outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
pickle.dump(game_data, outfile)
outfile.close()

sys.exit()