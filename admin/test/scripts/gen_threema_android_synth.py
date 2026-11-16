"""
Generate a synthetic, unpacked Threema for Android data backup for the threemaAndroidBackup tests.

Every value here is fabricated: names, Threema IDs, keys, texts, coordinates and media. A real
backup is one person's complete chat history, so none can be sanitised into a fixture. The CSV
headers, file names and the JSON layout of the message bodies follow a real Threema for Android
backup. Covered:

  - a backup folder carrying Threema's own name (threema-backup_<ID>_<ms>_1), read for the Account
    artifact, and a second backup whose folder lost that name, which must stay a separate set of
    conversations and leave the Account ID blank
  - both column layouts: the older one of the real backup, and the current one with display_tags,
    edited_at, deleted_at and g_msg_states, with a starred, an edited and a deleted message, call
    statuses flagged as status messages (Direction kept) and a GROUP_STATUS (Direction blank)
  - a decoy folder with a contacts.csv and a message_*.csv of another layout, which must add nothing
  - one-to-one chat: incoming and outgoing text, a multi-line text, a quote, an image file message
    with thumbnail whose caption is only in the JSON body and holds a line break, a voice message
    stored as an ISO-BMFF file with only a sound track (must be typed audio, not video), a video, an
    IMAGE message with no media file, a location and a call status
  - the CSV writer's doubled backslashes in JSON bodies, once making the body invalid JSON (a quote
    in the caption) and once turning a line break into a literal backslash-n
  - a contact with an empty chat file, a group with a status message and a member missing from
    contacts.csv, profile picture and avatar files, an orphaned media file and thumbnail
  - settings and an identity file (random base32; it decrypts to nothing)

Usage:
    python admin/test/scripts/gen_threema_android_synth.py [output_dir]

Then zip the output folder and feed it to make_test_data.py.
"""
import csv
import io
import json
import os
import random
import shutil
import struct
import sys

from PIL import Image

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "synth_threema_android")

MESSAGE_HEADER = ["apiid", "uid", "isoutbox", "isread", "issaved", "messagestae", "posted_at", "created_at",
                  "modified_at", "type", "body", "isstatusmessage", "isqueued", "caption",
                  "quoted_message_apiid", "delivered_at", "read_at"]
GROUP_MESSAGE_HEADER = MESSAGE_HEADER[:2] + ["identity"] + MESSAGE_HEADER[2:]
# The layout written by the current Threema source (BackupService.java, threema-android 097cc6b).
MESSAGE_HEADER_CURRENT = MESSAGE_HEADER + ["display_tags", "edited_at", "deleted_at"]
GROUP_MESSAGE_HEADER_CURRENT = GROUP_MESSAGE_HEADER + ["g_msg_states", "display_tags", "edited_at", "deleted_at"]
CONTACT_HEADER = ["identity", "publickey", "verification", "acid", "tacid", "firstname", "lastname",
                  "nick_name", "color", "hidden", "archived"]
GROUP_HEADER = ["id", "creator", "groupname", "created_at", "members", "deleted", "archived"]

OWN_ID = "TESTOWN1"
ALICE, BOB, CAROL, STRANGER = "TESTAB12", "TESTCD34", "TESTEF56", "TESTZZ99"
GROUP_ID = "0123456789abcdef"
T0 = 1700000000000  # 2023-11-14 22:13:20 UTC

rng = random.Random(20261116)


def hexs(n):
    return "".join(rng.choice("0123456789abcdef") for _ in range(n))


def uid():
    h = hexs(32)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def body_json(values):
    """A JSON body as found in the real backup this layout follows: every backslash doubled."""
    return json.dumps(values, ensure_ascii=False).replace("\\", "\\\\")


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in rows:
            writer.writerow([row.get(k, "") for k in header])


def image_bytes(fmt, colour):
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), colour).save(buf, fmt)
    return buf.getvalue()


def box(kind, payload):
    return struct.pack(">I", 8 + len(payload)) + kind + payload


def iso_bmff(handler):
    """A minimal ISO-BMFF file whose one track has the given handler (b'soun' or b'vide')."""
    hdlr = box(b"hdlr", b"\0\0\0\0" + b"\0\0\0\0" + handler + b"\0" * 12 + b"\0")
    moov = box(b"moov", box(b"trak", box(b"mdia", hdlr)))
    return box(b"ftyp", b"mp42\0\0\0\0mp42isom") + moov


