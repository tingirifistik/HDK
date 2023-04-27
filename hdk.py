import requests
from PIL import Image
from pytesseract import pytesseract
from os import remove, system
from time import sleep
from random import choice, randint


def TCNoUret():
    rakam = []
    tcNo = ""
    rakam.append(randint(1,9))
    for i in range(1, 9):
        rakam.append(randint(0,9))
    rakam.append(((rakam[0] + rakam[2] + rakam[4] + rakam[6] + rakam[8]) * 7 - (rakam[1] + rakam[3] + rakam[5] + rakam[7])) % 10)
    rakam.append((rakam[0] + rakam[1] + rakam[2] + rakam[3] + rakam[4] + rakam[5] + rakam[6] + rakam[7] + rakam[8] + rakam[9]) % 10)
    for r in rakam:
        tcNo += str(r)
    return tcNo


def Login(tc, parola):
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/?p=2&dil=0"
    cookies = {"key": "value"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Pragma": "no-cache", "Cache-Control": "no-cache", "Te": "trailers"}
    php = requests.get(url, headers=headers, cookies=cookies).cookies["PHPSESSID"]

    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/captcha.php?form=girisForm&r=0.29171246377395676&r=0.4973049864729181&r=0.6912122964211741&r=0.8208744773956634"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "image/avif,image/webp,*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=2&dil=0&devam=2f796f7264616d2f", "Sec-Fetch-Dest": "image", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    r = requests.get(url, headers=headers, cookies=cookies)
    with open("kod.jpeg", "wb") as f:
        f.write(r.content)

    pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    kod = pytesseract.image_to_string(Image.open("kod.jpeg"))[:-1]

    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=2&dil=0&devam=2f796f7264616d2f", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"dil": "0", "islem": "sUyeBilgi", "kiosk": "0", "yazilim": "yordam", "rezervasyonIslem": "oturumAc", "uyeKodKN": str(tc), "aSifre": str(parola), "code_girisForm": kod}
    r = requests.post(url, headers=headers, cookies=cookies, data=data)    
    if r.text == "Giriş işlemi başarılı":
        print("\nGiriş işlemi başarılı!")
        sleep(2.1)
        with open("config", "w", encoding="utf-8") as f:
            f.write(php)
    else:
        print("Kullanıcı bulunamadı. Yeniden deneyin.")
        sleep(3)
    remove("kod.jpeg")


def Musait(php):
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "tarihSaatGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg"}
    r = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    metin = ""
    t = 0
    while 1:
        try:
            metin+= "\n----------\n"+r["tarih"][t]["val"].split("T")[0]+"\n----------\n"
            s = 0
            while 1:
                try:
                    metin+= r["tarih"][t]["SaatGirisCikis_str"]["buckets"][s]["val"]+" --> "+ str(r["tarih"][t]["SaatGirisCikis_str"]["buckets"][s]["musait"]["count"])+"\n"
                    s+=1
                except IndexError:
                    break
            t+=1
        except IndexError:
            break
    return(metin)


def Rez(php, masa , sira, tarih, saat, oto):
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "sandalyeGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg"}
    r = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    for i in r["masalar"]:
        if i["masaAdi_str"] == "M-"+masa:
            for i in i["sandalyeAdi_str"]["buckets"]:
                if i["sandalyeAdi_str"] == "S-"+sira:
                    sandalye = (i["val"])
                    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
                    cookies = {"key": "value", "PHPSESSID": php}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
                    data = {"islem": "sandalyeMusaitlikGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg", "tarih": tarih, "saat": saat}
                    for i in requests.post(url, headers=headers, cookies=cookies, data=data).json():
                        if i["sandalyeKN_str"] == sandalye:
                            if i["cSaatAcKapa_str"] == "1":
                                url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
                                cookies = {"key": "value", "PHPSESSID": php}
                                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
                                data = {"islem": "odaRezervasyon", "hesKodu": '', "tckno": '', "recordid": i["RECORDID"], "cikis": saat.split(" - "[1]), "tarih": tarih, "kiosk": "0"}
                                r = requests.post(url, headers=headers, cookies=cookies, data=data)
                                print((r.text).replace("<br>", " ").replace("</b>", " "))
                                input("\n\nMenüye dönmek için 'Enter' tuşuna basınız..")
                                return 1
                            elif i["cSaatAcKapa_str"] == "0" and oto == 0:
                                print("Sandalye Dolu!")
                                sleep(2.2)
                            else:
                                return 0
                            break
                    break
            break


def Mevcut(php):
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "uyeUyari", "dil": "0", "kiosk": "0"}
    try:
        bol = requests.post(url, headers=headers, cookies=cookies, data=data).text.split("<p>")[1].split("</p>")[0].replace("<br>", " ")
    except IndexError:
        return("Yok")
    return(bol)  

    
