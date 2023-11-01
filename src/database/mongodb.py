from http.client import HTTPException
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pymongo

from src.config.config import Config, load_config

config: Config = load_config()


async def aggregate_salary_data(dt_from, dt_upto, group_type):
    dt_from = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    dt_upto = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")

    # Временные метки по всему заданному диапазону
    current_label = dt_from
    all_labels = []
    while current_label <= dt_upto:
        all_labels.append(current_label)
        if group_type == "hour":
            current_label += timedelta(hours=1)
        elif group_type == "day":
            current_label += timedelta(days=1)
        elif group_type == "month":
            current_label += relativedelta(months=1)

    # Конвертация формата времени
    formatted_labels = [label.strftime("%Y-%m-%dT%H:%M:%S") for label in all_labels]

    try:
        client = pymongo.MongoClient(config.db.url)
        db = client[config.db.db_name]
        collection = db[config.db.db_collection]

        pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": dt_from,
                        "$lte": dt_upto
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": {
                                "hour": "%Y-%m-%dT%H:00:00",
                                "day": "%Y-%m-%dT00:00:00",
                                "month": "%Y-%m-01T00:00:00"
                            }[group_type],
                            "date": "$dt"
                        }
                    },
                    "total_salary": {"$sum": "$value"}
                }
            },
            {
                "$project": {
                    "label": "$_id",
                    "value": "$total_salary"
                }
            },
            {
                "$sort": {
                    "label": 1
                }
            }
        ]

        result = list(collection.aggregate(pipeline))
    except Exception as e:
        raise HTTPException(f"Внутренняя ошибка сервера: {str(e)}")

    # Добавляем 0, если нет результата за какой-то период
    aggregation_data = {data["label"]: data.get("value") for data in result}
    dataset = [aggregation_data.get(label, 0) for label in formatted_labels]

    return {"dataset": dataset, "labels": formatted_labels}
