import flet as ft
import requests
import json
import base64

# --- GİZLİ ANAHTAR BÖLGESİ ---
# Kendi Base64 anahtarını buraya koy knk
HIDDEN_KEY = "QUl6YVN5QWFSdC15TnE5T2I2Ty1pU01YNnlWQ1JYaFhjVXloTGhJ" 

def get_key():
    # Bu fonksiyon kodu çalıştırdığında anahtarı gizlice çözer
    return base64.b64decode(HIDDEN_KEY).decode("utf-8")

def main(page: ft.Page):
    page.title = "Okirit AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F111A"  # Derin lacivert/siyah arka plan
    page.padding = 0  # Kenarları sıfırladık, container ile kontrol edeceğiz
    
    # API Linkini gizli anahtarla oluşturuyoruz
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={get_key()}"

    # Mesaj listesi
    chat = ft.ListView(
        expand=True,
        spacing=15,
        padding=20,
        auto_scroll=True,
    )

    def get_ai_response(prompt):
        payload = {
            "contents": [{
                "parts": [{"text": f"Senin adın Okirit. Uzman bir yazılımcısın. Kodları markdown formatında yaz: {prompt}"}]
            }]
        }
        try:
            response = requests.post(API_URL, json=payload)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Bağlantı hatası! Anahtarı kontrol et knk. Hata: {str(e)}"

    def send_click(e):
        if not user_input.value:
            return
        
        user_msg = user_input.value
        # Kullanıcı Baloncuğu
        chat.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(user_msg, color="white"),
                        bgcolor="#202C33",
                        padding=12,
                        border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
        user_input.value = ""
        page.update()

        # Okirit Baloncuğu
        ai_reply = get_ai_response(user_msg)
        chat.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Okirit", size=12, color="#00E676", weight="bold"),
                            ft.Markdown(ai_reply, selectable=True, extension_set="gitHubWeb"),
                        ], tight=True, spacing=5),
                        bgcolor="#1D2733",
                        padding=15,
                        border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15),
                        border=ft.border.all(1, "#2B394A"),
                        width=320,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
        page.update()

    # Üst Başlık (AppBar)
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.RECYCLING_ROUNDED, color="#00E676", size=30),
            ft.Text("OKİRİT AI", size=22, weight="bold", color="white", letter_spacing=2),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        bgcolor="#161925",
        border=ft.border.only(bottom=ft.border.BorderSide(1, "#2B394A"))
    )

    # Giriş Alanı Tasarımı
    user_input = ft.TextField(
        hint_text="Bir şeyler yaz...",
        border_color="#2B394A",
        focused_border_color="#00E676",
        fill_color="#161925",
        filled=True,
        expand=True,
        multiline=False,
        on_submit=send_click,
    )

    input_area = ft.Container(
        content=ft.Row([
            user_input,
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                icon_color="#00E676",
                icon_size=30,
                on_click=send_click
            ),
        ]),
        padding=20,
        bgcolor="#0F111A",
    )

    # Sayfaya ekle
    page.add(
        header,
        ft.Container(content=chat, expand=True),
        input_area
    )

if __name__ == "__main__":
    ft.app(target=main)