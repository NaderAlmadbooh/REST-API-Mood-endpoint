import requests
import mood #to avoid crashing due to unforseen use of definitions/objects

linkAddress = "http://127.0.0.1:5000/"
#Dummy data for demostration
moodEntries = [{"rating":5, "user_id":12, "date":12052005, "streak":5}, 
        {"rating":3, "user_id":13, "date":12052005, "streak":2},
        {"rating":0, "user_id":14, "date":12052005, "streak":4},
        {"rating":1, "user_id":15, "date":11052005, "streak":0}]
#testing put method
for i in range(len(moodEntries)):
    response = requests.put(linkAddress + "Mood/" + str(i), moodEntries[i])
    print(response.json())

#pause 
input()

# Testing get method
response = requests.get(linkAddress + "/Mood/2")
print(response.json())
# get method error handling
response = requests.get(linkAddress + "/Mood/20")
print(response.json())