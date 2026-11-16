"""
Generate synthetic, unpacked WhatsApp chat exports from Android and iOS for the whatsappExportedchats tests.

Every value here is fabricated: names, phone numbers, texts and media. A real export is a person's
conversation, so none can be sanitised into a fixture. The file names, line prefixes, attachment
markers and invisible characters follow real English-language exports from both platforms. Covered:

  - Android: 'date, time - ' lines without seconds, system lines without a sender, unsaved contacts
    shown as phone numbers, 'name (file attached)' with a caption on the next line, a voice note, a
    document keeping its own name inside a 'WhatsApp Chat with …' folder, a media file no message names
  - iOS: '[date, time] ' lines with seconds, CRLF, U+200E marks before lines and attachments, '~ name'
    with U+202F and a phone number wrapped in U+202A/U+202C, a group system message under the group's
    own name, an empty message 'Name:', '<attached: name>' and an attachment that is not in the export
  - one-to-one chats on both platforms that agree on the owner, so the groups get a Direction; the owner
    writes in one group and not in the other
  - a chat whose dates never settle the order of day and month (12-hour clock), which must keep only
    the printed timestamp
  - continuation lines, including one that starts with a bracket
  - a text file named WhatsApp*.txt that holds no message, which must add nothing

Usage:
    python admin/test/scripts/gen_whatsapp_export_synth.py [output_dir]

Then zip the output folder and feed it to make_test_data.py.
"""
import io
import os
import shutil
import struct
import sys

from PIL import Image

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "synth_whatsapp_export")

LRM, NNBSP, LRE, PDF = "\u200e", "\u202f", "\u202a", "\u202c"
OWNER, ALICE, BOB, GROUP = "Owner Name", "Alice Example", "Bob Sample", "Synthetic Group"


def image_bytes(fmt, colour):
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), colour).save(buf, fmt)
    return buf.getvalue()


def box(kind, payload):
    return struct.pack(">I", 8 + len(payload)) + kind + payload


def iso_bmff(handler):
    hdlr = box(b"hdlr", b"\0\0\0\0" + b"\0\0\0\0" + handler + b"\0" * 13)
    return box(b"ftyp", b"mp42\0\0\0\0mp42isom") + box(b"moov", box(b"trak", box(b"mdia", hdlr)))


def ogg_opus():
    return b"OggS\0\x02" + b"\0" * 20 + b"\x01\x13OpusHead\x01\x01" + b"\0" * 10


