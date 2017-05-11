#!/usr/bin/python

#gazzeter
gaz_sp = ["jiwa", "anak", "orang","warga","pasien","kasus","nyawa","penderita", "balita"]

gaz_o = ["demam", "berdarah", "dengue", "dbd", "db", "nyamuk", "di", "dan", "jadi", "kejadian", "harian", "minta", "waspada", "sepanjang", "tahu", "kampung", "sudah", "dalam", "puncak", "pasar", "tenggak", "deng", "gunawan", "kompas", "antara", "kesehatan", "kecil", "musi", "kalau", "deket", "ema", "kalian", "dari", "dalam", "bulan", "data", "haha", "berita", "2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020", "harap", "muncul","kalo","pada", "tawar", "merah", "pertengahan", "penyakit", "makan", "nya", "gua", "gue", "moga", "seneng", "banget", "bosen", "dah", "ta", "gada", "gara", "suruh", "tua", "dai", "kawan", "tangkis", "lawan", "tajuk", "fase", "besan", "selesai", "nyamok", "sadar", "bareng", "aman", "mantan", "butuh", "tanda", "mata", "akar", "cinta", "dukun", "banget", "teriak", "lancar", "batu", "mama", "moga", "sawah", "maen", "abang", "sarang", "pejuang", "danger", "pisan", "kopi", "taruna", "samaan", "ria", "bah", "situ", "mata", "bener", "bende", "jarum", "kamar", "panas", "isu", "mas", "suka", "parit", "mikir", "tembaga", "bareng", "muka", "kali", "dah", "sayang", "gada", "buk", "bobo", "lomba", "bayu", "selamat", "tipes", "utama", "long", "urat", "buntu", "kwa", "tes", "lewa", "dukun", "buruan", "pemulihan", "kayo", "dalil", "asam", "bu", "semangat", "kurma", "soon", "soa", "menang", "semangat", "sejati", "setia", "sampe", "kudu", "amal", "luas", "angkatan", "jamu", "kasih", "kantor", "bagus", "rawan", "kudu", "berkah", "manis", "titik", "teramat", "daun", "mendung", "karang", "sumber", "tukang", "kantor", "bola", "terjan", "kebon", "poko", "nonong", "waras", "kabar", "dingin", "jambu", "bengkak", "penyakitnya", "tenang", "suci", "tinggal" "negara", "peso", "bangun", "opo", "ladang", "kering", "sirih", "belalang", "mam", "ketinggalan", "bocor", "penurunan", "lambung", "besi", "ayah", "dateng", "anyar", "ruang", "alami", "negara", "sita"]
# gaz_o = ["demam", "berdarah", "dengue", "dbd", "db", "nyamuk"]
gaz_knd = ["tewas", "sakit", "derita", "kena", "rawat", "korban", "keritis", "mati", "kritis", "tinggal", "layang", "bunuh", "serang", "tular", "jangkit", "idap", "pengidap", "bahaya", "alami", "nyerang", "renggut","telan", "jatuh", "intai", "tumbang", "kepung", "indikasi", "cabut"]

#apabila di stemming maka kondisi diubah menjadi kata dasar. (penderita = derita)
gaz_org = ["warga","pemkot", "dinkes", "pemda", "pemkab", "dinas", "pemerintah", "rs", "rsa", "rsud", "rsu", "rsi", "rsj", "dprd", "kecamatan", "kabupaten", "kota", "desa", "pemdes", "kab","who", "puskesmas","korpri","kelurahan", "provinsi", "menkes","pmi","kab", "klinik","ugd", "dprd", "polda", "rspad", "rsij", "bpjs", "kelurahan", "rsia", "rsab", "polsek", "skalanews"]
#"kabupaten", 
#gaz_org delete warga

array_kon_mati = ["tewas", "mati", "bunuh", "tinggal", "layang", "renggut", "telan"]

array_kon_penderita = ["sakit", "derita", "kena", "rawat", "korban", "derita", "keritis", "tular", "jangkit", "idap", "alami"]

month = {"jan":"Januari","feb":"Februari","mar":"Maret","apr":"April","may":"Mei","jun":"Juni","jul":"Juli","aug":"Agustus","sep":"September","oct":"Oktober","nov":"November","dec":"Desember"}

month_index = {"Januari":"jan","Februari":"feb","Maret":"mar","April":"apr","Mei":"may","Juni":"jun","Juli":"jul","Agustus":"aug","September":"sep","Oktober":"oct","November":"nov","Desember":"dec"}

month_num = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]