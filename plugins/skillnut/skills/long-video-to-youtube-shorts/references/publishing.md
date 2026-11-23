# Publishing (step by step)

Everything behind the Publish half of Stage 4.

## 1. Get the files where the uploader can reach them

Cloud connectors (Composio, a Google Drive connector, a YouTube connector) run in the cloud and cannot read the user's disk. They also cannot receive a video as request text: a 5 MB file is millions of characters. So the bytes must reach the cloud some other way. In order of preference:

1. **A staging folder the user drops files into** (for example a Google Drive folder). Create the folder for them once and remember its ID. Their part takes ten seconds.
2. **A local uploader with its own credential** (for example rclone connected to their Drive once through a browser consent). Fully hands-off afterwards; this puts a credential on their machine, so say so and let them choose.
3. **A temporary public link from their machine** (a tunnel to a one-file server). Hands-off but exposes the file briefly and is often blocked by safety policy. Only with explicit approval.

Say this plainly up front. Do not burn time on workarounds the user has not agreed to.

Before uploading, compare each staged file's size with the local copy. A mismatch means a stale version (for example uploaded before a fix).

## 2. Upload once, as Private

With Composio: `GOOGLEDRIVE_DOWNLOAD_FILE` on the staged file returns a stored copy with an `s3url`; the key path inside it (`<project>/googledrive/GOOGLEDRIVE_DOWNLOAD_FILE/response/<hash>`) is the `s3key` that `YOUTUBE_MULTIPART_UPLOAD_VIDEO` takes as `videoFile`. Upload with title, description, tags, `categoryId` (28 is Science and Technology; list assignable ones with `YOUTUBE_LIST_VIDEO_CATEGORIES`), and `privacyStatus: private`.

Record each returned video ID immediately. Never re-run an upload to "check" it; that creates a second video.

## 3. Schedule the release

The upload tools usually have no "publish at" field. The YouTube Data API does: update the video's status with a future `publishAt` while it is private, and YouTube flips it to public at that moment.

Via Composio's workbench:

```python
res, err = proxy_execute("PUT", "https://www.googleapis.com/youtube/v3/videos", "youtube",
    query_params={"part": "status"},
    body={"id": VIDEO_ID, "status": {"privacyStatus": "private", "publishAt": "2026-10-24T12:30:00Z",
          "selfDeclaredMadeForKids": False, "embeddable": True, "publicStatsViewable": True, "license": "youtube"}})
```

- `publishAt` is UTC. Convert the user's local release time (6:00 PM IST is 12:30 UTC).
- Send the full status object; fields left out can reset.
- Set `selfDeclaredMadeForKids: False` explicitly.
- Read the status back for every video. A write can report success and still read back empty for a moment; re-read before re-applying.
- One Short per day. Space two Shorts from the same long video apart.

Without scheduling access, upload private and tell the user which day to flip each one, or offer to flip them when asked.

## 4. Remove YouTube's auto-captions

YouTube generates an automatic caption track (`trackKind: asr`) during processing. On a Short with burned-in titles it shows the same words twice.

- `YOUTUBE_LIST_CAPTION_TRACK` with the video ID; delete every `asr` track with `YOUTUBE_DELETE_CAPTION_TRACK` (`confirmDelete: true`).
- Tracks appear minutes after upload. Sweep once after uploading, then again after processing reports `succeeded`, and list again to confirm zero remain.
- YouTube may regenerate them later; tell the user to say so if they spot doubled text.

## 5. Clean up

- Delete each staging copy **permanently** (`GOOGLEDRIVE_GOOGLE_DRIVE_DELETE_FOLDER_OR_FILE_ACTION`), not to Trash, which still counts toward storage. Confirm each returns 404.
- Keep the user's local copies.
- Keep the staging folder for next time unless they ask otherwise.
- Update the README table in the user's folder: file, title, release time in their zone, link.

## 6. Rate limits

Google Drive returns a 403 "rate limit exceeded" when requests are bursted; back off a couple of seconds and retry. YouTube uploads draw on a daily API quota that is much smaller than it sounds; if an upload fails with a quota error, stop, tell the user, and continue the next day rather than retrying.