def Iptal(php):
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "uyeUyari", "dil": "0", "kiosk": "0"}
    try:
        bol = requests.post(url, headers=headers, cookies=cookies, data=data).text.split("<p>")[1].split("</p>")[0].split("<br> ")
    except IndexError:
        print("Rezervasyonunuz bulunmuyor!")
        sleep(2)
        return
    masa = bol[1].split("/")[0].strip()
    sandalye = bol[1].split("/")[1].strip()
    tarih = bol[2].split("2023")[0] 
    s = int(bol[2].split("2023 - ")[1].split(" - ")[0].split(":")[0])
    if s < 6 and s >= 0:
        saat = ("00:00:00 - 06:00:00")
    elif s < 13 and s >= 7:
        saat = ("07:00:00 - 13:00:00")
    elif s < 19 and s >= 13:
        saat = ("13:00:00 - 19:00:00")
    elif s < 24 and s >= 19:
        saat = ("19:00:00 - 23:59:59")
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "sandalyeGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg"}
    r = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    for i in r["masalar"]:
        if i["masaAdi_str"] == masa:
            for i in i["sandalyeAdi_str"]["buckets"]:
                if i["sandalyeAdi_str"] == sandalye:
                    sandalye = (i["val"])
                    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
                    cookies = {"key": "value", "PHPSESSID": php}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
                    data = {"islem": "sandalyeMusaitlikGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg", "tarih": tarih+"2023", "saat": saat}
                    for i in requests.post(url, headers=headers, cookies=cookies, data=data).json():
                        if i["sandalyeKN_str"] == sandalye:
                            url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
                            cookies = {"key": "value", "PHPSESSID": php}
                            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
                            data = {"islem": "rezervasyonIptal", "recordid": i["RECORDID"]}
                            r = requests.post(url, headers=headers, cookies=cookies, data=data)
                            if r.text != "[hata] Farklı üye: 401":
                                print(r.text)
                                input("\n\nMenüye dönmek için 'Enter' tuşuna basınız..")
                                break
                            else:
                                pass        
                    break
            break
        

def RandomSec(php, tarih, saat, oto):
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "sandalyeMusaitlikGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg", "tarih": tarih, "saat": saat}
    bos = []
    for i in requests.post(url, headers=headers, cookies=cookies, data=data).json():
        if i["cSaatAcKapa_str"] == "1":
            bos.append(i["RECORDID"])
    if len(bos) == 0 and oto == 0:
        print("Boş yer yok!")
        sleep(3)
        return
    elif len(bos) == 0 and oto == 1:
        return
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    while 1:
        data = {"islem": "odaRezervasyon", "hesKodu": '', "tckno": '', "recordid": choice(bos), "cikis": saat.split(" - "[1]), "tarih": tarih, "kiosk": "0"}
        r = requests.post(url, headers=headers, cookies=cookies, data=data)
        if "[hata]" not in r.text:
            print((r.text).replace("<br>", " ").replace("</b>", " "))
            input("\n\nMenüye dönmek için 'Enter' tuşuna basınız..")
            return 1


def FakeRez(php, tarih, saat):
    tc = TCNoUret()
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "sandalyeMusaitlikGetir", "dosya": "kurumsal/rezervasyon/H_Kat_Salon.jpg", "tarih": tarih, "saat": saat}
    bos = []
    for i in requests.post(url, headers=headers, cookies=cookies, data=data).json():
        if i["cSaatAcKapa_str"] == "1":
            bos.append(i["RECORDID"])
    if len(bos) == 0:
        print("Boş yer yok!")
        sleep(2)
        return 1
    url = "https://kutuphane.uskudar.bel.tr:443/yordam/inc/islem.fm.inc.php"
    cookies = {"key": "value", "PHPSESSID": php}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://kutuphane.uskudar.bel.tr", "Dnt": "1", "Referer": "https://kutuphane.uskudar.bel.tr/yordam/?p=7&dil=0", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
    data = {"islem": "odaRezervasyon", "hesKodu": '', "tckno": tc, "recordid": choice(bos), "cikis": saat.split(" - "[1]), "tarih": tarih, "kiosk": "0"}
    requests.post(url, headers=headers, cookies=cookies, data=data)
    print("Rezervasyon yapıldı --> "+tc)


