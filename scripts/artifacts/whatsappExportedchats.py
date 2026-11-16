__artifacts_v2__ = {
    "whatsappExportedchats": {
        "name": "Whatsapp Exported Chat",
        "description": "Messages from WhatsApp chat exports made on iOS (_chat.txt) or Android "
                       "(WhatsApp Chat with <name>.txt), one conversation per export, with continuation "
                       "lines kept in the preceding message and attached media where the file is in the export.",
        "author": "@AlexisBrignoni, Codex, @kalink0",
        "creation_date": "2022-03-12",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Whatsapp Exported Chat",
        "notes": "Reads the text file of an unpacked WhatsApp chat export: _chat.txt (iOS) or WhatsApp*.txt "
                 "(Android). A line opening with '[date, time] ' (iOS) or 'date, time - ' (Android) starts a "
                 "message; other lines continue it. Conversation is the chat name from the Android file name or "
                 "the iOS export folder ('WhatsApp Chat - <name>'). Source File keeps two exports of the same chat "
                 "apart, which Conversation alone does not, and is what LAVA's conversation view groups on. "
                 "Timestamp (as printed) is the device's local time as printed, with no offset. Timestamp (local "
                 "time, offset unknown) is that value as a date, only when the file settles the order of day and "
                 "month; LAVA shows it as UTC, which it is not. The export names no owner, so Direction is derived "
                 "and Direction Basis says how: in a one-to-one chat (two senders, one of them the chat name) the "
                 "other sender is the owner; in other chats it is the owner name every one-to-one chat of the "
                 "input agrees on; otherwise Direction is blank, as for group chats when the input holds exports "
                 "from two phones. Lines without a sender, and iOS group messages under the group's own name, are "
                 "system messages without Direction; iOS prints the encryption notice of a one-to-one chat under "
                 "the contact's name, so it takes that Direction. Media is the attached file named in the message when that "
                 "file is in the same folder; Android documents keep their own name and are found only inside a "
                 "folder named 'WhatsApp Chat…'. Tested on English-language exports of the same chats from Android "
                 "and iOS, whose one-to-one chats gave the same Direction on both.",
        "paths": ('*/_chat.txt', '*/WhatsApp*.txt',
                  '*/IMG-*-WA*', '*/VID-*-WA*', '*/AUD-*-WA*', '*/PTT-*-WA*', '*/DOC-*-WA*', '*/STK-*-WA*',
                  '*/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*', '*/WhatsApp Chat*/*'),
        "output_types": "standard",
        "artifact_icon": "message-circle",
        "data_views": {
            "conversation": {
                "conversationDiscriminatorColumn": "Source File",
                "conversationLabelColumn": "Conversation",
                "textColumn": "Message",
                "directionColumn": "Direction",
                "directionSentValue": "Outgoing",
                "timeColumn": "Timestamp (local time, offset unknown)",
                "senderColumn": "Sender",
                "mediaColumn": "Media",
            }
        },
    },
    "whatsappExportedchatsMedia": {
        "name": "Whatsapp Exported Chat - Media",
        "description": "Attachments of WhatsApp chat exports made on iOS or Android, each with the message that "
                       "names it, files no message names, and attachments named but not in the export.",
        "author": "@kalink0",
        "creation_date": "2026-11-16",
        "last_update_date": "2026-11-16",
        "requirements": "none",
        "category": "Whatsapp Exported Chat",
        "notes": "One row per attachment a message names (see the Whatsapp Exported Chat artifact for how messages, "
                 "Direction and the timestamps are read), and one row per media file in the export's folder that no "
                 "message names, with the message columns blank. File Present is No when the named file is not in "
                 "the folder, as when the chat was exported without media; File Present held Yes on every row of the "
                 "tested exports, all made with media. Source File keeps two exports of the same chat apart, which "
                 "Conversation alone does not. Content Type is read from the file's "
                 "bytes; an ISO-BMFF file whose only track is a sound track is typed audio/mp4. Media files are "
                 "found by the same name patterns as the chat artifact.",
        "paths": ('*/_chat.txt', '*/WhatsApp*.txt',
                  '*/IMG-*-WA*', '*/VID-*-WA*', '*/AUD-*-WA*', '*/PTT-*-WA*', '*/DOC-*-WA*', '*/STK-*-WA*',
                  '*/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*', '*/WhatsApp Chat*/*'),
        "output_types": "standard",
        "artifact_icon": "image",
    },
}

import datetime
import os
import re

from scripts.filetype import guess_mime
from scripts.ilapfuncs import artifact_processor, check_in_media
from scripts.meta_records import media_type_hint

