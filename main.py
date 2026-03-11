
# ============================================================
#  main.py  –  Seda Elektronik sedaio API Kod Rehberi
#  Bu dosya bir KOD REHBERİDİR. Kullanmak istediğiniz
#  bölümün yorum (#) işaretini kaldırın ve çalıştırın.
# ============================================================

# GEREKSİNİMLER:
#   pip install requests
#   py -m pip install requests veya python -m pip install requests
#
# DOSYA YAPISI:
#   project/
#       sedaio.py   <-- API kütüphanesi (bu dosyayla aynı klasörde olmalı)
#       main.py     <-- bu dosya

from sedaio import (
    HttpRelay, TcpRelay, UdpRelay,
    # --- Röle AÇMA ---
    R1_1, R2_1, R3_1, R4_1, R5_1, R6_1, R7_1, R8_1,
    R9_1, R10_1, R11_1, R12_1, R13_1, R14_1, R15_1, R16_1,
    # --- Röle KAPATMA ---
    R1_0, R2_0, R3_0, R4_0, R5_0, R6_0, R7_0, R8_0,
    R9_0, R10_0, R11_0, R12_0, R13_0, R14_0, R15_0, R16_0,
    # --- Röle TOGGLE ---
    R1_T, R2_T, R3_T, R4_T, R5_T, R6_T, R7_T, R8_T,
    R9_T, R10_T, R11_T, R12_T, R13_T, R14_T, R15_T, R16_T,
    # --- Özel ---
    ALL, OFF, NetCon,
    # --- TCP Linkage ---
    linkage_1_8, normal_1_8, linkage_9_16, normal_9_16,
    la_no_1_8, la_no_9_16,
)

# ============================================================
#  BAĞLANTI BİLGİLERİ  –  IP ve Port numarasını değiştirin
# ============================================================

IP   = "169.254.1.2" # Ethernet röle kartınızın ip no ve port numaralarını bu alana giriniz.
PORT = 3000


# ╔══════════════════════════════════════════════════════════╗
#  1. BÖLÜM: HTTP GET  (HttpRelay)
# ╚══════════════════════════════════════════════════════════╝
#
#  Nesneyi if __name__ == "__main__": bloğu içinde oluşturun.
#  Böylece cihaza ulaşılamasa bile import sırasında hata almazsınız.
#
#  get = HttpRelay(IP, PORT)

# ── A) Röle Açma ─────────────────────────────────────────
# get.relay_on(R1_1)    # Röle 1  aç  -> GET /1
# get.relay_on(R2_1)    # Röle 2  aç  -> GET /2
# get.relay_on(R3_1)    # Röle 3  aç  -> GET /3
# get.relay_on(R4_1)    # Röle 4  aç  -> GET /4
# get.relay_on(R5_1)    # Röle 5  aç  -> GET /5
# get.relay_on(R6_1)    # Röle 6  aç  -> GET /6
# get.relay_on(R7_1)    # Röle 7  aç  -> GET /7
# get.relay_on(R8_1)    # Röle 8  aç  -> GET /8
# get.relay_on(R9_1)    # Röle 9  aç  -> GET /9
# get.relay_on(R10_1)   # Röle 10 aç  -> GET /0
# get.relay_on(R11_1)   # Röle 11 aç  -> GET /a
# get.relay_on(R12_1)   # Röle 12 aç  -> GET /b
# get.relay_on(R13_1)   # Röle 13 aç  -> GET /c
# get.relay_on(R14_1)   # Röle 14 aç  -> GET /d
# get.relay_on(R15_1)   # Röle 15 aç  -> GET /e
# get.relay_on(R16_1)   # Röle 16 aç  -> GET /L
# get.relay_on(ALL)     # Tüm röleler aç -> GET /ALL

