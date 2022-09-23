# https://github.com/kresnasatya/api-harilibur
# https://api-harilibur.vercel.app/api => mendapatkan daftar hari libur tahun sekarang

# https://api-harilibur.vercel.app/api?year=2021 => mendapatkan daftar hari libur di tahun 2021

# https://api-harilibur.vercel.app/api?month=8&year=2021 => mendapatkan daftar hari libur di bulan 8 tahun 2021

# https://api-harilibur.vercel.app/api?month=8 => mendapatkan daftar hari libur di bulan 8 tahun sekarang

from email import header
import requests
import json

header ={
    'Accept': 'application/json'
}

def GetHariNasional():
    response = requests.get('https://api-harilibur.vercel.app/api', headers=header)
    data = response.text
    dataJson = json.loads(data)
    return dataJson

if __name__ == "__main__":
    print(GetHariNasional())