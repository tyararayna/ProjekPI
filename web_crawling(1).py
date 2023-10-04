import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

# Daftar tanggal yang akan digunakan dalam looping
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 12, 1)

# List untuk menyimpan semua tautan dari semua halaman
all_hrefs = []

# Perulangan melalui setiap tanggal
current_date = start_date
max_links = 100
counter = 0

while current_date <= end_date and counter < max_links:
    date_str = current_date.strftime("%Y/%m/%d")
    url = f"https://www.viva.co.id/indeks/berita/all/{date_str}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Mencari semua elemen <a> dengan class "article-list-title"
    links = soup.find_all('a', class_='article-list-title')

    # Mengambil semua href dari tautan-tautan tersebut dan menambahkannya ke all_hrefs
    hrefs = [link['href'] for link in links]
    all_hrefs.extend(hrefs)

    # Menghitung jumlah tautan yang sudah diekstrak
    counter += len(hrefs)

    # Menambahkan 1 hari ke tanggal saat ini
    current_date += timedelta(days=1)

# Menyimpan hasil ke dalam berkas CSV
with open('links.csv', 'w', newline='') as csvfile:
    fieldnames = ['Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for href in all_hrefs:
        writer.writerow({'Link': href})

# Menyimpan hasil ke dalam berkas TXT
with open('links.txt', 'w') as txtfile:
    for href in all_hrefs:
        txtfile.write(f"{href}\n")
