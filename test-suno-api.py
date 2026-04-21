import requests as req

headers = {
    "Authorization": "Bearer e1781944abd4eb6feb404b8760cf84b1",
    "Content-Type": "application/json"
}

body = {
    "customMode": True,
    "instrumental": True,
    "model": "V4_5ALL",
    "callBackUrl": "https://api.example.com/callback",
    "prompt": "mood=happy  occasion=birthhday  optional_story=age20",
    "style": "pop",
    "title": "happy birthday john",
    "vocalGender": "male"
    
    
}

resp = req.post("https://api.sunoapi.org/api/v1/generate", json=body, headers=headers)
print(resp.json())