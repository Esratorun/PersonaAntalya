import os
import requests
from datetime import datetime
import google.generativeai as genai
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session, send_from_directory
from flask_login import login_required, current_user
from app import db
from dotenv import load_dotenv

from app.models.place import Place
from app.models.restaurant import Restaurant
from app.models.favorite import Favorite

# Gizli kasayı (.env) aktif et
load_dotenv()

main_bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/persona-secimi', methods=['GET', 'POST'])
@login_required
def persona_select():
    if request.method == 'POST':
        secilen_persona = request.form.get('persona')
        secilen_diyet = request.form.get('diet')

        if not secilen_persona or not secilen_diyet:
            flash('Lütfen hem bir persona hem de bir beslenme tercihi seçin!', 'danger')
            return redirect(url_for('main.persona_select'))

        current_user.selected_persona = secilen_persona
        current_user.diet_preference = secilen_diyet
        db.session.commit()

        flash(f'Harika! Artık Antalya\'yı bir {secilen_persona} gözüyle keşfedeceksin 🌴', 'success')
        return redirect(url_for('main.explore'))

    return render_template('persona_select.html')


@main_bp.route('/kesfet')
@login_required
def explore():
    return render_template('explore.html')


@main_bp.route('/place/<int:id>')
@login_required
def place_detail(id):
    place = Place.query.get_or_404(id)
    is_favorite = Favorite.query.filter_by(user_id=current_user.id, place_id=id).first() is not None
    return render_template('place_detail.html', item=place, is_favorite=is_favorite, is_food=False)


@main_bp.route('/restaurant/<int:id>')
@login_required
def restaurant_detail(id):
    restaurant = Restaurant.query.get_or_404(id)
    is_favorite = Favorite.query.filter_by(user_id=current_user.id, restaurant_id=id).first() is not None
    return render_template('place_detail.html', item=restaurant, is_favorite=is_favorite, is_food=True)


@main_bp.route('/profil')
@login_required
def profile():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    fav_place_ids = [f.place_id for f in favorites if f.place_id]
    fav_rest_ids = [f.restaurant_id for f in favorites if f.restaurant_id]
    fav_places = Place.query.filter(Place.id.in_(fav_place_ids)).all() if fav_place_ids else []
    fav_restaurants = Restaurant.query.filter(Restaurant.id.in_(fav_rest_ids)).all() if fav_rest_ids else []
    return render_template('profile.html', fav_places=fav_places, fav_restaurants=fav_restaurants)


@main_bp.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'error': 'Dosya bulunamadı'})

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Dosya seçilmedi'})

    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"user_{current_user.id}_avatar.{ext}")

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        current_user.avatar = filename
        db.session.commit()

        return jsonify({'success': True, 'filename': filename})

    return jsonify({'success': False, 'error': 'Geçersiz dosya formatı'})


