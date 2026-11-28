# Editing a live Word contract safely (python-docx)

Used by Module 1 (building from a previous agreement) and Module 2 (applying redlines). Goal: change exactly what was agreed, keep the house style, never lose the user's own edits, and prove the result.

## 1. Backups and versions

- Before every version: copy the file to `<Document> BACKUP-pre-vN.docx` (or `BACKUP-pre<ChangeName>.docx`).
- If the file changed since your last script ran, the user edited it by hand. Back it up as `BACKUP-pre-vN (user edits).docx` and build on top of it. Never regenerate from an older source and lose those edits.
- One script per version (`edit_vN.py`). Its header lists every change in plain words, so the version history reads like a changelog.
- Keep scripts, dumps and backups in a working subfolder; only the final `.docx` and `.pdf` sit with the user's contracts.

## 2. Look before you edit

Dump the document to a text file first:
- every body element in order (paragraphs and tables), with paragraph index, style name, and for each run: text, bold, colour;
- the exact, untruncated text of every paragraph you plan to change;
- every paragraph containing "Exhibit".

Use the dump to write exact finders. Python-docx's `doc.paragraphs` skips text inside tables; walk `doc.element.body` (and `w:tbl` children) when the document has tables.

## 3. Finders that fail loudly

```python
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

def ptext(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))

def find_one(doc, prefix):
    hits = [Paragraph(el, doc._body) for el in doc.element.body.iter(qn("w:p"))
            if ptext(el).startswith(prefix)]
    assert len(hits) == 1, f"{len(hits)} matches for {prefix!r}"   # zero or two: stop
    return hits[0]
```

A finder that matches zero or several paragraphs stops the script. Better a stopped script than an edit in the wrong clause.

## 4. Formatting-preserving edits

Word splits text into runs at every formatting change, and often in the middle of words. Replacing `paragraph.text` destroys the formatting. Edit runs instead:

```python
def repl(p, old, new):
    """Replace `old` with `new` inside paragraph p, even when `old` spans several runs."""
    runs = p.runs; full = "".join(r.text for r in runs)
    i = full.find(old)
    assert i >= 0, f"{old!r} not in {p.text[:60]!r}"
    j = i + len(old); pos = 0; first = None
    for r in runs:
        a, b = pos, pos + len(r.text); pos = b
        if b <= i or a >= j:
            continue
        pre = r.text[:max(0, i - a)]; post = r.text[max(0, j - a):] if b > j else ""
        if first is None:
            r.text = pre + new + post; first = r
        else:
            r.text = post

def set_body(p, text, keep=1):
    """Keep the first `keep` runs (e.g. a bold clause label), put `text` in the next run, drop the rest."""
    runs = p.runs
    runs[keep].text = text
    for r in runs[keep + 1:]:
        r._r.getparent().remove(r._r)
```

- **New paragraphs:** deep-copy an existing paragraph of the right style (`copy.deepcopy(template._p)`), clear its runs, add new runs, insert with `anchor._p.addnext(new)`. Copy run properties (`w:rPr`) from a plain body run so font, size and colour match; add `w:b` for a bold label.
- **Table cells:** write into the first run of the cell's first paragraph and delete the other runs.
- **Deleting a section:** remove the paragraphs and any table plus the empty spacer paragraph after it.
- **Placeholder colour:** confirmed values switch from the placeholder colour (blue) to the body colour (black) on the run.

## 5. Renumber after deletions

Removing a statement-of-work section shifts every later number. After deletions:
- renumber the section headings and sub-numbers;
- search for "Section N", "see Section", "Exhibit N" and fix each one;
- check the main-body pointer to the statement-of-work cost section (clause 6.3) still points at the right number.

## 6. Verify every version

Run these and report the results:
1. **Forbidden strings:** the previous client's name and people, old product names, old fees and dates, old industry words, tools removed from scope. Expect zero.
2. **Required strings:** the client's legal name in the intro, section 2, Exhibit 1 and the signature block; the new fee; the effective date or its blank.
3. **Exhibit order:** the headings appear as Exhibit 1 (Mutual Confidentiality) then Exhibit 2 (Statement of Work); list every "Exhibit 1/2" reference with its paragraph and confirm each points to the right one.
4. **PDF pages:** export, then check the page where each exhibit starts and that both signature blocks are on the last page together.

## 7. Finalise for signature

- Blue placeholders with confirmed values turn black.
- Remaining placeholders (state, address, signatory, title, date) become underlined blanks `____________________`, so e-signature fields can be dropped on them.
- Remove the DRAFT footer.
- Export PDF; keep the Word master.
