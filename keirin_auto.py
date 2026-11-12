import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
DATA_FILE = Path("keirin_data.json")


def get_current_time():
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")


def load_data():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "races": [],
        "predictions": [],
        "results": []
    }


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def main():
    print("競輪AI PRO 自動分析システム")
    print("実行日時:", get_current_time())

    data = load_data()

    print("登録レース数:", len(data["races"]))
    print("予想データ数:", len(data["predictions"]))
    print("結果データ数:", len(data["results"]))

    save_data(data)

    print("データ保存成功")
    print("システム正常終了")


if __name__ == "__main__":
    main()
