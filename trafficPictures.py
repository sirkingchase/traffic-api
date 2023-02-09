import urllib.request
import json
import base64
from fastapi import FastAPI
from fastapi.responses import Response
app = FastAPI()

@app.get("/")
def hello():
  contents = urllib.request.urlopen('https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=IH%2035%20at%20LP%20337%20(MM%20185)&districtCode=SAT').read();
  jcon = json.loads(contents);
  pic = jcon["snippet"];
  imgdata = base64.b64decode(pic);
  return Response(content=imgdata, media_type="image/png");
