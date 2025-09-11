from flask import *
import time,csv,datetime

app = Flask(__name__)

lastestFileName = ""
rankingData = {"lastUpdate" : datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
               "data" : []}
with open("password.txt") as f:
    PASSWORD = f.read()

@app.route("/upload", methods=['GET', 'POST'])
def UploadCsvDataPage():
    global lastestFileName

    if request.method=="GET":
        return render_template("uploadPage.htm")
    else:
        if request.form["pass"] != PASSWORD:
            return 'パスワードが違います✖<br><a href="/upload">戻る</a>'
        f = request.files["file"]
        if f.content_type!="text/csv":
            return  'ファイル形式が違います✖<br><a href="/upload">戻る</a>'

        lastestFileName = "temp/"+f.filename
        f.save(lastestFileName)
        updateDataDict()
        return "<h1>アップロードに成功しました</h1><b><p>このページを閉じてください</p>"

def updateDataDict():
    global rankingData

    with open(lastestFileName , mode="r", encoding="utf-8") as f:
        rawCsvData = csv.reader(f)

        __rankingData = []
        isFirst = True
        for i in rawCsvData:
            if isFirst:
                isFirst = False
                continue

            __rankingData.append({"name" : i[2],
                                  "point" : str(int((float(i[3]) + int(i[5]) * 5)*10)/10),
                                  "battleAmount" : i[5]})
    ## sort
    rankingData_ = []
    while len(__rankingData) != 0:
        index = 0
        maxPoint = -10**10
        maxIndex = 0
        for i in __rankingData:
            if float(i["point"]) > maxPoint:
                maxIndex = index
                maxPoint = float(i["point"])
            
            index += 1
        
        rankingData_.append(__rankingData[maxIndex])
        del __rankingData[maxIndex]
    
    rankingData = {"lastUpdate" : datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
                   "data" : rankingData_}



@app.route("/download")
def DataDownload():
    return jsonify(rankingData)

@app.route("/web_viewer")
def webViewer():
    index = 0
    result = ""
    result += "<title>ChampionLeague ランキング</title>\n"
    result += f'<p>Update : {rankingData["lastUpdate"]}</p>\n'
    result += "<table>\n"
    result += "<tr><th>Rank</th><th>PlayerName</th><th>Points</th><th>G</th></tr>\n"
    for i in rankingData["data"]:
        index += 1
        result += f'<tr><td>{index}</td><td>{i["name"]}</td><td>{i["point"]}</td><td>{i["battleAmount"]}</td></tr>\n'
    result += "</table>"

    return result

if __name__=="__main__":
    app.run(debug=False,port=10000)