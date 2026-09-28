import json
import locale
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import urllib.request
import urllib.parse

CONFIG_FILE = "config.json"
SERVER_URL = "https://raw.githubusercontent.com/dijfkfkd/Project-Reprieve-Playtest-Idiomas/main"


class LauncherApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Project Reprieve - Launcher")
    self.root.geometry("450x480")
    self.root.config(bg="#1e1e1e")

    self.config_data = self.load_config()

    if not self.config_data.get("game_path"):
      self.ask_game_path()

    # Detectar y aplicar automáticamente el idioma del sistema la primera vez
    if not self.config_data.get("auto_lang_applied"):
      self.detectar_y_aplicar_idioma_sistema()

    self.create_main_menu()

  def load_config(self):
    if os.path.exists(CONFIG_FILE):
      try:
        with open(CONFIG_FILE, "r") as f:
          return json.load(f)
      except:
        pass
    return {"game_path": "", "auto_lang_applied": False}

  def save_config(self):
    try:
      with open(CONFIG_FILE, "w") as f:
        json.dump(self.config_data, f)
    except Exception as e:
      print(f"Error guardando config: {e}")

  def ask_game_path(self):
    messagebox.showinfo(
        "Configuración",
        "Por favor, selecciona la carpeta raíz de Project Reprieve Playtest.",
    )
    path = filedialog.askdirectory(title="Seleccionar carpeta del juego")
    if path:
      self.config_data["game_path"] = path
      self.save_config()
    else:
      if not self.config_data.get("game_path"):
        self.root.destroy()

  def detectar_y_aplicar_idioma_sistema(self):
    try:
      sys_lang, _ = locale.getdefaultlocale()
      if sys_lang:
        sys_lang = sys_lang.lower()
        target_folder = "Spanish"

        if "ru" in sys_lang:
          target_folder = "Russian"
        elif "pt" in sys_lang:
          target_folder = "Brazil"
        elif "fr" in sys_lang:
          target_folder = "France"
        elif "es" in sys_lang:
          target_folder = "Latin America"

        self.descargar_idioma_silencioso(target_folder)
        self.config_data["auto_lang_applied"] = True
        self.save_config()
    except Exception as e:
      print(f"No se pudo detectar el idioma del sistema: {e}")

  def descargar_idioma_silencioso(self, folder_name):
    game_path = self.config_data.get("game_path")
    if not game_path or not os.path.exists(game_path):
      return

    def tarea():
      try:
        encoded_folder = urllib.parse.quote(folder_name)
        base_lang_url = f"{SERVER_URL}/{encoded_folder}"
        files_to_download = [
            "lang.ini",
            "achieves.ini",
            "Oldang",
            "symbolism.txt",
        ]
        for file_name in files_to_download:
          try:
            file_url = f"{base_lang_url}/{file_name}"
            dest_path = os.path.join(game_path, file_name)
            urllib.request.urlretrieve(file_url, dest_path)
          except Exception:
            pass  # Omite silenciosamente si algún archivo opcional no existe
      except Exception as e:
        print(f"Error en descarga automática de idioma: {e}")

    threading.Thread(target=tarea).start()

  def create_main_menu(self):
    for widget in self.root.winfo_children():
      widget.destroy()

    title_label = tk.Label(
        self.root,
        text="PROJECT REPRIEVE",
        font=("Arial", 16, "bold"),
        bg="#1e1e1e",
        fg="white",
    )
    title_label.pack(pady=20)

    btn_style = {
        "font": ("Arial", 11, "bold"),
        "bg": "#333333",
        "fg": "white",
        "width": 20,
        "height": 2,
        "bd": 0,
        "cursor": "hand2",
    }

    tk.Button(
        self.root, text="JUGAR", command=self.lanzar_juego, **btn_style
    ).pack(pady=8)
    tk.Button(
        self.root, text="IDIOMAS", command=self.menu_idiomas, **btn_style
    ).pack(pady=8)
    tk.Button(
        self.root, text="SALIR", command=self.root.destroy, **btn_style
    ).pack(pady=8)

  def lanzar_juego(self):
    try:
      os.system("start steam://rungameid/4582690")
      messagebox.showinfo("Lanzador", "Iniciando juego a través de Steam...")
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo iniciar Steam: {e}")

  def menu_idiomas(self):
    for widget in self.root.winfo_children():
      widget.destroy()

    tk.Label(
        self.root,
        text="SELECCIONAR IDIOMA",
        font=("Arial", 14, "bold"),
        bg="#1e1e1e",
        fg="white",
    ).pack(pady=10)

    btn_style = {
        "font": ("Arial", 10, "bold"),
        "bg": "#444444",
        "fg": "white",
        "width": 22,
        "height": 1,
    }

    tk.Button(
        self.root,
        text="🇷🇺 Ruso",
        command=lambda: self.descargar_idioma("Russian"),
        **btn_style,
    ).pack(pady=4)
    tk.Button(
        self.root,
        text="🇧🇷 Brasil",
        command=lambda: self.descargar_idioma("Brazil"),
        **btn_style,
    ).pack(pady=4)
    tk.Button(
        self.root,
        text="🇪🇸 España",
        command=lambda: self.descargar_idioma("Spanish"),
        **btn_style,
    ).pack(pady=4)
    tk.Button(
        self.root,
        text="🌎 Latam",
        command=lambda: self.descargar_idioma("Latin America"),
        **btn_style,
    ).pack(pady=4)
    tk.Button(
        self.root,
        text="🇫🇷 Francia",
        command=lambda: self.descargar_idioma("France"),
        **btn_style,
    ).pack(pady=4)

    btn_votar = {
        "font": ("Arial", 10, "bold"),
        "bg": "#2b5c8f",
        "fg": "white",
        "width": 22,
        "height": 1,
    }
    tk.Button(
        self.root,
        text="📊 Sugerir nuevo idioma",
        command=self.abrir_ventana_sugerencia,
        **btn_votar,
    ).pack(pady=8)

    tk.Button(
        self.root,
        text="Volver",
        command=self.create_main_menu,
        font=("Arial", 9),
        bg="#222",
        fg="#aaa",
        width=10,
    ).pack(pady=10)

  def descargar_idioma(self, folder_name):
    game_path = self.config_data.get("game_path")
    if not game_path or not os.path.exists(game_path):
      messagebox.showerror("Error", "La ruta del juego no es válida.")
      self.ask_game_path()
      return

    def tarea():
      try:
        encoded_folder = urllib.parse.quote(folder_name)
        base_lang_url = f"{SERVER_URL}/{encoded_folder}"
        files_to_download = [
            "lang.ini",
            "achieves.ini",
            "Oldang",
            "symbolism.txt",
        ]

        descargados = 0
        for file_name in files_to_download:
          try:
            file_url = f"{base_lang_url}/{file_name}"
            dest_path = os.path.join(game_path, file_name)
            urllib.request.urlretrieve(file_url, dest_path)
            descargados += 1
          except Exception:
            pass

        if descargados > 0:
          messagebox.showinfo(
              "Éxito",
              f"¡Idioma y archivos ({folder_name}) instalados correctamente!",
          )
        else:
          messagebox.showerror(
              "Error", "No se pudo descargar ningún archivo de esta carpeta."
          )
      except Exception as e:
        messagebox.showerror(
            "Error de Descarga",
            f"Fallo al descargar en '{folder_name}'.\nDetalle: {str(e)}",
        )

    threading.Thread(target=tarea).start()

  def abrir_ventana_sugerencia(self):
    ventana_sugerencia = tk.Toplevel(self.root)
    ventana_sugerencia.title("Sugerir Idioma")
    ventana_sugerencia.geometry("320x180")
    ventana_sugerencia.config(bg="#1e1e1e")
    ventana_sugerencia.resizable(False, False)

    tk.Label(
        ventana_sugerencia,
        text="¿Qué idioma te gustaría que añadamos?",
        font=("Arial", 10, "bold"),
        bg="#1e1e1e",
        fg="white",
    ).pack(pady=15)

    entry_idioma = tk.Entry(
        ventana_sugerencia, font=("Arial", 11), width=22, justify="center"
    )
    entry_idioma.pack(pady=5)
    entry_idioma.focus()

    def enviar():
      idioma = entry_idioma.get().strip()
      if not idioma:
        messagebox.showwarning(
            "Campo vacío", "Por favor, escribe un idioma.", parent=ventana_sugerencia
        )
        return

      WEBHOOK_URL = "https://discord.com/api/webhooks/1553800193374159040/-nD6l7J1eIMdqSH1P5SdxfMGrhXlSdy6TNVHgc4lt2Lp5Of2BfS86-C0SIndPHBT0335"

      try:
        mensaje = {
            "content": (
                f"📥 **Nueva sugerencia de idioma:** `{idioma}` (Enviado"
                " desde el Launcher)"
            )
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }

        req = urllib.request.Request(
            WEBHOOK_URL, data=json.dumps(mensaje).encode("utf-8"), headers=headers
        )
        urllib.request.urlopen(req)

        messagebox.showinfo(
            "¡Enviado!",
            "¡Gracias! Tu sugerencia ha sido enviada al desarrollador.",
            parent=ventana_sugerencia,
        )
        ventana_sugerencia.destroy()
      except Exception as e:
        messagebox.showerror(
            "Error",
            f"No se pudo enviar la sugerencia.\nDetalle: {e}",
            parent=ventana_sugerencia,
        )

    tk.Button(
        ventana_sugerencia,
        text="Enviar sugerencia",
        command=enviar,
        font=("Arial", 10, "bold"),
        bg="#2b5c8f",
        fg="white",
        width=18,
        height=1,
    ).pack(pady=15)


if __name__ == "__main__":
  try:
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()
  except Exception as e:
    messagebox.showerror("Error Crítico", f"El launcher falló: {str(e)}")