import os, tempfile, zipfile, shutil, uuid, subprocess, mimetypes
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from converters import convert_to_pdf


TMP_ROOT = "/tmp/pdfmvp"
os.makedirs(TMP_ROOT, exist_ok=True)
app = FastAPI()


class EmailReq(BaseModel):
token: str
to: str


@app.post("/api/convert")
async def convert(files: list[UploadFile] = File(...), mode: str = Query("download")):
batch = os.path.join(TMP_ROOT, str(uuid.uuid4()))
os.makedirs(batch, exist_ok=True)
out_dir = os.path.join(batch, "out"); os.makedirs(out_dir, exist_ok=True)


pdf_paths = []
for f in files[:20]:
if f.size and f.size > 50*1024*1024: # 50MB guard
shutil.rmtree(batch, ignore_errors=True)
return JSONResponse({"error":"File too large"}, status_code=413)
# save upload
in_path = os.path.join(batch, f.filename)
with open(in_path, 'wb') as w: w.write(await f.read())
pdf_path = await convert_to_pdf(in_path, out_dir)
if not pdf_path:
shutil.rmtree(batch, ignore_errors=True)
return JSONResponse({"error": f"Failed for {f.filename}"}, status_code=400)
pdf_paths.append(pdf_path)


if mode == 'download':
# If single file, return it directly; otherwise zip
if len(pdf_paths) == 1:
return FileResponse(pdf_paths[0], filename=os.path.basename(pdf_paths[0]))
zip_path = os.path.join(batch, "converted.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
for p in pdf_paths: z.write(p, arcname=os.path.basename(p))
return FileResponse(zip_path, filename="converted.zip", headers={"X-Filename":"converted.zip"})


# email mode — return a token to reference this bundle shortly
token = os.path.basename(batch)
# zip now; /api/email will read & send, then cleanup
zip_path = os.path.join(batch, "converted.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
for p in pdf_paths: z.write(p, arcname=os.path.basename(p))
return JSONResponse({"token": token})


@app.post("/api/email")
async def email(req: EmailReq):
import smtplib
from email.message import EmailMessage


batch = os.path.join(TMP_ROOT, req.token)
zip_path = os.path.join(batch, "converted.zip")
if not os.path.exists(zip_path):
return {"ok": True}
