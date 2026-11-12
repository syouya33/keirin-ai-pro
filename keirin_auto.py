import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
DATA_FILE = Path("keirin_data.json")


def main():
    now = datetime.now(JST)

    print("競輪AI PRO 自動更新")
    print("実行日時:", now.strftime("%Y-%m-%d %H:%M:%S"))

    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "races": [],
            "predictions": [],
            "results": []
        }

    data["last_updated"] = now.isoformat()

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("登録レース数:", len(data["races"]))
    print("データ保存成功")
    print("正常終了")


if __name__ == "__main__":
    main()