# ── B) Röle Kapatma ───────────────────────────────────────
# get.relay_off(R1_0)   # Röle 1  kapat -> GET /i
# get.relay_off(R2_0)   # Röle 2  kapat -> GET /g
# get.relay_off(R3_0)   # Röle 3  kapat -> GET /h
# get.relay_off(R4_0)   # Röle 4  kapat -> GET /j
# get.relay_off(R5_0)   # Röle 5  kapat -> GET /k
# get.relay_off(R6_0)   # Röle 6  kapat -> GET /l
# get.relay_off(R7_0)   # Röle 7  kapat -> GET /m
# get.relay_off(R8_0)   # Röle 8  kapat -> GET /n
# get.relay_off(R9_0)   # Röle 9  kapat -> GET /o
# get.relay_off(R10_0)  # Röle 10 kapat -> GET /p
# get.relay_off(R11_0)  # Röle 11 kapat -> GET /q
# get.relay_off(R12_0)  # Röle 12 kapat -> GET /t
# get.relay_off(R13_0)  # Röle 13 kapat -> GET /u
# get.relay_off(R14_0)  # Röle 14 kapat -> GET /v
# get.relay_off(R15_0)  # Röle 15 kapat -> GET /w
# get.relay_off(R16_0)  # Röle 16 kapat -> GET /M
# get.relay_off(OFF)    # Tüm röleler kapat -> GET /OFF

# ── C) Röle Toggle ────────────────────────────────────────
# get.relay_toggle(R1_T)    # Röle 1  toggle -> GET /y0
# get.relay_toggle(R2_T)    # Röle 2  toggle -> GET /y1
# get.relay_toggle(R3_T)    # Röle 3  toggle -> GET /y2
# get.relay_toggle(R4_T)    # Röle 4  toggle -> GET /y3
# get.relay_toggle(R5_T)    # Röle 5  toggle -> GET /y4
# get.relay_toggle(R6_T)    # Röle 6  toggle -> GET /y5
# get.relay_toggle(R7_T)    # Röle 7  toggle -> GET /y6
# get.relay_toggle(R8_T)    # Röle 8  toggle -> GET /y7
# get.relay_toggle(R9_T)    # Röle 9  toggle -> GET /z0
# get.relay_toggle(R10_T)   # Röle 10 toggle -> GET /z1
# get.relay_toggle(R11_T)   # Röle 11 toggle -> GET /z2
# get.relay_toggle(R12_T)   # Röle 12 toggle -> GET /z3
# get.relay_toggle(R13_T)   # Röle 13 toggle -> GET /z4
# get.relay_toggle(R14_T)   # Röle 14 toggle -> GET /z5
# get.relay_toggle(R15_T)   # Röle 15 toggle -> GET /z6
# get.relay_toggle(R16_T)   # Röle 16 toggle -> GET /z7

# ── D) Durum Okuma ────────────────────────────────────────
# Tek seferlik okuma:
# status = get.read_status()
# print(status)
# Örnek çıktı:
# {"PORTB": "00000101", "PORTD": "00000000", "PORTA": "11111111",
#  "PORTE": "00000000", "TEMP1": 22.3, "TEMP2": 22.2}
# PORT değerleri 8 haneli binary string: bit0=Röle1, bit1=Röle2 ...

# Her 400ms'de sürekli okuma (Ctrl+C ile durdurulur):
# get.read_status_loop()

# ── E) Ağ Konfigürasyonu Okuma ────────────────────────────
# Cihazın IP, Gateway, Subnet Mask bilgilerini gösterir:
# print(get.config())
# Örnek çıktı:
# NETWORK IP:= 169.254.1.2 PORTNO: 3000 GATEWAY:= 169.254.1.1 SUBNET MASK:= 255.255.255.0


# ╔══════════════════════════════════════════════════════════╗
#  2. BÖLÜM: TCP MODBUS RTU  (TcpRelay)
# ╚══════════════════════════════════════════════════════════╝
#
#  Nesneyi if __name__ == "__main__": bloğu içinde oluşturun.
#  Böylece cihaza ulaşılamasa bile import sırasında hata almazsınız.
#  Bağlantı kesilirse arka planda (non-blocking) yeniden bağlanır.
#  Bağlantı sonunda tcp.disconnect() çağrın.
#
#  tcp = TcpRelay(IP, PORT)

# ── A) Röle Açma ─────────────────────────────────────────
# tcp.relay_on(R1_1)    # Röle 1  aç   (Relay 0 on)
# tcp.relay_on(R2_1)    # Röle 2  aç   (Relay 1 on)
# tcp.relay_on(R3_1)    # Röle 3  aç
# tcp.relay_on(R4_1)    # Röle 4  aç
# tcp.relay_on(R5_1)    # Röle 5  aç
# tcp.relay_on(R6_1)    # Röle 6  aç
# tcp.relay_on(R7_1)    # Röle 7  aç
# tcp.relay_on(R8_1)    # Röle 8  aç
# tcp.relay_on(R9_1)    # Röle 9  aç
# tcp.relay_on(R10_1)   # Röle 10 aç
# tcp.relay_on(R11_1)   # Röle 11 aç
# tcp.relay_on(R12_1)   # Röle 12 aç
# tcp.relay_on(R13_1)   # Röle 13 aç
# tcp.relay_on(R14_1)   # Röle 14 aç
# tcp.relay_on(R15_1)   # Röle 15 aç
# tcp.relay_on(R16_1)   # Röle 16 aç
# tcp.relay_on(ALL)     # Tüm röleler aç

