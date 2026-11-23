# The document build (step by step)

The construction manual for the training document itself. Word (`.docx` via python-docx) is the default output; the structure below holds for Markdown and for a shareable page too, only the rendering changes.

Write the generator to a file and run it. Do not paste a long script into a shell command: it fails to spawn.

## 1. The shape of the document

Fixed order, every time. The reader should never have to jump backwards.

1. **Cover block.** Title, one-line subtitle, and a metadata table: who it is for, the source meeting with date and duration, who presented, who else was there, the recording link, and a one-line scope statement saying the document contains only what the recording contained.
2. **How to use this document.** Four or five bullets: it is chronological, each module has a timestamp, what the "where to look" lines are, and any recording artefact to ignore (the self-view overlay).
3. **A sources note.** One highlighted box explaining that plain text is what the presenter said and "On screen:" is what was visible but unspoken. This single box is what lets a reader trust the rest.
4. **Glossary.** Every term the presenter used, in their sense, in plain language. Two columns. Written for someone who has never seen the product.
5. **The navigation map**, when the recording shows one. A table of the areas of the product, what each holds, and the URL each sits at. This is often the single most useful page in the document and it is free: the address bar is in every screenshot.
6. **Plan at a glance.** Module number, topic, timestamp range. One row per module.
7. **The modules**, in the presenter's order, numbered from zero.
8. **Action items** the user personally agreed to, with timestamps.
9. **Left open.** Raised, never resolved.
10. **Appendix**, only if a reference table is genuinely too long to sit inline.

## 2. The module template

Every module is built from the same parts, and only the parts it needs:

```
Heading:      Module N - <what the presenter was doing>
Stamp line:   <one-line description of the moment>  |  Recording MM:SS - MM:SS
Explanation:  plain-language prose, layman register
Steps:        numbered list, performance order, real button and field names
Screenshot:   image, centred
Caption:      "Presenter's screen at MM:SS - <what this shows>"
Locator:      "Where to look: <where on this screen the control sits>"
On screen:    what the frame showed that was never said out loud
Q&A block:    the attendee's question and the answer, shaded, only where one was asked
Note box:     a caveat the presenter flagged, or a correction
```

Three rules on the parts:

- **The stamp line is not optional.** It is what makes the document checkable against the source.
- **The locator always follows the screenshot.** A screenshot with no locator makes the reader hunt, which is the exact problem this document exists to solve.
- **Q&A blocks sit at the point in the walkthrough where they were asked**, never collected into a section at the end. They were prompted by what was on screen at that moment, and they only make sense there.

## 3. Writing the locator line

This is the skill's core deliverable and it is worth doing carefully. A locator describes position in terms a reader can act on before they know the product:

- Anchor to the frame: top left, top right, under the page title, at the far right of each row, at the foot of the form.
- Anchor to a neighbour: "after the View action", "the third item in the menu", "beside the search box".
- Name what the control looks like: the blue button, the three dots, the chip with the cross on it.
- Say what it does in the same sentence when it is not obvious from the label.

> Where to look: the three dots sit at the far right of each list row, after the View and Automations actions. "Clone list" is the third item in the menu.

> Where to look: four fields run across the top of the form, Segment Name and Type on the left, Tag Name and Description on the right. Below them, "Segment Criteria" with the "+ Add filter" button, which is where every filter gets added.

Avoid pixel coordinates, avoid "as you can see", and avoid describing the cursor position at that instant. The reader's window will not match the presenter's.

## 4. The helper set (python-docx)

Build these once at the top of the generator and the rest of the script becomes declarative.

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

MAXW = 6.3  # inches: page width less 1in margins each side

def shade(cell, fill):                      # table cell background
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill); tcPr.append(shd)

def _norm(parts):                           # accept ("text", bold) pairs or bare strings
    out = []
    for pt in parts:
        if not pt: continue
        out.append((pt, False) if isinstance(pt, str) else (pt[0], bool(pt[1])))
    return out

def stamp(doc, label, ts):                  # the timestamp line under a module heading
    para = doc.add_paragraph(); r = para.add_run(f"{label}  |  Recording {ts}")
    r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x70,0x70,0x70)

def qa(doc, question, answer):              # the attendee's question, shaded
    t = doc.add_table(rows=2, cols=1); t.style = "Table Grid"
    for cell, fill, lbl, txt in ((t.rows[0].cells[0], "EAF1F8", "Your question: ", question),
                                 (t.rows[1].cells[0], "F7F7F7", "Their answer: ",  answer)):
        shade(cell, fill)
        cell.paragraphs[0].add_run(lbl).bold = True
        cell.paragraphs[0].add_run(txt)

def screen(doc, path, caption, look=None, ts=None, width=MAXW):
    para = doc.add_paragraph(); para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run().add_picture(path, width=Inches(min(width, MAXW)))
    cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f"Presenter's screen{f' at {ts}' if ts else ''} - {caption}")
    r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x60,0x60,0x60)
    if look:
        lk = doc.add_paragraph()
        a = lk.add_run("Where to look: "); a.bold = True; a.font.size = Pt(10)
        lk.add_run(look).font.size = Pt(10)
```

Set the base style once (Calibri 11, headings in a dark blue), set margins to one inch, and set the East Asian font name alongside the Latin one or Word substitutes a fallback:

```python
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
```

## 5. Images in the document

- Size to the text column: `Inches(6.3)` for a full screenshot on a 1-inch-margin page. A 1740px-wide image at that width prints at about 275 DPI.
- Detail crops go in at their natural proportion, capped at the same width.
- Centre the image, caption it, follow it with the locator.
- Palette-compress every image first (see `screenshot-extraction.md`, section 6). Twenty uncompressed screenshots make a 15 MB file; the same document with palette PNGs lands near 5 MB.
- Never stretch a crop to full width. An upscaled 600px detail looks broken next to a sharp full screenshot.

## 6. Corrections

When the screen and the transcript disagree, the document states both, briefly, in a note box:

> **Small correction:** The presenter said "about 46 companies" while the result was still loading; that was the row number visible at that moment. The finished answer reported 50.

Two reasons this earns its place. It stops the reader trusting a wrong number, and it stops them distrusting the document when it contradicts what they remember hearing. Never silently overwrite a spoken figure.

## 7. Verification checklist

Run before delivering:

1. **Reads back.** Open the saved file with python-docx, list the Heading 1s, and confirm the module sequence is complete and in order.
2. **Image count** matches the number of `screen()` calls, and the embedded media count in the archive matches too.
3. **Every screenshot has a caption and a locator.** Count them; the numbers should agree.
4. **Every module has a timestamp range**, and the ranges advance monotonically.
5. **File size** is sane for email.
6. **Scope holds.** Nothing in the document came from outside the recording.

```python
from docx import Document
import zipfile
d = Document(path)
print([p.text for p in d.paragraphs if p.style.name == "Heading 1"])
print("images:", len([n for n in zipfile.ZipFile(path).namelist() if n.startswith("word/media/")]))
```

## 8. Other output formats

- **Markdown.** Same structure. Images as relative links into an `images/` folder beside the file; keep the caption and locator as italic and bold lines under each.
- **Shareable page.** Same structure, one scrolling page, images inline at full column width. Worth it when the audience is a team rather than one person.
- **Never split** the training document across several files. One linear artefact is the entire point; a reader who has to open four files to follow a walkthrough has been given notes, not training.