_TIME = r'\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AaPp]\.?\s?[Mm]\.?)?'
_DATE = r'\d{1,4}[/.-]\d{1,2}[/.-]\d{1,4}'
IOS_LINE = re.compile(r'^\[(' + _DATE + r',?\s+' + _TIME + r')[^\]]*\]\s?(.*)$')
ANDROID_LINE = re.compile(r'^(' + _DATE + r',?\s+' + _TIME + r')\s+-\s(.*)$')
IOS_ATTACHED = re.compile(r'<[^<>:]+: ([^<>]+)>')
ANDROID_ATTACHED = re.compile(r'^(\S[^\n]*?\.\w{2,5}) \([^()]+\)$')
ANDROID_NAME = re.compile(r'^WhatsApp Chat with (.+)\.txt$')
IOS_FOLDER = re.compile(r'^WhatsApp Chat - (.+)$')
INVISIBLE = dict.fromkeys(map(ord, '\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069'))
DATE_PARTS = re.compile(r'^(\d{1,4})[/.-](\d{1,2})[/.-](\d{1,4}),?\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s?([AaPp])?')


def _date_order(printed):
    """'ymd', 'dmy', 'mdy' or None, from every timestamp of one file."""
    parts = [DATE_PARTS.match(p) for p in printed]
    parts = [m for m in parts if m]
    if not parts:
        return None
    if all(len(m.group(1)) == 4 for m in parts):
        return 'ymd'
    first_over = any(int(m.group(1)) > 12 for m in parts)
    second_over = any(int(m.group(2)) > 12 for m in parts)
    if first_over and not second_over:
        return 'dmy'
    if second_over and not first_over:
        return 'mdy'
    return None


def _parse(printed, order):
    match = DATE_PARTS.match(printed or '')
    if not match or not order:
        return ''
    a, b, c, hour, minute, second, half = match.groups()
    values = {'ymd': (a, b, c), 'dmy': (c, b, a), 'mdy': (c, a, b)}[order]
    year, month, day = (int(v) for v in values)
    if year < 100:
        year += 2000
    hour = int(hour)
    if half:
        hour = hour % 12 + (12 if half.lower() == 'p' else 0)
    try:
        return datetime.datetime(year, month, day, hour, int(minute), int(second or 0))
    except ValueError:
        return ''


def _conversation(path):
    name = os.path.basename(path)
    android = ANDROID_NAME.match(name)
    if android:
        return android.group(1)
    if name == '_chat.txt':
        ios = IOS_FOLDER.match(os.path.basename(os.path.dirname(path)))
        if ios:
            return ios.group(1)
    return ''


def _split_sender(rest):
    name, separator, text = rest.partition(': ')
    if separator:
        return name.translate(INVISIBLE).strip(), text
    if rest.endswith(':') and ': ' not in rest:
        return rest[:-1].translate(INVISIBLE).strip(), ''
    return '', rest


def _read_chat(path):
    """Messages of one export as [printed, line, sender, text, text opened with U+200E]."""
    messages = []
    pending = None
    with open(path, encoding='utf-8', errors='backslashreplace') as handle:
        for count, line in enumerate(handle, start=1):
            line = line.rstrip('\r\n')
            bare = line.lstrip('\u200e\ufeff')
            match = IOS_LINE.match(bare) or ANDROID_LINE.match(bare)
            if match:
                if pending is not None:
                    messages.append(pending)
                printed, rest = match.groups()
                sender, text = _split_sender(rest)
                pending = [printed, count, sender, text.lstrip('\u200e'), text.startswith('\u200e')]
            elif pending is not None:
                pending[3] += '\n' + line.replace('\u200e', '')
            elif line:
                pending = ['', count, '', line.replace('\u200e', ''), False]
    if pending is not None:
        messages.append(pending)
    return messages


def _attachment(text):
    ios = IOS_ATTACHED.search(text)
    if ios:
        return ios.group(1).strip()
    # Android prints a caption on the line after 'name (file attached)'.
    android = ANDROID_ATTACHED.match(text.split('\n', 1)[0].strip())
    if android:
        return android.group(1)
    return ''


def _one_to_one_owner(conversation, messages):
    """The other sender of a one-to-one chat: two senders, one of them the chat name.

    iOS prints a group's system messages under the group's name, each opening with U+200E, so a
    group where one member wrote would also show two senders. The chat-named sender must therefore
    have written at least one message that does not open with that mark."""
    named = {m[2] for m in messages if m[2]}
    if not conversation or len(named) != 2 or conversation not in named:
        return None
    if not any(m[2] == conversation and not m[4] for m in messages):
        return None
    return (named - {conversation}).pop()