# ── B) Röle Kapatma ───────────────────────────────────────
# tcp.relay_off(R1_0)   # Röle 1  kapat
# tcp.relay_off(R2_0)   # Röle 2  kapat
# tcp.relay_off(R3_0)   # Röle 3  kapat
# tcp.relay_off(R4_0)   # Röle 4  kapat
# tcp.relay_off(R5_0)   # Röle 5  kapat
# tcp.relay_off(R6_0)   # Röle 6  kapat
# tcp.relay_off(R7_0)   # Röle 7  kapat
# tcp.relay_off(R8_0)   # Röle 8  kapat
# tcp.relay_off(R9_0)   # Röle 9  kapat
# tcp.relay_off(R10_0)  # Röle 10 kapat
# tcp.relay_off(R11_0)  # Röle 11 kapat
# tcp.relay_off(R12_0)  # Röle 12 kapat
# tcp.relay_off(R13_0)  # Röle 13 kapat
# tcp.relay_off(R14_0)  # Röle 14 kapat
# tcp.relay_off(R15_0)  # Röle 15 kapat
# tcp.relay_off(R16_0)  # Röle 16 kapat
# tcp.relay_off(OFF)    # Tüm röleler kapat

# ── C) Linkage / Normal Mod ───────────────────────────────
# tcp.relay_la(linkage_1_8)   # 1-8 Röle LINKAGE moda geçir  (IO Board)
# tcp.relay_la(normal_1_8)    # 1-8 Röle NORMAL moda geçir
# tcp.relay_la(linkage_9_16)  # 9-16 Röle LINKAGE moda geçir (IO Board)
# tcp.relay_la(normal_9_16)   # 9-16 Röle NORMAL moda geçir

# ── D) Linkage / Normal Mod Sorgulama ─────────────────────
# tcp.relay_linkage_or_normal(la_no_1_8)   # 1-8 Röle: Linkage mı Normal mi?
# tcp.relay_linkage_or_normal(la_no_9_16)  # 9-16 Röle: Linkage mı Normal mi?

