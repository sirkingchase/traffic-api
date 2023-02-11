import urllib.request
import json
import base64
from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image
import io
import base64
from io import BytesIO
from fastapi.responses import FileResponse

app = FastAPI()

cams=urllib.request.urlopen('https://its.txdot.gov/its/DistrictIts/GetCctvStatusListByDistrict?districtCode=AUS').read();
jCams = json.loads(cams);

#for key in jCams["roadwayCctvStatuses"].keys():
#  print(key);

j35 = jCams["roadwayCctvStatuses"]["IH35"];

c = [s for s in j35 if float(s['lonString']) > -198.195 and s["statusDescription"] == "Device Online"];

cu = [];

for name in c:
  cu.append((name['icd_Id']).replace(' ','%20'));
  print(name['icd_Id']);

@app.get("/35")
def hello():
  cct = "IH 35 at FM 306 (MM 191)";
  base_url = 'https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=';
  last_res = '&districtCode=AUS';
  print (base_url + cct.replace(' ','%20') + last_res);

  contents = urllib.request.urlopen(base_url + cct.replace(' ','%20') + last_res).read();
  jcon = json.loads(contents);
  pic = jcon["snippet"];
  imgdata = base64.b64decode(pic);
  return Response(content=imgdata, media_type="image/png");

@app.get("/list")
def comb():

  base64_images = [];
  image_files = [];

  for n in cu:
    base_url = 'https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=';
    last_res = '&districtCode=AUS';
    print (base_url + n + last_res);
    contents = urllib.request.urlopen(base_url + n + last_res).read();
    jcon = json.loads(contents);
    try:
      pic = jcon["snippet"];
      base64_images.append(pic);
    except Exception:
        pass  # or you could use 'continue'


  for base64_string in base64_images:
      buffer = io.BytesIO(base64.b64decode(base64_string))
      try:
        image_file = Image.open(buffer)
        image_files.append(image_file)
      except Exception:
        pass  # or you could use 'continue'

# Save image to BytesIO
  combined_image = image_files[0].save( 
      'output.tiff', 
      save_all=True, 
      append_images=image_files[1:]
      )

  return FileResponse("output.tiff")



@app.get("/combined")
def comb():

  cct = "IH 35 at FM 306 (MM 191)";
  base_url = 'https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=';
  last_res = '&districtCode=AUS';
  print (base_url + cct.replace(' ','%20') + last_res);

  contents = urllib.request.urlopen(base_url + cct.replace(' ','%20') + last_res).read();
  jcon = json.loads(contents);
  pic1 = jcon["snippet"];

  contents = urllib.request.urlopen('https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=IH%2035%20at%20LP%20337%20(MM%20185)&districtCode=AUS').read();
  jcon = json.loads(contents);
  pic2 = jcon["snippet"];

  base64_images = [pic1, pic2]
  image_files = [];

  for base64_string in base64_images:
      buffer = io.BytesIO(base64.b64decode(base64_string))
      image_file = Image.open(buffer)
      image_files.append(image_file)

# Save image to BytesIO
  combined_image = image_files[0].save( 
      'output.tiff', 
      save_all=True, 
      append_images=image_files[1:]
      )

  return FileResponse("output.tiff")

@app.get("/")
def hello():
  contents = urllib.request.urlopen('https://its.txdot.gov/its/DistrictIts/GetCctvSnapshotByIcdId?icdId=IH%2035%20at%20LP%20337%20(MM%20185)&districtCode=AUS').read();
  jcon = json.loads(contents);
  pic = jcon["snippet"];
  imgdata = base64.b64decode(pic);
  return Response(content=imgdata, media_type="image/png");
