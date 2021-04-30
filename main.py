import fastapi
import uvicorn
import csv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from tempfile import mkstemp

app: FastAPI = FastAPI()


@app.post("/file/")
def create_file(file: UploadFile = File(...), quotes=False):
    """Func for replace..."""
    name = file.filename
    # input as a bytes, so we need to decode it with japanese codepage
    data_str = file.file.read().decode("SHIFT_JIS")
    # next we split to list
    data = data_str.split("\n")
    # and cut first line
    data_out = data[1:]
    temp_0 = []
    for line in data_out:
        l = line.strip().split(",")
        temp_0.append(l)

    temp_1 = []
    for line in temp_0:
        l = []
        for elem in line:
            l.append(elem.strip().replace("\\", "").replace("\t", "").replace('"', ""))
        # now we change in dates temp[6,7,8] first '/' to '年' and second '/' to '月'
        for idx in [6, 7, 8]:
            if "/" in l[idx]:
                l[idx] = l[idx].replace("/", "年", 1)  # first occurrence
                l[idx] = l[idx].replace("/", "月", 1)  # second occurrence
        temp_1.append(l.copy())

    fpcsv = mkstemp()[1] + ".csv"
    print(fpcsv)
    with open(fpcsv, "w", newline='') as csvfile:
        outwriter = csv.writer(csvfile, delimiter=',')
        outwriter.writerows(temp_1)

    return FileResponse(fpcsv)


    # return {
    #     "Nazwa pliku": file.filename,
    #     "Dane wejściowe str": data_str,
    #     "Dane wejściowe": data,
    #     "Dane wyjściowe": data_out,
    # }


@app.get('/')
def index():
    """Index homepage to get file."""
    cont = """
    This is Page for getting CSV file for <a href="https://akademiasorobanu.pl"> Akademia Sorobanu</a> <hr/>
    <form action="/file/" enctype="multipart/form-data" method="post">
    <label for="file"> Wybierz plik CSV </label>
    <input name="file" type="file">
    <!---
    <br/>
    <input type="checkbox" id="quotes" name="quotes" checked>
    <label for="quotes"> CSV ze znakami cudzysłowu </label>
    <br/> --->
    <input type="submit" value="Wyślij plik i zmień dane">
    </form>
    
    """
    return fastapi.responses.HTMLResponse(cont)


if __name__ == "__main__":
    uvicorn.run(app)