# ── E) Flash ON (index 0-47) ──────────────────────────────
# Her röle için 6 farklı süre seçeneği mevcuttur (800ms-5000ms).
# Gruplama: Her grup 6 index. No.0=index 0-5, No.1=index 6-11 ...
#
# tcp.flash_on(0)   # No.0 Relay1  800ms
# tcp.flash_on(1)   # No.0 Relay1 1000ms
# tcp.flash_on(2)   # No.0 Relay1 2000ms
# tcp.flash_on(3)   # No.0 Relay1 3000ms
# tcp.flash_on(4)   # No.0 Relay1 4000ms
# tcp.flash_on(5)   # No.0 Relay1 5000ms
# tcp.flash_on(6)   # No.1 Relay2  800ms
# tcp.flash_on(7)   # No.1 Relay2 1000ms
# tcp.flash_on(8)   # No.1 Relay2 2000ms
# tcp.flash_on(9)   # No.1 Relay2 3000ms
# tcp.flash_on(10)  # No.1 Relay2 4000ms
# tcp.flash_on(11)  # No.1 Relay2 5000ms
# tcp.flash_on(12)  # No.2 Relay3  800ms
# tcp.flash_on(13)  # No.2 Relay3 1000ms
# tcp.flash_on(14)  # No.2 Relay3 2000ms
# tcp.flash_on(15)  # No.2 Relay3 3000ms
# tcp.flash_on(16)  # No.2 Relay3 4000ms
# tcp.flash_on(17)  # No.2 Relay3 5000ms
# tcp.flash_on(18)  # No.3 Relay4  800ms
# tcp.flash_on(19)  # No.3 Relay4 1000ms
# tcp.flash_on(20)  # No.3 Relay4 2000ms
# tcp.flash_on(21)  # No.3 Relay4 3000ms
# tcp.flash_on(22)  # No.3 Relay4 4000ms
# tcp.flash_on(23)  # No.3 Relay4 5000ms
# tcp.flash_on(24)  # No.4 Relay5  800ms
# tcp.flash_on(25)  # No.4 Relay5 1000ms
# tcp.flash_on(26)  # No.4 Relay5 2000ms
# tcp.flash_on(27)  # No.4 Relay5 3000ms
# tcp.flash_on(28)  # No.4 Relay5 4000ms
# tcp.flash_on(29)  # No.4 Relay5 5000ms
# tcp.flash_on(30)  # No.5 Relay6  800ms
# tcp.flash_on(31)  # No.5 Relay6 1000ms
# tcp.flash_on(32)  # No.5 Relay6 2000ms
# tcp.flash_on(33)  # No.5 Relay6 3000ms
# tcp.flash_on(34)  # No.5 Relay6 4000ms
# tcp.flash_on(35)  # No.5 Relay6 5000ms
# tcp.flash_on(36)  # No.6 Relay7  800ms
# tcp.flash_on(37)  # No.6 Relay7 1000ms
# tcp.flash_on(38)  # No.6 Relay7 2000ms
# tcp.flash_on(39)  # No.6 Relay7 3000ms
# tcp.flash_on(40)  # No.6 Relay7 4000ms
# tcp.flash_on(41)  # No.6 Relay7 5000ms
# tcp.flash_on(42)  # No.7 Relay8  800ms
# tcp.flash_on(43)  # No.7 Relay8 1000ms
# tcp.flash_on(44)  # No.7 Relay8 2000ms
# tcp.flash_on(45)  # No.7 Relay8 3000ms
# tcp.flash_on(46)  # No.7 Relay8 4000ms
# tcp.flash_on(47)  # No.7 Relay8 5000ms

# ── F) Flash OFF (index 0-47) ─────────────────────────────
# tcp.flash_off(0)   # No.0 Relay1  800ms
# tcp.flash_off(1)   # No.0 Relay1 1000ms
# tcp.flash_off(2)   # No.0 Relay1 2000ms
# tcp.flash_off(3)   # No.0 Relay1 3000ms
# tcp.flash_off(4)   # No.0 Relay1 4000ms
# tcp.flash_off(5)   # No.0 Relay1 5000ms
# tcp.flash_off(6)   # No.1 Relay2  800ms
# tcp.flash_off(7)   # No.1 Relay2 1000ms
# tcp.flash_off(8)   # No.1 Relay2 2000ms
# tcp.flash_off(9)   # No.1 Relay2 3000ms
# tcp.flash_off(10)  # No.1 Relay2 4000ms
# tcp.flash_off(11)  # No.1 Relay2 5000ms
# tcp.flash_off(12)  # No.2 Relay3  800ms
# tcp.flash_off(13)  # No.2 Relay3 1000ms
# tcp.flash_off(14)  # No.2 Relay3 2000ms
# tcp.flash_off(15)  # No.2 Relay3 3000ms
# tcp.flash_off(16)  # No.2 Relay3 4000ms
# tcp.flash_off(17)  # No.2 Relay3 5000ms
# tcp.flash_off(18)  # No.3 Relay4  800ms
# tcp.flash_off(19)  # No.3 Relay4 1000ms
# tcp.flash_off(20)  # No.3 Relay4 2000ms
# tcp.flash_off(21)  # No.3 Relay4 3000ms
# tcp.flash_off(22)  # No.3 Relay4 4000ms
# tcp.flash_off(23)  # No.3 Relay4 5000ms
# tcp.flash_off(24)  # No.4 Relay5  800ms
# tcp.flash_off(25)  # No.4 Relay5 1000ms
# tcp.flash_off(26)  # No.4 Relay5 2000ms
# tcp.flash_off(27)  # No.4 Relay5 3000ms
# tcp.flash_off(28)  # No.4 Relay5 4000ms
# tcp.flash_off(29)  # No.4 Relay5 5000ms
# tcp.flash_off(30)  # No.5 Relay6  800ms
# tcp.flash_off(31)  # No.5 Relay6 1000ms
# tcp.flash_off(32)  # No.5 Relay6 2000ms
# tcp.flash_off(33)  # No.5 Relay6 3000ms
# tcp.flash_off(34)  # No.5 Relay6 4000ms
# tcp.flash_off(35)  # No.5 Relay6 5000ms
# tcp.flash_off(36)  # No.6 Relay7  800ms
# tcp.flash_off(37)  # No.6 Relay7 1000ms
# tcp.flash_off(38)  # No.6 Relay7 2000ms
# tcp.flash_off(39)  # No.6 Relay7 3000ms
# tcp.flash_off(40)  # No.6 Relay7 4000ms
# tcp.flash_off(41)  # No.6 Relay7 5000ms
# tcp.flash_off(42)  # No.7 Relay8  800ms
# tcp.flash_off(43)  # No.7 Relay8 1000ms
# tcp.flash_off(44)  # No.7 Relay8 2000ms
# tcp.flash_off(45)  # No.7 Relay8 3000ms
# tcp.flash_off(46)  # No.7 Relay8 4000ms
# tcp.flash_off(47)  # No.7 Relay8 5000ms