def _is_chat_file(name):
    return not name.startswith('.') and (name == '_chat.txt' or (name.startswith('WhatsApp') and
                                                                 name.endswith('.txt')))


def _load_chats(files_found):
    """Every export of files_found as (path, conversation, rows); each row a dict of one message."""
    chats = []
    for file_found in files_found:
        file_found = str(file_found)
        if not _is_chat_file(os.path.basename(file_found)):
            continue
        messages = _read_chat(file_found)
        if any(m[0] for m in messages):
            chats.append((file_found, _conversation(file_found), messages))

    owners = {}
    for path, conversation, messages in chats:
        owner = _one_to_one_owner(conversation, messages)
        if owner:
            owners[path] = owner
    shared_owner = next(iter(set(owners.values()))) if len(set(owners.values())) == 1 else None

    loaded = []
    for path, conversation, messages in chats:
        order = _date_order([m[0] for m in messages if m[0]])
        owner, basis = owners.get(path), 'one-to-one chat'
        if owner is None and shared_owner:
            owner, basis = shared_owner, 'owner name from one-to-one chats'
        rows = []
        for printed, count, sender, text, _ in messages:
            direction = row_basis = ''
            # iOS prints a group's system messages with the group name as the sender.
            if owner and sender and not (path not in owners and sender == conversation):
                direction, row_basis = ('Outgoing' if sender == owner else 'Incoming'), basis
            rows.append({'time': _parse(printed, order), 'printed': printed, 'line': count, 'sender': sender,
                         'text': text, 'direction': direction, 'basis': row_basis, 'attach': _attachment(text)})
        loaded.append((path, conversation, rows))
    return loaded


def _check_in(path, name):
    """Media reference and content type of a file, typed by its bytes (audio-only ISO-BMFF as audio)."""
    hint = media_type_hint(path)
    try:
        content_type = hint or guess_mime(path) or ''
    except OSError:
        content_type = ''
    return check_in_media(path, name, force_type=hint), content_type


@artifact_processor
def whatsappExportedchats(context):
    chats = _load_chats(context.get_files_found())
    data_list = []
    for path, conversation, rows in chats:
        folder = os.path.dirname(path)
        for row in rows:
            media = ''
            if row['attach'] and os.path.isfile(os.path.join(folder, row['attach'])):
                media = _check_in(os.path.join(folder, row['attach']), row['attach'])[0]
            data_list.append((row['time'], row['direction'], row['sender'], conversation, row['text'], media,
                              row['printed'], row['basis'], row['line'], context.get_relative_path(path)))

    data_headers = (('Timestamp (local time, offset unknown)', 'datetime'), 'Direction', 'Sender', 'Conversation',
                    'Message', ('Media', 'media'), 'Timestamp (as printed)', 'Direction Basis', 'Line',
                    'Source File')
    return data_headers, data_list, '\n'.join(path for path, _, _ in chats)


@artifact_processor
def whatsappExportedchatsMedia(context):
    files_found = [str(f) for f in context.get_files_found()]
    chats = _load_chats(files_found)
    by_folder = {}
    for path in files_found:
        if os.path.isfile(path) and not _is_chat_file(os.path.basename(path)):
            by_folder.setdefault(os.path.dirname(path), set()).add(os.path.basename(path))

    data_list = []
    sources = []
    for path, conversation, rows in chats:
        folder = os.path.dirname(path)
        present = by_folder.get(folder, set())
        named = set()
        for row in rows:
            name = row['attach']
            if not name:
                continue
            named.add(name)
            media = content_type = ''
            if name in present:
                media, content_type = _check_in(os.path.join(folder, name), name)
                sources.append(os.path.join(folder, name))
            data_list.append((row['time'], row['direction'], row['sender'], conversation, media, content_type,
                              name, 'Yes' if name in present else 'No', row['printed'], row['line'],
                              context.get_relative_path(path)))
        for name in sorted(present - named):
            media, content_type = _check_in(os.path.join(folder, name), name)
            sources.append(os.path.join(folder, name))
            data_list.append(('', '', '', conversation, media, content_type, name, 'Yes', '', '',
                              context.get_relative_path(path)))

    data_headers = (('Timestamp (local time, offset unknown)', 'datetime'), 'Direction', 'Sender', 'Conversation',
                    ('Media', 'media'), 'Content Type', 'File Name', 'File Present', 'Timestamp (as printed)',
                    'Line', 'Source File')
    return data_headers, data_list, '\n'.join(sources or [path for path, _, _ in chats])
