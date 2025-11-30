from machine import Pin, SPI
from pn532 import PN532
import time

# Importamos a nossa nova classe
from conexao import ConectorInternet
from leds import ControleLED
from rotina import ControleRotina
from buzzer import MusicPlayer
# --- CONFIGURAÇÕES DO USUÁRIO ---
SSID = "S23 Ultra de pedro"
SENHA = "pedrobibi2535"
URL_API = "https://cf-handler.onrender.com/tag" # Use seu servidor aqui

# --- INICIALIZAÇÃO DOS OBJETOS ---

# Configuração dos LEDs
PINO_LED = 4      # Pino onde ligou o DIN da fita
NUM_LEDS = 20      # Quantos LEDs tem na sua fita/anel
PINO_BUZZER = 15

# 1. Instancia o objeto de conexão
internet = ConectorInternet(SSID, SENHA, URL_API)
leds = ControleLED(PINO_LED, NUM_LEDS)
rotina = ControleRotina(PINO_LED, NUM_LEDS, PINO_BUZZER) 
player = MusicPlayer(PINO_BUZZER)

# 2. Configura o Hardware PN532 (SPI)
# VSPI Padrão: CLK=18, MISO=19, MOSI=23, CS=5
spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs_pin = Pin(5, Pin.OUT)
cs_pin.on()

pn = PN532(spi, cs_pin)

def setup():
    # Indica visualmente que o sistema ligou (Luz Branca Fraca)
    leds.preencher(20, 20, 20)
    print("Iniciando sistema...")
    time.sleep(1)

    # --- BLOCO DE CONEXÃO ROBUSTA ---
    print(f"Tentando conectar ao Wi-Fi: {SSID}")
    
    # Enquanto NÃO conseguir conectar, fica preso neste loop
    while not internet.conectar_wifi():
        print("Falha na conexão. Tentando novamente em 3 segundos...")
        
        # Feedback Visual de Erro (Pisca Vermelho)
        leds.indicar_erro()
        
        # Espera um pouco antes de tentar de novo
        time.sleep(3)
        
        # Volta para cor de "Tentando" (Amarelo ou Branco)
        leds.preencher(20, 20, 0) 

    # Se saiu do loop, é porque conectou!
    print("Wi-Fi Conectado com Sucesso!")
    leds.indicar_sucesso() # Pisca Verde
    time.sleep(0.5)

    # --- INICIALIZAÇÃO DO NFC ---
    print("Inicializando Leitor NFC...")
    try:
        pn.SAM_configuration()
        print("PN532 Configurado.")
    except Exception as e:
        print(f"Erro ao iniciar PN532: {e}")
        leds.indicar_erro()
    
    # Limpa os LEDs e deixa o sistema pronto
    leds.limpar()
    print("Sistema pronto. Aproxime a TAG.")

def loop():
    while True:
        # Leitura da TAG
        uid = pn.read_passive_target(timeout=100)
        print(uid)
        
        if uid is not None:
            # Formata o UID
            uid_str = ''.join('{:02x}'.format(i) for i in uid).upper()
            print(f"\n[EVENTO] Tag lida: {uid_str}")
            
            leds.indicar_processamento()
            
            # --- AQUI USAMOS A CLASSE PARA ENVIAR ---
            resposta = internet.enviar_leitura(uid_str)
            print(resposta)
            
            if resposta:
                print(resposta) 
                if resposta["routine_id"]:
                    rotina.definir_rotina(resposta["routine_id"])
                else:
                    leds.processa_led_id(resposta["led_color"])
                    player.processa_music_id(resposta["music_id"])
                    
                    
            
            # Delay para evitar múltiplas leituras seguidas
            time.sleep(5)
            print("Pronto para próxima leitura.")
            print("Aaaaaaaaaaa")
        else:
            # Mantém o loop rodando sem travar
            pass

# Execução
try:
    setup()
    loop()
except KeyboardInterrupt:
    print("Encerrado pelo usuário.")


