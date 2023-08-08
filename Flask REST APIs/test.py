import requests

BASE = "http://127.0.0.1:5000/" #Server our APL is running on

#Array of video data
data = [
    {"likes": 10, "name": "MST Visualizer", "views": 100},
    {"likes": 15, "name": "Path Finder Visualizer", "views": 1000},
    {"likes": 20, "name": "Sorting Visualizer", "views": 500},
]

#Let's do a bunch of put requests
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json()) #Print our response in JSON so it doesn't look a response object

input() #Putting this for a temporary pause so I can press enter

#Testing get request
response = requests.get(BASE + "video/2")
print(response.json())

#Testing delete request
response = requests.delete(BASE + "video/2")
print(response)