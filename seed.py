from app import create_app, db
from app.models.place import Place
from app.models.restaurant import Restaurant

app = create_app()

def seed_database():
    with app.app_context():

        # ==========================================
        # 2. TURİSTİK MEKANLAR (GEZİ ROTALARI) - 50 ADET
        # ==========================================
        places = [
            # --- TARİHÇİ İÇİN (10 Mekan) ---
            Place(name="Kaleiçi (Old Town)", district="Muratpaşa", category="historical", rating=4.9,
                  image_url="/static/images/places/kaleici.jpg", latitude=36.8841, longitude=30.7050,
                  description="Antalya'nın kalbi, dar sokakları ve tarihi evleriyle."),
            Place(name="Hadrian Kapısı", district="Muratpaşa", category="historical", rating=4.8,
                  image_url="/static/images/places/hadrian.jpg", latitude=36.8850, longitude=30.7083),
            Place(name="Termessos Antik Kenti", district="Döşemealtı", category="historical", rating=4.9,
                  image_url="/static/images/places/termessos.jpg", latitude=36.9833, longitude=30.4633),
            Place(name="Olympos Antik Kenti", district="Kumluca", category="historical", rating=4.7,
                  image_url="/static/images/places/olympos.jpg", latitude=36.3983, longitude=30.4633),
            Place(name="Perge Antik Kenti", district="Aksu", category="historical", rating=4.8,
                  image_url="/static/images/places/perge.jpg", latitude=36.9589, longitude=30.8533),
            Place(name="Aspendos Tiyatrosu", district="Serik", category="historical", rating=5.0,
                  image_url="/static/images/places/aspendos.jpg", latitude=36.9392, longitude=31.1719),
            Place(name="Phaselis Antik Kenti", district="Kemer", category="historical", rating=4.9,
                  image_url="/static/images/places/phaselis.jpg", latitude=36.5514, longitude=30.5528),
            Place(name="Myra Antik Kenti", district="Demre", category="historical", rating=4.8,
                  image_url="/static/images/places/myra.jpg", latitude=36.2583, longitude=29.9833),
            Place(name="Xanthos Antik Kenti", district="Kaş", category="historical", rating=4.7,
                  image_url="/static/images/places/xanthos.jpg", latitude=36.3569, longitude=29.3183),
            Place(name="Antalya Müzesi", district="Muratpaşa", category="museum", rating=5.0,
                  image_url="/static/images/places/muze.jpg", latitude=36.8856, longitude=30.6800),

            # --- INFLUENCER İÇİN (10 Mekan) ---
            Place(name="Aşağı Düden Şelalesi", district="Muratpaşa", category="nature", rating=4.9,
                  image_url="/static/images/places/asagi_duden.jpg", latitude=36.8521, longitude=30.7831),
            Place(name="Kaputaş Plajı", district="Kaş", category="beach", rating=5.0,
                  image_url="/static/images/places/kaputas.jpg", latitude=36.2289, longitude=29.4492),
            Place(name="Land of Legends", district="Serik", category="nature", rating=4.8,
                  image_url="/static/images/places/legends.jpg", latitude=36.8767, longitude=31.0583),
            Place(name="Kekova Batık Şehir", district="Demre", category="historical", rating=4.9,
                  image_url="/static/images/places/kekova.jpg", latitude=36.1950, longitude=29.8450),
            Place(name="Kurşunlu Şelalesi", district="Aksu", category="nature", rating=4.8,
                  image_url="/static/images/places/kursunlu.jpg", latitude=36.9939, longitude=30.8256),
            Place(name="Tünektepe Teleferik", district="Konyaaltı", category="nature", rating=4.6,
                  image_url="/static/images/places/tunek.jpg", latitude=36.8300, longitude=30.5900),
            Place(name="Göynük Kanyonu", district="Kemer", category="nature", rating=4.8,
                  image_url="/static/images/places/goynuk.jpg", latitude=36.6667, longitude=30.5550),
            Place(name="Karaalioğlu Parkı", district="Muratpaşa", category="nature", rating=4.7,
                  image_url="/static/images/places/karaalioglu.jpg", latitude=36.8783, longitude=30.7067),
            Place(name="Sandland Kum Heykel", district="Muratpaşa", category="museum", rating=4.5,
                  image_url="/static/images/places/sandland.jpg", latitude=36.8456, longitude=30.7936),
            Place(name="Tazı Kanyonu", district="Manavgat", category="nature", rating=5.0,
                  image_url="/static/images/places/tazi.jpg", latitude=37.1956, longitude=31.1794),

            # --- MASALCI İÇİN (10 Mekan) ---
            Place(name="Olympos Yanartaş", district="Kumluca", category="nature", rating=4.8,
                  image_url="/static/images/places/yanartas.jpg", latitude=36.4311, longitude=30.4556),
            Place(name="Korsan Koyu", district="Kumluca", category="beach", rating=4.7,
                  image_url="/static/images/places/korsan.jpg", latitude=36.3150, longitude=30.4600),
            Place(name="Dim Mağarası", district="Alanya", category="nature", rating=4.6,
                  image_url="/static/images/places/dim.jpg", latitude=36.5400, longitude=32.1100),
            Place(name="Tahtalı Dağı Teleferik", district="Kemer", category="nature", rating=4.9,
                  image_url="/static/images/places/tahtali.jpg", latitude=36.5417, longitude=30.4417),
            Place(name="Adrasan Koyu", district="Kumluca", category="beach", rating=4.8,
                  image_url="/static/images/places/adrasan.jpg", latitude=36.3075, longitude=30.4650),
            Place(name="Karain Mağarası", district="Döşemealtı", category="historical", rating=4.6,
                  image_url="/static/images/places/karain.jpg", latitude=37.0783, longitude=30.5717),
            Place(name="Sülüklü Göl", district="Kaş", category="nature", rating=4.5,
                  image_url="/static/images/places/suluklu.jpg", latitude=36.4000, longitude=29.6000),
            Place(name="Yivli Minare", district="Muratpaşa", category="historical", rating=4.7,
                  image_url="/static/images/places/yivli.jpg", latitude=36.8867, longitude=30.7056),
            Place(name="Köprülü Kanyon", district="Manavgat", category="nature", rating=4.9,
                  image_url="/static/images/places/koprulu.jpg", latitude=37.1950, longitude=31.1783),
            Place(name="Göğübeli Yaylası", district="Elmalı", category="nature", rating=4.7,
                  image_url="/static/images/places/gogubeli.jpg", latitude=36.7369, longitude=29.9156),

            # --- EFSANE AVCISI İÇİN (10 Mekan) ---
            Place(name="Arykanda Antik Kenti", district="Finike", category="historical", rating=4.8,
                  image_url="/static/images/places/arykanda.jpg", latitude=36.5133, longitude=30.0583),
            Place(name="Sillyon Antik Kenti", district="Serik", category="historical", rating=4.5,
                  image_url="/static/images/places/sillyon.jpg", latitude=36.9883, longitude=30.9850),
            Place(name="Kocain Mağarası", district="Döşemealtı", category="nature", rating=4.6,
                  image_url="/static/images/places/kocain.jpg", latitude=37.1000, longitude=30.6500),
            Place(name="Beldibi Mağarası", district="Kemer", category="historical", rating=4.4,
                  image_url="/static/images/places/beldibi.jpg", latitude=36.7333, longitude=30.5667),
            Place(name="Rhodiapolis", district="Kumluca", category="historical", rating=4.5,
                  image_url="/static/images/places/rhodiapolis.jpg", latitude=36.3833, longitude=30.2667),
            Place(name="Lyrboton Kome", district="Kepez", category="historical", rating=4.4,
                  image_url="/static/images/places/lyrboton.jpg", latitude=36.9833, longitude=30.6333),
            Place(name="Antiocheia Ad Cragum", district="Gazipaşa", category="historical", rating=4.7,
                  image_url="/static/images/places/antiocheia.jpg", latitude=36.1500, longitude=32.4167),
            Place(name="Yalan Dünya Mağarası", district="Gazipaşa", category="nature", rating=4.8,
                  image_url="/static/images/places/yalan.jpg", latitude=36.2167, longitude=32.3833),
            Place(name="Uçansu Şelalesi", district="Serik", category="nature", rating=4.6,
                  image_url="/static/images/places/ucansu.jpg", latitude=37.0500, longitude=30.9667),
            Place(name="Gökbük Kanyonu", district="Finike", category="nature", rating=4.5,
                  image_url="/static/images/places/gokbuk.jpg", latitude=36.4333, longitude=30.1333),

            # --- GURME (EFSANEVİ LEZZET DURAKLARI) İÇİN (10 Mekan) ---
            Place(name="Topçu Kebap (1885)", district="Muratpaşa", category="gurme", rating=4.9,
                  image_url="/static/images/places/topcu.jpg", latitude=36.8860, longitude=30.7040,
                  description="Antalya'nın en eski restoranı, tahinli piyazın ve şiş köftenin doğduğu efsanevi mekan."),
            Place(name="Börekçi Tevfik", district="Muratpaşa", category="gurme", rating=4.9,
                  image_url="/static/images/places/tevfik.jpg", latitude=36.8855, longitude=30.7050,
                  description="1930'lardan beri aynı dükkanda, hamuru havada çevirerek yapılan meşhur serpme börek efsanesi."),
            Place(name="Akdeniz Dondurma (Merkez)", district="Muratpaşa", category="gurme", rating=4.8,
                  image_url="/static/images/places/akdeniz.jpg", latitude=36.8872, longitude=30.7035,
                  description="Antalya'ya özgü keçi sütlü 'Yanık Dondurma'nın ilk adreslerinden, tarihi bir tatlı molası."),
            Place(name="Yenigün Reçelleri Tarihi Mağazası", district="Muratpaşa", category="gurme", rating=4.7,
                  image_url="/static/images/places/yenigun.jpg", latitude=36.8850, longitude=30.7060,
                  description="Patlıcandan bergamota, Antalya'nın ünlü reçel kültürünü yaşatan asırlık dükkan."),
            Place(name="Hakkı Baba Dönercisi", district="Muratpaşa", category="gurme", rating=4.8,
                  image_url="/static/images/places/hakkibaba.jpg", latitude=36.8830, longitude=30.7020,
                  description="1924'ten beri odun ateşinde yaprak döner yapan, şehrin en köklü lezzet miraslarından biri."),
            Place(name="Şişçi Ramazan", district="Korkuteli", category="gurme", rating=4.9,
                  image_url="/static/images/places/ramazan.jpg", latitude=37.0655, longitude=30.1965,
                  description="Antalya'nın meşhur şiş köfte ve tahinli piyaz ikilisinin Toroslardaki efsanevi temsilcisi."),
            Place(name="Dönerciler Çarşısı", district="Muratpaşa", category="gurme", rating=4.5,
                  image_url="/static/images/places/donerciler.jpg", latitude=36.8865, longitude=30.7045,
                  description="Şehrin tam kalbinde, yan yana dizilmiş tarihi dönercilerin iştah açan kokularıyla dolu çarşı."),
            Place(name="Tarihi Çaybaşı Simit Fırını", district="Muratpaşa", category="gurme", rating=4.7,
                  image_url="/static/images/places/caybasi.jpg", latitude=36.8810, longitude=30.7100,
                  description="Odun ateşinde pişen, Antalya'ya özgü pekmezli çıtır simitlerin çıktığı asırlık fırın."),
            Place(name="Parlak Restaurant", district="Muratpaşa", category="gurme", rating=4.6,
                  image_url="/static/images/places/parlak.jpg", latitude=36.8875, longitude=30.7055,
                  description="1950'lerden beri kapısında kömür ateşinde piliç çevrilen, Antalya yerlisinin vazgeçilmez mekanı."),
            Place(name="Nur Pastanesi (Yanık Dondurma)", district="Korkuteli", category="gurme", rating=4.8,
                  image_url="/static/images/places/nur.jpg", latitude=37.0660, longitude=30.1970,
                  description="Torosların karı ve keçi sütüyle yapılan yanık dondurma efsanesinin Korkuteli'ndeki doğuş noktası."),
        ]

        # ==========================================
        # 3. RESTORANLAR (BESLENME TERCİHLERİ) - 40 ADET
        # ==========================================
        restaurants = [
            # --- STANDART (10 Restoran) ---
            Restaurant(name="7 Mehmet", district="Konyaaltı", diet_category="standart", rating=5.0,
                       image_url="/static/images/rests/7mehmet.jpg", latitude=36.8833, longitude=30.6667, price_level="₺₺₺", opening_time="11:00", closing_time="23:30"),
            Restaurant(name="Piyazcı Sami", district="Muratpaşa", diet_category="standart", rating=4.7,
                       image_url="/static/images/rests/sami.jpg", latitude=36.8845, longitude=30.7060, price_level="₺"),
            Restaurant(name="Börekçi Tevfik", district="Muratpaşa", diet_category="standart", rating=4.8,
                       image_url="/static/images/rests/tevfik.jpg", latitude=36.8850, longitude=30.7055, price_level="₺"),
            Restaurant(name="Sıralı Kebap", district="Muratpaşa", diet_category="standart", rating=4.9,
                       image_url="/static/images/rests/sirali.jpg", latitude=36.8520, longitude=30.7780, price_level="₺₺₺"),
            Restaurant(name="Balıkçı Hasan", district="Muratpaşa", diet_category="standart", rating=4.6,
                       image_url="/static/images/rests/hasan.jpg", latitude=36.8810, longitude=30.7040, price_level="₺₺₺"),
            Restaurant(name="Vahap Usta Et", district="Konyaaltı", diet_category="standart", rating=4.8,
                       image_url="/static/images/rests/vahap.jpg", latitude=36.8640, longitude=30.6380, price_level="₺₺₺"),
            Restaurant(name="Konyalılar Restoran", district="Muratpaşa", diet_category="standart", rating=4.5,
                       image_url="/static/images/rests/konyalilar.jpg", latitude=36.8900, longitude=30.7100, price_level="₺₺"),
            Restaurant(name="Asmani Restaurant", district="Muratpaşa", diet_category="standart", rating=4.9,
                       image_url="/static/images/rests/asmani.jpg", latitude=36.8600, longitude=30.7300, price_level="₺₺₺"),
            Restaurant(name="Ulupınar Şelale", district="Kemer", diet_category="standart", rating=4.7,
                       image_url="/static/images/rests/ulupinar.jpg", latitude=36.4200, longitude=30.4500, price_level="₺₺"),
            Restaurant(name="Akdeniz Dondurma", district="Muratpaşa", diet_category="standart", rating=4.8,
                       image_url="/static/images/rests/dondurma.jpg", latitude=36.8870, longitude=30.7030, price_level="₺"),

            # --- VEGAN (10 Restoran) ---
            Restaurant(name="Vegan House", district="Muratpaşa", diet_category="vegan", rating=4.9,
                       image_url="/static/images/rests/veganhouse.jpg", latitude=36.8790, longitude=30.7120, price_level="₺₺"),
            Restaurant(name="Rokka Pizza", district="Muratpaşa", diet_category="vegan", rating=4.8,
                       image_url="/static/images/rests/rokka.jpg", latitude=36.8840, longitude=30.7040, price_level="₺₺"),
            Restaurant(name="Leman Kültür", district="Konyaaltı", diet_category="vegan", rating=4.5,
                       image_url="/static/images/rests/leman.jpg", latitude=36.8650, longitude=30.6400, price_level="₺₺"),
            Restaurant(name="The Sudd Coffee", district="Muratpaşa", diet_category="vegan", rating=4.7,
                       image_url="/static/images/rests/sudd.jpg", latitude=36.8520, longitude=30.7770, price_level="₺₺"),
            Restaurant(name="Pancho Villa", district="Muratpaşa", diet_category="vegan", rating=4.6,
                       image_url="/static/images/rests/pancho.jpg", latitude=36.8810, longitude=30.7090, price_level="₺₺"),
            Restaurant(name="Kaleiçi Meyhanesi", district="Muratpaşa", diet_category="vegan", rating=4.8,
                       image_url="/static/images/rests/meyhane.jpg", latitude=36.8830, longitude=30.7050, price_level="₺₺₺"),
            Restaurant(name="Oburus Momus", district="Kaş", diet_category="vegan", rating=4.9,
                       image_url="/static/images/rests/oburus.jpg", latitude=36.2000, longitude=29.6370, price_level="₺₺"),
            Restaurant(name="Pisekar Vegan Cafe", district="Muratpaşa", diet_category="vegan", rating=4.7,
                       image_url="/static/images/rests/pisekar.jpg", latitude=36.8850, longitude=30.7150, price_level="₺₺"),
            Restaurant(name="Doğal Yaşam Evi", district="Döşemealtı", diet_category="vegan", rating=4.8,
                       image_url="/static/images/rests/dogal.jpg", latitude=36.9850, longitude=30.5830, price_level="₺₺"),
            Restaurant(name="Roots Cafe", district="Muratpaşa", diet_category="vegan", rating=4.6,
                       image_url="/static/images/rests/roots.jpg", latitude=36.8800, longitude=30.7000, price_level="₺₺"),

            # --- VEJETARYEN (10 Restoran) ---
            Restaurant(name="Vanilla Lounge", district="Muratpaşa", diet_category="vejetaryen", rating=4.9,
                       image_url="/static/images/rests/vanilla.jpg", latitude=36.8842, longitude=30.7045, price_level="₺₺₺"),
            Restaurant(name="Nar Beach Bistro", district="Muratpaşa", diet_category="vejetaryen", rating=4.5,
                       image_url="/static/images/rests/nar.jpg", latitude=36.8780, longitude=30.7030, price_level="₺₺"),
            Restaurant(name="Pio Gastro Bar", district="Muratpaşa", diet_category="vejetaryen", rating=4.7,
                       image_url="/static/images/rests/pio.jpg", latitude=36.8835, longitude=30.7040, price_level="₺₺₺"),
            Restaurant(name="Seraser Fine Dining", district="Muratpaşa", diet_category="vejetaryen", rating=5.0,
                       image_url="/static/images/rests/seraser.jpg", latitude=36.8838, longitude=30.7052, price_level="₺₺₺"),
            Restaurant(name="Big Yellow Taxi", district="Konyaaltı", diet_category="vejetaryen", rating=4.4,
                       image_url="/static/images/rests/taxi.jpg", latitude=36.8660, longitude=30.6420, price_level="₺₺"),
            Restaurant(name="Shakespeare Bistro", district="Muratpaşa", diet_category="vejetaryen", rating=4.6,
                       image_url="/static/images/rests/shakespeare.jpg", latitude=36.8530, longitude=30.7760, price_level="₺₺"),
            Restaurant(name="Mermerli Restaurant", district="Muratpaşa", diet_category="vejetaryen", rating=4.8,
                       image_url="/static/images/rests/mermerli.jpg", latitude=36.8820, longitude=30.7030, price_level="₺₺₺"),
            Restaurant(name="Ayar Meyhanesi", district="Muratpaşa", diet_category="vejetaryen", rating=4.7,
                       image_url="/static/images/rests/ayar.jpg", latitude=36.8840, longitude=30.7060, price_level="₺₺₺"),
            Restaurant(name="Karaf Wine Bistro", district="Muratpaşa", diet_category="vejetaryen", rating=4.9,
                       image_url="/static/images/rests/karaf.jpg", latitude=36.8830, longitude=30.7055, price_level="₺₺"),
            Restaurant(name="The Beaver Coffee", district="Muratpaşa", diet_category="vejetaryen", rating=4.6,
                       image_url="/static/images/rests/beaver.jpg", latitude=36.8815, longitude=30.7080, price_level="₺₺"),

            # --- GLUTENSİZ (10 Restoran) ---
            Restaurant(name="Glutensiz Ada Cafe", district="Muratpaşa", diet_category="glutensiz", rating=4.8,
                       image_url="/static/images/rests/glutensizada.jpg", latitude=36.8900, longitude=30.7100, price_level="₺₺"),
            Restaurant(name="Çölyakla Yaşam Kafe", district="Muratpaşa", diet_category="glutensiz", rating=4.9,
                       image_url="/static/images/rests/colyak.jpg", latitude=36.8880, longitude=30.7050, price_level="₺₺"),
            Restaurant(name="Quppa Caffe", district="Konyaaltı", diet_category="glutensiz", rating=4.6,
                       image_url="/static/images/rests/quppa.jpg", latitude=36.8650, longitude=30.6440, price_level="₺₺"),
            Restaurant(name="Sıralı Kebap (Glutensiz)", district="Muratpaşa", diet_category="glutensiz", rating=4.8,
                       image_url="/static/images/rests/sirali.jpg", latitude=36.8520, longitude=30.7780, price_level="₺₺₺"),
            Restaurant(name="Balıkçı İrfan", district="Muratpaşa", diet_category="glutensiz", rating=4.7,
                       image_url="/static/images/rests/irfan.jpg", latitude=36.8800, longitude=30.7020, price_level="₺₺₺"),
            Restaurant(name="Antalya Steakhouse", district="Muratpaşa", diet_category="glutensiz", rating=4.8,
                       image_url="/static/images/rests/steakhouse.jpg", latitude=36.8540, longitude=30.7750, price_level="₺₺₺"),
            Restaurant(name="Vegan House (Glutensiz)", district="Muratpaşa", diet_category="glutensiz", rating=4.7,
                       image_url="/static/images/rests/veganhouse.jpg", latitude=36.8790, longitude=30.7120, price_level="₺₺"),
            Restaurant(name="Günaydın Kebap", district="Muratpaşa", diet_category="glutensiz", rating=4.6,
                       image_url="/static/images/rests/gunaydin.jpg", latitude=36.8600, longitude=30.7300, price_level="₺₺₺"),
            Restaurant(name="SushiCo", district="Muratpaşa", diet_category="glutensiz", rating=4.7,
                       image_url="/static/images/rests/sushico.jpg", latitude=36.8550, longitude=30.7740, price_level="₺₺₺"),

        ]

        # Toplu ekleme işlemi
        db.session.add_all(places)
        db.session.add_all(restaurants)

        try:
            db.session.commit()
            print(f"BAŞARILI: {len(places)} mekan ve {len(restaurants)} restoran eklendi!")
        except Exception as e:
            db.session.rollback()
            print(f"HATA: Veri eklenirken bir sorun oluştu: {e}")

if __name__ == "__main__":
    seed_database()