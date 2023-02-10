import urllib.request
import json
import base64
from fastapi import FastAPI
from fastapi.responses import Response
app = FastAPI()

cams=urllib.request.urlopen('https://its.txdot.gov/its/DistrictIts/GetCctvStatusListByDistrict?districtCode=SAT').read();
jCams = json.loads(cams);

#for key in jCams["roadwayCctvStatuses"].keys():
#  print(key);

j35 = jCams["roadwayCctvStatuses"]["IH35"];

c = [s for s in j35 if float(s['lonString']) > -98.195];

cu = [];

for name in c:
  cu.append((name['icd_Id']).replace(' ','%20'));
  print(name['icd_Id']);

@app.get("/35")
def hello():
  cct = "IH 35 at E Watson Ln (MM 194)";
  base_url = 'https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=';
  last_res = '&districtCode=SAT';
  print (base_url + cct.replace(' ','%20') + last_res);

  contents = urllib.request.urlopen(base_url + cct.replace(' ','%20') + last_res).read();
  jcon = json.loads(contents);
  pic = jcon["snippet"];
  imgdata = base64.b64decode(pic);
  return Response(content=imgdata, media_type="image/png");


@app.get("/")
def hello():
  contents = urllib.request.urlopen('https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=IH%2035%20at%20LP%20337%20(MM%20185)&districtCode=SAT').read();
  jcon = json.loads(contents);
  pic = jcon["snippet"];
  imgdata = base64.b64decode(pic);
  return Response(content=imgdata, media_type="image/png");
