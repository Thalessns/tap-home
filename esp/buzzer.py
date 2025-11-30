from machine import Pin, PWM
from time import sleep

class MusicPlayer:
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty_u16(0) # Silêncio inicial
        
        # Frequências das notas (Hz)
        self.NOTES = {
            'B0': 31, 'C1': 33, 'CS1': 35, 'D1': 37, 'DS1': 39, 'E1': 41, 'F1': 44, 'FS1': 46, 'G1': 49, 'GS1': 52, 'A1': 55, 'AS1': 58, 'B1': 62,
            'C2': 65, 'CS2': 69, 'D2': 73, 'DS2': 78, 'E2': 82, 'F2': 87, 'FS2': 93, 'G2': 98, 'GS2': 104, 'A2': 110, 'AS2': 117, 'B2': 123,
            'C3': 131, 'CS3': 139, 'D3': 147, 'DS3': 156, 'E3': 165, 'F3': 175, 'FS3': 185, 'G3': 196, 'GS3': 208, 'A3': 220, 'AS3': 233, 'B3': 247,
            'C4': 262, 'CS4': 277, 'D4': 294, 'DS4': 311, 'E4': 330, 'F4': 349, 'FS4': 370, 'G4': 392, 'GS4': 415, 'A4': 440, 'AS4': 466, 'B4': 494,
            'C5': 523, 'CS5': 554, 'D5': 587, 'DS5': 622, 'E5': 659, 'F5': 698, 'FS5': 740, 'G5': 784, 'GS5': 831, 'A5': 880, 'AS5': 932, 'B5': 988,
            'C6': 1047, 'CS6': 1109, 'D6': 1175, 'DS6': 1245, 'E6': 1319, 'F6': 1397, 'FS6': 1480, 'G6': 1568, 'GS6': 1661, 'A6': 1760, 'AS6': 1865, 'B6': 1976,
            'C7': 2093, 'CS7': 2217, 'D7': 2349, 'DS7': 2489, 'E7': 2637, 'F7': 2794, 'FS7': 2960, 'G7': 3136, 'GS7': 3322, 'A7': 3520, 'AS7': 3729, 'B7': 3951,
            'REST': 0
        }

    def play_tone(self, note, duration_ms):
        freq = self.NOTES.get(note, 0)
        
        if freq > 0:
            self.buzzer.freq(freq)
            self.buzzer.duty_u16(32768) # 50% volume
        else:
            self.buzzer.duty_u16(0)
            
        sleep(duration_ms / 1000)
        self.buzzer.duty_u16(0) # Para o som (staccato)
        sleep(0.02) # Pequena pausa entre notas para não embolar

    def play_song(self, song_data, tempo_bpm):
        # Calcula a duração de uma semínima (beat) em ms
        beat_duration = 60000 / tempo_bpm
        
        print(f"Tocando música a {tempo_bpm} BPM...")
        
        for note, length in song_data:
            # length: 4 = semínima, 8 = colcheia, etc.
            # Convertendo notação musical para duração em ms
            duration = (beat_duration * 4) / length
            self.play_tone(note, duration)
        
        print("Fim da música.")
        sleep(1)
        
    def processa_music_id(self, id):
        mario_bros = [
        ('E5',8), ('E5',8), ('REST',8), ('E5',8), ('REST',8), ('C5',8), ('E5',4), 
        ('G5',4), ('REST',4), ('G4',4), ('REST',4),
        ('C5',4), ('G4',8), ('REST',8), ('E4',4), ('A4',4), ('B4',4), ('AS4',8), ('A4',4),
        ('G4',6), ('E5',6), ('G5',6), ('A5',4), ('F5',8), ('G5',8),
        ('REST',8), ('E5',4), ('C5',8), ('D5',8), ('B4',4)
        ]

        tetris_theme = [
            ('E5',4), ('B4',8), ('C5',8), ('D5',4), ('C5',8), ('B4',8),
            ('A4',4), ('A4',8), ('C5',8), ('E5',4), ('D5',8), ('C5',8),
            ('B4',4), ('B4',8), ('C5',8), ('D5',4), ('E5',4),
            ('C5',4), ('A4',4), ('A4',4), ('REST',4),
            ('D5',4), ('F5',8), ('A5',4), ('G5',8), ('F5',8),
            ('E5',4), ('C5',8), ('E5',4), ('D5',8), ('C5',8),
            ('B4',4), ('B4',8), ('C5',8), ('D5',4), ('E5',4),
            ('C5',4), ('A4',4), ('A4',4)
        ]

        nokia_tune = [
            ('E5', 8), ('D5', 8), ('FS4', 4), ('GS4', 4),
            ('CS5', 8), ('B4', 8), ('D4', 4), ('E4', 4),
            ('B4', 8), ('A4', 8), ('CS4', 4), ('E4', 4),
            ('A4', 2) 
        ]
        
        if id == 1:
            print("tocando")
            self.play_song(mario_bros, tempo_bpm=200)
        if id == 2:
            self.play_song(tetris_theme, tempo_bpm=144)
        if id == 3:
            self.play_song(nokia_tune, tempo_bpm=180)