PDF_BYTES = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def write(folder, name, data, newline="\n"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    if isinstance(data, str):
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(newline.join(data.split("\n")))
    else:
        with open(path, "wb") as handle:
            handle.write(data)


def android(root):
    chat = os.path.join(root, "android", f"WhatsApp Chat with {ALICE}")
    write(chat, f"WhatsApp Chat with {ALICE}.txt", "\n".join([
        "01/12/2025, 09:00 - Messages and calls are end-to-end encrypted. Tap to learn more.",
        f"01/12/2025, 09:01 - {ALICE}: Good morning",
        f"01/12/2025, 09:02 - {OWNER}: Morning! Here is the plan",
        "[step 1] buy coffee",
        "[step 2] drink coffee",
        f"01/12/2025, 09:03 - {ALICE}: IMG-20251201-WA0001.jpg (file attached)",
        "Caption on the next line",
        f"01/12/2025, 09:04 - {OWNER}: PTT-20251201-WA0002.opus (file attached)",
        f"13/12/2025, 18:30 - {ALICE}: Report.pdf (file attached)",
        f"13/12/2025, 18:31 - {OWNER}: Thanks",
        "",
    ]))
    write(chat, "IMG-20251201-WA0001.jpg", image_bytes("JPEG", (200, 30, 30)))
    write(chat, "PTT-20251201-WA0002.opus", ogg_opus())
    write(chat, "Report.pdf", PDF_BYTES)

    group = os.path.join(root, "android", f"WhatsApp Chat with {GROUP}")
    write(group, f"WhatsApp Chat with {GROUP}.txt", "\n".join([
        "14/12/2025, 10:00 - Messages and calls are end-to-end encrypted. Tap to learn more.",
        f"14/12/2025, 10:00 - {ALICE} created group \"{GROUP}\"",
        "14/12/2025, 10:01 - You were added",
        f"14/12/2025, 10:02 - {ALICE}: Welcome everyone",
        "14/12/2025, 10:03 - +49 151 0000001: Hi, I am not in your contacts",
        "14/12/2025, 10:04 - +49 151 0000001: VID-20251202-WA0003.mp4 (file attached)",
        f"14/12/2025, 10:05 - {OWNER}: Hello group",
        "",
    ]))
    write(group, "VID-20251202-WA0003.mp4", iso_bmff(b"vide"))
    write(group, "IMG-20251202-WA0099.jpg", image_bytes("JPEG", (90, 90, 90)))  # named by no message


def ios(root):
    chat = os.path.join(root, "ios", f"WhatsApp Chat - {ALICE}")
    write(chat, "_chat.txt", "\n".join([
        f"[01.12.25, 09:00:00] {ALICE}: {LRM}Messages and calls are end-to-end encrypted.",
        f"[01.12.25, 09:01:10] {ALICE}: Good morning",
        f"[01.12.25, 09:02:20] {OWNER}: Morning!",
        f"{LRM}[01.12.25, 09:03:30] {ALICE}: {LRM}<attached: 00000003-PHOTO-2025-12-01-09-03-30.jpg>",
        f"{LRM}[01.12.25, 09:04:40] {OWNER}: {LRM}<attached: 00000004-AUDIO-2025-12-01-09-04-40.opus>",
        f"[13.12.25, 18:30:00] {OWNER}:",
        f"[13.12.25, 18:31:00] {ALICE}: Second line follows",
        "and here it is",
        "",
    ]), newline="\r\n")
    write(chat, "00000003-PHOTO-2025-12-01-09-03-30.jpg", image_bytes("JPEG", (30, 200, 30)))
    write(chat, "00000004-AUDIO-2025-12-01-09-04-40.opus", ogg_opus())

    group = os.path.join(root, "ios", f"WhatsApp Chat - {GROUP}")
    write(group, "_chat.txt", "\n".join([
        f"[14.12.25, 10:00:00] {GROUP}: {LRM}Messages and calls are end-to-end encrypted.",
        f"[14.12.25, 10:00:05] {GROUP}: {LRM}{ALICE} created this group",
        f"[14.12.25, 10:02:00] {ALICE}: Welcome everyone",
        f"[14.12.25, 10:03:00] ~{NNBSP}Pushname: Hi, I am not in your contacts",
        f"[14.12.25, 10:03:30] {LRE}+49{chr(0xa0)}151{chr(0xa0)}0000002{PDF}: Me neither",
        f"{LRM}[14.12.25, 10:04:00] ~{NNBSP}Pushname: {LRM}<attached: 00000009-VIDEO-2025-12-02-10-04-00.mp4>",
        "",
    ]), newline="\r\n")  # the owner writes nothing in this group; the video is not in the export

    ambiguous = os.path.join(root, "ios", f"WhatsApp Chat - {BOB}")
    write(ambiguous, "_chat.txt", "\n".join([
        f"[1/2/25, 9:05:00{NNBSP}AM] {BOB}: Dates here never show a field above 12",
        f"[1/2/25, 1:15:00{NNBSP}PM] {OWNER}: So only the printed timestamp is kept",
        "",
    ]), newline="\r\n")


def decoy(root):
    write(os.path.join(root, "other"), "WhatsApp notes.txt", "Shopping list\nmilk\n")


def main():
    if os.path.exists(BASE):
        shutil.rmtree(BASE)
    android(BASE)
    ios(BASE)
    decoy(BASE)
    print(f"Written to {BASE}")
    print("Known values: 29 messages (Android 7 + 7, iOS 7 + 6 + 2), 8 media rows "
          "(7 files present of which 1 named by no message, 1 named attachment missing)")


if __name__ == "__main__":
    main()
