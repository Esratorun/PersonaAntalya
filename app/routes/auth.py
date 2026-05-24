from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

# 'auth' adında yeni bir rota grubu oluşturuyoruz
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/kayit', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(">>> 1. KAYIT BUTONUNA BASILDI! <<<")
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Veritabanında bu e-posta var mı kontrol et
        user = User.query.filter_by(email=email).first()
        if user:
            print(">>> 2. HATA: BU E-POSTA ZATEN VAR <<<")
            flash('Bu e-posta adresi zaten kullanılıyor. Lütfen giriş yapın.', 'danger')
            return redirect(url_for('auth.register'))

        print(">>> 3. YENİ KULLANICI VERİTABANINA EKLENİYOR <<<")
        # Yeni kullanıcıyı güvenli şifre (hash) ile oluşturuyoruz
        yeni_kullanici = User(
            email=email,
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(yeni_kullanici)
        db.session.commit()

        print(">>> 4. KAYIT BAŞARILI, GİRİŞ SAYFASINA YÖNLENDİRİLİYOR <<<")
        flash('Kayıt başarılı! Şimdi giriş yapabilirsin.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/giris', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(">>> 1. GİRİŞ BUTONUNA BASILDI! <<<")
        email = request.form.get('email')
        password = request.form.get('password')

        # Kullanıcıyı e-postasıyla bul
        user = User.query.filter_by(email=email).first()

        if user:
            print(f">>> 2. KULLANICI BULUNDU: {user.username} <<<")
            if check_password_hash(user.password_hash, password):
                print(">>> 3. ŞİFRE DOĞRU! GİRİŞ YAPILIYOR <<<")
                login_user(user)  # Flask-Login'e kullanıcıyı tanıtıyoruz
                flash('Giriş başarılı. Hoş geldin!', 'success')

                # =========================================================
                # YENİ: AKILLI YÖNLENDİRME (ONBOARDING KONTROLÜ)
                # =========================================================
                # Eğer kullanıcının henüz bir personası yoksa (yeni üyeyse) seçim ekranına gitsin
                if not getattr(user, 'selected_persona', None):
                    print(">>> 4. PERSONASI YOK, SEÇİM EKRANINA YÖNLENDİRİLİYOR <<<")
                    return redirect(url_for('main.persona_select'))

                # Eğer kullanıcının zaten bir personası varsa doğrudan Keşfet (harita) sayfasına gitsin
                print(">>> 4. PERSONASI VAR, DOĞRUDAN KEŞFET SAYFASINA YÖNLENDİRİLİYOR <<<")
                # Not: Eğer rota ismin 'explore' ise böyle kalabilir, farklıysa burayı güncelleyebilirsin.
                return redirect(url_for('main.explore'))

            else:
                print(">>> 3. HATA: ŞİFRE YANLIŞ! <<<")
                flash('Giriş bilgileri hatalı. Şifreni kontrol et.', 'danger')
        else:
            print(">>> 2. HATA: BÖYLE BİR E-POSTA VERİTABANINDA YOK! <<<")
            flash('Giriş bilgileri hatalı. E-postanı kontrol et.', 'danger')

    return render_template('login.html')


@auth_bp.route('/cikis')
@login_required
def logout():
    logout_user()
    flash('Güvenle çıkış yaptın. Görüşmek üzere!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/sifremi-unuttum', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Şimdilik sadece simüle ediyoruz
        flash('Şifre sıfırlama bağlantısı e-posta adresine gönderildi.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')