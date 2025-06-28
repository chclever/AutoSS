import customtkinter
import logger
import json
# Переменные
custom_font = ("Noto Sans", 22, "bold")
version = "v1.0.0"

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
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    if tab_name == "Changelog":
        label = customtkinter.CTkLabel(content_frame, text="Changelog Content", font=custom_font).pack(pady=20)
    elif tab_name == "Panel":
        label = customtkinter.CTkLabel(content_frame, text="Panel Content", font=custom_font).pack(pady=20)
    elif tab_name == "Config":
        label = customtkinter.CTkLabel(content_frame, text="Config Content", font=custom_font).pack(pady=20)
    elif tab_name == "Logs":
        label = customtkinter.CTkLabel(content_frame, text="Logs Content",font=custom_font).pack(pady=20)
    elif tab_name == "Donate":
        label = customtkinter.CTkLabel(content_frame, text="Donate",font=custom_font).pack(pady=20)
    elif tab_name == "Settings":
        
        label = customtkinter.CTkLabel(content_frame, text="Settings",font=custom_font)
        label.pack(pady=20)
    
        switch = customtkinter.CTkSwitch(
            master=content_frame,
            text="Dark Theme",
            command=lambda:update_theme(switch),
            width=60,
            height=30,
        )
        switch.pack(pady=20)
    
        if config["SenderSS"]["theme"].lower() == "dark":
            switch.select()
        else:
            switch.deselect()    
    
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

if __name__ == '__main__':
    logger.log("Запускаю приложение...")
    root.mainloop()

