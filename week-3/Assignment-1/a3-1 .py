import os
import time
import sys


sys.stdout.reconfigure(encoding='utf-8')


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'nhan.nmea')

def parse_nmea_file(filepath):
    
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line.startswith('$'):
                    continue
                
                parts = line.split(',')
                
                
                if parts[0] == "$GPRMC" and len(parts) > 9:
                    raw_time = parts[1]
                    raw_date = parts[9]
                    speed_knots = parts[7]
                    
                    speed_kmh = float(speed_knots) * 1.852 if speed_knots else 0
                    
                    print(f"\n[{raw_time[:2]}:{raw_time[2:4]}:{raw_time[4:6]} UTC] NGÀY: {raw_date[:2]}/{raw_date[2:4]}/{raw_date[4:6]}")
                    print(f" >> TỐC ĐỘ: {speed_kmh:.2f} km/h")

            
                elif parts[0] == "$GPGGA" and len(parts) > 9:
                    altitude = parts[9]
                    unit = parts[10]
                    print(f" >> ĐỘ CAO HIỆN TẠI: {altitude} {unit}")
                    print("-" * 30)
                
                time.sleep(0.5)
                
    except FileNotFoundError:
        print("\n[LỖI] KHÔNG TÌM THẤY FILE!")
        print(f"Máy tính đang tìm ở đường dẫn này: {filepath}")
    except Exception as e:
        print(f"\n[LỖI KHÔNG XÁC ĐỊNH] {e}")


parse_nmea_file(file_path)