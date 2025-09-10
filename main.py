from flask import *
import time,csv,datetime

app = Flask(__name__)

lastestFileName = ""
rankingData = {"lastUpdate" : datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
               "data" : []}

@app.route("/upload", methods=['GET', 'POST'])
def UploadCsvDataPage():
    global lastestFileName

    if request.method=="GET":
        return render_template("uploadPage.htm")
    else:
        f = request.files["file"]
        if f.content_type!="text/csv":
            return "ファイル形式が違います✖"

        lastestFileName = "temp/"+f.filename
        f.save(lastestFileName)
        updateDataDict()
        return "<p>OK 200</p>"

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

if __name__=="__main__":
    app.run(debug=False,port=10000)