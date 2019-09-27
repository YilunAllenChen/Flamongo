# Installation and Adding Dependencies
1. Install [MongoDB](https://www.baidu.com/link?url=9QjmcC7pACCkFg7-kkowZnJY1gQ1SKZqwgfj2zoBe4WdPPoB-P7uXQlmZ4X1o9uv&wd=&eqid=fc9cfab80019786b000000035d64ba35).
2. Create a database called mydb if it doesn't exist already.
3. under mydb, create a collection called VWMockServerDB.
4. Make sure that MongoDB runs on port 27017.

4. Adding Python Dependencies:
```bash
    pip install flask pyMongo flask_pymongo
```

# Running Server
Under the repo, do:
```bash
    python app.py
```

The server by default runs on  (localhost). You can change the setting by locating this code segment in app.py:
```Python
if __name__ == '__main__':
    app.run(host='192.168.1.1', port=5000, debug=True)
```

# Data Formatting Example:
## Using POST request to upload/update a scenario
URL:
```bash
/simulator/editor/  # Upload/update scenario data
```
Send a POST request to the url above that looks like this:
```json 
{
    "_id": 2,
    "name": "faketown2",
    "des": "faketown is a fake town.",
    "longitude": 304.10,
    "latitude": 103.20,
    "date": 20190342,
    "mockDate": 20190401,
    "carNum": "AL9290",
    "vehicleNum": "ABH213",
    "hisViolationCount": 0,
    "newViolationCount": 1,
    "mockWeather": "Cloudy",
    "mockTimeSlot": "NA",
    "mockTrafficRes": "None specified.",
    "mockHoliday": "Wow. No holiday."
}
```
If the scenario data with the given ID already exists in the database, it will be overwritten by the newly uploaded data. 

You should get a response that looks like:
```json
{
    "message": "success",
    "payload": {
        "_id": 2,
        "carNum": "AL9290",
        "date": 20190342,
        "des": "faketown is a fake town.",
        "hisViolationCount": 0,
        "latitude": 103.2,
        "longitude": 304.1,
        "mockDate": 20190401,
        "mockHoliday": "Wow. No holiday.",
        "mockTimeSlot": "NA",
        "mockTrafficRes": "None specified.",
        "mockWeather": "Cloudy",
        "name": "faketown2",
        "newViolationCount": 1,
        "vehicleNum": "ABH213"
    },
    "status": 1
}
```

## Using POST request to delete scenario
URL:
```bash
192.168.1.118:5000/simulator/delete # Delete scenario
```
Send a POST request to the url above that looks like this:
```json
{
	"ID": "131"
}
```

You should get a response that looks like:


```json
{
  "status": 1,
  "message": "target scenario deleted successfully."
}
```
OR:

```json
{
  "status": -1,
  "message": "No scenario found with the specified ID."
}
```

## Using POST request to select scenario
URL:
```bash
/simulator/selectscenario # Select scenario
```
Send a POST request to the url above that looks like this:
```json
{
	"id": "1567049415392"
}
```
The response will have the scenario data you just selected under its 'payload'.

You should get a response that looks like:
```json
{
    "status": 1,
    "message": "success",
    "payload": {
        "_id": {
            "$oid": "5d6747ee51daaa7898a7bd5f"
        },
        "date": "0",
        "mockTimeSlot": "",
        "mockTrafficRes": ".....",
        "newViolationCount": "0",
        "latitude": "0.0",
        "des": "额度",
        "mockHoliday": ".......",
        "name": "计算机",
        "id": "1567049415392",
        "hisViolationCount": "0",
        "mockWeather": "......",
        "longitude": "0.0",
        "mockDate": "0"
    }
}
```
Now that scenario ID is "1567049415392". When you try to get data from the server, it will automatically fetch data from the scenario with id 100.

## Using GET request to acquire all scenario data uploaded
URLs:
```bash
/simulator/getall #obtain all scenario data.
```

You should get a response that looks like:
```json
{
    "message": "success",
    "payload": [
        {
            "_id": 1,
            "carNum": "AL9290",
            "date": 20190342,
            "des": "faketown is a fake town.",
            "hisViolationCount": 0,
            "latitude": 103.2,
            "longitude": 304.1,
            "mockDate": 20190401,
            "mockHoliday": "Wow. No holiday.",
            "mockTimeSlot": "NA",
            "mockTrafficRes": "None specified.",
            "mockWeather": "Sunny",
            "name": "faketown",
            "newViolationCount": 1,
            "vehicleNum": "ABH213"
        },
        {
            "_id": 2,
            "carNum": "AL9290",
            "date": 20190342,
            "des": "faketown is a fake town.",
            "hisViolationCount": 0,
            "latitude": 103.2,
            "longitude": 304.1,
            "mockDate": 20190401,
            "mockHoliday": "Wow. No holiday.",
            "mockTimeSlot": "NA",
            "mockTrafficRes": "None specified.",
            "mockWeather": "Cloudy",
            "name": "faketown2",
            "newViolationCount": 1,
            "vehicleNum": "ABH213"
        }
    ],
    "status": 1
}
```
Note that all scenario data are in json form, put into a list and contained in the "payload" part of the response.

## Using GET request to obtain certain data
URLs:
```bash
/dev-onlineservice-weather/weather/qWeatherByLatLng?provider=103020&dataType=JSON    
# Weather

/v1/cms/festival/attribute?provider=103020&dataType=JSON    
# Holiday

/violation-web/1.0/violation/query?provider=103020&dataType=JSON 
# Violation

/getTimeSlot?provider=103020&dataType=JSON   
# Timeslots
```
OR:
```bash
/getData/mockWeather?provider=103020&dataType=JSON    
# Weather

/getData/mockHoliday?provider=103020&dataType=JSON    
# Holiday

/getData/mockTrafficRes?provider=103020&dataType=JSON
# Violation

/getData/mockTimeSlot?provider=103020&dataType=JSON
# Timeslots
```
You should get a response that looks like (Using weather as an example):
```json
{
    "temperature": 10,
    "weather": "Sunny"
}
```