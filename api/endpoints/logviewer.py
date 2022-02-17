from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from os import path


router = APIRouter()


@router.get("/")
async def get_logs():
    if path.exists("././gps_reports.log"):
        infile = "././gps_reports.log"
        return FileResponse(path=infile, filename="YourLogsSir.log", status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="logs file does not exist")


@router.get("/html", response_class=HTMLResponse)
async def read_items():

    if path.exists("././gps_reports.log"):
        infile = "././gps_reports.log"

        text = r"""
            <html>
            <head>
                <style>
                    .symbol {
                        font-size: 0.9em;
                        font-family: Times New Roman;
                        border-radius: 1em;
                        padding: .1em .6em .1em .6em;
                        font-weight: bolder;
                        color: white;
                        background-color: #4E5A56;
                    }

                    .icon-info { background-color: #3229CF; }
                    .icon-error { background: #e64943; font-family: Consolas; }
                    .icon-tick { background: #13c823; }
                    .icon-excl { background: #ffd54b; color: black; }

                    .icon-info:before { content: 'i'; }
                    .icon-error:before { content: 'x'; }
                    .icon-tick:before { content: '\002713'; }
                    .icon-excl:before { content: '!'; }
                    .notify {
                        background-color:#e3f7fc; 
                        color:#555; 
                        border:.1em solid;
                        border-color: #8ed9f6;
                        border-radius:10px;
                        font-family:Tahoma,Geneva,Arial,sans-serif;
                        font-size:1.1em;
                        padding:10px 10px 10px 10px;
                        margin:10px;
                        cursor: default;
                    }

                    .notify-yellow { background: #fff8c4; border-color: #f7deae; }
                    .notify-red { background: #ffecec; border-color: #fad9d7; }
                    .notify-green { background: #e9ffd9; border-color: #D1FAB6; }
                </style>
                <title>GPS-Reports LOGS</title>
            </head>
            <body style='margin:100px'>
                <a href="#bottom">Go To Bottom</a>
                <h1 style='text-align: center; font-family:Tahoma,Geneva,Arial,sans-serif; color:#'>Log Viewer - GPS reporting</h1>
            """

        with open(infile) as f:
            for line in f:
                if "ERROR" in line:
                    tag = f"<div class='notify notify-red'><span class='symbol icon-error'></span> {line} </div>"
                elif "INFO" in line:
                    tag = f"<div class='notify'><span class='symbol icon-info'></span> {line} </div>"
                elif "WARNING" in line:
                    tag = f"<div class='notify notify-yellow'><span class='symbol icon-excl'></span> {line} </div>"
                elif "CRITICAL" in line:
                    tag = f"<div class='notify notify-red'><span class='symbol icon-error'></span> {line} </div>"
                text = text + tag

        html_content = text + "<div id='bottom'></div></body></html>"

        return HTMLResponse(content=html_content, status_code=200)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="logs file does not exist")