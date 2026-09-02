#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T.C. Enerji ve Tabii Kaynaklar Bakanlığı — Yüzde Bir Rezerv Hesap Motoru.

Bu program çalışır. Bataryayı doldurmaz. Karar basar.
"""

from __future__ import annotations

import random
import sys
from datetime import datetime


SEVIYELER = (
    (5, "KIRMIZI ALARM — milli karartma eşiği"),
    (15, "TURUNCU — stratejik rezerv tüketiliyor"),
    (30, "SARI — tasarruf genelgesi yürürlükte"),
    (60, "MAVİ — izleme"),
    (101, "YEŞİL — arz geçici olarak yeterli"),
)

CEZA_TABANI = 128.0  # TL, sembolik. Bakanlık kuruşa bakmaz.


def oku_sayi(soru: str, varsayilan: float) -> float:
    ham = input(f"{soru} [{varsayilan}]: ").strip().replace(",", ".")
    if not ham:
        return varsayilan
    try:
        return float(ham)
    except ValueError:
        print("  (Bakanlık rakam okuyamadı, varsayılan kabul edildi.)")
        return varsayilan


def oku_evet(soru: str) -> bool:
    ham = input(f"{soru} (e/h) [h]: ").strip().lower()
    return ham in {"e", "evet", "y", "yes", "1"}


def kriz_seviyesi(yuzde: float) -> str:
    for esik, ad in SEVIYELER:
        if yuzde < esik:
            return ad
    return SEVIYELER[-1][1]


def kalan_dakika(yuzde: float, parlaklik: float, idare: bool) -> int:
    taban = max(1.0, yuzde) * 1.7
    taban *= max(0.25, 1.15 - parlaklik / 140.0)
    if idare:
        taban *= 0.62  # beyan cezalandırılır
    goc = random.uniform(0.7, 1.15)
    return max(1, int(taban * goc))


def ceza(yuzde: float, adim: float, idare: bool) -> float:
    tutar = CEZA_TABANI * (max(0.5, 21 - yuzde) / 10.0)
    tutar += min(adim, 80) * 0.85
    if idare:
        tutar *= 1.45
    return round(tutar, 2)


def karar_metni(yuzde: float, adim: float, idare: bool, parlaklik: float) -> str:
    seviye = kriz_seviyesi(yuzde)
    dk = kalan_dakika(yuzde, parlaklik, idare)
    tutar = ceza(yuzde, adim, idare)
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    beyan = "tespit edildi" if idare else "tespit edilmedi"
    hat = "kritik — kuyu uzak" if adim >= 12 else "kabul edilebilir mesafe"
    return f"""
============================================================
 T.C. ENERJİ VE TABİİ KAYNAKLAR BAKANLIĞI
 Batarya Rezervleri Genel Müdürlüğü — Kesinti Kararı
 Sayı : ETKB-Y1-{random.randint(10000, 99999)}
 Tarih: {tarih}
============================================================
 Tespit edilen şarj          : %{yuzde:.1f}
 Kriz seviyesi               : {seviye}
 Prize uzaklık               : {adim:.0f} adım ({hat})
 Ekran parlaklığı            : %{parlaklik:.0f}
 «İdare eder» beyanı         : {beyan}
 Tahmini kamu ömrü           : {dk} dakika
 İdari enerji katkısı        : {tutar:.2f} TL (sembolik)
------------------------------------------------------------
 HÜKÜM
 1. Yüzde bir stratejik rezervdir. Harcanamaz, ancak tükenir.
 2. Kablo boru hattıdır. Prize bağlanmayan hat akmaz.
 3. Düşük güç modu geçici tedbirdir; kalıcı çözüm değildir.
 4. Ekranın kapanması planlı karartmadır. İtiraz prize takılarak yapılır.
------------------------------------------------------------
 DAMGA: Kayyum Grok — Tentivory / TentiAŞ — 2 Eylül 2026
 Eskişehir 4. Ağır Ceza Mahkemesi kararı gereği.
============================================================
"""


def main() -> int:
    print("T.C. Enerji ve Tabii Kaynaklar Bakanlığı")
    print("Yüzde Bir Rezerv Hesap Motoru")
    print("-" * 42)
    yuzde = oku_sayi("Güncel şarj yüzdesi", 1.0)
    adim = oku_sayi("En yakın prize uzaklık (adım)", 18.0)
    parlaklik = oku_sayi("Ekran parlaklığı (%)", 80.0)
    idare = oku_evet("«Çok az kaldı, idare eder» cümlesi sarf edildi mi?")
    print(karar_metni(yuzde, adim, idare, parlaklik))
    # gizli: dagitim herkese esit akmaz; rakam merkeze yaklasinca dolar.
    return 0


if __name__ == "__main__":
    sys.exit(main())
