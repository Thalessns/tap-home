import network
import urequests
import json
import time

class ConectorInternet:
    def __init__(self, ssid, password, server_url):
        self.ssid = ssid
        self.password = password
        self.server_url = server_url
        self.wlan = network.WLAN(network.STA_IF)
        
    def conectar_wifi(self):
        # --- FIX PARA "Wifi Internal Error" ---
        # Desliga e liga a interface para limpar o estado do rádio
        try:
            self.wlan.active(False)
            time.sleep(0.5) 
            self.wlan.active(True)
        except Exception as e:
            print(f"Aviso ao reiniciar rádio: {e}")

        if not self.wlan.isconnected():
            print(f'Conectando a {self.ssid}...')
            try:
                self.wlan.connect(self.ssid, self.password)
            except OSError as error:
                print(f"Erro ao solicitar conexão: {error}")
                self.wlan.active(False) # Reseta para a próxima tentativa
                return False
            
            # Aguarda conexão com timeout
            tentativas = 0
            while not self.wlan.isconnected() and tentativas < 20:
                time.sleep(0.5)
                tentativas += 1
                print(".", end="")
        
        if self.wlan.isconnected():
            print('\nWi-Fi Conectado:', self.wlan.ifconfig())
            return True
        else:
            print('\nFalha ao conectar no Wi-Fi.')
            self.wlan.active(False) # Desliga para economizar e limpar erro
            return False

    def enviar_leitura(self, uid_str):
        if not self.wlan.isconnected():
            print("Wi-Fi desconectado. Tentando reconectar...")
            if not self.conectar_wifi():
                return None

        print(f"Enviando {uid_str} para API...")
        
        try:
            # Monta a URL com o parâmetro tag_id
            url_completa = f"{self.server_url}?tag_id={uid_str}"
            response = urequests.get(url_completa)
            retorno = None
            
            # Verifica sucesso (200-299)
            if response.status_code >= 200 and response.status_code < 300:
                try:
                    retorno = response.json()
                except:
                    # Se não for JSON, retorna o texto puro (fallback)
                    retorno = response.text
                print(f"Sucesso! (Status {response.status_code})")
            else:
                print(f"Erro no servidor: {response.status_code} - {response.text}")
                
            response.close() # Sempre fechar a conexão
            return retorno
            
        except Exception as e:
            print("Erro na requisição HTTP:", e)
            return None