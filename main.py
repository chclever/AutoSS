import customtkinter
import logger
import json
import math
import time

# Переменные
custom_font = ("Noto Sans", 22, "bold")
version = "v1.0.0"
color_step = 0

# Window cfg
root = customtkinter.CTk()

root.geometry("800x350")
root.resizable(False, False)
root.title(f"[Snake] AutoSender by Fiero | {version}")

# Theme load
try:
    logger.create_config_if_not_exists()
    
    config = logger.get_config()
    logger.log("Загрузка темы и конфига...")
    
    customtkinter.ThemeManager.load_theme("./assets/lavender.json")
    
    mode = config["SenderSS"]["theme"]
    
    logger.log(f"Тема установлена ({mode})")
    
    if mode == "light":
        customtkinter.set_appearance_mode("light")
    elif mode == "dark":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("system")
except Exception as e:
    logger.log(f"Ошибка при загрузке темы/конфига: {e}")

def update_color():
    global color_step
    r = int((math.sin(color_step) * 55 + 200))
    b = int((math.sin(color_step + math.pi) * 55 + 200))
    g = 50
    r = max(200, min(255, r))
    g = max(0, min(100, g))
    b = max(200, min(255, b))
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    program_name.configure(text_color=hex_color)
    color_step += 0.05
    root.after(25, update_color)

def update_theme(switch):
    try:
        is_dark_mode = switch.get()
        
        if is_dark_mode:
            customtkinter.set_appearance_mode("dark")
            theme_name = "dark"
        else:
            customtkinter.set_appearance_mode("light")
            theme_name = "light"
        
        config["SenderSS"]["theme"] = theme_name
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        logger.log(f"Тема установлена ({theme_name})")
        
    except Exception as e:
        logger.log(f"Error theme: {e}")


sidebar = customtkinter.CTkFrame(root, width=150, corner_radius=0)
sidebar.pack(side="left", fill="y")

content_frame = customtkinter.CTkFrame(root)
content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

def show_tab(tab_name):

    def clear_logs():
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.configure(state="disabled")    
    

    for widget in content_frame.winfo_children():
        widget.destroy()
    
    if tab_name == "Changelog":
        label = customtkinter.CTkLabel(content_frame, text="Changelog Content", font=custom_font).pack(padx=10, pady=20, anchor = "w")
    elif tab_name == "Panel":
        label = customtkinter.CTkLabel(content_frame, text="Panel Content", font=custom_font).pack(padx=10, pady=20, anchor = "w")
    elif tab_name == "Config":
        label = customtkinter.CTkLabel(content_frame, text="Config Content", font=custom_font).pack(padx=10, pady=20, anchor = "w")
    elif tab_name == "Logs":
        label = customtkinter.CTkLabel(content_frame, text="Logs", font=custom_font)
        label.pack(padx=10, pady=20, anchor = "w")
        
        textbox = customtkinter.CTkTextbox(content_frame, state="disabled", wrap="none", scrollbar_button_color="#AAAAAA", scrollbar_button_hover_color="#888888")
        textbox.pack(fill="both", expand=True, padx=10)
        
        clear_btn = customtkinter.CTkButton(content_frame, text="Clear it", font=custom_font, command=clear_logs)
        clear_btn.pack(fill="both", padx=10, pady=10)
    
    elif tab_name == "Donate":
        label = customtkinter.CTkLabel(content_frame, text="Donate",font=custom_font).pack(pady=20)
    elif tab_name == "Settings":
        label = customtkinter.CTkLabel(
            content_frame,
            text="Settings",
            font=custom_font,
            anchor="center"
        )
        label.pack(padx=10, pady=20, anchor = "w")
        
        theme_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
        theme_frame.pack(pady=10, padx=20, fill="x")
        
        switch = customtkinter.CTkSwitch(
            master=theme_frame,
            text="Dark Theme",
            command=lambda: update_theme(switch),
            width=40,
            height=30,
            font=custom_font
        )
        switch.pack(pady=10, padx=20, side="left")
        
        delay_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
        delay_frame.pack(pady=10, padx=20, fill="x")
        
        delay_label = customtkinter.CTkLabel(
            delay_frame,
            text="Delay: 0 ms",
            font=custom_font
        )
        delay_label.pack(pady=20, padx=20, anchor="w")
        
        def slider_event(value):
            if value >= 1:
                # add_log_message("Slider updated: {value} ")
                delay_label.configure(text=f"Delay: {int(value)}s or {int(value)//60}m {int(value)%60}s", text_color="white")
            else:
                delay_label.configure(text=f"Delay {int(value)}s (too low!)", text_color="red")
        def save_click():
            save_btn.configure(text=f"Saved!", text_color="green")
            
            
        delay_entry = customtkinter.CTkSlider(
            delay_frame,
            from_=0,
            to=600,
            command=slider_event,
            number_of_steps=360,
            width=300
        )
        delay_entry.pack(pady=10, padx=20, fill="x")
        delay_entry.set(0)
        
        if config["SenderSS"]["theme"].lower() == "dark":
            switch.select()
        else:
            switch.deselect()
        
        save_btn = customtkinter.CTkButton(content_frame, width=200 ,text="save", font=custom_font, command=save_click)
        save_btn.pack(pady=5,padx=20, anchor="se")
    
    

program_name = customtkinter.CTkLabel(sidebar, text="AutoSS " + version, font=custom_font)
btn_changelog = customtkinter.CTkButton(sidebar, text="Changelog",font=custom_font ,command=lambda: show_tab("Changelog"))
btn_panel = customtkinter.CTkButton(sidebar, text="Panel", font=custom_font,command=lambda: show_tab("Panel"))
btn_config = customtkinter.CTkButton(sidebar, text="Config",font=custom_font,  command=lambda: show_tab("Config"))
btn_logs = customtkinter.CTkButton(sidebar, text="Logs", font=custom_font, command=lambda: show_tab("Logs"))
btn_settings = customtkinter.CTkButton(sidebar, text="Settings",font=custom_font ,command=lambda: show_tab("Settings"))
btn_donate = customtkinter.CTkButton(sidebar, text="Donate", font=custom_font, command=lambda: show_tab("Donate"))

program_name.pack(pady=15, padx=10, fill="x")
btn_changelog.pack(pady=5, padx=10, fill="x")
btn_panel.pack(pady=5, padx=10, fill="x")
btn_config.pack(pady=5, padx=10, fill="x")
btn_logs.pack(pady=5, padx=10, fill="x")
btn_settings.pack(pady=5, padx=10, fill="x")
btn_donate.pack(pady=5, padx=10, fill="x")

show_tab("Changelog")
update_color()

if __name__ == '__main__':
    logger.log("Запускаю приложение...")
    root.mainloop()

