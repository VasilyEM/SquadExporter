# -----------------------------------------------------------
# Экспортёр данных по участникам команд Fanat1k.ru из squadeasy
#
# (C) 2021 Mardanov Vasily
# email vmardanov@gmail.com
# -----------------------------------------------------------

print("Start exporting!")

# импортим необходимые либы
import json
import requests


#функция парсинга json данных по участникам команды + запись в файл
def getUserDataRAW(userJson):
    x=0
    for x in range(len(userJson["members"])):
        #у пользователя Артём отсутствует в параметрах json поле last_name, потому добавлена обработка
        if 'last_name' in userJson["members"][x]:
            try: fileOut=userJson['members'][x]['first_name']+' '+ userJson["members"][x]["last_name"]+";"+str(userJson["members"][x]["statistics"]["total_points_this_week"]/100)+";"+str(userJson["members"][x]["statistics"]["total_distance_league"]/1000)
            except KeyError: pass
        else:   
            try: fileOut=userJson['members'][x]['first_name']+";"+str(userJson["members"][x]["statistics"]["total_points_this_week"]/100)+";"+str(userJson["members"][x]["statistics"]["total_distance_league"]/1000)
            except KeyError: pass
        fileOutReplace= str(fileOut).replace (".", ",")   #замена точек на запятые для корректного открытия в экселе
        fileOutput.write(str(fileOutReplace)+ '\n')


#функция получения json данных по участникам команды. Оборачивается в цикл на этапе перебора id команд
def getUserData(teamIdFunc,authTokenFunc):
    urlAthlete = 'https://api.squadeasy.com/api/v3/squad/squad/withmembers/'
    teamIdFunc=teamIdFunc.rstrip("\n") #отрезаем символ конца строки
    headersAthlete = {'content-type': 'application/json', 'Authorization': 'JWT '+authTokenFunc,'web-api-key': '8C4VfqUwTyn0wx2838HWSXQ1WqZO8R2S', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br'}
    dataAthlete = {"squad_id":teamIdFunc}
    responseAthlete = requests.post(urlAthlete,  data=json.dumps(dataAthlete), headers=headersAthlete)
    responseAthleteData = responseAthlete.json()
    getUserDataRAW(responseAthleteData)


# точка входа, сперва получаем токен авторизации, далее для каждой команды получаем данные по спортсменам
# id команд хранятся в файле конфига

# загрузка файла авторизационных данных
fileLogin = open("loginID.txt", "r")
emailLogin = fileLogin.readline().rstrip("\n")
passwordLogin = fileLogin.readline().rstrip("\n")

# логин в системе, получение авторизационного токена
url = 'https://api.squadeasy.com/api/v3/auth/login/'
headers = {'content-type': 'application/json'}
params = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br'}
data = {"email":emailLogin,"password":passwordLogin,"device_id":"ZdG6F/nKri9EWfBt0PQyPBk7Wen1DSpdzr8TTN6eG5d2xK/q4oSx/8SVbRUUAQFA"}
#print ("data = ",data)
response = requests.post(url, params=params, data=json.dumps(data), headers=headers)
responseData = response.json()

#файл для записи итогов
fileOutput = open("out.csv", "w")
fileOutput.write("Name;Score;Distance" '\n')

# загрузка файла с id участников
file = open("teamID.txt", "r")
for teamId in file:
    getUserData (teamId,responseData["token"])


fileOutput.close() 
file.close() 
print("export successful!")