# =====================================================================
# HAFIZALI ETKİLEŞİMLİ PERSONA AJANI (SOHBET API) - TAM DONANIMLI
# =====================================================================
@main_bp.route('/api/chat/<string:item_type>s/<int:id>', methods=['POST'])
@login_required
def chat_with_persona(item_type, id):
    data = request.get_json()
    user_message = data.get('message')

    if item_type == 'place':
        item = Place.query.get_or_404(id)
    else:
        item = Restaurant.query.get_or_404(id)

    # 1. KULLANICI BİLGİLERİNİ ÇEKELİM
    persona = current_user.selected_persona or "Tarihçi"
    guzel_persona_ismi = persona.replace('_', ' ').title()
    diet_pref = getattr(current_user, 'diet_preference', 'standart').upper()

    session_key = f"chat_memory_{item_type}_{id}"
    if session_key not in session:
        session[session_key] = []
    chat_history = session[session_key]

    # 2. CANLI SAAT VE HAVA DURUMU SİSTEMİ (UNUTULAN KISIM EKLENDİ)
    current_time = datetime.now().strftime("%H:%M")
    weather_desc = "harika bir Antalya havası var"
    try:
        api_key_weather = os.getenv("OPENWEATHER_API_KEY")
        if api_key_weather:
            w_url = f"http://api.openweathermap.org/data/2.5/weather?q=Antalya&appid={api_key_weather}&units=metric&lang=tr"
            w_res = requests.get(w_url, timeout=3).json()
            if w_res.get('main'):
                weather_desc = f"{round(w_res['main']['temp'])}°C ve {w_res['weather'][0]['description']}"
    except:
        pass

    # 3. VERİTABANI GERÇEKLERİNİ TOPLAYALIM
    db_context = f"- Mekan Adı: {item.name}\n"
    db_context += f"- İlçe / Bölge: {getattr(item, 'district', 'Belirtilmemiş')}\n"

    if item_type == 'restaurant':
        db_context += f"- Türü: Restoran / Yemek Mekanı\n"
        db_context += f"- Fiyat Segmenti: {getattr(item, 'price_level', '₺₺')}\n"
        db_context += f"- Sunulan Mutfak / Diyet Kategorisi: {getattr(item, 'diet_category', 'STANDART').upper()}\n"
        db_context += f"- Açılış Saati: {getattr(item, 'opening_time', '09:00')}\n"
        db_context += f"- Kapanış Saati: {getattr(item, 'closing_time', '23:30')}\n"
    else:
        db_context += f"- Türü: Gezi Noktası / Tarihi veya Doğal Alan\n"
        db_context += f"- Kategorisi: {getattr(item, 'category', 'Belirtilmemiş')}\n"

    db_context += f"- Veritabanı Genel Açıklaması: {getattr(item, 'description', 'Sistemde detaylı bir tanıtım metni bulunmamaktadır.')}\n"

    try:
        # GÜVENLİK GÜNCELLEMESİ
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API Anahtarı bulunamadı! Lütfen .env dosyasını kontrol et.")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 4. TAM DONANIMLI VE KATI SİSTEM PROMPTU
        system_prompt = f"""
        Sen PersonaAntalya uygulamasının profesyonel, dürüst ve saygılı yapay zeka rehberisin.
        Kullanıcıyla '{guzel_persona_ismi}' perspektifinden sohbet ediyorsun. 
        Şu an incelenen mekan: {item.name}

        [VERİTABANINDAKİ GERÇEK BİLGİLER - BUNLARIN DIŞINA ÇIKMAK YASAKTIR]
        {db_context}

        [CANLI BAĞLAM BİLGİLERİ]
        - Anlık Saat: {current_time}
        - Antalya Anlık Hava Durumu: {weather_desc}
        - Turistin Beslenme Tercihi: {diet_pref}

        [KATI ASKERİ KURALLAR]
        1. MENÜ/FİYAT UYDURMA: Eğer [VERİTABANINDAKİ GERÇEK BİLGİLER] kısmında detaylı bir yemek menüsü yoksa, kullanıcı menüyü veya yemekleri sorduğunda KESİNLİKLE uydurma! Doğrudan şunu söyle: "Bu mekanın detaylı menüsü ve güncel fiyat listesi sistemimizde dijital olarak yer almıyor, maalesef bu konuda sana uydurma bilgiler vermek istemem."
        2. ÇALIŞAN GİBİ DAVRANMA: Sen mekanın sahibi veya garsonu DEĞİLSİN. "Bizim lezzetlerimiz", "hoş geldin canım", "kruvasan yaptık" gibi lakayıt kelimeler kullanma. Dışarıdan mekanı anlatan objektif bir rehber ol.
        3. ÇALIŞMA SAATLERİ VE HAVA DURUMU: Anlık saate ({current_time}) ve hava durumuna ({weather_desc}) uygun olarak, gerçekçi ve mantıklı yönlendirmeler yap.
        4. KISA VE NET CEVAPLAR: Sohbet ortamı olduğu için cevaplarını gereksiz uzatma, kısa ve net cevaplar ver.

        [SOHBET GEÇMİŞİ]
        """

        prompt_context = system_prompt
        for msg in chat_history:
            prompt_context += f"{'Kullanıcı' if msg['role'] == 'user' else 'Sen'}: {msg['text']}\n"

        prompt_context += f"Kullanıcı: {user_message}\nSen:"

        response = model.generate_content(prompt_context)
        reply = response.text

        chat_history.append({"role": "user", "text": user_message})
        chat_history.append({"role": "model", "text": reply})
        session[session_key] = chat_history
        session.modified = True

        return jsonify({'success': True, 'reply': reply})

    except Exception as e:
        print("\n" + "=" * 50)
        print("🚨 AJAN (SOHBET) API HATASI 🚨")
        print(f"Hata Detayı: {e}")
        print("=" * 50 + "\n")
        return jsonify({'success': False,
                        'reply': "Şu an bağım koptu dostum, birazdan tekrar sorabilir misin? (Not: Terminaldeki hata detayını kontrol et.)"})


# =====================================================================
# MOBİL UYGULAMA (PWA) İÇİN SERVİS DOSYASI ÇAĞIRICISI
# =====================================================================
@main_bp.route('/service-worker.js')
def service_worker():
    return send_from_directory('..', 'service-worker.js')