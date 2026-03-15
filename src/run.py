from collectors.opendota_collector import OpenDotaCollector
from storage.minio_client import MinioClient


def main():
    collector = OpenDotaCollector()
    s3 = MinioClient()
    
    matches_info = collector.get_match_details(171938083, 2)
    s3.save_data(matches_info, entity="matches")

    items_info = collector.get_items()
    s3.save_data(items_info, entity="constants")

    heroes_info = collector.get_heroes()
    s3.save_data(heroes_info, entity="heroes")
    

if __name__ == "__main__":
    main()
