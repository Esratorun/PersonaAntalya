from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app import db
from app.models.place import Place
from app.models.restaurant import Restaurant
from app.models.favorite import Favorite
from app.models.review import Review
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

import google.generativeai as genai

# Gizli kasayı (.env) aktif et
load_dotenv()

api_bp = Blueprint('api', __name__, url_prefix='/api')


# =====================================================================
# PERSONA VE KATEGORİ EŞLEŞTİRME ZEKASI
# =====================================================================
def get_persona_categories(persona_name):
    if not persona_name:
        return []

    p = persona_name.lower()
    if 'tarih' in p:
        return ['historical', 'museum']
    elif 'influencer' in p:
        return ['nature', 'beach']
    elif 'masal' in p:
        return ['nature', 'historical']
    elif 'gurme' in p:
        return ['gurme']  # Gurme sadece gurme yerlerini görsün
    elif 'efsane' in p:
        return ['historical', 'nature']
    return []


@api_bp.route('/places')
def get_places():
    try:
        places = Place.query.all()

        fav_place_ids = []
        user_persona_cats = []

        if current_user.is_authenticated:
            try:
                user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
                fav_place_ids = [f.place_id for f in user_favorites if f.place_id]
                user_persona_cats = get_persona_categories(current_user.selected_persona)
            except Exception:
                pass

        mekanlar_listesi = []
        for p in places:
            is_match = False
            if p.category in user_persona_cats:
                is_match = True

            mekanlar_listesi.append({
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "district": p.district,
                "rating": p.rating,
                "image_url": p.image_url,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "is_favorite": p.id in fav_place_ids,
                "is_persona_match": is_match
            })

        return jsonify({'success': True, 'data': mekanlar_listesi})
    except Exception as e:
        return jsonify({'success': False, 'data': [], 'error': str(e)})