def msg(apiid, out, posted, mtype, body, **extra):
    row = {"apiid": apiid, "uid": extra.pop("uid", uid()), "isoutbox": "1" if out else "0", "isread": "1",
           "issaved": "1", "messagestae": "READ" if out else "", "posted_at": str(posted),
           "created_at": str(posted + (0 if out else 5000)), "modified_at": "", "type": mtype, "body": body,
           "isstatusmessage": "0", "isqueued": "1" if out else "0", "caption": "",
           "quoted_message_apiid": "", "delivered_at": "", "read_at": ""}
    row.update(extra)
    return row


def file_body(mime, size, name, caption, thumb_mime, meta=None):
    return body_json([hexs(32), hexs(64), mime, size, name, 0, True, caption, thumb_mime, meta or {}])


def build_named_backup(root):
    os.makedirs(root)
    write_csv(os.path.join(root, "contacts.csv"), CONTACT_HEADER, [
        {"identity": ALICE, "publickey": hexs(64), "verification": "2", "firstname": "Alice",
         "lastname": "Example", "color": "-1234567", "hidden": "0", "archived": "0"},
        {"identity": BOB, "publickey": hexs(64), "verification": "0", "nick_name": "bobby",
         "color": "-7654321", "hidden": "0", "archived": "1"},
        {"identity": CAROL, "publickey": hexs(64), "verification": "1", "firstname": "Carol",
         "lastname": "Sample", "color": "-1111111", "hidden": "1", "archived": "0"},
    ])
    write_csv(os.path.join(root, "groups.csv"), GROUP_HEADER, [
        {"id": GROUP_ID, "creator": ALICE, "groupname": "Synthetic Group", "created_at": str(T0 - 86400000),
         "members": f"{ALICE};{CAROL};{STRANGER}", "deleted": "0", "archived": "0"},
    ])
    for name, header in (("ballot.csv", ["id", "aid", "creator", "ref", "ref_id", "name", "state"]),
                         ("distribution_list.csv", ["id", "distribution_list_name", "created_at"])):
        write_csv(os.path.join(root, name), header, [])
    with open(os.path.join(root, "settings"), "w", encoding="utf-8") as handle:
        handle.write('"version","16"\n')
    with open(os.path.join(root, "identity"), "w", encoding="ascii") as handle:
        chars = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567") for _ in range(80))
        handle.write("-".join(chars[i:i + 4] for i in range(0, 80, 4)))

    image_uid, voice_uid, video_uid = uid(), uid(), uid()
    alice = [
        msg("a001", False, T0, "TEXT", "Hello from Alice"),
        msg("a002", True, T0 + 60000, "TEXT", "Hi Alice", quoted_message_apiid="a001",
            delivered_at=str(T0 + 61000), read_at=str(T0 + 62000)),
        msg("a003", True, T0 + 120000, "FILE",
            file_body("image/jpeg", 631, "IMG_0001.jpg", "First line\nsecond line", "image/jpeg", {"h": 8, "w": 8}),
            uid=image_uid),
        msg("a004", False, T0 + 180000, "FILE",
            file_body("audio/aac", 120, "voice.aac", 'Listen to "this"', None, {"d": 3.2}), uid=voice_uid),
        msg("a005", False, T0 + 240000, "FILE",
            file_body("video/mp4", 120, "clip.mp4", None, "image/jpeg", {"d": 1.0}), uid=video_uid,
            caption="Video caption in column"),
        msg("a006", False, T0 + 300000, "IMAGE", ""),
        msg("a007", False, T0 + 360000, "LOCATION",
            body_json([52.520008, 13.404954, 12.5, "Example Street 1, 10115 Berlin", "Example Place"])),
        msg("a008", True, T0 + 420000, "VOIP_STATUS", body_json([1, {"duration": 42, "status": 2}])),
        msg("a009", False, T0 + 480000, "TEXT", "Line one\nLine two\nLine three"),
    ]
    write_csv(os.path.join(root, f"message_{ALICE}.csv"), MESSAGE_HEADER, alice)
    write_csv(os.path.join(root, f"message_{BOB}.csv"), MESSAGE_HEADER, [])

    group = [
        dict(msg("g001", False, T0 + 1000, "TEXT", "Alice created the group"), isstatusmessage="1"),
        dict(msg("g002", False, T0 + 2000, "TEXT", "Hi all, Carol here"), identity=CAROL),
        dict(msg("g003", False, T0 + 3000, "TEXT", "Message from someone not in contacts"), identity=STRANGER),
        msg("g004", True, T0 + 4000, "TEXT", "Owner writing to the group"),
    ]
    write_csv(os.path.join(root, f"group_message_{GROUP_ID}-{ALICE}.csv"), GROUP_MESSAGE_HEADER, group)

    media = {
        f"message_media_{image_uid}": image_bytes("JPEG", (200, 30, 30)),
        f"message_thumbnail_{image_uid}": image_bytes("JPEG", (30, 200, 30)),
        f"message_media_{voice_uid}": iso_bmff(b"soun"),
        f"message_media_{video_uid}": iso_bmff(b"vide"),
        f"message_thumbnail_{video_uid}": image_bytes("PNG", (30, 30, 200)),
        f"message_media_{uid()}": image_bytes("PNG", (90, 90, 90)),        # orphan
        f"message_thumbnail_{uid()}": image_bytes("JPEG", (60, 60, 60)),   # orphan
        f"contact_profile_pic_{ALICE}": image_bytes("JPEG", (250, 200, 0)),
        f"contact_avatar_{BOB}": image_bytes("JPEG", (0, 200, 250)),
    }
    for name, data in media.items():
        with open(os.path.join(root, name), "wb") as handle:
            handle.write(data)
    return len(alice) + len(group), len([n for n in media if n.startswith("message_")])


