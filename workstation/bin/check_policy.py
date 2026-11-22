#!/usr/bin/env python3
"""
check_policy.py - Script tự động kiểm tra việc triển khai chính sách AutoConfig
trên máy trạm Firefox theo yêu cầu của bài lab browser-hijack-defense.
Tương thích hoàn toàn với Python 3.5+.
"""

import sys
import os
import re

LOCAL_SETTINGS = "/usr/lib/firefox/defaults/pref/local-settings.js"
MOZILLA_CFG = "/usr/lib/firefox/mozilla.cfg"
USER_JS = os.path.expanduser("~/.mozilla/firefox/default/user.js")

def check():
    errors = []

    # 1. Kiểm tra local-settings.js
    if not os.path.isfile(LOCAL_SETTINGS):
        errors.append("Không tìm thấy file cấu hình: " + LOCAL_SETTINGS)
    else:
        with open(LOCAL_SETTINGS, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if not re.search(r'pref\s*\(\s*["\']general\.config\.filename["\']\s*,\s*["\']mozilla\.cfg["\']\s*\)', content):
                errors.append(LOCAL_SETTINGS + " chưa khai báo pref('general.config.filename', 'mozilla.cfg');")

    # 2. Kiểm tra mozilla.cfg
    if not os.path.isfile(MOZILLA_CFG):
        errors.append("Không tìm thấy file chính sách: " + MOZILLA_CFG)
    else:
        with open(MOZILLA_CFG, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        if len(lines) == 0 or not lines[0].strip().startswith("//"):
            errors.append("Dòng đầu tiên của " + MOZILLA_CFG + " bắt buộc phải là một comment (//) theo quy chuẩn AutoConfig.")

        full_cfg = "".join(lines)

        # Kiểm tra khóa homepage về http://novacorp.local:8080/
        if not re.search(r'lockPref\s*\(\s*["\']browser\.startup\.homepage["\']\s*,\s*["\']http://novacorp\.local:8080/?["\']\s*\)', full_cfg):
            errors.append("Chưa khóa đúng browser.startup.homepage về http://novacorp.local:8080/ bằng lockPref.")

        # Kiểm tra khóa search engine mặc định
        if not re.search(r'lockPref\s*\(\s*["\']browser\.search\.defaultenginename["\']', full_cfg):
            errors.append("Chưa cấu hình lockPref cho browser.search.defaultenginename.")

        # Kiểm tra chặn cài đặt extension mới (xpinstall.enabled = false)
        if not re.search(r'lockPref\s*\(\s*["\']xpinstall\.enabled["\']\s*,\s*false\s*\)', full_cfg):
            errors.append("Chưa chặn cài đặt extension mới: lockPref('xpinstall.enabled', false);")

    # 3. Kiểm tra user.js đã dọn sạch chưa
    if os.path.isfile(USER_JS):
        with open(USER_JS, "r", encoding="utf-8", errors="ignore") as f:
            user_content = f.read()
            if "ads.local" in user_content or "AdsSearch" in user_content:
                errors.append("File " + USER_JS + " vẫn còn chứa cấu hình của browser hijacker (ads.local hoặc AdsSearch).")

    if errors:
        print("[KIỂM TRA CHÍNH SÁCH THẤT BẠI]")
        for err in errors:
            print(" - " + err)
        print("FAIL")
        sys.exit(1)
    else:
        print("[KIỂM TRA CHÍNH SÁCH THÀNH CÔNG]")
        print(" - local-settings.js đã kích hoạt AutoConfig nạp mozilla.cfg.")
        print(" - mozilla.cfg tuân thủ quy chuẩn dòng đầu comment.")
        print(" - browser.startup.homepage đã bị khóa về http://novacorp.local:8080/.")
        print(" - browser.search.defaultenginename đã bị khóa.")
        print(" - xpinstall.enabled đã bị khóa về false (chặn cài extension).")
        print(" - Profile user.js đã được làm sạch hoàn toàn.")
        print("PASS")
        sys.exit(0)

if __name__ == "__main__":
    check()
