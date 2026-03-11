
# ============================================================
#  sedaio.py  –  Seda Elektronik Ethernet Röle Kartı API
#  Protokoller : HTTP GET | TCP Modbus RTU | UDP GET
#  Sınıflar    : HttpRelay | TcpRelay | UdpRelay
#  Versiyon    : 1.0
# ============================================================

import re
import time
import socket
import logging
import threading
import binascii

try:
    import requests
except ImportError:
    requests = None  # HttpRelay / UdpRelay.read_status için gerekli

logging.basicConfig(level=logging.INFO, format="[sedaio] %(levelname)s: %(message)s")
logger = logging.getLogger("sedaio")

# ============================================================
#  GLOBAL SABİTLER  –  GET / TCP / UDP ortak değişkenler
# ============================================================

# --- Röle AÇMA değişkenleri (Röle 1-16) ---
R1_1  = "1"
R2_1  = "2"
R3_1  = "3"
R4_1  = "4"
R5_1  = "5"
R6_1  = "6"
R7_1  = "7"
R8_1  = "8"
R9_1  = "9"
R10_1 = "0"
R11_1 = "a"
R12_1 = "b"
R13_1 = "c"
R14_1 = "d"
R15_1 = "e"
R16_1 = "L"

# --- Röle KAPATMA değişkenleri (Röle 1-16) ---
R1_0  = "i"
R2_0  = "g"
R3_0  = "h"
R4_0  = "j"
R5_0  = "k"
R6_0  = "l"
R7_0  = "m"
R8_0  = "n"
R9_0  = "o"
R10_0 = "p"
R11_0 = "q"
R12_0 = "t"
R13_0 = "u"
R14_0 = "v"
R15_0 = "w"
R16_0 = "M"

# --- Röle TOGGLE değişkenleri (GET Röle 1-16) ---
R1_T  = "y0"
R2_T  = "y1"
R3_T  = "y2"
R4_T  = "y3"
R5_T  = "y4"
R6_T  = "y5"
R7_T  = "y6"
R8_T  = "y7"
R9_T  = "z0"
R10_T = "z1"
R11_T = "z2"
R12_T = "z3"
R13_T = "z4"
R14_T = "z5"
R15_T = "z6"
R16_T = "z7"

# --- Tüm Röleler ---
ALL = "ALL"
OFF = "OFF"

# --- Network Konfigürasyon ---
NetCon = "IP?"

# --- TCP Linkage / Normal mod değişkenleri ---
linkage_1_8  = "linkage_1_8"
normal_1_8   = "normal_1_8"
linkage_9_16 = "linkage_9_16"
normal_9_16  = "normal_9_16"

# --- TCP Linkage sorgu değişkenleri ---
la_no_1_8  = "la_no_1_8"
la_no_9_16 = "la_no_9_16"


# ============================================================
#  YARDIMCI FONKSİYON
# ============================================================

def _parse_status(raw: str) -> dict:
    """
    Kartın /s endpoint'inden dönen ham metni parse eder.
    Döndürür: {"PORTB": str, "PORTD": str, "PORTA": str, "PORTE": str,
               "TEMP1": float, "TEMP2": float}
    PORT değerleri 8 haneli binary string'e dönüştürülür.
    Örn: 5 -> "00000101", 255 -> "11111111"
    """
    result = {}
    for port in ["PORTB", "PORTD", "PORTA", "PORTE"]:
        m = re.search(rf"(?:var\s+)?{port}\s*=\s*(\d+)", raw)
        if m:
            val = int(m.group(1))
            result[port] = bin(val)[2:].zfill(8)
        else:
            result[port] = "00000000"
    for temp in ["TEMP1", "TEMP2"]:
        m = re.search(rf"(?:var\s+)?{temp}\s*=\s*([\d]+\.[\d]+)", raw)
        if m:
            result[temp] = float(m.group(1))
        else:
            result[temp] = 0.0
    return result


# ============================================================
#  1) HttpRelay  –  HTTP GET Protokolü
# ============================================================

