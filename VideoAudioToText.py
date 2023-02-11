import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import moviepy.editor as mp
import speech_recognition as sr
from tkinter import ttk
import subprocess

All_Languages = {
  "Arabic - South Africa": "af-ZA",
  "Arabic - SAlgeria": "ar-DZ",
  "Arabic - SBahrain": "ar-BH",
  "Arabic - SEgypt": "ar-EG",
  "Arabic - SIsrael": "ar-IL",
  "Arabic - SIraq": "ar-IQ",
  "Arabic - SJordan": "ar-JO",
  "Arabic - SKuwait": "ar-KW",
  "Arabic - SLebanon": "ar-LB",
  "Arabic - SMorocco": "ar-MA",
  "Arabic - SOman": "ar-OM",
  "Arabic - SPalestinian Territory": "ar-PS",
  "Arabic - SQatar": "ar-QA",
  "Arabic - SSaudi Arabia": "ar-SA",
  "Arabic - STunisia": "ar-TN",
  "Arabic - SUAE": "ar-AE",
  "Basque - Spain": "eu-ES",
  "Bulgarian - Bulgaria": "bg-BG",
  "Catalan - Spain": "ca-ES",
  "Chinese Mandarin - China (Simp.)": "cmn-Hans-CN",
  "Chinese Mandarin - Hong Kong SAR (Trad.)": "cmn-Hans-HK",
  "Chinese Mandarin - Taiwan (Trad.)": "cmn-Hant-TW",
  "Chinese Cantonese - Hong Kong": "yue-Hant-HK",
  "Croatian - Croatia": "hr_HR",
  "Czech - Czech Republic": "cs-CZ",
  "Danish - Denmark": "da-DK",
  "English - Australia": "en-AU",
  "English - Canada": "en-CA",
  "English - India": "en-IN",
  "English - Ireland": "en-IE",
  "English - New Zealand": "en-NZ",
  "English - Philippines": "en-PH",
  "English - South Africa": "en-ZA",
  "English - United Kingdom": "en-GB",
  "English - United States": "en-US",
  "Farsi - Iran": "fa-IR",
  "French - France": "fr-FR",
  "Filipino - Philippines": "fil-PH",
  "Galician - Spain": "gl-ES",
  "German - Germany": "de-DE",
  "Greek - Greece": "el-GR",
  "Finnish - Finland": "fi-FI",
  "Hebrew - Israel": "he-IL",
  "Hindi - India": "hi-IN",
  "Hungarian - Hungary": "hu-HU",
  "Indonesian - Indonesia": "id-ID",
  "Icelandic - Iceland": "is-IS",
  "Italian - Italy": "it-IT",
  "Italian - Switzerland": "it-CH",
  "Japanese - Japan": "ja-JP",
  "Korean - Korea": "ko-KR",
  "Lithuanian - Lithuania": "lt-LT",
  "Malaysian - Malaysia": "ms-MY",
  "Dutch - Netherlands": "nl-NL",
  "Norwegian - Norway": "nb-NO",
  "Polish - Poland": "pl-PL",
  "Portuguese - Brazil": "pt-BR",
  "Portuguese - Portugal": "pt-PT",
  "Romanian - Romania": "ro-RO",
  "Russian - Russia": "ru-RU",
  "Serbian - Serbia": "sr-RS",
  "Slovak - Slovakia": "sk-SK",
  "Slovenian - Slovenia": "sl-SI",
  "Spanish - Argentina": "es-AR",
  "Spanish - Bolivia": "es-BO",
  "Spanish - Chile": "es-CL",
  "Spanish - Colombia": "es-CO",
  "Spanish - Costa Rica": "es-CR",
  "Spanish - Dominican Republic": "es-DO",
  "Spanish - Ecuador": "es-EC",
  "Spanish - El Salvador": "es-SV",
  "Spanish - Guatemala": "es-GT",
  "Spanish - Honduras": "es-HN",
  "Spanish - México": "es-MX",
  "Spanish - Nicaragua": "es-NI",
  "Spanish - Panamá": "es-PA",
  "Spanish - Paraguay": "es-PY",
  "Spanish - Perú": "es-PE",
  "Spanish - Puerto Rico": "es-PR",
  "Spanish - Spain": "es-ES",
  "Spanish - Uruguay": "es-UY",
  "Spanish - United States": "es-US",
  "Spanish - Venezuela": "es-VE",
  "Swedish - Sweden": "sv-SE",
  "Thai - Thailand": "th-TH",
  "Turkish - Turkey": "tr-TR",
  "Ukrainian - Ukraine": "uk-UA",
  "Vietnamese - Viet Nam": "vi-VN",
  "Zulu - South Africa": "zu-ZA"
}

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Video/Audio to Text Application")
        self.geometry("300x300")
        
        self.label = tk.Label(self.master, text="Select a language:")
        self.label.pack()

        self.var = tk.StringVar(self.master)
        self.var.set("English")

        self.language_options = tk.OptionMenu(self.master, self.var, *All_Languages.keys())
        self.language_options.pack(pady=10)

        self.video_button = tk.Button(self, text="Select Video", command=self.select_video)
        self.video_button.pack(pady=10)
        
        self.audio_button = tk.Button(self, text="Select Audio", command=self.select_audio)
        self.audio_button.pack(pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.wmv;*.flv;*.mov;*.webm;*.vob;*.ts")])
        if not file_path:
            return
        
        # extract audio from the video file
        video = mp.VideoFileClip(file_path)
        audio = video.audio
        audio.write_audiofile("temp_audio.wav")

        recognizer = sr.Recognizer()
        audio_clip = sr.AudioFile("temp_audio.wav")
        
        with audio_clip as source:
            audio = recognizer.record(source)
        selected_language = self.var.get()
        code = All_Languages.get(selected_language)
        print(code)
        
        try:
            transcript = recognizer.recognize_google(audio, language=code)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", "Could not request results from Google Speech Recognition service: {0}".format(e))
        
        self.show_text_window(transcript)

    def show_text_window(self, transcript):
        self.text_window = tk.Toplevel(self)
        self.text_window.title("Transcript")
        self.text_window.geometry("500x400")
        self.text = tk.Text(self.text_window)
        self.text_scrollbar = tk.Scrollbar(self.text, orient="vertical")
        self.text_scrollbar.pack(side="right", fill="y")
        self.text_scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.text_scrollbar.set)

        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, transcript)

        self.close_button = tk.Button(self.text_window, text="Close", command=self.text_window.destroy)
        self.close_button.pack(side=tk.BOTTOM)
        self.text_window.mainloop()

    def select_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.flac;*.aiff;*.aif")])
        if not file_path:
            return
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = False
        # recognizer.pause_threshold = 1
        print(recognizer.energy_threshold)
        audio_clip = sr.AudioFile(file_path)

        with audio_clip as source:
            audio = recognizer.record(source)
        selected_language = self.var.get()
        code = All_Languages.get(selected_language)

        try:
            transcript = recognizer.recognize_google(audio, language=code)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", "Could not request results from Google Speech Recognition service: {0}".format(e))

        self.show_text_window(transcript)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
