#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import requests
import datetime
from typing import Dict, List, Any

def parse_city_coordinates(xml_file: str) -> List[Dict[str, Any]]:
    """XML dosyasından şehir koordinatlarını oku."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        cities = []
        for city_elem in root.findall('.//city'):
            city = {
                'id': city_elem.get('id'),
                'country': city_elem.get('country'),
                'name': city_elem.get('name'),
                'latitude': city_elem.get('latitude'),
                'longitude': city_elem.get('longitude')
            }
            cities.append(city)
            
        return cities
    except Exception as e:
        print(f"XML dosyası okunurken hata oluştu: {e}")
        return []

def get_weather_data(latitude: str, longitude: str) -> Dict[str, Any]:
    """Open-Meteo API'sinden hava durumunu çek."""
    url = f"https://api.open-meteo.com/v1/forecast"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 
                   'is_day', 'precipitation', 'rain', 'showers', 'snowfall', 
                   'weather_code', 'cloud_cover', 'pressure_msl', 'surface_pressure', 
                   'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m'],
        'timezone': 'auto'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API isteği sırasında hata oluştu: {e}")
        return {}

def weather_code_to_description(code: int) -> str:
    """Hava durumu kodlarını Türkçe açıklamaya çevir."""
    weather_codes = {
        0: "Açık",
        1: "Çoğunlukla Açık",
        2: "Parçalı Bulutlu",
        3: "Bulutlu",
        45: "Sisli",
        48: "Yoğun Sisli",
        51: "Hafif Çisenti",
        53: "Çisenti",
        55: "Yoğun Çisenti",
        56: "Dondurucu Hafif Çisenti",
        57: "Dondurucu Yoğun Çisenti",
        61: "Hafif Yağmur",
        63: "Yağmur",
        65: "Şiddetli Yağmur",
        66: "Dondurucu Hafif Yağmur",
        67: "Dondurucu Şiddetli Yağmur",
        71: "Hafif Kar",
        73: "Kar",
        75: "Yoğun Kar",
        77: "Kar Taneleri",
        80: "Hafif Sağanak",
        81: "Sağanak",
        82: "Şiddetli Sağanak",
        85: "Hafif Kar Sağanağı",
        86: "Şiddetli Kar Sağanağı",
        95: "Gök Gürültülü Fırtına",
        96: "Dolu ile Gök Gürültülü Fırtına",
        99: "Şiddetli Dolu ile Gök Gürültülü Fırtına"
    }
    return weather_codes.get(code, "Bilinmeyen")

def create_weather_xml(cities_weather: List[Dict[str, Any]]) -> ET.Element:
    """Hava durumu verilerinden XML oluştur."""
    root = ET.Element("weather_data")
    root.set("generated_at", datetime.datetime.now().isoformat())
    
    for city_weather in cities_weather:
        if not city_weather.get('weather'):
            continue
            
        city_elem = ET.SubElement(root, "city")
        city_elem.set("id", city_weather['id'])
        city_elem.set("name", city_weather['name'])
        
        current = city_weather['weather'].get('current', {})
        if not current:
            continue
            
        weather_elem = ET.SubElement(city_elem, "current_weather")
        
        # Hava durumu özellikleri ekleniyor
        ET.SubElement(weather_elem, "temperature").text = str(current.get('temperature_2m', 'N/A'))
        ET.SubElement(weather_elem, "temperature_unit").text = city_weather['weather'].get('current_units', {}).get('temperature_2m', '°C')
        
        ET.SubElement(weather_elem, "humidity").text = str(current.get('relative_humidity_2m', 'N/A'))
        ET.SubElement(weather_elem, "apparent_temperature").text = str(current.get('apparent_temperature', 'N/A'))
        
        weather_code = current.get('weather_code')
        ET.SubElement(weather_elem, "weather_code").text = str(weather_code) if weather_code is not None else 'N/A'
        ET.SubElement(weather_elem, "weather_description").text = weather_code_to_description(weather_code) if weather_code is not None else 'Bilinmeyen'
        
        ET.SubElement(weather_elem, "is_day").text = str(current.get('is_day', 'N/A'))
        ET.SubElement(weather_elem, "precipitation").text = str(current.get('precipitation', 'N/A'))
        ET.SubElement(weather_elem, "rain").text = str(current.get('rain', 'N/A'))
        ET.SubElement(weather_elem, "snowfall").text = str(current.get('snowfall', 'N/A'))
        
        ET.SubElement(weather_elem, "cloud_cover").text = str(current.get('cloud_cover', 'N/A'))
        ET.SubElement(weather_elem, "pressure").text = str(current.get('pressure_msl', 'N/A'))
        
        ET.SubElement(weather_elem, "wind_speed").text = str(current.get('wind_speed_10m', 'N/A'))
        ET.SubElement(weather_elem, "wind_direction").text = str(current.get('wind_direction_10m', 'N/A'))
        ET.SubElement(weather_elem, "wind_gusts").text = str(current.get('wind_gusts_10m', 'N/A'))
        
    return root

def save_xml(root: ET.Element, filename: str) -> None:
    """XML'i dosyaya kaydet."""
    tree = ET.ElementTree(root)
    
    # XML'i düzgün bir şekilde formatla
    ET.indent(tree, space="  ")
    
    # XML dosyasını kaydet
    try:
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Hava durumu verileri {filename} dosyasına kaydedildi.")
    except Exception as e:
        print(f"XML dosyası kaydedilirken hata oluştu: {e}")

def main():
    # XML dosyasından şehir koordinatlarını oku
    cities = parse_city_coordinates("city_coordinates.xml")
    print(f"{len(cities)} şehir koordinatları başarıyla okundu.")
    
    # Her şehir için hava durumu verilerini topla
    cities_weather = []
    for city in cities:
        print(f"{city['name']} için hava durumu alınıyor...")
        weather_data = get_weather_data(city['latitude'], city['longitude'])
        
        city_weather = {
            'id': city['id'],
            'name': city['name'],
            'weather': weather_data
        }
        cities_weather.append(city_weather)
    
    # Hava durumu verilerinden XML oluştur
    weather_xml = create_weather_xml(cities_weather)
    
    # XML'i dosyaya kaydet
    save_xml(weather_xml, "tr_today_weather.xml")

if __name__ == "__main__":
    main()