class HttpRelay:
    """
    Seda Elektronik HTTP GET Röle Kartı API sınıfı.

    Kullanım:
        get = HttpRelay("169.254.1.2", 3000)
        get.relay_on(R1_1)
        get.relay_off(R1_0)
        get.relay_toggle(R1_T)
        get.relay_on(ALL)
        get.relay_off(OFF)
        status = get.read_status()
        get.read_status_loop()
        get.config()
    """

    def __init__(self, ip: str, port: int, timeout: int = 3):
        if requests is None:
            raise ImportError("HttpRelay için 'requests' kütüphanesi gereklidir: pip install requests")
        self.ip      = ip
        self.port    = port
        self.timeout = timeout
        self._base   = f"http://{ip}:{port}"
        self._loop_running = False

    def _get(self, param: str) -> bool:
        """Ham GET isteği gönderir."""
        url = f"{self._base}/{param}"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            logger.info(f"GET {url} -> {r.status_code}")
            return True
        except Exception as e:
            logger.error(f"GET hatası ({url}): {e}")
            return False

    def relay_on(self, param: str) -> bool:
        """Röle açar. Parametre: R1_1 ... R16_1 veya ALL"""
        return self._get(param)

    def relay_off(self, param: str) -> bool:
        """Röle kapatır. Parametre: R1_0 ... R16_0 veya OFF"""
        return self._get(param)

    def relay_toggle(self, param: str) -> bool:
        """Röle toggle yapar. Parametre: R1_T ... R16_T"""
        return self._get(param)

    def read_status(self) -> dict:
        """
        /s endpoint'inden tek seferlik okuma yapar.
        Döndürür: {"PORTB": str, "PORTD": str, "PORTA": str, "PORTE": str,
                   "TEMP1": float, "TEMP2": float}
        PORT değerleri 8 haneli binary string (örn: "00000101")
        """
        url = f"{self._base}/s"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            return _parse_status(r.text)
        except Exception as e:
            logger.error(f"read_status hatası: {e}")
            return False

    def read_status_loop(self, interval: float = 0.4):
        """
        /s endpoint'inden her 400ms'de bir okuma yapar.
        Çıkmak için Ctrl+C kullanın.
        Döndürür: {"PORTB": str, "PORTD": str, "PORTA": str, "PORTE": str,
                   "TEMP1": float, "TEMP2": float}
        PORT değerleri 8 haneli binary string (örn: "00000101")
        """
        self._loop_running = True
        logger.info("read_status_loop başladı. Durdurmak için Ctrl+C.")
        try:
            while self._loop_running:
                data = self.read_status()
                if data:
                    print(data)
                time.sleep(interval)
        except KeyboardInterrupt:
            self._loop_running = False
            logger.info("read_status_loop durduruldu.")

    def config(self) -> str:
        """
        /IP? endpoint'inden ağ konfigürasyonunu okur.
        Döndürür: IP, PORTNO, GATEWAY, SUBNET MASK bilgileri (ham metin)
        """
        url = f"{self._base}/{NetCon}"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            logger.info(f"config -> {r.text.strip()}")
            return r.text.strip()
        except Exception as e:
            logger.error(f"config hatası: {e}")
            return False


# ============================================================
#  2) TcpRelay  –  TCP Modbus RTU Protokolü
# ============================================================

