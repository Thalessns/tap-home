from machine import Pin, PWM
from neopixel import NeoPixel
import time
import random
import math

class ControleRotina:
    def __init__(self, pino_led, qtd_leds, pino_buzzer):
        self.np = NeoPixel(Pin(pino_led), qtd_leds)
        self.qtd = qtd_leds
        self.buzzer = PWM(Pin(pino_buzzer))
        self.buzzer.duty(0)
        self.buzzer.freq(1000)
        
        # Estado atual
        self.rotina_atual = None 
        self.passo = 0
        
        # Config do modo calmo
        self.paleta_calma = [(0, 20, 100), (0, 100, 100), (50, 0, 80)]
        self.cor_calma_atual = (0, 0, 50)

    def limpar(self):
        for i in range(self.qtd):
            self.np[i] = (0, 0, 0)
        self.np.write()
        self.buzzer.duty(0)

    def definir_rotina(self, id_rotina):
        """Define qual será a próxima animação"""
        print(f"Alterando rotina para: {id_rotina}")
        self.rotina_atual = str(id_rotina)
        self.executar_passo()
        self.limpar() # Limpa o anterior antes de começar o novo

    def executar_passo(self):
        """Executa UM quadro da animação e retorna imediatamente"""
        
        if self.rotina_atual == "1":
            try:
                cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
                while True:
                    cor = random.choice(cores)
                    tom = random.randint(100, 800)
                    self.buzzer.freq(tom)
                    self.buzzer.duty(512)
                    for i in range(self.qtd): self.np[i] = cor
                    self.np.write()
                    time.sleep_ms(100)
                    self.buzzer.duty(0)
                    self.limpar()
                    time.sleep_ms(100)
            except KeyboardInterrupt:
                self.limpar()

        elif self.rotina_atual == "2":
            try:
                paleta = [(0, 20, 100), (0, 100, 100), (50, 0, 80)]
                notas = [659, 784, 880, 987, 1175, 1318]
                r, g, b = random.choice(paleta)
                fator_largura, fator_movimento = 0.5, 0.2
                
                # Roda por um tempo longo, mas não infinito neste exemplo para poder testar outras
                for t in range(500): 
                    for i in range(self.qtd):
                        angulo = (i * fator_largura) + (t * fator_movimento)
                        brilho = (math.sin(angulo) + 1) / 2 
                        self.np[i] = (int(r * brilho), int(g * brilho), int(b * brilho))
                    self.np.write()
                    
                    if random.random() < 0.15:
                        self.buzzer.freq(random.choice(notas))
                        self.buzzer.duty(100)
                    else:
                        self.buzzer.duty(0)
                    time.sleep_ms(50)
                self.limpar()
            except KeyboardInterrupt:
                self.limpar()

        else:
            # Se não tiver rotina, garante que está tudo apagado
            # time.sleep_ms(50)
            pass