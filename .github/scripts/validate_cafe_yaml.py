import yaml
import sys
import os
import glob
import re

REQUIRED_FIELDS = ['title', 'location', 'price', 'table_chair', 'outlets', 'outlets_count', 'wifi']
OPTIONAL_FIELDS = ['naver_map_link', hours_weekday', 'hours_weekend', 'congestion_weekday', 'congestion_weekend', 'scale', 'features', 'region_kr', 'subregion_kr', 'wifi_speed']
CONGESTION_VALUES = ['여유', '보통', '혼잡']
OUTLETS_COUNT_VALUES = ['많음', '적음']
WIFI_SPEED_VALUES = ['빠름', '느림']

def validate_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data:
            print(f"Error: {file_path} has no YAML data")
            return False
        
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] in [None, '']:
                print(f"Error: {file_path} missing or empty '{field}'")
                return False
        
        if not isinstance(data['outlets'], bool):
            print(f"Error: {file_path} invalid 'outlets' (must be true/false)")
            return False
        if not isinstance(data['wifi'], bool):
            print(f"Error: {file_path} invalid 'wifi' (must be true/false)")
            return False
        
        # if data['congestion_weekday'] not in CONGESTION_VALUES:
        #     print(f"Error: {file_path} invalid 'congestion_weekday' (must be {CONGESTION_VALUES})")
        #     return False
        # if data['congestion_weekend'] not in CONGESTION_VALUES:
        #     print(f"Error: {file_path} invalid 'congestion_weekend' (must be {CONGESTION_VALUES})")
        #     return False
        
        if data['outlets_count'] not in OUTLETS_COUNT_VALUES:
            print(f"Error: {file_path} invalid 'outlets_count' (must be {OUTLETS_COUNT_VALUES})")
            return False
        # if data['wifi_speed'] not in WIFI_SPEED_VALUES:
        #     print(f"Error: {file_path} invalid 'wifi_speed' (must be {WIFI_SPEED_VALUES})")
        #     return False
        
        for field in OPTIONAL_FIELDS:
            if field in data and data[field] in [None, '']:
                print(f"Error: {file_path} empty optional field '{field}'")
                return False
        
        filename = os.path.basename(file_path)
        if filename != f"{data['title']}.yaml":
            print(f"Error: {file_path} filename must match title '{data['title']}.yaml'")
            return False
        
        existing_titles = [yaml.safe_load(open(f, 'r', encoding='utf-8')).get('title') for f in glob.glob('**/*.yaml', recursive=True) if f != file_path]
        if data['title'] in existing_titles:
            print(f"Error: {file_path} duplicate title '{data['title']}'")
            return False
        
        # Markdown 파일 쌍 확인
        md_file = file_path.replace('.yaml', '.md')
        if not os.path.exists(md_file):
            print(f"Error: {file_path} missing corresponding Markdown file '{md_file}'")
            return False
        
        # 특수문자 체크
        if re.search(r'[,&!]', filename):
            print(f"Error: {file_path} contains invalid characters (',', '&', '!')")
            return False
        
        print(f"Success: {file_path} passed validation")
        return True
    
    except Exception as e:
        print(f"Error: {file_path} failed - {str(e)}")
        return False

def main():
    changed_files = sys.argv[1].split() if len(sys.argv) > 1 else []
    if not changed_files:
        print("No YAML files changed")
        sys.exit(0)
    
    all_valid = True
    for file_path in changed_files:
        if file_path.endswith('.yaml'):
            if not validate_yaml(file_path):
                all_valid = False
    
    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()