while 1:
    try:
        try:
            with open("config", "r", encoding="utf-8")as f:
                phpsessid = f.read()
        except FileNotFoundError:
            system("cls||clear")
            print("Herhangi bir işlem yapmadan önce giriş yapmalısın!")
            sleep(3)
        system("cls||clear")
        print(r"""
  _   _ ____  _  __
 | | | |  _ \| |/ /
 | |_| | | | | ' / 
 |  _  | |_| | . \ 
 |_| |_|____/|_|\_\
                  
            by tingirifistik
      """)
        try:
            print(f" Aktif Rezervasyon: {Mevcut(phpsessid)}\n")
        except NameError:
            print(f" Aktif Rezervasyon: Bilinmiyor\n")
        menu = int(input(" 1- Giriş Yap\n 2- Boş Yer Sayısı\n 3- Rezervasyonu Iptal Et\n\n 4- Rezervasyon Yap\n 5- Dolu Yer Boşaldığı An Al\n\n 6- Rastgele Rezervasyon Yap\n 7- Herhangi Bir Yer Boşaldığı An Al\n\n 8- Sahte Rezervasyon Yap\n\n 9- Çıkış\n\n Seçim: "))
        system("cls||clear")
        if menu == 1:
            try:
                tc = int(input("T.C. Kimlik No: "))
                if len(str(tc)) != 11:
                    raise ValueError
            except ValueError:
                print("Geçerli bir T.C. Kimlik No giriniz!")
                continue
            parola = input("Parola: ")
            Login(tc, parola)
        elif menu == 2:
            print(Musait(phpsessid))    
            input("\n\n\nMenüye dönmek için 'Enter' tuşuna basınız..")
        elif menu == 4:
            print("Sorulacak soruları parantez içinde verilen örnekteki gibi cevapla! \n(Boşluk karakterlerine dikkat et!)")
            sleep(3.5)
            system("cls||clear")
            masa = input("Masa No (M-31): M-")
            sandalte = input("\nSandalye No (S-131): S-")
            tarih = input("\nRezervasyon Tarihi (31.08.2023): ")
            saat = input("\nRezervasyon Saati (00:00:00 - 06:00:00): ")
            oto = 0
            Rez(phpsessid, masa, sandalte, tarih, saat, 0)
        elif menu == 5:
            print("Sorulacak soruları parantez içinde verilen örnekteki gibi cevapla! \n(Boşluk karakterlerine dikkat et!)")
            sleep(3.5)
            system("cls||clear")
            masa = input("Masa No (M-31): M-")
            sandalte = input("\nSandalye No (S-131): S-")
            tarih = input("\nRezervasyon Tarihi (31.08.2023): ")
            saat = input("\nRezervasyon Saati (00:00:00 - 06:00:00): ")
            oto = 1
            system("cls||clear")
            print("Yerin boşalması bekleniyor..\n")
            while 1:
                if Rez(phpsessid, masa, sandalte, tarih, saat, 1) == 1:
                    break
                sleep(6.31)
        elif menu == 3:
            Iptal(phpsessid)
        elif menu == 6:
            print("Sorulacak soruları parantez içinde verilen örnekteki gibi cevapla! \n(Boşluk karakterlerine dikkat et!)")
            sleep(3.5)
            system("cls||clear")
            tarih = input("\nRezervasyon Tarihi (31.08.2023): ")
            saat = input("\nRezervasyon Saati (00:00:00 - 06:00:00): ")
            system("cls||clear")
            RandomSec(phpsessid, tarih, saat, 0)
        elif menu == 7:
            print("Sorulacak soruları parantez içinde verilen örnekteki gibi cevapla! \n(Boşluk karakterlerine dikkat et!)")
            sleep(3.5)
            system("cls||clear")
            tarih = input("\nRezervasyon Tarihi (31.08.2023): ")
            saat = input("\nRezervasyon Saati (00:00:00 - 06:00:00): ")
            system("cls||clear")
            print("Boş yer bekleniyor..\n")
            while 1:
                if RandomSec(phpsessid, tarih, saat, 1) == 1:
                    break
                sleep(6.31)
        elif menu == 8:
            print("Sorulacak soruları parantez içinde verilen örnekteki gibi cevapla! \n(Boşluk karakterlerine dikkat et!)")
            sleep(3.5)
            system("cls||clear")
            tarih = input("\nRezervasyon Tarihi (31.08.2023): ")
            saat = input("\nRezervasyon Saati (00:00:00 - 06:00:00): ")
            adet = int(input("\nKaç adet rezervasyon yapılsın: "))
            system("cls||clear")
            x = 0
            while x < adet:
                if FakeRez(phpsessid, tarih, saat) == 1:
                    break
                x+=1
            print(f"\nToplam {x} adet sahte rezervasyon yapıldı!")
            input("\n\nMenüye dönmek için 'Enter' tuşuna basınız..")
        elif menu == 9:
            break
        else:
            raise ValueError
    except ValueError:
        system("cls||clear")
        print("Hatalı giriş yaptınız. Tekrar deneyin!")
        sleep(3)