# ── G) Röle Durum Okuma ───────────────────────────────────
# tcp.read_relay_status_8bit()  # 1-8 Röle durumu hex olarak
# tcp.read_relay_status_9_16()  # 9-16 Röle durumu hex olarak
# tcp.RS_18_8BIT()              # 1-8 Röle durumu 1/0 olarak
# tcp.RS_916_8BIT()             # 9-16 Röle durumu 1/0 olarak

# ── H) Input Durum Okuma ──────────────────────────────────
# tcp.read_input_status()  # 8 input durumu hex olarak
# tcp.read_input_binary()  # 8 input durumu 1/0 olarak

# ── Bağlantı Kapatma ──────────────────────────────────────
# tcp.disconnect()

# ── CRC16 Flash Parametre Geliştirme ──────────────────────
# Farklı zamanlama süreleri için kendi hex parametrenizi oluşturabilirsiniz.
# Adımlar:
#   1) İlk 6 byte'ı belirleyin. Örnek: 01 05 02 00 00 07 (röle1, 700ms)
#   2) Bu 6 byte için CRC16 (Modbus, little endian) hesaplayın:
#      https://github.com/sedaelektronik/modbus-crc16-parameter-generator
#   3) CRC çıktısını (2 byte, LE) sonuna ekleyin: 01 05 02 00 00 07 8D B0
#   4) 5. byte (index 4) süreyi hex olarak tutar: 07=700ms, 0A=1000ms
#      Maksimum süre: FF FF = ~4.25 dakika
# Bu parametreyi TcpRelay._FLASH_MAP sözlüğüne ekleyerek kullanabilirsiniz.


# ╔══════════════════════════════════════════════════════════╗
#  3. BÖLÜM: UDP GET  (UdpRelay)
# ╚══════════════════════════════════════════════════════════╝
#
#  Nesneyi if __name__ == "__main__": bloğu içinde oluşturun.
#  Röle kontrolü UDP üzerinden yapılır.
#  Status okuma ve config HTTP GET üzerinden yapılır.
#  UDP ürünler aynı zamanda GET özelliğine sahiptir.
#
#  udp = UdpRelay(IP, PORT)

# ── A) Röle Açma ─────────────────────────────────────────
# udp.relay_on(R1_1)    # Röle 1  aç  -> UDP "1"
# udp.relay_on(R2_1)    # Röle 2  aç  -> UDP "2"
# udp.relay_on(R3_1)    # Röle 3  aç  -> UDP "3"
# udp.relay_on(R4_1)    # Röle 4  aç  -> UDP "4"
# udp.relay_on(R5_1)    # Röle 5  aç  -> UDP "5"
# udp.relay_on(R6_1)    # Röle 6  aç  -> UDP "6"
# udp.relay_on(R7_1)    # Röle 7  aç  -> UDP "7"
# udp.relay_on(R8_1)    # Röle 8  aç  -> UDP "8"
# udp.relay_on(R9_1)    # Röle 9  aç  -> UDP "9"
# udp.relay_on(R10_1)   # Röle 10 aç  -> UDP "0"
# udp.relay_on(R11_1)   # Röle 11 aç  -> UDP "a"
# udp.relay_on(R12_1)   # Röle 12 aç  -> UDP "b"
# udp.relay_on(R13_1)   # Röle 13 aç  -> UDP "c"
# udp.relay_on(R14_1)   # Röle 14 aç  -> UDP "d"
# udp.relay_on(R15_1)   # Röle 15 aç  -> UDP "e"
# udp.relay_on(R16_1)   # Röle 16 aç  -> UDP "L"
# udp.relay_on(ALL)     # Tüm röleler aç -> UDP "ALL"

