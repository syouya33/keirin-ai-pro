import csv
import io
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))
OUTPUT = Path("keirin_data.json")

BASE = (
    "https://raw.githubusercontent.com/"
    "Kenseimk/keirin-data/main/keirin_data/"
)

def download_csv(year, month):
    url = BASE + f"{year}_{month:02d}_keirin.csv"

    print("取得先:", url)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "KeirinAIPro/1.0"}
    )

    with urllib.request.urlopen(
        request, timeout=30
    ) as response:
        content = response.read()

    text = content.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def main():
    now = datetime.now(JST)

    print("競輪AI PRO 出走表取得開始")
    print("実行日時:", now.isoformat())

    races = {}
    errors = []

    # 当月と翌月の公開データを確認
    months = [
        (now.year, now.month),
        (
            (now.replace(day=28) + timedelta(days=4)).year,
            (now.replace(day=28) + timedelta(days=4)).month
        )
    ]

    for year, month in months:
        try:
            rows = download_csv(year, month)
            print("取得行数:", len(rows))

            for row in rows:
                date = row.get("date", "")
                race_id = row.get("race_id", "")
                name = row.get("player_name", "")

                if not date or not race_id or not name:
                    continue

                # 当日以降の出走表のみ対象
                if date < now.strftime("%Y-%m-%d"):
                    continue

                key = race_id

                if key not in races:
                    races[key] = {
                        "race_id": race_id,
                        "date": date,
                        "venue": row.get("venue_slug", ""),
                        "race_no": row.get("race_no", ""),
                        "players": []
                    }

                races[key]["players"].append({
                    "number": row.get("banum", ""),
                    "name": name,
                    "score": row.get("race_score", ""),
                    "class": row.get("player_class", ""),
                    "style": row.get("running_style", ""),
                    "line": row.get("lineup", ""),
                    "pref": row.get("pref", "")
                })

        except Exception as e:
            errors.append(str(e))
            print("取得エラー:", e)

    # 取得できたデータのみ保存
    if not races:
        print("出走表を取得できませんでした")
        print("取得先の更新状況を確認してください")
        raise RuntimeError("有効な出走表が0件です")

    data = {
        "updated_at": now.isoformat(),
        "source": "Kenseimk/keirin-data",
        "races": list(races.values()),
        "predictions": [],
        "results": [],
        "errors": errors
    }

    OUTPUT.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("取得レース数:", len(races))
    print("データ保存成功")


if __name__ == "__main__":
    main()
