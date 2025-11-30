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
  * **`pn532.py`**: Driver para comunicação com o módulo NFC PN532 via protocolo SPI. https://github.com/Carglglz/NFC_PN532_SPI
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

##  Como importar e editar o .aia no MIT App Inventor

Siga o passo a passo abaixo para importar o aplicativo Android (arquivo `.aia`) e personalizar o comportamento diretamente no [MIT App Inventor](https://ai2.appinventor.mit.edu/).

1. **Baixe o arquivo .aia**
  - Localize o arquivo dentro da pasta `frontend/` deste repositório (ou faça download direto do link fornecido).
  - Guarde o arquivo em um local fácil de encontrar, pois será enviado para o App Inventor.

2. **Acesse o MIT App Inventor**
  - Entre em <https://ai2.appinventor.mit.edu/> usando sua conta Google.
  - Caso seja o primeiro acesso, aceite os termos de uso e crie um projeto vazio apenas para desbloquear a interface.

3. **Importe o projeto .aia**
  - No canto superior esquerdo, clique em **Projects → Import project (.aia) from my computer**.
  - Selecione o arquivo `.aia` baixado e confirme com **OK**.
  - O projeto aparecerá na lista “My Projects”; clique nele para abrir.

4. **Organize o projeto**
  - Clique em **Projects → Save project as…** para duplicar e renomear (opcional, mas recomendado para manter um backup).
  - Utilize nomes curtos e sem espaços para facilitar deploys futuros.

5. **Edite a interface (Designer)**
  - Aba **Designer**: arraste componentes, altere textos, ícones e cores dos botões.

6. **Atualize a lógica (Blocks)**
  - Aba **Blocks**: conecte blocos para mudar fluxos, validações ou chamadas HTTP.
  - Procure pelo bloco pela URL da API (`Variável Global` contendo o endpoint) e ajuste para apontar para o backend correto.

7. **Teste rapidamente**
  - Instale o app **MIT AI2 Companion** no Android.
  - Clique em **Connect → AI Companion** dentro do App Inventor e escaneie o QR Code para visualizar as alterações em tempo real.
  - Observe o log na aba **Blocks** para depurar erros de request (por exemplo, códigos HTTP diferentes de 200).

8. **Gere um novo APK**
  - Após validar, vá em **Build → App (provide QR code for .apk)** ou **Build → App (save .apk to my computer)**.
  - Distribua o APK atualizado para os dispositivos que irão interagir com o leitor NFC.

## Tutorial: Deploy da API no Render

O backend FastAPI localizado em `src/app/main.py` pode ser publicado como um **Web Service** no Render para ser consumido pelo aplicativo mobile.

### 1. Preparar o repositório

1. Confirme que o projeto está versionado no GitHub e contém `entrypoint.py`, `requirements.txt`, `setup.py` e a pasta `src/` atualizados.
2. (Opcional) Inclua `gunicorn` no `requirements.txt` para usar o servidor de produção recomendado.
3. Faça push das mudanças na branch que servirá de base para o deploy (ex.: `main`).

### 2. Criar o serviço no Render

1. No painel do Render escolha **New → Web Service** e conecte sua conta GitHub.
2. Selecione o repositório `cf-handler` e a branch desejada.
3. Defina um nome (ex.: `cf-handler-api`) e deixe o plano **Free**.
4. Em **Environment** escolha **Python 3** (conforme `setup.py`).

### 3. Comandos de Build e Start

- **Build command**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

- **Start command** (recomendado)

```bash
gunicorn -k uvicorn.workers.UvicornWorker src.app.main:app --bind 0.0.0.0:$PORT --workers ${WEB_CONCURRENCY:-2}
```

> Alternativa: `python entrypoint.py`, desde que defina `APP_HOST=0.0.0.0` e `APP_PORT=$PORT` nas variáveis de ambiente.

### 4. Variáveis de ambiente

Configure em **Environment → Environment Variables**:

| Nome | Valor | Motivo |
| --- | --- | --- |
| `APP_HOST` | `0.0.0.0` | Faz o FastAPI escutar a interface pública. |
| `APP_PORT` | `$PORT` | Mantém compatibilidade com `AppConfig`. |
| `DATABASE_URL` (opcional) | URL do banco (SQLite, MySQL, etc.) | Personalize se migrar do SQLite local. |
| Segredos adicionais | tokens, URLs de APIs | Usar variáveis ou Secret Files do Render. |

### 5. Banco de dados

- **SQLite**: crie um *Persistent Disk* (ex.: `/data`) e altere `src/database/config.py` para `sqlite+aiosqlite:///data/sqlite_db.db`.
- **MySQL/Postgres**: crie um serviço gerenciado, copie a string de conexão e sobrescreva o valor na variável `DATABASE_URL`. Ajuste o módulo `Database` para usar o driver correspondente.

### 6. Deploy e verificação

1. Clique em **Create Web Service** e acompanhe o primeiro build.
2. Caso alguma dependência falhe, corrija no repositório e envie novo commit; o Render reconstruirá automaticamente (Auto Deploy).
3. Após o status “Live”, teste os endpoints:

```bash
curl https://<seu-servico>.onrender.com/musics
curl "https://<seu-servico>.onrender.com/tag?tag_id=ABC123"
```

4. Abra `/docs` para conferir o Swagger exposto pelo FastAPI.
5. Atualize o aplicativo/ESP32 para apontar para a nova URL do Render.

##  Como testar todo o fluxo

1. **Garanta o backend online**  
  - Deploy no Render publicado e respondendo (`curl https://<servico>.onrender.com/tag?tag_id=test`).
  - Verifique os logs do Render e anote a URL pública, pois será usada no app e no ESP32.

2. **Instale e abra o aplicativo (.apk)**  
  - Baixe o APK gerado a partir do MIT App Inventor, permita instalações de fonte externa e abra o app.  
  - Nas configurações iniciais, confirme se a URL da API aponta para o domínio do Render.

3. **Ligue o ESP32**  
  - Energize via USB ou fonte 5 V; acompanhe o feedback dos LEDs para confirmar conexão Wi-Fi.  
  - Se a conexão falhar, revise SSID/SENHA no `main.py` e reinicie o microcontrolador.

4. **Cadastre uma tag pelo aplicativo**  
  - Toque em **“Cadastre-se!”** e aproxime a tag NFC da parte traseira do celular para preencher `Tag Lida: {TAG_ID}`.  
  - Escolha cor, música e (opcionalmente) rotina; confirme em **“Cadastrar Tag Agora!”**.  
  - Verifique se a API respondeu com sucesso via logs no Render.

5. **Valide no hardware**  
  - Encoste a mesma tag no PN532 conectado ao ESP32.
  - Aguarde a chamada HTTP → o servidor retorna as preferências → o ESP aciona LEDs/Buzzer conforme configurado.  
  - Caso não ocorra nada, monitore o serial do ESP (Thonny/rshell) e confirme se a resposta JSON contém os campos esperados.
-----