class TcpRelay:
    """
    Seda Elektronik TCP Modbus RTU Röle Kartı API sınıfı.
    Non-blocking otomatik yeniden bağlanma threading ile sağlanır.

    Kullanım:
        tcp = TcpRelay("169.254.1.2", 3000)
        tcp.relay_on(R1_1)
        tcp.relay_off(R1_0)
        tcp.relay_toggle(R1_T)
        tcp.relay_on(ALL)
        tcp.relay_off(OFF)
        tcp.relay_la(linkage_1_8)
        tcp.relay_la(normal_1_8)
        tcp.relay_linkage_or_normal(la_no_1_8)
        tcp.flash_on(0)   # 0-47
        tcp.flash_off(0)  # 0-47
        tcp.read_relay_status_8bit()
        tcp.read_relay_status_9_16()
        tcp.RS_18_8BIT()
        tcp.RS_916_8BIT()
        tcp.read_input_status()
        tcp.read_input_binary()
    """

    # ----------------------------------------------------------
    #  Dahili Hex Eşleştirme Sözlüğü
    # ----------------------------------------------------------
    _RELAY_MAP = {
        # -------------------------------------------------------
        # Anahtarlar global sabitlerin DEĞERLERİyle eşleşir.
        # Örn: R2_1 = "2"  →  anahtar "2"
        #      R2_0 = "g"  →  anahtar "g"
        # -------------------------------------------------------

        # 1-16 Röle ON  (Relay 0 = R1 ... Relay 15 = R16)
        "1": b'\x01\x05\x00\x00\xFF\x00\x8C\x3A',  # R1_1
        "2": b'\x01\x05\x00\x01\xFF\x00\xDD\xFA',  # R2_1
        "3": b'\x01\x05\x00\x02\xFF\x00\x2D\xFA',  # R3_1
        "4": b'\x01\x05\x00\x03\xFF\x00\x7C\x3A',  # R4_1
        "5": b'\x01\x05\x00\x04\xFF\x00\xCD\xFB',  # R5_1
        "6": b'\x01\x05\x00\x05\xFF\x00\x9C\x3B',  # R6_1
        "7": b'\x01\x05\x00\x06\xFF\x00\x6C\x3B',  # R7_1
        "8": b'\x01\x05\x00\x07\xFF\x00\x3D\xFB',  # R8_1
        "9": b'\x01\x05\x00\x08\xFF\x00\x0D\xF8',  # R9_1
        "0": b'\x01\x05\x00\x09\xFF\x00\x5C\x38',  # R10_1
        "a": b'\x01\x05\x00\x0A\xFF\x00\xAC\x38',  # R11_1
        "b": b'\x01\x05\x00\x0B\xFF\x00\xFD\xF8',  # R12_1
        "c": b'\x01\x05\x00\x0C\xFF\x00\x4C\x39',  # R13_1
        "d": b'\x01\x05\x00\x0D\xFF\x00\x1D\xF9',  # R14_1
        "e": b'\x01\x05\x00\x0E\xFF\x00\xED\xF9',  # R15_1
        "L": b'\x01\x05\x00\x0F\xFF\x00\xBC\x39',  # R16_1

        # 1-16 Röle OFF
        "i": b'\x01\x05\x00\x00\x00\x00\xCD\xCA',  # R1_0
        "g": b'\x01\x05\x00\x01\x00\x00\x9C\x0A',  # R2_0
        "h": b'\x01\x05\x00\x02\x00\x00\x6C\x0A',  # R3_0
        "j": b'\x01\x05\x00\x03\x00\x00\x3D\xCA',  # R4_0
        "k": b'\x01\x05\x00\x04\x00\x00\x8C\x0B',  # R5_0
        "l": b'\x01\x05\x00\x05\x00\x00\xDD\xCB',  # R6_0
        "m": b'\x01\x05\x00\x06\x00\x00\x2D\xCB',  # R7_0
        "n": b'\x01\x05\x00\x07\x00\x00\x7C\x0B',  # R8_0
        "o": b'\x01\x05\x00\x08\x00\x00\x4C\x08',  # R9_0
        "p": b'\x01\x05\x00\x09\x00\x00\x1D\xC8',  # R10_0
        "q": b'\x01\x05\x00\x0A\x00\x00\xED\xC8',  # R11_0
        "t": b'\x01\x05\x00\x0B\x00\x00\xBC\x08',  # R12_0
        "u": b'\x01\x05\x00\x0C\x00\x00\x0D\xC9',  # R13_0
        "v": b'\x01\x05\x00\x0D\x00\x00\x5C\x09',  # R14_0
        "w": b'\x01\x05\x00\x0E\x00\x00\xAC\x09',  # R15_0
        "M": b'\x01\x05\x00\x0F\x00\x00\xFD\xC9',  # R16_0

        # 1-16 Röle TOGGLE
        "y0": b'\x01\x05\x00\x00\x55\x00\xF2\x9A',  # R1_T
        "y1": b'\x01\x05\x00\x01\x55\x00\xA3\x5A',  # R2_T
        "y2": b'\x01\x05\x00\x02\x55\x00\x53\x5A',  # R3_T
        "y3": b'\x01\x05\x00\x03\x55\x00\x02\x9A',  # R4_T
        "y4": b'\x01\x05\x00\x04\x55\x00\xB3\x5B',  # R5_T
        "y5": b'\x01\x05\x00\x05\x55\x00\xE2\x9B',  # R6_T
        "y6": b'\x01\x05\x00\x06\x55\x00\x12\x9B',  # R7_T
        "y7": b'\x01\x05\x00\x07\x55\x00\x43\x5B',  # R8_T
        "z0": b'\x01\x05\x00\x08\x55\x00\x73\x58',  # R9_T
        "z1": b'\x01\x05\x00\x09\x55\x00\x22\x98',  # R10_T
        "z2": b'\x01\x05\x00\x0A\x55\x00\xD2\x98',  # R11_T
        "z3": b'\x01\x05\x00\x0B\x55\x00\x83\x58',  # R12_T
        "z4": b'\x01\x05\x00\x0C\x55\x00\x32\x99',  # R13_T
        "z5": b'\x01\x05\x00\x0D\x55\x00\x63\x59',  # R14_T
        "z6": b'\x01\x05\x00\x0E\x55\x00\x93\x59',  # R15_T
        "z7": b'\x01\x05\x00\x0F\x55\x00\xC2\x99',  # R16_T

        # Tümü ON / OFF
        "ALL": b'\x01\x05\x00\xFF\xFF\x00\xBC\x0A',
        "OFF": b'\x01\x05\x00\xFF\x00\x00\xFD\xFA',

        # Linkage / Normal mod
        "normal_1_8":   b'\x01\x10\x10\x00\x00\x08\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0B\x5C',
        "linkage_1_8":  b'\x01\x10\x10\x00\x00\x08\x10\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x7C\xB1',
        "normal_9_16":  b'\x01\x10\x10\x00\x00\x09\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x5A\xA0',
        "linkage_9_16": b'\x01\x10\x10\x00\x00\x09\x10\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x2D\x4D',

        # Linkage sorgu
        "la_no_1_8":  b'\x01\x03\x10\x00\x00\x08\x40\xCC',
        "la_no_9_16": b'\x01\x03\x10\x00\x00\x09\x81\x0C',

        # Röle durum sorgular
        "read_relay_status_8bit":  b'\x01\x01\x00\x00\x00\x08\x3D\xCC',
        "read_relay_status_9_16":  b'\x01\x01\x00\x00\x00\x09\xFC\x0C',
        "RS_18_8BIT":              b'\x01\x03\x10\x00\xFF\x08\x01\x3C',
        "RS_916_8BIT":             b'\x01\x03\x10\x00\xFF\x09\xC0\xFC',

        # Input durum sorgular
        "read_input_status": b'\x01\x02\x00\x00\x00\x08\x79\xCC',
        "read_input_binary": b'\x01\x03\x10\x00\x01\x08\x41\x5C',
    }

    # ----------------------------------------------------------
    #  Flash ON – 48 parametre (index 0-47)
    #  flash_on(0)  = No.0 relay1 800ms
    #  flash_on(1)  = No.0 relay1 1000ms
    #  flash_on(2)  = No.0 relay1 2000ms
    #  flash_on(3)  = No.0 relay1 3000ms
    #  flash_on(4)  = No.0 relay1 4000ms
    #  flash_on(5)  = No.0 relay1 5000ms
    #  flash_on(6)  = No.1 relay2 800ms
    #  ...
    #  flash_on(47) = No.7 relay8 5000ms
    # ----------------------------------------------------------
    _FLASH_MAP = {
        "FON_0":  b'\x01\x05\x02\x00\x00\x08\xCD\xB4',
        "FON_1":  b'\x01\x05\x02\x00\x00\x0A\x4C\x75',
        "FON_2":  b'\x01\x05\x02\x00\x00\x14\xCC\x7D',
        "FON_3":  b'\x01\x05\x02\x00\x00\x1E\x4C\x7A',
        "FON_4":  b'\x01\x05\x02\x00\x00\x28\xCC\x6C',
        "FON_5":  b'\x01\x05\x02\x00\x00\x32\x4D\xA7',
        "FON_6":  b'\x01\x05\x02\x01\x00\x08\x9C\x74',
        "FON_7":  b'\x01\x05\x02\x01\x00\x0A\x1D\xB5',
        "FON_8":  b'\x01\x05\x02\x01\x00\x14\x9D\xBD',
        "FON_9":  b'\x01\x05\x02\x01\x00\x1E\x1D\xBA',
        "FON_10": b'\x01\x05\x02\x01\x00\x28\x9D\xAC',
        "FON_11": b'\x01\x05\x02\x01\x00\x32\x1C\x67',
        "FON_12": b'\x01\x05\x02\x02\x00\x08\x6C\x74',
        "FON_13": b'\x01\x05\x02\x02\x00\x0A\xED\xB5',
        "FON_14": b'\x01\x05\x02\x02\x00\x14\x6D\xBD',
        "FON_15": b'\x01\x05\x02\x02\x00\x1E\xED\xBA',
        "FON_16": b'\x01\x05\x02\x02\x00\x28\x6D\xAC',
        "FON_17": b'\x01\x05\x02\x02\x00\x32\xEC\x67',
        "FON_18": b'\x01\x05\x02\x03\x00\x08\x3D\xB4',
        "FON_19": b'\x01\x05\x02\x03\x00\x0A\xBC\x75',
        "FON_20": b'\x01\x05\x02\x03\x00\x14\x3C\x7D',
        "FON_21": b'\x01\x05\x02\x03\x00\x1E\xBC\x7A',
        "FON_22": b'\x01\x05\x02\x03\x00\x28\x3C\x6C',
        "FON_23": b'\x01\x05\x02\x03\x00\x32\xBD\xA7',
        "FON_24": b'\x01\x05\x02\x04\x00\x08\x8C\x75',
        "FON_25": b'\x01\x05\x02\x04\x00\x0A\x0D\xB4',
        "FON_26": b'\x01\x05\x02\x04\x00\x14\x8D\xBC',
        "FON_27": b'\x01\x05\x02\x04\x00\x1E\x0D\xBB',
        "FON_28": b'\x01\x05\x02\x04\x00\x28\x8D\xAD',
        "FON_29": b'\x01\x05\x02\x04\x00\x32\x0C\x66',
        "FON_30": b'\x01\x05\x02\x05\x00\x08\xDD\xB5',
        "FON_31": b'\x01\x05\x02\x05\x00\x0A\x5C\x74',
        "FON_32": b'\x01\x05\x02\x05\x00\x14\xDC\x7C',
        "FON_33": b'\x01\x05\x02\x05\x00\x1E\x5C\x7B',
        "FON_34": b'\x01\x05\x02\x05\x00\x28\xDC\x6D',
        "FON_35": b'\x01\x05\x02\x05\x00\x32\x5D\xA6',
        "FON_36": b'\x01\x05\x02\x06\x00\x08\x2D\xB5',
        "FON_37": b'\x01\x05\x02\x06\x00\x0A\xAC\x74',
        "FON_38": b'\x01\x05\x02\x06\x00\x14\x2C\x7C',
        "FON_39": b'\x01\x05\x02\x06\x00\x1E\xAC\x7B',
        "FON_40": b'\x01\x05\x02\x06\x00\x28\x2C\x6D',
        "FON_41": b'\x01\x05\x02\x06\x00\x32\xAD\xA6',
        "FON_42": b'\x01\x05\x02\x07\x00\x08\x7C\x75',
        "FON_43": b'\x01\x05\x02\x07\x00\x0A\xFD\xB4',
        "FON_44": b'\x01\x05\x02\x07\x00\x14\x7D\xBC',
        "FON_45": b'\x01\x05\x02\x07\x00\x1E\xFD\xBB',
        "FON_46": b'\x01\x05\x02\x07\x00\x28\x7D\xAD',
        "FON_47": b'\x01\x05\x02\x07\x00\x32\xFC\x66',

        # Flash OFF – 48 parametre (index 0-47)
        # flash_off(0)  = No.0 relay1 800ms
        # flash_off(47) = No.7 relay8 5000ms
        "FOFF_0":  b'\x01\x05\x04\x00\x00\x08\xCD\x3C',
        "FOFF_1":  b'\x01\x05\x04\x00\x00\x0A\x4C\xFD',
        "FOFF_2":  b'\x01\x05\x04\x00\x00\x14\xCC\xF5',
        "FOFF_3":  b'\x01\x05\x04\x00\x00\x1E\x4C\xF2',
        "FOFF_4":  b'\x01\x05\x04\x00\x00\x28\xCC\xE4',
        "FOFF_5":  b'\x01\x05\x04\x00\x00\x32\x4D\x2F',
        "FOFF_6":  b'\x01\x05\x04\x01\x00\x08\x9C\xFC',
        "FOFF_7":  b'\x01\x05\x04\x01\x00\x0A\x1D\x3D',
        "FOFF_8":  b'\x01\x05\x04\x01\x00\x14\x9D\x35',
        "FOFF_9":  b'\x01\x05\x04\x01\x00\x1E\x1D\x32',
        "FOFF_10": b'\x01\x05\x04\x01\x00\x28\x9D\x24',
        "FOFF_11": b'\x01\x05\x04\x01\x00\x32\x1C\xEF',
        "FOFF_12": b'\x01\x05\x04\x02\x00\x08\x6C\xFC',
        "FOFF_13": b'\x01\x05\x04\x02\x00\x0A\xED\x3D',
        "FOFF_14": b'\x01\x05\x04\x02\x00\x14\x6D\x35',
        "FOFF_15": b'\x01\x05\x04\x02\x00\x1E\xED\x32',
        "FOFF_16": b'\x01\x05\x04\x02\x00\x28\x6D\x24',
        "FOFF_17": b'\x01\x05\x04\x02\x00\x32\xEC\xEF',
        "FOFF_18": b'\x01\x05\x04\x03\x00\x08\x3D\x3C',
        "FOFF_19": b'\x01\x05\x04\x03\x00\x0A\xBC\xFD',
        "FOFF_20": b'\x01\x05\x04\x03\x00\x14\x3C\xF5',
        "FOFF_21": b'\x01\x05\x04\x03\x00\x1E\xBC\xF2',
        "FOFF_22": b'\x01\x05\x04\x03\x00\x28\x3C\xE4',
        "FOFF_23": b'\x01\x05\x04\x03\x00\x32\xBD\x2F',
        "FOFF_24": b'\x01\x05\x04\x04\x00\x08\x8C\xFD',
        "FOFF_25": b'\x01\x05\x04\x04\x00\x0A\x0D\x3C',
        "FOFF_26": b'\x01\x05\x04\x04\x00\x14\x8D\x34',
        "FOFF_27": b'\x01\x05\x04\x04\x00\x1E\x0D\x33',
        "FOFF_28": b'\x01\x05\x04\x04\x00\x28\x8D\x25',
        "FOFF_29": b'\x01\x05\x04\x04\x00\x32\x0C\xEE',
        "FOFF_30": b'\x01\x05\x04\x05\x00\x08\xDD\x3D',
        "FOFF_31": b'\x01\x05\x04\x05\x00\x0A\x5C\xFC',
        "FOFF_32": b'\x01\x05\x04\x05\x00\x14\xDC\xF4',
        "FOFF_33": b'\x01\x05\x04\x05\x00\x1E\x5C\xF3',
        "FOFF_34": b'\x01\x05\x04\x05\x00\x28\xDC\xE5',
        "FOFF_35": b'\x01\x05\x04\x05\x00\x32\x5D\x2E',
        "FOFF_36": b'\x01\x05\x04\x06\x00\x08\x2D\x3D',
        "FOFF_37": b'\x01\x05\x04\x06\x00\x0A\xAC\xFC',
        "FOFF_38": b'\x01\x05\x04\x06\x00\x14\x2C\xF4',
        "FOFF_39": b'\x01\x05\x04\x06\x00\x1E\xAC\xF3',
        "FOFF_40": b'\x01\x05\x04\x06\x00\x28\x2C\xE5',
        "FOFF_41": b'\x01\x05\x04\x06\x00\x32\xAD\x2E',
        "FOFF_42": b'\x01\x05\x04\x07\x00\x08\x7C\xFD',
        "FOFF_43": b'\x01\x05\x04\x07\x00\x0A\xFD\x3C',
        "FOFF_44": b'\x01\x05\x04\x07\x00\x14\x7D\x34',
        "FOFF_45": b'\x01\x05\x04\x07\x00\x1E\xFD\x33',
        "FOFF_46": b'\x01\x05\x04\x07\x00\x28\x7D\x25',
        "FOFF_47": b'\x01\x05\x04\x07\x00\x32\xFC\xEE',
    }

    def __init__(self, ip: str, port: int, timeout: int = 5, reconnect_interval: float = 3.0):
        self.ip                 = ip
        self.port               = port
        self.timeout            = timeout
        self.reconnect_interval = reconnect_interval
        self._sock              = None
        self._lock              = threading.Lock()
        self._connected         = False
        self._reconnect_thread  = None
        self._stop_reconnect    = False
        self._connect()

    # --- Bağlantı yönetimi ---

    def _connect(self) -> bool:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.ip, self.port))
            with self._lock:
                self._sock      = s
                self._connected = True
            logger.info(f"TCP bağlandı: {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"TCP bağlantı hatası: {e}")
            self._connected = False
            return False

    def _start_reconnect(self):
        """Non-blocking arka plan yeniden bağlanma thread'i."""
        if self._reconnect_thread and self._reconnect_thread.is_alive():
            return
        self._stop_reconnect   = False
        self._reconnect_thread = threading.Thread(target=self._reconnect_loop, daemon=True)
        self._reconnect_thread.start()

    def _reconnect_loop(self):
        while not self._stop_reconnect and not self._connected:
            logger.warning(f"Yeniden bağlanılıyor... ({self.reconnect_interval}s)")
            time.sleep(self.reconnect_interval)
            if self._connect():
                break

    def disconnect(self):
        """Bağlantıyı kapatır."""
        self._stop_reconnect = True
        with self._lock:
            if self._sock:
                try:
                    self._sock.close()
                except Exception:
                    pass
                self._sock      = None
                self._connected = False

    # --- Ham gönderim ---

    def _send(self, data: bytes) -> bytes:
        """Veri gönderir, cevabı alır. Hata durumunda reconnect başlatır."""
        with self._lock:
            if not self._connected or self._sock is None:
                logger.warning("Bağlantı yok, gönderim yapılamadı.")
                self._start_reconnect()
                return b''
            try:
                self._sock.sendall(data)
                logger.debug(f"TX: {binascii.hexlify(data, b' ').decode().upper()}")
                rx = self._sock.recv(1024)
                if rx:
                    logger.debug(f"RX: {binascii.hexlify(rx, b' ').decode().upper()}")
                return rx
            except Exception as e:
                logger.error(f"Gönderim hatası: {e}")
                self._connected = False
                self._sock      = None
        self._start_reconnect()
        return b''

    def _send_key(self, key: str) -> bytes:
        """_RELAY_MAP'ten key ile hex gönderir."""
        try:
            cmd = self._RELAY_MAP[key]
            return self._send(cmd)
        except KeyError:
            logger.error(f"Geçersiz Parametre: '{key}' _RELAY_MAP içinde bulunamadı.")
            return b''

    # --- Ortak metotlar ---

    def relay_on(self, param: str) -> bytes:
        """Röle açar. Parametre: R1_1 ... R16_1 veya ALL"""
        return self._send_key(param)

    def relay_off(self, param: str) -> bytes:
        """Röle kapatır. Parametre: R1_0 ... R16_0 veya OFF"""
        return self._send_key(param)

    def relay_toggle(self, param: str) -> bytes:
        """Röle toggle yapar. Parametre: R1_T ... R16_T"""
        return self._send_key(param)

    def relay_la(self, param: str) -> bytes:
        """
        Linkage / Normal mod ayarlar.
        Parametre: linkage_1_8 | normal_1_8 | linkage_9_16 | normal_9_16
        """
        return self._send_key(param)

    def relay_linkage_or_normal(self, param: str) -> bytes:
        """
        Röle modunu sorgular (Linkage mı Normal mı?).
        Parametre: la_no_1_8 | la_no_9_16
        """
        return self._send_key(param)

    def flash_on(self, index: int) -> bytes:
        """
        Flash ON komutu gönderir. index: 0-47
        flash_on(0)  = No.0 relay1 800ms
        flash_on(1)  = No.0 relay1 1000ms
        flash_on(2)  = No.0 relay1 2000ms
        flash_on(3)  = No.0 relay1 3000ms
        flash_on(4)  = No.0 relay1 4000ms
        flash_on(5)  = No.0 relay1 5000ms
        flash_on(6)  = No.1 relay2 800ms  ...  flash_on(47) = No.7 relay8 5000ms
        """
        try:
            key = f"FON_{index}"
            cmd = self._FLASH_MAP[key]
            return self._send(cmd)
        except KeyError:
            logger.error(f"Geçersiz flash_on index: {index}. Geçerli aralık: 0-47")
            return b''

    def flash_off(self, index: int) -> bytes:
        """
        Flash OFF komutu gönderir. index: 0-47
        flash_off(0)  = No.0 relay1 800ms
        flash_off(47) = No.7 relay8 5000ms
        """
        try:
            key = f"FOFF_{index}"
            cmd = self._FLASH_MAP[key]
            return self._send(cmd)
        except KeyError:
            logger.error(f"Geçersiz flash_off index: {index}. Geçerli aralık: 0-47")
            return b''

    def read_relay_status_8bit(self) -> bytes:
        """1-8 Röle durum hex sorgular."""
        return self._send_key("read_relay_status_8bit")

    def read_relay_status_9_16(self) -> bytes:
        """9-16 Röle durum hex sorgular."""
        return self._send_key("read_relay_status_9_16")

    def RS_18_8BIT(self) -> bytes:
        """1-8 Röle durumunu 1/0 olarak sorgular."""
        return self._send_key("RS_18_8BIT")

    def RS_916_8BIT(self) -> bytes:
        """9-16 Röle durumunu 1/0 olarak sorgular."""
        return self._send_key("RS_916_8BIT")

    def read_input_status(self) -> bytes:
        """8 input durumunu hex olarak sorgular."""
        return self._send_key("read_input_status")

    def read_input_binary(self) -> bytes:
        """8 input durumunu 1/0 olarak sorgular."""
        return self._send_key("read_input_binary")


    


# ============================================================
#  3) UdpRelay  –  UDP GET Protokolü
# ============================================================

class UdpRelay:
    """
    Seda Elektronik UDP GET Röle Kartı API sınıfı.
    Röle kontrolü UDP üzerinden ASCII parametre göndererek yapılır.
    Status okuma ve config HTTP GET üzerinden yapılır.

    Kullanım:
        udp = UdpRelay("169.254.1.2", 3000)
        udp.relay_on(R1_1)
        udp.relay_off(R1_0)
        udp.relay_toggle(R1_T)
        udp.relay_on(ALL)
        udp.relay_off(OFF)
        status = udp.read_status()
        udp.read_status_loop()
        udp.config()
    """

    # UDP üzerinden gönderilecek parametre → bytes eşleşmesi
    _UDP_MAP = {
        # Röle AÇMA
        "1": b"1", "2": b"2", "3": b"3", "4": b"4",
        "5": b"5", "6": b"6", "7": b"7", "8": b"8",
        "9": b"9", "0": b"0", "a": b"a", "b": b"b",
        "c": b"c", "d": b"d", "e": b"e", "L": b"L",
        # Röle KAPATMA
        "i": b"i", "g": b"g", "h": b"h", "j": b"j",
        "k": b"k", "l": b"l", "m": b"m", "n": b"n",
        "o": b"o", "p": b"p", "q": b"q", "t": b"t",
        "u": b"u", "v": b"v", "w": b"w", "M": b"M",
        # Toggle
        "y0": b"y0", "y1": b"y1", "y2": b"y2", "y3": b"y3",
        "y4": b"y4", "y5": b"y5", "y6": b"y6", "y7": b"y7",
        "z0": b"z0", "z1": b"z1", "z2": b"z2", "z3": b"z3",
        "z4": b"z4", "z5": b"z5", "z6": b"z6", "z7": b"z7",
        # Tümü
        "ALL": b"ALL", "OFF": b"OFF",
    }

    def __init__(self, ip: str, port: int, timeout: int = 3, reconnect_interval: float = 3.0):
        if requests is None:
            raise ImportError("UdpRelay.read_status için 'requests' kütüphanesi gereklidir: pip install requests")
        self.ip                 = ip
        self.port               = port
        self.timeout            = timeout
        self.reconnect_interval = reconnect_interval
        self._sock              = None
        self._connected         = False
        self._lock              = threading.Lock()
        self._reconnect_thread  = None
        self._stop_reconnect    = False
        self._loop_running      = False
        self._base_http         = f"http://{ip}:{port}"
        self._connect()

    # --- Bağlantı yönetimi ---

    def _connect(self) -> bool:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(self.timeout)
            with self._lock:
                self._sock      = s
                self._connected = True
            logger.info(f"UDP soketi hazır: {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"UDP soket hatası: {e}")
            self._connected = False
            return False

    def _start_reconnect(self):
        if self._reconnect_thread and self._reconnect_thread.is_alive():
            return
        self._stop_reconnect   = False
        self._reconnect_thread = threading.Thread(target=self._reconnect_loop, daemon=True)
        self._reconnect_thread.start()

    def _reconnect_loop(self):
        while not self._stop_reconnect and not self._connected:
            logger.warning(f"UDP yeniden bağlanılıyor... ({self.reconnect_interval}s)")
            time.sleep(self.reconnect_interval)
            if self._connect():
                break

    def disconnect(self):
        self._stop_reconnect = True
        with self._lock:
            if self._sock:
                try:
                    self._sock.close()
                except Exception:
                    pass
                self._sock      = None
                self._connected = False

    # --- Ham gönderim ---

    def _send(self, data: bytes) -> bool:
        with self._lock:
            if not self._connected or self._sock is None:
                logger.warning("UDP bağlantı yok, gönderim yapılamadı.")
                self._start_reconnect()
                return False
            try:
                self._sock.sendto(data, (self.ip, self.port))
                logger.info(f"UDP TX: {data.decode(errors='replace')} -> {self.ip}:{self.port}")
                return True
            except Exception as e:
                logger.error(f"UDP gönderim hatası: {e}")
                self._connected = False
                self._sock      = None
        self._start_reconnect()
        return False

    def _send_param(self, param: str) -> bool:
        try:
            data = self._UDP_MAP[param]
            return self._send(data)
        except KeyError:
            logger.error(f"Geçersiz Parametre: '{param}' _UDP_MAP içinde bulunamadı.")
            return False

    # --- Ortak metotlar ---

    def relay_on(self, param: str) -> bool:
        """Röle açar. Parametre: R1_1 ... R16_1 veya ALL"""
        return self._send_param(param)

    def relay_off(self, param: str) -> bool:
        """Röle kapatır. Parametre: R1_0 ... R16_0 veya OFF"""
        return self._send_param(param)

    def relay_toggle(self, param: str) -> bool:
        """Röle toggle yapar. Parametre: R1_T ... R16_T"""
        return self._send_param(param)

    def read_status(self) -> dict:
        """
        HTTP GET /s endpoint'inden tek seferlik okuma yapar.
        Döndürür: {"PORTB": str, "PORTD": str, "PORTA": str, "PORTE": str,
                   "TEMP1": float, "TEMP2": float}
        PORT değerleri 8 haneli binary string (örn: "00000101")
        """
        url = f"{self._base_http}/s"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            return _parse_status(r.text)
        except Exception as e:
            logger.error(f"read_status hatası: {e}")
            return False

    def read_status_loop(self, interval: float = 0.4):
        """
        HTTP GET /s endpoint'inden her 400ms'de bir okuma yapar.
        Çıkmak için Ctrl+C kullanın.
        """
        self._loop_running = True
        logger.info("read_status_loop başladı. Durdurmak için Ctrl+C.")
        try:
            while self._loop_running:
                data = self.read_status()
                if data:
                    print(data)
                time.sleep(interval)
        except KeyboardInterrupt:
            self._loop_running = False
            logger.info("read_status_loop durduruldu.")

    def config(self) -> str:
        """
        HTTP GET /IP? endpoint'inden ağ konfigürasyonunu okur.
        Döndürür: IP, PORTNO, GATEWAY, SUBNET MASK bilgileri (ham metin)
        """
        url = f"{self._base_http}/{NetCon}"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            logger.info(f"config -> {r.text.strip()}")
            return r.text.strip()
        except Exception as e:
            logger.error(f"config hatası: {e}")
            return False
