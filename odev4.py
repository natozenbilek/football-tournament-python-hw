# Introduction to Python, Ödev 4
# IEEE Hacettepe University Student Branch, Güz 2026
#
# Bu ödevin sonunda kendi function'larınızı yazıp onlardan değer alan,
# print ile return'ü ayıran, hatalı girdide yeniden soran ve kendi
# class'ını yazan programlar yazabileceksiniz. Tema: fakülteler arası
# futbol turnuvası.
#
# Son teslim: 15 Kasım 2026 Pazar 23.59
# Teslim formu: https://forms.gle/eMHjvPfSRP9cp1JH7
# Ödev reposu: https://github.com/natozenbilek/football-tournament-python-hw
#
# Ödevi nasıl yapacaksınız
# 1. Bu dosyayı kontrol.py ile birlikte python-kurs klasörünüze koyun ve
#    PyCharm'da açın.
# 2. Her görevde "# TODO" satırının yerine kodunuzu yazın. Function'ların
#    ve class'ın ilk satırları hazır; gövdedeki pass'i silip kendi
#    satırlarınızı yazın.
# 3. Dosyayı Run ile çalıştırın. Her görevin başlık satırından sonraki
#    çıktısı, o görevin "Beklenen çıktı" kısmıyla birebir aynı olmalı.
#    4. görev sizden sayı ister: Run penceresine yazıp Enter'a basın.
# 4. Bitince formda "İsim" alanına isminizi yazın, odev4.py'yi "Ödev dosyası"
#    alanına yükleyin ve "Kişisel verileriniz" sorusundaki onay kutusunu
#    işaretleyin. Söylemek istediğiniz bir şey varsa "Açıklama" alanına
#    yazabilirsiniz; bu alan isteğe bağlı.
#
# Dosya bu haliyle de hatasız çalışır: function'lar henüz bir şey return
# etmediği için çıktıda None görürsünüz.
# Yalnızca Ders 1, 2, 3 ve 4'te gördüğümüz yapıları kullanın.


print("=== 1. Puan ===")
# Turnuvada galibiyet 3 puan, beraberlik 1 puan, yenilgi 0 puan.
# points(wins, draws) function'ı takımın puanını return etsin; wins galibiyet,
# draws beraberlik sayısı.
# Function ekrana bir şey yazmasın; yazmayı aşağıdaki print satırları yapar.


def points(wins, draws):
    # TODO
    pass


print("Mühendislik:", points(4, 1))
print("Tıp:", points(2, 3))
print("Hukuk:", points(0, 5))
#
# Beklenen çıktı:
# Mühendislik: 13
# Tıp: 9
# Hukuk: 5


print("=== 2. Maçın sonucu ===")
# result(home, away) ev sahibinin (home) ve deplasmanın (away) attığı golleri
# alsın ve maçın sonucunu bir str olarak return etsin: ev sahibinin golü
# fazlaysa "ev sahibi kazandı", deplasmanınki fazlaysa "deplasman kazandı",
# eşitse "berabere".
# if, elif ve else kullanın; her dalda bir return olsun.


def result(home, away):
    # TODO
    pass


print("Mühendislik 2-1 Tıp:", result(2, 1))
print("Hukuk 0-0 Eczacılık:", result(0, 0))
print("Tıp 1-3 Hukuk:", result(1, 3))
#
# Beklenen çıktı:
# Mühendislik 2-1 Tıp: ev sahibi kazandı
# Hukuk 0-0 Eczacılık: berabere
# Tıp 1-3 Hukuk: deplasman kazandı


print("=== 3. Bozuk iki function ===")
# Aşağıdaki iki function hata vermeden çalışıyor ama yanlış sonuç veriyor.
# İkisini de düzeltin. Her birinin altındaki "# Neden:" satırına neden
# bozuk olduğunu tek cümleyle yazın.


def goal_difference(scored, conceded):
    print(scored - conceded)


# Neden:


def add_goals(total, goals):
    total = total + goals


# Neden:


difference = goal_difference(9, 4)
print("Gol farkı:", difference)
total = 0
add_goals(total, 3)
add_goals(total, 2)
print("Toplam gol:", total)
# Function'ları düzelttikten sonra bu satırlardan gerekenleri de değiştirin.
#
# Beklenen çıktı:
# Gol farkı: 5
# Toplam gol: 5


print("=== 4. Skoru sormak ===")
# ask_score(prompt, low, high), prompt'u gösterip kullanıcıdan bir tam sayı
# istesin ve sayı low ile high arasında (ikisi de dahil) gelene kadar
# yeniden sorsun. Tam sayı yazılmazsa "Tam sayı girin." yazsın; sayı
# aralığın dışındaysa f-string ile "0 ile 20 arasında bir sayı girin."
# gibi low ve high'ı yazsın. Doğru sayıyı return etsin.
# while True, try ve except ValueError kullanın.
# Çalıştırınca sırayla üç, 25 ve 3 yazın.


def ask_score(prompt, low, high):
    # TODO
    pass


goals = ask_score("Mühendislik kaç gol attı? ", 0, 20)
print("Mühendislik", goals, "gol attı.")
#
# Beklenen çıktı:
# Mühendislik kaç gol attı? üç
# Tam sayı girin.
# Mühendislik kaç gol attı? 25
# 0 ile 20 arasında bir sayı girin.
# Mühendislik kaç gol attı? 3
# Mühendislik 3 gol attı.


print("=== 5. Oyuncu ===")
# Player class'ının her object'i bir oyuncunun adını (name), forma
# numarasını (number) ve attığı gol sayısını (goals) tutsun.
# - __init__ name ve number'ı attribute olarak saklasın; goals 0'dan başlasın.
# - score_goal() oyuncunun golünü bir artırsın.
# - summary() "Arda (10): 2 gol" biçiminde bir str return etsin.


class Player:
    def __init__(self, name, number):
        # TODO
        pass

    def score_goal(self):
        # TODO
        pass

    def summary(self):
        # TODO
        pass


arda = Player("Arda", 10)
kerem = Player("Kerem", 7)
arda.score_goal()
kerem.score_goal()
arda.score_goal()
print(arda.summary())
print(kerem.summary())
#
# Beklenen çıktı:
# Arda (10): 2 gol
# Kerem (7): 1 gol


print("=== Meraklısına ===")
# Zorunlu değil.
# Final berabere bitti, penaltılara gidiliyor. import random ile bir
# penalty() function'ı yazın: random.randint(1, 4) 1 gelirse kaleci
# kurtarsın ve function False, yoksa True return etsin. İki takım beşer
# penaltı atsın; golleri iki counter ile sayın (home ve away). Beş penaltıdan sonra
# eşitlik sürerse, eşitlik bozulana kadar takımlar birer penaltı daha
# atsın (while). Sonucu ve kazananı yazdırın.
# TODO
#
# Örnek çıktı (sayılar her çalıştırmada değişir):
# Penaltılar: Mühendislik 4 - 3 Tıp
# Kazanan: Mühendislik
