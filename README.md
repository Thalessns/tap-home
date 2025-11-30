-----

#  Leitor NFC Inteligente com ESP32

Este projeto implementa um sistema IoT utilizando **MicroPython** e um **ESP32** para ler tags NFC (via módulo PN532), consultar uma API externa e executar feedbacks visuais (LEDs NeoPixel) e sonoros (Buzzer) baseados na resposta do servidor.

 <img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/99c713aa-1c95-4838-b7c0-f2856db36791" />

##  Hardware Necessário

  * **Microcontrolador:** ESP32
  * **Leitor NFC:** Módulo PN532 (Configurado em modo SPI)
  * **Visual:** Fita ou Anel de LEDs endereçáveis (NeoPixel/WS2812)
  * **Áudio:** Buzzer passivo
  * **Fonte de Alimentação:** 5V (USB ou externa)

###  Pinagem (Wiring)

Conforme configurado em `main.py`:

| Componente | Pino Módulo | GPIO ESP32 | Observação |
| :--- | :--- | :--- | :--- |
| **PN532 (SPI)** | SCK | 18 | Clock |
| | MISO | 19 | Master In Slave Out |
| | MOSI | 23 | Master Out Slave In |
| | CS / SS | 5 | Chip Select |
| **LEDs** | DIN | 4 | Data In |
| **Buzzer** | I/O | 15 | PWM |

> **Nota:** Certifique-se de que o GND de todos os componentes esteja conectado ao GND do ESP32.

##  Configuração

Antes de rodar o projeto, edite o arquivo `main.py` com suas credenciais e endpoint:

```python
# --- CONFIGURAÇÕES DO USUÁRIO ---
SSID = "SEU_WIFI_AQUI"
SENHA = "SUA_SENHA_AQUI"
URL_API = "https://seu-backend.com/api/tag" 
```

###  Formato da API

O sistema envia um GET request: `URL_API?tag_id=UID_DA_TAG`

O sistema espera uma resposta **JSON** com a seguinte estrutura para decidir o que fazer:

```json
{
  "routine_id": "1",      // Se presente, toca uma rotina complexa (luz + som)
  "led_color": 2,         // Se routine_id for null, usa cor fixa (1=Vermelho, 2=Verde, etc)
  "music_id": 1           // Se routine_id for null, toca música (1=Mario, 2=Tetris, etc)
}
```

##  Estrutura dos Arquivos

  * **`main.py`**: Arquivo principal. Gerencia o loop de leitura, conexão Wi-Fi e orquestra os periféricos.
  * **`pn532.py`**: Driver para comunicação com o módulo NFC PN532 via protocolo SPI.
  * **`conexao.py`**: Gerencia a conexão Wi-Fi (com reconexão automática) e requisições HTTP (`urequests`).
  * **`leds.py`**: Classe para controle básico dos LEDs (cores sólidas, indicação de erro/sucesso).
  * **`rotina.py`**: Implementa animações complexas de luz combinadas com sequências de tons no buzzer.
  * **`buzzer.py`**: *Music Player* com notas musicais e músicas pré-programadas (Mario Bros, Tetris, Nokia).

##  Como Executar

1.  Instale o firmware MicroPython no seu ESP32.
2.  Faça o upload de todos os arquivos `.py` para a raiz do dispositivo (usando Thonny IDE ou `ampy`).
3.  Reinicie o ESP32.
4.  O sistema irá:
      * Acender os LEDs (Branco fraco) ao iniciar.
      * Tentar conectar ao Wi-Fi (Pisca amarelo/erro se falhar).
      * Piscar **Verde** ao conectar com sucesso.
      * Aguardar a aproximação de uma Tag NFC.

## 📦 Dependências

  * Biblioteca padrão do MicroPython (`machine`, `network`, `time`, `neopixel`, `urequests`).
  * Driver `pn532.py` (incluso no repositório, portado/adaptado de Adafruit/CircuitPython).

-----