# =====================================================================
# YENİ: AKILLANDIRILMIŞ VE KATI KURALLI YAPAY ZEKA ROTASI
# =====================================================================
@api_bp.route('/<string:item_type>s/<int:id>')
def get_item_detail(item_type, id):
    try:
        # 1. Veritabanından veriyi çekelim
        if item_type == 'place':
            item = db.session.get(Place, id)
        elif item_type == 'restaurant':
            item = db.session.get(Restaurant, id)
        else:
            return jsonify({'success': False, 'error': 'Geçersiz tür'})

        if not item:
            return jsonify({'success': False, 'error': 'Kayıt bulunamadı'})

        # 2. Chat kutusundan gelen soruyu yakalayalım (?q=...)
        user_query = request.args.get('q', '').strip()

        # 3. Persona ve Diyet
        if current_user.is_authenticated and getattr(current_user, 'selected_persona', None):
            persona_name = current_user.selected_persona
            diet_pref = getattr(current_user, 'diet_preference', 'standart').upper()
        else:
            persona_name = "Tarihçi"
            diet_pref = "STANDART"

        guzel_persona_ismi = persona_name.replace('_', ' ').title()

        # 4. Canlı Saat ve Hava Durumu
        current_time = datetime.now().strftime("%H:%M")
        weather_desc = "harika bir Antalya havası var"
        try:
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if api_key:
                w_url = f"http://api.openweathermap.org/data/2.5/weather?q=Antalya&appid={api_key}&units=metric&lang=tr"
                w_res = requests.get(w_url, timeout=3).json()
                if w_res.get('main'):
                    weather_desc = f"{round(w_res['main']['temp'])}°C ve {w_res['weather'][0]['description']}"
        except:
            pass

        # 5. VERİTABANI GERÇEKLERİ (Yapay zekanın sınırları)
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
            GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
            if not GEMINI_API_KEY:
                raise ValueError("API Anahtarı bulunamadı! Lütfen .env dosyasını kontrol et.")

            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.5-flash')


            # 6. KATI KURALLI, PROFESYONEL VE NET PROMPT
            prompt = f"""
                        Sen PersonaAntalya uygulamasının profesyonel, gerçekçi ve son derece dürüst yapay zeka asistanısın. 
                        Kullanıcı '{guzel_persona_ismi}' modunu seçtiği için bu perspektiften bilgiler vereceksin ancak ASLA lakayıt, ciddiyetsiz veya mekanın sahibiymiş gibi (örneğin 'kruvasanlarımız', 'hoş geldin canım', 'bizim lezzetlerimiz' vb.) konuşmayacaksın. Tıpkı standart bir yapay zeka gibi saygılı, net ve sadece gerçek bilgi odaklı olacaksın.

                        Konu Edilen Mekan: {item.name}

                        [VERİTABANINDAKİ GERÇEK BİLGİLER - BUNLAR DIŞINDA BİLGİ UYDURMAK YASAKTIR]
                        {db_context}

                        [CANLI BAĞLAM BİLGİLERİ]
                        - Anlık Saat: {current_time}
                        - Antalya Anlık Hava Durumu: {weather_desc}
                        - Turistin Beslenme Tercihi: {diet_pref}

                        [SÜPER KRİTİK GÖREVLER VE ASKERİ KURALLAR]
                        1. MENÜ VE FİYAT UYDURMAK KESİNLİKLE YASAKTIR: Kullanıcı sana menüyü, yemekleri veya fiyatları sorarsa ve [VERİTABANINDAKİ GERÇEK BİLGİLER] kısmında madde madde bir menü yoksa, KESİNLİKLE kafandan yiyecek veya içecek uydurma! Doğrudan, profesyonelce şunu söyle: "Bu mekanın detaylı menüsü ve güncel fiyat listesi internette dijital olarak paylaşılmamıştır, bu nedenle size kesin bir menü bilgisi sunamıyorum."
                        2. ÇALIŞMA SAATLERİ VE DURUM: Sadece yukarıdaki açılış/kapanış saatlerini baz alarak net cevap ver.
                        3. MEKAN ÇALIŞANI GİBİ DAVRANMA: Sen mekanın sahibi veya garsonu değilsin. "Lezzetlerimiz", "Bekleriz", "Yaptık" gibi kelimeler KULLANMA. Dışarıdan, objektif bir rehber gibi konuş.
                        4. KAPSAM DIŞI SORULAR: Eğer kullanıcı bu mekanla veya Antalya turizmiyle tamamen alakasız bir soru sorarsa (Örn: "Bana kod yaz", "Matematik çöz"), kibarca sadece mekan hakkında bilgi verebileceğini söyleyip reddet.
                        """

            # 7. ÇALIŞMA MODU SEÇİMİ
            if user_query:
                prompt += f"""
                            [SOHBET MODU]
                            Kullanıcı şu an sana şu soruyu sordu: "{user_query}"
                            Lütfen genel bir mekan tanıtımı YAPMA. Yukarıdaki katı kurallara uyarak sadece kullanıcının sorusuna net, profesyonel ve doğru bir cevap ver. Bilmiyorsan "Bilmiyorum/Veri bulunmuyor" de.
                            """
            else:
                prompt += f"""
                            [TANITIM MODU]
                            Kullanıcı henüz soru sormadı. Bu mekanı profesyonel bir dille tanıtan, saati ({current_time}), havayı ({weather_desc}) ve diyeti ({diet_pref}) metne doğalca yedirdiğin, objektif ve 2 paragraflık şık bir giriş yazısı hazırla.
                            """

            response = model.generate_content(prompt)
            yapay_zeka_hikayesi = response.text

        except Exception as gemini_error:
            print("\n" + "=" * 50)
            print("🚨 GEMINI API HATASI 🚨")
            print(f"Detay: {gemini_error}")
            print("=" * 50 + "\n")
            yapay_zeka_hikayesi = f"Burası harika bir yer! (Not: Yapay zeka sisteminde küçük bir pürüz oluştu, lütfen daha sonra tekrar dene)."

        return jsonify({
            'success': True,
            'persona_content': {
                'persona': guzel_persona_ismi,
                'story': yapay_zeka_hikayesi
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Lütfen giriş yapın.'})

        restaurants = Restaurant.query.all()

        try:
            user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
            favorite_ids = [f.restaurant_id for f in user_favorites if f.restaurant_id]
        except:
            favorite_ids = []

        data = []
        user_diet = getattr(current_user, 'diet_preference', 'standart')
        if not user_diet:
            user_diet = 'standart'
        user_diet = user_diet.lower()

        current_time_str = datetime.now().strftime("%H:%M")

        for r in restaurants:
            r_diet = getattr(r, 'diet_category', 'standart')
            if not r_diet:
                r_diet = 'standart'
            r_diet = r_diet.lower()

            is_suitable = False
            if user_diet == 'standart':
                is_suitable = True
            elif user_diet == 'vegan' and r_diet == 'vegan':
                is_suitable = True
            elif user_diet == 'vejetaryen' and r_diet in ['vejetaryen', 'vegan']:
                is_suitable = True
            elif user_diet == 'glutensiz' and r_diet == 'glutensiz':
                is_suitable = True
            elif user_diet == r_diet:
                is_suitable = True

            is_open = False
            open_t = getattr(r, 'opening_time', '09:00')
            close_t = getattr(r, 'closing_time', '23:30')

            if open_t <= close_t:
                is_open = open_t <= current_time_str <= close_t
            else:
                is_open = current_time_str >= open_t or current_time_str <= close_t

            data.append({
                'id': r.id,
                'name': r.name,
                'district': getattr(r, 'district', 'Merkez'),
                'latitude': r.latitude,
                'longitude': r.longitude,
                'image_url': getattr(r, 'image_url', ''),
                'diet_category': r_diet.upper(),
                'is_favorite': r.id in favorite_ids,
                'is_suitable': is_suitable,
                'price_level': getattr(r, 'price_level', '₺₺'),
                'is_open': is_open,
                'opening_time': open_t,
                'closing_time': close_t
            })

        return jsonify({'success': True, 'data': data})

    except Exception as e:
        print(f"Restoranlar çekilirken hata: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/favorites/toggle', methods=['POST'])
@login_required
def toggle_favorite():
    try:
        data = request.get_json()
        item_type = data.get('type')
        item_id = data.get('id')

        if not item_type or not item_id:
            return jsonify({'success': False, 'error': 'Geçersiz veri'})

        existing_fav = None
        if item_type == 'place':
            existing_fav = Favorite.query.filter_by(user_id=current_user.id, place_id=item_id).first()
        elif item_type == 'restaurant':
            existing_fav = Favorite.query.filter_by(user_id=current_user.id, restaurant_id=item_id).first()

        if existing_fav:
            db.session.delete(existing_fav)
            db.session.commit()
            return jsonify({'success': True, 'status': 'removed'})
        else:
            new_fav = Favorite(user_id=current_user.id)
            if item_type == 'place':
                new_fav.place_id = item_id
            elif item_type == 'restaurant':
                new_fav.restaurant_id = item_id

            db.session.add(new_fav)
            db.session.commit()
            return jsonify({'success': True, 'status': 'added'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/weather', methods=['GET'])
def get_weather():
    try:
        city = "Antalya"
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=tr"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_info = {
                'temp': round(data['main']['temp']),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon']
            }
            return jsonify({'success': True, 'data': weather_info})
        else:
            return jsonify({'success': False, 'error': 'Hava durumu servisine ulaşılamadı.'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/weather/coords', methods=['GET'])
def get_weather_coords():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        api_key = os.getenv("OPENWEATHER_API_KEY")

        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=tr"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_info = {
                'temp': round(data['main']['temp']),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon']
            }
            return jsonify({'success': True, 'data': weather_info})
        else:
            return jsonify({'success': False, 'error': 'Lokasyon havası alınamadı'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/reviews/add', methods=['POST'])
@login_required
def add_review():
    try:
        data = request.get_json()
        item_type = data.get('type')
        item_id = data.get('id')
        rating = data.get('rating')
        comment = data.get('comment', '')

        if not all([item_type, item_id, rating]):
            return jsonify({'success': False, 'error': 'Lütfen bir puan (yıldız) seçin.'})

        new_review = Review(user_id=current_user.id, rating=int(rating), comment=comment)

        if item_type == 'place':
            new_review.place_id = item_id
        elif item_type == 'restaurant':
            new_review.restaurant_id = item_id

        db.session.add(new_review)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Yorumun başarıyla eklendi!'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/reviews/get/<item_type>/<int:item_id>', methods=['GET'])
def get_reviews(item_type, item_id):
    try:
        if item_type == 'place':
            reviews = Review.query.filter_by(place_id=item_id).order_by(Review.created_at.desc()).all()
        else:
            reviews = Review.query.filter_by(restaurant_id=item_id).order_by(Review.created_at.desc()).all()

        review_list = []
        for r in reviews:
            if r.user.first_name and r.user.last_name:
                display_name = f"{r.user.first_name} {r.user.last_name}"
            elif getattr(r.user, 'username', None):
                display_name = r.user.username
            else:
                display_name = "Kayıtlı Kullanıcı"

            review_list.append({
                'id': r.id,
                'user_name': display_name,
                'rating': r.rating,
                'comment': r.comment,
                'date': r.created_at.strftime("%d.%m.%Y %H:%M")
            })

        return jsonify({'success': True, 'data': review_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})