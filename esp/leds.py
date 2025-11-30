from machine import Pin
from neopixel import NeoPixel
import time
import random

class ControleLED:
    def __init__(self, pino_gpio, qtd_leds):
        # Configura o pino e a quantidade de LEDs
        self.np = NeoPixel(Pin(pino_gpio), qtd_leds)
        self.qtd = qtd_leds
        self.limpar() # Começa apagado

    def limpar(self):
        """Apaga todos os LEDs"""
        for i in range(self.qtd):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def preencher(self, r, g, b):
        """Acende todos os LEDs com uma cor específica"""
        for i in range(self.qtd):
            self.np[i] = (r, g, b)
        self.np.write()

    def indicar_processamento(self):
        """Cor Azul suave para indicar que está pensando"""
        self.preencher(0, 0, 50) 

    def indicar_sucesso(self):
        """Pisca Verde"""
        for _ in range(2):
            self.preencher(0, 255, 0) # Verde Forte
            time.sleep(0.2)
            self.limpar()
            time.sleep(0.1)

    def indicar_erro(self):
        """Pisca Vermelho"""
        for _ in range(3):
            self.preencher(255, 0, 0) # Vermelho Forte
            time.sleep(0.1)
            self.limpar()
            time.sleep(0.1)
            
    def processa_led_id(self, id):
        print(type(id))
        if id == 1:
            self.preencher(255, 0, 0)
        elif id == 2:
            self.preencher(0, 255, 0)
        elif id == 3:
            self.preencher(0, 0, 255)
        elif id == 4:
            # Cor Aleatória
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.preencher(r, g, b)
        