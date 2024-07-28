import datetime
from gtts import gTTS
#https://gtts.readthedocs.io/en/latest/module.html

async def create_audio_async(text, filename = 'temp.mp3',lang="pt", tld="com.br"):
    tts = gTTS(text, lang=lang, tld=tld)
    tts.save(filename)

def create_audio(text, filename = 'temp.mp3',lang="pt", tld="com.br"):
    tts = gTTS(text, lang=lang, tld=tld)
    tts.save(filename)

if __name__ == "__main__":
    now = datetime.datetime.now()
    create_audio(f"Agora são {now.hour} horas e {now.minute} minutos exatamente")
    from playsound import playsound
    playsound('temp.mp3')
