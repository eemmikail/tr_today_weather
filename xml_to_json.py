#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json

def convert_xml_to_json(xml_file, json_file):
    # XML dosyasını oku
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Oluşturulma zamanını al
    generated_at = root.get('generated_at')
    
    # Her şehir için JSON nesnesi oluştur
    city_list = []
    
    for city_elem in root.findall('.//city'):
        city_id = city_elem.get('id')
        city_name = city_elem.get('name')
        
        # Hava durumu verileri
        weather = city_elem.find('.//current_weather')
        if weather is None:
            continue
        
        city_data = {
            "id": city_id,
            "name": city_name,
            "temperature": float(weather.find('temperature').text) if weather.find('temperature') is not None else None,
            "temperature_unit": weather.find('temperature_unit').text if weather.find('temperature_unit') is not None else "°C",
            "humidity": int(weather.find('humidity').text) if weather.find('humidity') is not None else None,
            "apparent_temperature": float(weather.find('apparent_temperature').text) if weather.find('apparent_temperature') is not None else None,
            "weather_code": int(weather.find('weather_code').text) if weather.find('weather_code') is not None else None,
            "weather_description": weather.find('weather_description').text if weather.find('weather_description') is not None else None,
            "is_day": int(weather.find('is_day').text) if weather.find('is_day') is not None else None,
            "precipitation": float(weather.find('precipitation').text) if weather.find('precipitation') is not None else None,
            "rain": float(weather.find('rain').text) if weather.find('rain') is not None else None,
            "snowfall": float(weather.find('snowfall').text) if weather.find('snowfall') is not None else None,
            "cloud_cover": int(weather.find('cloud_cover').text) if weather.find('cloud_cover') is not None else None,
            "pressure": float(weather.find('pressure').text) if weather.find('pressure') is not None else None,
            "wind_speed": float(weather.find('wind_speed').text) if weather.find('wind_speed') is not None else None,
            "wind_direction": int(weather.find('wind_direction').text) if weather.find('wind_direction') is not None else None,
            "wind_gusts": float(weather.find('wind_gusts').text) if weather.find('wind_gusts') is not None else None,
            "generated_at": generated_at
        }
        
        city_list.append(city_data)
    
    # Her şehri tek satır olarak JSON dosyasına yaz
    with open(json_file, 'w', encoding='utf-8') as f:
        for city_data in city_list:
            json_line = json.dumps(city_data, ensure_ascii=False)
            f.write(json_line + "\n")
    
    print(f"{len(city_list)} şehir verisi JSON formatında {json_file} dosyasına kaydedildi.")

if __name__ == "__main__":
    convert_xml_to_json("tr_today_weather.xml", "tr_today_weather.json") 