# ── B) Röle Kapatma ───────────────────────────────────────
# udp.relay_off(R1_0)   # Röle 1  kapat -> UDP "i"
# udp.relay_off(R2_0)   # Röle 2  kapat -> UDP "g"
# udp.relay_off(R3_0)   # Röle 3  kapat -> UDP "h"
# udp.relay_off(R4_0)   # Röle 4  kapat -> UDP "j"
# udp.relay_off(R5_0)   # Röle 5  kapat -> UDP "k"
# udp.relay_off(R6_0)   # Röle 6  kapat -> UDP "l"
# udp.relay_off(R7_0)   # Röle 7  kapat -> UDP "m"
# udp.relay_off(R8_0)   # Röle 8  kapat -> UDP "n"
# udp.relay_off(R9_0)   # Röle 9  kapat -> UDP "o"
# udp.relay_off(R10_0)  # Röle 10 kapat -> UDP "p"
# udp.relay_off(R11_0)  # Röle 11 kapat -> UDP "q"
# udp.relay_off(R12_0)  # Röle 12 kapat -> UDP "t"
# udp.relay_off(R13_0)  # Röle 13 kapat -> UDP "u"
# udp.relay_off(R14_0)  # Röle 14 kapat -> UDP "v"
# udp.relay_off(R15_0)  # Röle 15 kapat -> UDP "w"
# udp.relay_off(R16_0)  # Röle 16 kapat -> UDP "M"
# udp.relay_off(OFF)    # Tüm röleler kapat -> UDP "OFF"

# ── C) Durum Okuma (HTTP GET üzerinden) ───────────────────
# Tek seferlik okuma:
# status = udp.read_status()
# print(status)
# Örnek çıktı:
# {"PORTB": "00000101", "PORTD": "00000000", "PORTA": "11111111",
#  "PORTE": "00000000", "TEMP1": 22.3, "TEMP2": 22.2}

# Her 400ms'de sürekli okuma (Ctrl+C ile durdurulur):
# udp.read_status_loop()

# ── D) Ağ Konfigürasyonu Okuma (HTTP GET üzerinden) ───────
# print(udp.config())

# ── Bağlantı Kapatma ──────────────────────────────────────
# udp.disconnect()


# ============================================================
#  ÖRNEK KULLANIM  –  aktif kod bloğu
# ============================================================

if __name__ == "__main__":
    import time

    print("=" * 50)
    print("  Seda Elektronik sedaio API – Test")
    print(f"  Hedef: {IP}:{PORT}")
    print("=" * 50)

    # Nesneler burada oluşturuluyor – cihaza ulaşılamazsa
    # sadece bu blok hata verir, import sırasında değil.
    get = HttpRelay(IP, PORT)
    tcp = TcpRelay(IP, PORT)
    udp = UdpRelay(IP, PORT)

    # --- HTTP GET örneği ---
    print("\n[GET] Röle 1 aç...")
    get.relay_on(R1_1)
    time.sleep(1)

    print("[GET] Röle 1 kapat...")
    get.relay_off(R1_0)
    time.sleep(0.5)

    print("[GET] Durum oku...")
    s = get.read_status()
    print(f"  Durum: {s}")

    # --- TCP örneği ---
    print("\n[TCP] Röle 1 aç...")
    tcp.relay_on(R1_1)
    time.sleep(1)

    print("[TCP] Röle 1 kapat...")
    tcp.relay_off(R1_0)
    time.sleep(0.5)

    print("[TCP] Röle 1 durum oku...")
    r = tcp.read_relay_status_8bit()
    if r:
        print(f"  Cevap: {r.hex(' ').upper()}")

    tcp.disconnect()

    # --- UDP örneği ---
    print("\n[UDP] Röle 1 aç...")
    udp.relay_on(R1_1)
    time.sleep(1)

    print("[UDP] Röle 1 kapat...")
    udp.relay_off(R1_0)
    time.sleep(0.5)

    print("[UDP] Durum oku (HTTP)...")
    s = udp.read_status()
    print(f"  Durum: {s}")

    udp.disconnect()

    print("\n  Tamamlandı.")
