from pypdf import PdfReader, PdfWriter
from pathlib import Path

def full_name(o):
    parts, p = [], o
    while p is not None:
        if "/T" in p:
            parts.append(str(p["/T"]))
        p = p.get("/Parent")
        p = p.get_object() if p else None
    return ".".join(reversed(parts))

class Form:
    def __init__(self, path):
        self.w = PdfWriter()
        self.w.append(PdfReader(path))
        self.widgets = {}
        n = 0
        for page in self.w.pages:
            ws = [a.get_object() for a in page.get("/Annots", [])
                  if a.get_object().get("/Subtype") == "/Widget"]
            ws.sort(key=lambda o: (-float(o["/Rect"][3]), float(o["/Rect"][0])))
            for o in ws:
                n += 1
                self.widgets[n] = o

    def put(self, n, value):
        o = self.widgets[n]
        if isinstance(value, bool):  # checkbox: True/False
            on = next(k for k in o["/AP"]["/N"].keys() if k != "/Off")
            value = on if value else "/Off"
        self.w.update_page_form_field_values(None, {full_name(o): str(value)})

    def save(self, path):
        self.w.set_need_appearances_writer(True)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.w.write(path)