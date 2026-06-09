from pathlib import Path
p = Path("src/gepaw/app/channels/qrcode_auth_handler.py")
data = p.read_bytes()
# Use \r\n
old = b"_WECOM_SOURCE = PROJECT_NAME.lower()\r\n"
new = b"_WECOM_SOURCE = PROJECT_NAME.lower()\r\n_FEISHU_SOURCE = \"gepaw\"\r\n"
print("found:", old in data)
data = data.replace(old, new)
old2 = b'                    scan_url = f"{verification_uri}&source={PROJECT_NAME}"\r\n                else:\r\n                    scan_url = f"{verification_uri}?source={PROJECT_NAME}"'
new2 = b'                    scan_url = f"{verification_uri}&source={_FEISHU_SOURCE}"\r\n                else:\r\n                    scan_url = f"{verification_uri}?source={_FEISHU_SOURCE}"'
print("found2:", old2 in data)
data = data.replace(old2, new2)
p.write_bytes(data)
print("done")
