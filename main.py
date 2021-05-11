import csv
from tempfile import mkstemp
import fastapi
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app: FastAPI = FastAPI()


def error(msg):
    """returning an error message in HTMLResponse"""
    cont = f"""
    <h2>ERROR</h2><hr>{msg}<hr>
    Input codepage: SHIFT_JIS; The good structure is something like this: <br>
    <pre>
    "ÝĐÔ","m","Žłş","óąłş","śk","wN","śNú","ęčú","čú","ŞĚ","JĂń","","Ć","óąÔ","iÔ","ćZ","Z","ŠćZ","`[Z"
    "		9999999999","AkademiaSorobanu","AkademiaSorobanu","AkademiaSorobanu","XXX Blanka","-2","2012/03/23","2021/03/28","2021/03/28","ş21-3","454","9","","1","1339","100","0","90","0"
    "		9999999999","AkademiaSorobanu","AkademiaSorobanu","AkademiaSorobanu","XXX Wiktoria","-2","2012/02/14","2021/03/28","2021/03/28","ş21-3","454","9","","2","1340","100","0","80","0"
    </pre>
    """
    return fastapi.responses.HTMLResponse(cont)


@app.post("/file/")
def create_file(file: UploadFile = File(...), quotes=False):
    """Func for replace..."""
    name = file.filename
    # input as a bytes, so we need to decode it with japanese codepage
    try:
        data_str = file.file.read().decode("SHIFT_JIS")
    except:
        return error(f"{name} - bad codepage or no file ....")
    # next we split to list
    data = data_str.split("\n")
    # and cut first line
    if len(data) < 2:
        return error(f"{name} - too little lines ;-)")

    data_out = data[1:]
    temp_0 = [line.strip().split(",") for line in data_out]

    fields = len(temp_0[0])
    print(f"Ilość pól w {name} / {type(temp_0[0])}: {fields}")
    print("test linii",temp_0[0])
    if not temp_0:
        return error(f"Some strange error with converting to list")

    if fields == 18:
        pass
    else:
        return error(f"Incorrect number of fields: {fields} - should be 18.")

    temp_1 = []
    for line in temp_0:
        new_line = [
            elem.strip().replace("\\", "").replace("\t", "").replace('"', "")
            for elem in line
        ]

        # now we change in dates temp[6,7,8] first '/' to '年' and second '/' to '月'
        for idx in [6, 7, 8]:
            if "/" in new_line[idx]:
                new_line[idx] = new_line[idx].replace("/", "年", 1)  # first occurrence
                new_line[idx] = new_line[idx].replace("/", "月", 1)  # second occurrence
        temp_1.append(new_line.copy())

    fpcsv = mkstemp()[1] + ".csv"
    print(fpcsv)
    with open(fpcsv, "w", newline="") as csvfile:
        outwriter = csv.writer(csvfile, delimiter=",")
        outwriter.writerows(temp_1)

    return FileResponse(fpcsv)


@app.get("/")
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