def build_renamed_backup(root):
    """A backup in the current column layout, unpacked into a folder that lost Threema's name."""
    os.makedirs(root)
    write_csv(os.path.join(root, "contacts.csv"), CONTACT_HEADER, [
        {"identity": ALICE, "publickey": hexs(64), "verification": "2", "firstname": "Alice",
         "lastname": "Example", "color": "-1234567", "hidden": "0", "archived": "0"},
        {"identity": CAROL, "publickey": hexs(64), "verification": "1", "firstname": "Carol",
         "lastname": "Sample", "color": "-1111111", "hidden": "0", "archived": "0"},
    ])
    write_csv(os.path.join(root, "groups.csv"), GROUP_HEADER, [
        {"id": GROUP_ID, "creator": ALICE, "groupname": "Synthetic Group", "created_at": str(T0 - 86400000),
         "members": f"{ALICE};{CAROL}", "deleted": "0", "archived": "0"},
    ])
    one = [
        msg("r001", False, T0 - 600000, "TEXT", "Second backup, same chat partner", display_tags="1"),
        msg("r002", True, T0 - 540000, "TEXT", "Edited reply", edited_at=str(T0 - 530000)),
        msg("r003", False, T0 - 520000, "TEXT", "", deleted_at=str(T0 - 510000)),
        dict(msg("", True, T0 - 500000, "VOIP_STATUS", body_json([1, {"duration": 7, "status": 2}])),
             isstatusmessage="1"),
        dict(msg("", False, T0 - 490000, "VOIP_STATUS", body_json([1, {"status": 1}])), isstatusmessage="1"),
    ]
    write_csv(os.path.join(root, f"message_{ALICE}.csv"), MESSAGE_HEADER_CURRENT, one)
    group = [
        dict(msg("", False, T0 - 480000, "GROUP_STATUS", body_json({"type": 1})), isstatusmessage="1"),
        dict(msg("q001", True, T0 - 470000, "TEXT", "Group message with delivery states"),
             g_msg_states=json.dumps({CAROL: "READ"})),
        dict(msg("q002", False, T0 - 460000, "TEXT", "Reply in the group"), identity=CAROL),
    ]
    write_csv(os.path.join(root, f"group_message_{GROUP_ID}-{ALICE}.csv"), GROUP_MESSAGE_HEADER_CURRENT, group)
    return len(one) + len(group)


def build_decoy(root):
    os.makedirs(root)
    write_csv(os.path.join(root, "contacts.csv"), ["identity", "name"], [{"identity": ALICE, "name": "Decoy"}])
    write_csv(os.path.join(root, f"message_{ALICE}.csv"), ["id", "timestamp", "text"],
              [{"id": "1", "timestamp": str(T0), "text": "not a Threema message"}])


def main():
    if os.path.exists(BASE):
        shutil.rmtree(BASE)
    named, named_files = build_named_backup(os.path.join(BASE, f"threema-backup_{OWN_ID}_{T0 + 600000}_1"))
    renamed = build_renamed_backup(os.path.join(BASE, "unpacked_backup"))
    build_decoy(os.path.join(BASE, "other_return"))
    print(f"Written to {BASE}")
    print(f"Known values: {named + renamed} messages ({named} + {renamed}), {named_files} message media files, "
          f"5 contacts, 2 groups, 2 account rows (one with a blank ID)")


if __name__ == "__main__":
    main()
