import customtkinter as ctk
import cv2
from PIL import Image
from ultralytics import YOLO

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Visión Artificial - YOLO")
        self.geometry("1100x650")

        # --- Cargar Modelo (CORREGIDO) ---
        self.model_path = r"C:\Users\angel\Desktop\proyecto Integrador\best.pt"  # <-- IMPORTANTE
        self.model = YOLO(self.model_path)

        # Variables de control
        self.running = False
        self.cap = None

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="IA CONTROL", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        self.btn_start = ctk.CTkButton(self.sidebar, text="Encender Cámara", command=self.toggle_camera)
        self.btn_start.pack(pady=10)

        self.btn_stop = ctk.CTkButton(self.sidebar, text="Detener", command=self.stop_camera, state="disabled")
        self.btn_stop.pack(pady=10)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Estado: Offline", text_color="gray")
        self.info_label.pack(side="bottom", pady=20)

        # Video
        self.video_container = ctk.CTkFrame(self, fg_color="black")
        self.video_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.video_label = ctk.CTkLabel(self.video_container, text="")
        self.video_label.pack(expand=True, fill="both")

    def toggle_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # <-- mejora en Windows
            if self.cap.isOpened():
                self.running = True
                self.btn_start.configure(state="disabled")
                self.btn_stop.configure(state="normal")
                self.info_label.configure(text="Estado: EN VIVO", text_color="green")
                self.update_frame()

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                # --- IA optimizada ---
                results = self.model(frame, imgsz=640, conf=0.5, verbose=False)
                frame_out = results[0].plot()

                # Convertir imagen
                img = cv2.cvtColor(frame_out, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 550))

                self.video_label.configure(image=imgtk)
                self.video_label.image = imgtk

            self.after(10, self.update_frame)

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()

        self.video_label.configure(image=None, text="Cámara Apagada")
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.info_label.configure(text="Estado: Offline", text_color="gray")


if __name__ == "__main__":
    app = DetectorApp()
    app.mainloop()