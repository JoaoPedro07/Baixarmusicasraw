from __future__ import unicode_literals
from tkinter import Frame, Button, END, Tk, RIGHT, Label, LEFT, BOTTOM
from tkinter.scrolledtext import ScrolledText 
import os
import requests
from bs4 import BeautifulSoup
try:
    import youtube_dl
except:
    os.system("pip install youtube-dl")
#Por João Pedro

class App:
     def __init__(self, master=None):
             self.root = master
             self.root.title("Musicas")
             self.root.geometry("230x260")

             self.frame = Frame(self.root)

             self.msg = Label(self.frame, text="Insira as músicas que \ndeseja baixar no \ncampo abaixo", font=("Arial", "12"))
             self.msg.grid(row=1, column=1)

             self.scrolled = ScrolledText(self.frame, width=25, height=10)
             self.scrolled.grid(row=2, column=1)

             self.button = Button(self.frame, text="Enviar", command=self.sair, font=("Arial", "12"), width=5, height=1)
             self.button.grid(row=3, column=1)

             self.frame.pack()

     def sair(self):
             with open("musicas.txt", "w") as file:
                     file.write(self.scrolled.get(1.0, END))
             self.root.destroy()

class Automacao():
    
    def __init__(self):
        pass
    
    def BuscarMusica(self, nome):
        self.nome = nome
        page = requests.get("https://www.youtube.com/results?search_query={}".format(self.nome))
        soup = BeautifulSoup(page.content, "html.parser")
        url = soup.find_all("a", class_="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link")[0]["href"]
        return "https://www.youtube.com" + url

    def BaixarMusica(self, url):
        self.url = url
        outtmpl = self.nome + '.mp3'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
                'preferredquality': '192',
                },
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([str(self.url)])



if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()
    auto = Automacao()
    with open("musicas.txt", "r") as file:
        musicas = file.readlines()

    for music in musicas:
        url = auto.BuscarMusica(nome=music.strip("'\n'"))
        auto.BaixarMusica(url=url)



