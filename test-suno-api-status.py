import requests as req

headers = {
    "Authorization": "Bearer e1781944abd4eb6feb404b8760cf84b1"
}


resp= req.get("https://api.sunoapi.org/api/v1/generate/record-info?taskId=88241affcfb5702b5504969a3460e212",headers=headers)
print(resp.json())