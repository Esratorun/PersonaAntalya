from app import create_app, db

app = create_app()

#Uygulama ayağa kalkmadan önce veritabanı tablolarını oluşturur.
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Sunucumuzu başlatıyoruz (host='0.0.0.0' diyerek diğer cihazlardan da girilebilmesini sağladık)
    app.run(debug=True, host='0.0.0.0')