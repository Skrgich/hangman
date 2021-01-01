import random
import pygame

pygame.init()

prozor_sirina=1280
prozor_visina=720
prozor=pygame.display.set_mode((prozor_sirina,prozor_visina))

BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)

btn_font = pygame.font.SysFont("arial", 35)
guess_font = pygame.font.SysFont("monospace", 50)
lost_font = pygame.font.SysFont('arial', 45)
rijec = ''
tipke = []
pogodjeno = []
hangmanPics = [pygame.image.load('0.png'), pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'), pygame.image.load('4.png'), pygame.image.load('5.png'), pygame.image.load('6.png')]

ikona=pygame.image.load('icon.png')
pygame.display.set_icon(ikona)

pygame.display.set_caption('Hangman')

pozadina=pygame.image.load('background.png')
poz_lok=pozadina.get_rect()



greske = 0

def redraw_game_window():
    global pogodjeno
    global hangmanPics
    global greske

    prozor.fill([255, 255, 255])
    prozor.blit(pozadina, poz_lok)

    for i in range(len(tipke)):
        if tipke[i][4]:
            pygame.draw.rect(prozor, BLACK, ((tipke[i][1]-25, tipke[i][2]-25),(50,50)))
            pygame.draw.rect(prozor, tipke[i][0], ((tipke[i][1]-23, tipke[i][2]-23),(46,46) ))#tipke[i][3] - 2
            oznaka_tipke = btn_font.render(chr(tipke[i][5]), 1, BLACK)
            prozor.blit(oznaka_tipke, (tipke[i][1] - (oznaka_tipke.get_width() / 2), tipke[i][2] - (oznaka_tipke.get_height() / 2)))
    
    odmaknuto= raz_rijec(rijec,pogodjeno)
    oznaka_tipke_1=guess_font.render(odmaknuto, 1, BLACK)
    otk_tekst = oznaka_tipke_1.get_rect()
    sirina =otk_tekst [2]

    prozor.blit(oznaka_tipke_1,(prozor_sirina/2 - sirina/2, 550))
    slika=hangmanPics[greske]
    prozor.blit(slika, (prozor_sirina/2 - slika.get_width()/2 + 20, 220))
    pygame.display.update()



def slucajna_rijec():
    file = open('words.txt')
    f = file.readlines()
    print(f)
    i = random.randrange(0, len(f) )
    return f[i][:-1]

def vjesanje(pokusaj):
    global rijec
    if pokusaj.lower() not in rijec.lower():
        return True
    else:
        return False

def raz_rijec(rijec, pogodjeno=[]):
    raz_rj=''
    pog_slova= pogodjeno
    for i in range(len(rijec)):
        if rijec[i] != ' ':
            raz_rj+='_ '
            for j in range(len(pog_slova)):
                if rijec[i].upper() == pog_slova[j]:
                    raz_rj= raz_rj[:-2]
                    raz_rj+=rijec[i].upper()+ ' '
        else:
            raz_rj+= ' '
    return raz_rj

def pritisak_gumba(x,y):
    for i in range(len(tipke)):
        if x<tipke[i][1] + 20 and x > tipke[i][1]-20 and y<tipke[i][2] +20 and y>tipke[i][2]-20:
            return tipke[i][5]
    return None

def kraj(pobjeda=False):
    global greske
    gubitak_txt="You lost, press any key to continue"
    pobjeda_txt="You won! Press any key to continue"
    redraw_game_window()
    pygame.time.delay(1000)

    prozor.fill([255, 255, 255])
    prozor.blit(pozadina, poz_lok)
    if pobjeda==True:
        oznaka=lost_font.render(pobjeda_txt, 1, BLACK)
    else:
        oznaka=lost_font.render(gubitak_txt, 1, BLACK)

    rijec_txt=lost_font.render(rijec.upper(),1,BLACK)
    rijec_je=lost_font.render("The word was: ",1,BLACK)

    prozor.blit(rijec_txt, (prozor_sirina/2 - rijec_txt.get_width()/2, 295))
    prozor.blit(rijec_je,   (prozor_sirina/2 - rijec_je.get_width()/2, 245))
    prozor.blit(oznaka, (prozor_sirina / 2 - oznaka.get_width() / 2, 140))

    pygame.display.update()

    ponovno=True
    while ponovno:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                ponovno = False
    reset()

def reset():
    global pogodjeno
    global tipke
    global rijec
    global greske
    for i in range(len(tipke)):
        tipke[i][4] = True

    greske=0
    rijec=slucajna_rijec()
    pogodjeno=[]

razmak = round(prozor_sirina / 13)
for i in range(26):
    if i<13:
        y=45
        x=50+(razmak * i)
    else:
        x=50+(razmak * (i%13))
        y=125
    tipke.append([LIGHT_BLUE,x,y,25,True,65+i])
    #([boja, x_pos, y_pos, radius, vidljivost, slovo])

rijec=slucajna_rijec()
u_igri=True

while u_igri:
    redraw_game_window()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            u_igri=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                u_igri=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            poz_klika=pygame.mouse.get_pos()
            slovo=pritisak_gumba(poz_klika[0],poz_klika[1])
            if slovo!=None:
                pogodjeno.append(chr(slovo))
                tipke[slovo-65][4]=None
                if vjesanje(chr(slovo)):
                    if greske==5:
                        kraj()
                    else:
                        greske+=1
                else:
                    print(raz_rijec(rijec,pogodjeno))
                    if raz_rijec(rijec,pogodjeno).count('_')==0:
                        kraj(True)


pygame.quit()