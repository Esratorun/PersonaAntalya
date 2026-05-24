# PersonaAntalya 🌴

PersonaAntalya, Antalya'yı ziyaret eden turistlere sıradan bir gezi rehberi sunmak yerine, onların kişisel ilgi alanlarına (personalara) özel, yapay zeka destekli dinamik ve etkileşimli bir keşif deneyimi sunacaktır.

## 🌟 Temel Özellikler

* **Persona Tabanlı Keşif:** Kullanıcılar; Tarihçi, Influencer, Masalcı, Gurme veya Efsane Avcısı gibi personalardan birini seçecek ve tüm uygulama bu kimliğe göre şekillenecektir.
* **Akıllı Rota Optimizasyonu (Haversine):** Sistem, kullanıcının canlı konumunu alacak ve seçilen personaya uygun mekanları gerçek dünya mesafesine göre en yakından en uzağa doğru matematiksel bir hassasiyetle dizecektir.
* **Yapay Zeka Destekli Hikayeleştirme:** Google Gemini entegrasyonu sayesinde, her mekan seçilen personanın ağzından, anlık hava durumu ve saate uygun bir dille anlatılacaktır.
* **Etkileşimli Harita Mimarisi:** Kullanıcılar rotalarını Leaflet.js tabanlı interaktif bir harita üzerinde görecek ve anlık hava durumu verileriyle planlamalarını kolayca yapacaktır.
* **Diyet Dostu Lezzet Rotaları:** Kullanıcının vegan, vejetaryen veya glutensiz gibi beslenme tercihlerine uygun restoranlar filtrelenip özel lezzet rotaları oluşturulacaktır.

## 🛠️ Kullanılan Teknolojiler

* **Arka Uç (Backend):** Python, Flask, Flask-Login, SQLAlchemy
* **Ön Yüz (Frontend):** HTML5, CSS3, JavaScript, Bootstrap 5, SweetAlert2
* **Harita & Konum Altyapısı:** Leaflet.js, OpenStreetMap API
* **Yapay Zeka (AI):** Google Gemini 1.5 Flash (Generative AI)
* **Canlı Veri API:** OpenWeatherMap (Anlık Hava Durumu)
* **Veritabanı:** SQLite

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda yerel ortamda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

**1. Projeyi Klonlayın:**
```bash
git clone [https://github.com/Esratorun/PersonaAntalya.git](https://github.com/Esratorun/PersonaAntalya.git)
cd PersonaAntalya
