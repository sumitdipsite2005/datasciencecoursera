import subprocess
import time
import os
import signal
import sys
import json
from datetime import datetime, timedelta
import winsound
import ctypes
import threading
from send2trash import send2trash
import re

# DOWNLOAD MODE SELECTOR
DOWNLOAD_MODE = "ffmpeg"  # Change "ffmpeg" to "nm3u8dl" to use N_m3u8DL-RE
# DOWNLOAD_MODE = "nm3u8dl"  # Change "ffmpeg" to "nm3u8dl" to use N_m3u8DL-RE

# ==================== CONFIG FOR FFMPEG DOWNLOAD ===================================================================
# LIVE_URL = "http://best.asiantv.co.uk:80/testttt/XJWNzrGnV4HH/2358" # SELECT 1 50fps
# LIVE_URL = "http://best.asiantv.co.uk:80/testttt/XJWNzrGnV4HH/2359" # SELECT 2 50fps for NPL & FIH hockey - SHOWING SELECT 1 NOT 2
# LIVE_URL = "http://best.asiantv.co.uk:80/testttt/XJWNzrGnV4HH/10278" # kantipur max 50fps for NPL
# LIVE_URL = "http://best.asiantv.co.uk:80/testttt/XJWNzrGnV4HH/7275" # ASTRO CRICKET 50fps (disturbed)
# LIVE_URL = "http://best.asiantv.co.uk:80/testttt/XJWNzrGnV4HH/657" # SONY TEN 1 50fps
LIVE_URL = "http://best.asiantv.co.uk:80/testttt/XJWNzrGnV4HH/658" # SONY TEN 2 50fps

# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/357058.ts" # SELECT 1 50fps (OTHER IPTV) - sometimes more reliable than best.asiantv
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/357057.ts" # SELECT 2 25fps (OTHER IPTV)
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/459892.ts" # Fox Cricket 50fps
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/21299.ts" # WILLOW
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/41200.ts" # WILLOW 2
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/357089.ts" # TEN 1
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/357087.ts" # TEN 1
LIVE_URL = "https://best-streams.tv//live/97850877/39590786/357086.ts" # TEN 2
# LIVE_URL = "https://best-streams.tv//live/97850877/39590786/356874.ts" # TEN 2 50tbr

# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/2318.ts" # SELECT 1 25fps
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/2319.ts" # SELECT 2 25fps
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/1896.ts" # VARIETY 2
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/2105.ts" # Fox Cricket 50fps
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/1879.ts" # Astro Cricket 50fps
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/2889308.ts" # Sky Sports NZ UHD
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/724038.ts" # WILLOW
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/724039.ts" # WILLOW 2
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/1566414.ts" # TEN 1
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/2411.ts" # TEN 2
# LIVE_URL = "https://simba2000.org/live/RJJordan6488/aGtVwCbNhg/2342519.ts" # KAYO2 UHD


# ======================================================================================================================


# ==================== CONFIG FOR N_m3u8DL-RE DOWNLOAD  ===================================================================

# N_M3U8DL CONFIG (if DOWNLOAD_MODE == "nm3u8dl")
# Part A: Dynamic per-source (URL + headers + keys)
# TEN1
# NM3U8DL_PART_A = 'N_m3u8DL-RE "https://ottlive.dishhome.com.np/protected/hgTOzZkB0RDJ74Ryniuo/dash/manifest.mpd" -H "Accept: */*" -H "Origin: https://www.dishhomego.com.np" -H "Referer: https://www.dishhomego.com.np/" -H "Sec-GPC: 1" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" -H "deviceid: mizx3psj-16ys0e" --key 62747f52ec004ad1917ca0bfc6aca227:7b645068423dff890dacfb89d147959f --key f569dfc7b7284f59998b0dda60336bd8:15e67d65b4cc7670471e6e4aedbe1b35 --use-shaka-packager'

# TEN2
# NM3U8DL_PART_A = 'N_m3u8DL-RE "https://ottlive.dishhome.com.np/protected/hwTOzZkB0RDJ74Ryniuo/dash/manifest.mpd" -H "Accept: */*" -H "Origin: https://www.dishhomego.com.np" -H "Referer: https://www.dishhomego.com.np/" -H "Sec-GPC: 1" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" -H "deviceid: mizx3psj-16ys0e" --key 4b97896105a843968d423d19ace1a168:d5dc232816c06aa316d1e5f3a96b1043 --key 64bca661f75346d5b99d5a516e99adf9:141f8b12c8414aeb2864d8df2c519098 --use-shaka-packager'

# 7AU
# NM3U8DL_PART_A = 'N_m3u8DL-RE --custom-proxy "http://b01yr39q3b:dmmrxlltij@46.203.126.63:7777"  "https://csm-e-cesevextprdausw2live-066c0421d9fce3fab.bln1.yospace.com/csm/extlive/sevenprd01,ADE1CT.m3u8?yo.eb.bp=flat&appId=7plus&deviceType=web&platformType=web&ppId=cd7879b06cb4f677c1646ab19f231ae4d8763ff04bafe729c7f810cfe5169dbb&videoType=live&accountId=5650355166001&advertId=null&uaId=cd7879b06cb4f677c1646ab19f231ae4d8763ff04bafe729c7f810cfe5169dbb&optinDeviceType=&optinAdTracking=0&tvid=8de136859112468c9dd916a6052ba74b&pc=5000&deviceId=fb3338d5-8826-49b2-91db-dc87eaa4ed01&mstatus=true&hl=en&ozid=5a15f68d-952c-427a-bc65-20169a3a7b49&deviceSubType=desktop&referenceId=ADE1MPL&vid=6363897109112&yo.hb=5000&pp=csai-web&custParams=y%253D6%2526c%253Dn%2526dpc%253D3205%2526oi1%253Dcccd520d-2f07-3dea-17d0-8210a2dac07d%2526od1%253DA6%2526ois%253Dd4addaab-1cec-7daa-7272-9db5e15526f5%2526ouc%253D1&y=6&c=n&dpc=3205&sessionid=ZHQtd2Vi_Y2ktMEhOSFEyREZOMVVDNzowMDAwMDAyMg_ZGktZmIzMzM4ZDUtODgyNi00OWIyLTkxZGItZGM4N2VhYTRlZDAx_dWktOGU0MWM4YjJjOWJkNDI1MDk0OWY5N2QxN2JiYzk2ZmU_ci0w&yo.pp=c2Vzc2lvbmlkPVpIUXRkMlZpX1kya3RNRWhPU0ZFeVJFWk9NVlZETnpvd01EQXdNREF5TWdfWkdrdFptSXpNek00WkRVdE9EZ3lOaTAwT1dJeUxUa3haR0l0WkdNNE4yVmhZVFJsWkRBeF9kV2t0T0dVME1XTTRZakpqT1dKa05ESTFNRGswT1dZNU4yUXhOMkppWXprMlptVV9jaTB3JmhkbnRzPXN0PTE3NjU2OTc5Nzl-ZXhwPTE3NjU3MjY3MDV-YWNsPS8qfmlkPVpIUXRkMlZpX1kya3RNRWhPU0ZFeVJFWk9NVlZETnpvd01EQXdNREF5TWdfWkdrdFptSXpNek00WkRVdE9EZ3lOaTAwT1dJeUxUa3haR0l0WkdNNE4yVmhZVFJsWkRBeF9kV2t0T0dVME1XTTRZakpqT1dKa05ESTFNRGswT1dZNU4yUXhOMkppWXprMlptVV9jaTB3fmhtYWM9NjYzMjllNjQwOGIyMTA1MDVmMTU4YzE1N2M0MGIxNjYwMTMxY2FhYTNjMDMyMTUyYzVhNmMyYzNkODM0OTBlNSZQb2xpY3k9ZXlKVGRHRjBaVzFsYm5RaU9sdDdJbEpsYzI5MWNtTmxJam9pYUhSMGNITTZMeThxWEZ3fktuTmxjM05wYjI1cFpEMWFTRkYwWkRKV2FWOVpNbXQwVFVWb1QxTkdSWGxTUlZwUFRWWldSRTU2YjNkTlJFRjNUVVJCZVUxblgxcEhhM1JhYlVsNlRYcE5ORnBFVlhSUFJHZDVUbWt3TUU5WFNYbE1WR3Q0V2tkSmRGcEhUVFJPTWxab1dWUlNiRnBFUVhoZlpGZHJkRTlIVlRCTlYwMDBXV3BLYWs5WFNtdE9SRWt4VFVSck1FOVhXVFZPTWxGNFRqSkthVmw2YXpKYWJWVmZZMmt3ZHlvaUxDSkRiMjVrYVhScGIyNGlPbnNpUkdGMFpVeGxjM05VYUdGdUlqcDdJa0ZYVXpwRmNHOWphRlJwYldVaU9qRTNOalUzTWpZM01EVjlMQ0pFWVhSbFIzSmxZWFJsY2xSb1lXNGlPbnNpUVZkVE9rVndiMk5vVkdsdFpTSTZNVGMyTlRZNU56azNPSDE5ZlYxOSZTaWduYXR1cmU9Tkw3VVFUcEx5UVF5OTZpMGJ0cXg5aGJVUWdmTzBsb1Y1OVdEU0F5fnE0R2FIYldWdERKd3J3QmVUczJ1eUMzLUc5V3VqYWhndnJQYlJqTmd4ZTdBR2lxcXRkVFg4dXlhRzZQODFNcDhiUDFIekt3fkVacERkNGJOdTlpOHZwSXF6eW1mUmRZN25BcGxRdWZJRncyNllmSDBTUFcxcWtzM0ZvZllGdHlraVJFa2EycENMMkNkWjFwdWhUd3NjfllHbS1aR0t3amF4cUZpeEZ2cU9uTnVKM0NRZmR4NzRwVU9Ya25Td0MtYzd5SkZPNDdxVTJQNW9GZ0owclhGdFhOTlIxY2Y4QkhKMS1lRFVrQndqaWRhclVMMVdEYlZ4NUI5UTk3ZEJQT345ZFhNfnJhRXNiV2tUZTNVY29PVVpGQlc1cHE1RGNqbkpmc25Eb1FOcmhyQUR3X18mS2V5LVBhaXItSWQ9QVBLQUlPVDRNNktONkNRT0FXRVE&&yo.oh=Y3NtLWUtc2V2ZW5leHRwcmRsaXZlLWViLmJsbjEueW9zcGFjZS5jb20=" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" -H "Accept: */*" -H "Sec-GPC: 1" -H "Origin: null" -H "Referer: https://7plus.com.au/" --key 41e535ac332631a2a14c7f16e15a9cc8:27c134cb6c9631c6d682570ee74329be --use-shaka-packager'

# 7mate
#NM3U8DL_PART_A = 'N_m3u8DL-RE --custom-proxy "http://b01yr39q3b:dmmrxlltij@46.203.126.63:7777"  "https://csm-e-sevenextprdlive-eb.bln1.yospace.com/csm/extlive/sevenprd01,ADE3.m3u8?appId=7plus&deviceType=web&platformType=web&ppId=cd7879b06cb4f677c1646ab19f231ae4d8763ff04bafe729c7f810cfe5169dbb&videoType=live&accountId=5650355166001&advertId=null&uaId=cd7879b06cb4f677c1646ab19f231ae4d8763ff04bafe729c7f810cfe5169dbb&optinDeviceType=&optinAdTracking=0&tvid=8de136859112468c9dd916a6052ba74b&pc=5000&deviceId=fb3338d5-8826-49b2-91db-dc87eaa4ed01&mstatus=true&hl=en&ozid=0a47c7d2-9151-4eed-9394-545dbf243083&deviceSubType=desktop&referenceId=ADE3MPL&vid=6363901713112&yo.hb=5000&pp=csai-web&custParams=y%253D6%2526c%253Dn%2526dpc%253D3205%2526oi1%253Dcccd520d-2f07-3dea-17d0-8210a2dac07d%2526od1%253DA6%2526ois%253Dd4addaab-1cec-7daa-7272-9db5e15526f5%2526ouc%253D1&y=6&c=n&dpc=3205&yo.pp=aGRudHM9c3Q9MTc2NTY5OTk1MX5leHA9MTc2NTcyODcxOX5hY2w9Lyp-aG1hYz05NTAyMjU1MDFkODExNzQ2YWZiMTZjZGViYWEwMTg4MTJlNzYxZGMzOTYxOTE4OGQxMzk2ZTA4MTYyNjM5MmM2JlBvbGljeT1leUpUZEdGMFpXMWxiblFpT2x0N0lrTnZibVJwZEdsdmJpSTZleUpFWVhSbFRHVnpjMVJvWVc0aU9uc2lRVmRUT2tWd2IyTm9WR2x0WlNJNk1UYzJOVGN5T0RjeE9YMHNJa1JoZEdWSGNtVmhkR1Z5VkdoaGJpSTZleUpCVjFNNlJYQnZZMmhVYVcxbElqb3hOelkxTmprNU9UVXdmWDE5WFgwXyZTaWduYXR1cmU9am1-a1BLZEd4YnNwWk5uYWlFbm1jODdKeVJ1Sm9UcEZYSGFQVFk1eXZ4V3ZVdU5BVm56ekdTSldMZVNneWVqMjJ6c3RnUkVETXo2flpNeFVhTmlzVG1ZUHUtUnpTfnVlNm54QmNiZi11fjRyZm5iV3IyWFJTUnpWdlJUbzVFOGhiaHNIRmoyNjdQaWxrTFhJUURFQWJEajhpMFVWM0MwcnZiY0lsU3BxVm1kN2ZRNVRqTlNmREFjS1R5b1dQTEIwUFpEQm5VeDAxdmRJSkFSajhXQllQNHVITktlVUl3NHgyeHRHUlFrMU5Ic1pZUFR2RkluUnZEcXRoQWxsMzRQNXpCZ0VFVUpndDJ6Zi1lU3RacW1-UFdENHFTSjlhcnhRUUVlfllEQTdITFh-SThzSUlaT3ZUZHZ1QzFSeFMwRkVKQ3VITWNKcTh1ZUlwd3JNay16SVlBX18mS2V5LVBhaXItSWQ9QVBLQUlPVDRNNktONkNRT0FXRVE&" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" -H "Accept: */*" -H "Sec-GPC: 1" -H "Origin: null" -H "Referer: https://7plus.com.au/" --key 41e535ac332631a2a14c7f16e15a9cc8:27c134cb6c9631c6d682570ee74329be --use-shaka-packager'


# FOR TEST
NM3U8DL_PART_A = 'N_m3u8DL-RE --custom-proxy "http://b01yr39q3b:dmmrxlltij@46.203.126.63:7777" "https://csm-e-sevenextprdlive-eb.bln1.yospace.com/csm/extlive/sevenprd01,ADE1CT.m3u8?yo.eb.bp=flat&appId=7plus&deviceType=web&platformType=web&ppId=cd7879b06cb4f677c1646ab19f231ae4d8763ff04bafe729c7f810cfe5169dbb&videoType=live&accountId=5650355166001&advertId=null&uaId=cd7879b06cb4f677c1646ab19f231ae4d8763ff04bafe729c7f810cfe5169dbb&optinDeviceType=&optinAdTracking=0&tvid=8de136859112468c9dd916a6052ba74b&pc=5000&deviceId=fb3338d5-8826-49b2-91db-dc87eaa4ed01&mstatus=true&hl=en&ozid=5a15f68d-952c-427a-bc65-20169a3a7b49&deviceSubType=desktop&referenceId=ADE1MPL&vid=6363897109112&yo.hb=5000&pp=csai-web&custParams=y%253D6%2526c%253Dn%2526dpc%253D3205%2526oi1%253Dcccd520d-2f07-3dea-17d0-8210a2dac07d%2526od1%253DA6%2526ois%253Dd4addaab-1cec-7daa-7272-9db5e15526f5%2526ouc%253D1&y=6&c=n&dpc=3205&sessionid=ZHQtd2Vi_Y2ktMEhOSFEyREZOMVVDNzowMDAwMDAyMg_ZGktZmIzMzM4ZDUtODgyNi00OWIyLTkxZGItZGM4N2VhYTRlZDAx_dWktOGU0MWM4YjJjOWJkNDI1MDk0OWY5N2QxN2JiYzk2ZmU_ci0w&yo.pp=c2Vzc2lvbmlkPVpIUXRkMlZpX1kya3RNRWhPU0ZFeVJFWk9NVlZETnpvd01EQXdNREF5TWdfWkdrdFptSXpNek00WkRVdE9EZ3lOaTAwT1dJeUxUa3haR0l0WkdNNE4yVmhZVFJsWkRBeF9kV2t0T0dVME1XTTRZakpqT1dKa05ESTFNRGswT1dZNU4yUXhOMkppWXprMlptVV9jaTB3JmhkbnRzPXN0PTE3NjU2OTc5Nzl-ZXhwPTE3NjU3MjY3MDV-YWNsPS8qfmlkPVpIUXRkMlZpX1kya3RNRWhPU0ZFeVJFWk9NVlZETnpvd01EQXdNREF5TWdfWkdrdFptSXpNek00WkRVdE9EZ3lOaTAwT1dJeUxUa3haR0l0WkdNNE4yVmhZVFJsWkRBeF9kV2t0T0dVME1XTTRZakpqT1dKa05ESTFNRGswT1dZNU4yUXhOMkppWXprMlptVV9jaTB3fmhtYWM9NjYzMjllNjQwOGIyMTA1MDVmMTU4YzE1N2M0MGIxNjYwMTMxY2FhYTNjMDMyMTUyYzVhNmMyYzNkODM0OTBlNSZQb2xpY3k9ZXlKVGRHRjBaVzFsYm5RaU9sdDdJbEpsYzI5MWNtTmxJam9pYUhSMGNITTZMeThxWEZ3fktuTmxjM05wYjI1cFpEMWFTRkYwWkRKV2FWOVpNbXQwVFVWb1QxTkdSWGxTUlZwUFRWWldSRTU2YjNkTlJFRjNUVVJCZVUxblgxcEhhM1JhYlVsNlRYcE5ORnBFVlhSUFJHZDVUbWt3TUU5WFNYbE1WR3Q0V2tkSmRGcEhUVFJPTWxab1dWUlNiRnBFUVhoZlpGZHJkRTlIVlRCTlYwMDBXV3BLYWs5WFNtdE9SRWt4VFVSck1FOVhXVFZPTWxGNFRqSkthVmw2YXpKYWJWVmZZMmt3ZHlvaUxDSkRiMjVrYVhScGIyNGlPbnNpUkdGMFpVeGxjM05VYUdGdUlqcDdJa0ZYVXpwRmNHOWphRlJwYldVaU9qRTNOalUzTWpZM01EVjlMQ0pFWVhSbFIzSmxZWFJsY2xSb1lXNGlPbnNpUVZkVE9rVndiMk5vVkdsdFpTSTZNVGMyTlRZNU56azNPSDE5ZlYxOSZTaWduYXR1cmU9Tkw3VVFUcEx5UVF5OTZpMGJ0cXg5aGJVUWdmTzBsb1Y1OVdEU0F5fnE0R2FIYldWdERKd3J3QmVUczJ1eUMzLUc5V3VqYWhndnJQYlJqTmd4ZTdBR2lxcXRkVFg4dXlhRzZQODFNcDhiUDFIekt3fkVacERkNGJOdTlpOHZwSXF6eW1mUmRZN25BcGxRdWZJRncyNllmSDBTUFcxcWtzM0ZvZllGdHlraVJFa2EycENMMkNkWjFwdWhUd3NjfllHbS1aR0t3amF4cUZpeEZ2cU9uTnVKM0NRZmR4NzRwVU9Ya25Td0MtYzd5SkZPNDdxVTJQNW9GZ0owclhGdFhOTlIxY2Y4QkhKMS1lRFVrQndqaWRhclVMMVdEYlZ4NUI5UTk3ZEJQT345ZFhNfnJhRXNiV2tUZTNVY29PVVpGQlc1cHE1RGNqbkpmc25Eb1FOcmhyQUR3X18mS2V5LVBhaXItSWQ9QVBLQUlPVDRNNktONkNRT0FXRVE&" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" -H "Accept: */*" -H "Sec-GPC: 1" -H "Origin: null" -H "Referer: https://7plus.com.au/" --key b5b4358467dc35b6be6a9a07e3ada12e:b54c19acdb2cfb1336c57ee81fd689ab --use-shaka-packager'

# Part B: Static options (appended to command with dynamic chunk name)
NM3U8DL_PART_B = '-M format=ts --live-real-time-merge --live-pipe-mux --download-retry-count 30 --http-request-timeout 90 --select-video best --select-audio best'

# Monitoring thresholds
NM3U8DL_SLOW_CHECK_THRESHOLD = 3   # consecutive slow checks before restart
NM3U8DL_SPEED_DEGRADATION_FACTOR = 0.05  # consider stalling if speed drops to ~5% of expected (300-400 Kbps range)
# ======================================================================================================================




# Optional scheduling
# SCHEDULE_START   = "2025-12-14 15:50"     # e.g. "2025-12-09 13:30"; empty string = start immediately
SCHEDULE_START   = ""
RUN_DURATION_MIN = 300   # e.g. 180 for 3 hours, or None for "run until stopped"
# RUN_DURATION_MIN = None

# BASE_NAME = "IND v SA 3rd T20I LIVE FULL MATCH Fox Cricket IPTV2"
# BASE_NAME = "2025-26 FIH Hockey Pro League M12 ARG v PAK LIVE FULL MATCH Star Sports Select1 1080p50fps IPTV3"
BASE_NAME = "Under-19s Asia Cup 202526 M08 LIVE SONY TEN2 IPTV2"
# BASE_NAME = "BBL 2025 M01 PS v SS LIVE 7AU"
# BASE_NAME = "TEST"





# These will be initialized later, after wait_until_start()
run_ts = None
FINAL_FILE = None
final_base = None
CHUNKS_DIR = None
LIST_FILE = None
TERMCAP_PATH = None

FFMPEG_PROGRESS_PERIOD = 1   # seconds
STABILITY_SEC = 15          # minimum good duration in seconds
BLACK_LEN = 1.0             # use only integers
stop_flag = False
chunk_index = 0             # chunk_001.ts, chunk_002.ts, ...
best_w = 0
best_h = 0
best_fps = 0
same_params = True  # assume all GOOD chunks share same params
# N_m3u8DL monitoring globals
nm3u8dl_selected_bitrate = 0  # will be set from stdout parsing
nm3u8dl_stall_flag = False
manifest_fail_count = 0      # NEW - for scenarios 2,4 (bitrate==0)
stall_recovery_count = 0     # NEW - for real stalls (bitrate>0, growth==0)
nm3u8dl_stop_event = None

start_time = time.time()

stats = {
    "process_start": None,
    "process_end": None,
    "good_chunks": 0,
    "bad_chunks": 0,
    "good_time": 0.0,      # sum of GOOD chunk durations (seconds)
    "min_chunk": None,
    "max_chunk": None,
    "sessions": [],        # list of dicts: {"start": ts, "dur": dur}
    "last_good_br_kbps": None,
}

class WindowsInhibitor:
    ES_CONTINUOUS       = 0x80000000
    ES_SYSTEM_REQUIRED  = 0x00000001

    def inhibit(self):
        ctypes.windll.kernel32.SetThreadExecutionState(
            self.ES_CONTINUOUS | self.ES_SYSTEM_REQUIRED
        )

    def uninhibit(self):
        ctypes.windll.kernel32.SetThreadExecutionState(
            self.ES_CONTINUOUS
        )

def log(*args, **kwargs):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = " ".join(str(a) for a in args)
    line = f"{ts} {msg}"
    print(line, **kwargs)
    termcap_write(line)

def ensure_chunks_dir():
    os.makedirs(CHUNKS_DIR, exist_ok=True)

def init_termcap():
    """Create/overwrite the temp terminal capture log inside CHUNKS_DIR."""
    global TERMCAP_PATH
    ensure_chunks_dir()
    TERMCAP_PATH = os.path.join(CHUNKS_DIR, "_terminal_capture.tmp.log")
    try:
        with open(TERMCAP_PATH, "w", encoding="utf-8", errors="replace") as _:
            pass
    except Exception:
        TERMCAP_PATH = None

def termcap_write(full_terminal_line: str):
    """Write EXACTLY what was printed to terminal (already timestamped)."""
    if not TERMCAP_PATH or not full_terminal_line:
        return
    try:
        with open(TERMCAP_PATH, "a", encoding="utf-8", errors="replace") as f:
            f.write(full_terminal_line if full_terminal_line.endswith("\n") else full_terminal_line + "\n")
    except Exception:
        pass

def append_termcap_to_summarylog(summary_path: str) -> int:
    if not TERMCAP_PATH or not os.path.exists(TERMCAP_PATH):
        return 0

    appended = 0
    with open(summary_path, "a", encoding="utf-8", errors="replace") as out:
        out.write("\n\n")
        out.write("====================================================================\n")
        out.write("TERMINAL OUTPUT (captured during run)\n")
        out.write("====================================================================\n")

        with open(TERMCAP_PATH, "r", encoding="utf-8", errors="replace") as inp:
            while True:
                buf = inp.read(1024 * 1024)
                if not buf:
                    break
                out.write(buf)
                appended += len(buf)

    return appended
        
def beep_bad():
    # Three short soft beeps: bip bip bip
    freq = 500  # Hz
    dur = 200   # ms
    gap = 600    # ms between beeps
    for _ in range(3):
        winsound.Beep(freq, dur)
        time.sleep(gap / 1000.0)

def beep_good():
    # One longer soft beep: beeeeep
    winsound.Beep(700, 600)  # 800 Hz for 0.6s

def alarm_critical():
    """
    CRITICAL ALARM: Loud beeping (10 seconds) + blocking message box.
    User MUST click OK to dismiss. Guarantees attention.
    Used when recovery fails after 2 attempts.
    """
    # Sound alarm: 20 beeps × 0.5s each = 10 seconds of loud noise
    for _ in range(20):
        winsound.Beep(1000, 500)  # 1000 Hz (high pitch), 500ms duration
        time.sleep(0.1)  # 100ms gap between beeps
    
    # Pop up blocking message box - user MUST click OK to continue
    ctypes.windll.user32.MessageBoxW(0,
        "CRITICAL: Download recovery failed after 2 attempts.\n\n"
        "Cannot recover from stall - manifest may have expired or token invalid.\n\n"
        "Finalizing recording with downloaded content.\n\n"
        "Click OK to proceed.",
        "STREAM DOWNLOAD FAILED",
        0x10)  # MB_ICONHAND = stop sign icon

def run_ffmpeg_with_capture(cmd, cwd, tag="FFmpeg"):
    import threading
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    last_progress_line = None
    progress_line_active = False
    kv = {}

    def monitor_thread():
        nonlocal last_progress_line, progress_line_active, kv
        try:
            while True:
                line = proc.stderr.readline()
                if not line:
                    break
                s = line.strip()
                m = re.match(r'^([A-Za-z0-9_]+)=(.*)$', s)
                if m:
                    k, v = m.group(1), m.group(2)
                    kv[k] = v
                    if k == "progress":
                        parts = []
                        for key in ("frame", "fps", "total_size", "out_time", "bitrate", "speed"):
                            if key in kv:
                                label = "time" if key == "out_time" else ("size" if key == "total_size" else key)
                                parts.append(f"{label}={kv[key]}")
                        prog = " ".join(parts)
                        if prog:
                            sys.stdout.write("\r" + prog + " " * 80)
                            sys.stdout.flush()
                            progress_line_active = True
                            last_progress_line = prog
                        kv = {}
                    continue
                if progress_line_active:
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    progress_line_active = False
                if s:
                    log(f"{tag}: {s}")
        except Exception as e:
            log(f"{tag} monitor error: {e}")

    t = threading.Thread(target=monitor_thread, daemon=True)
    t.start()
    
    rc = proc.wait()
    
    try:
        t.join(timeout=3)
    except:
        pass
    
    if progress_line_active:
        sys.stdout.write("\n")
        sys.stdout.flush()
    if last_progress_line:
        log(f"{tag}: {last_progress_line}")
    return rc

    
def fmt_hms(seconds):
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    else:
        return f"{m:02d}:{s:02d}"

def is_stream_alive():
    try:
        # Try to read a very short snippet with ffprobe (or ffmpeg -t 1 -f null -)
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width",
                "-of", "csv=p=0",
                LIVE_URL,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False
     
def monitor_nm3u8dl_stdout(proc, refresh_interval=60):
    """
    Monitor N_m3u8DL: capture stream info, log progress once per refresh interval.
    Logs all startup info until "Save Name", then switches to progress-only mode.
    """
    last_log_time = time.time()
    latest_progress = {}
    log_interval = refresh_interval  # Once per refresh interval
    
    startup_complete = False
    
    log(f"N_m3u8DL: Monitoring interval set to {refresh_interval}s")
    
    try:
        while proc.poll() is None:
            line = proc.stdout.readline() if proc.stdout else ""
            if not line:
                time.sleep(0.1)
                continue
            
            # **PHASE 1: Log only key startup info until "Mux with named pipe"**
            if not startup_complete:
                # Log ONLY these specific lines:
                # - Lines starting with "Extracted" or "Live stream" or "Selected streams"
                # - Lines with resolution info (Vid/Aud streams with bitrate info)
                # - Save Name and Mux with named pipe
                
                is_stream_line = ("Vid " in line or "Aud " in line) and "Kbps" in line and "Segments" in line
                is_key_line = any(keyword in line for keyword in [
                    "Extracted",
                    "Live stream",
                    "Selected streams",
                    "Save Name",
                    "Mux with named pipe"
                ])
                
                if is_stream_line or is_key_line:
                    # Strip timestamp prefix from N_m3u8DL output
                    stripped_line = line.strip()
                    if " INFO " in stripped_line or " WARN " in stripped_line:
                        stripped_line = re.sub(r'^\d{2}:\d{2}:\d{2}\.\d{3}\s+', '', stripped_line)
                    log(f"N_m3u8DL: {stripped_line}")
                    if "Mux with named pipe" in line:
                        startup_complete = True
            
            # **PHASE 2: Log progress only (after startup complete)**
            if startup_complete:
                # Store latest progress lines (both Vid and Aud)
                if ("Vid " in line or "Aud " in line) and "Kbps" in line and "%" in line:
                    # Only log if it's actual download progress (not 0% or empty lines)
                    if "0% 0.00Bps" not in line and ("Waiting" in line or "Recording" in line):
                        if "Vid " in line:
                            latest_progress['vid'] = line.strip()
                        if "Aud " in line:
                            latest_progress['aud'] = line.strip()
                
                # Log latest progress every refresh interval
                now = time.time()
                if now - last_log_time >= log_interval:
                    if latest_progress.get('vid'):
                        log(f"N_m3u8DL: {latest_progress['vid']}")
                    if latest_progress.get('aud'):
                        log(f"N_m3u8DL: {latest_progress['aud']}")
                    last_log_time = now
            
            time.sleep(0.01)
    except Exception as e:
        log(f"N_m3u8DL stdout monitor error: {e}")



def monitor_nm3u8dl_file_growth(chunk_path, stop_event, check_interval=60):
    """
    Monitor chunk file growth for stalls.
    
    Args:
        chunk_path: path to chunk file to monitor
        check_interval: how often to check file growth (seconds)
    """
    global nm3u8dl_stall_flag
    prev_size = 0
    slow_check_count = 0
    
    stall_threshold_kbps = nm3u8dl_selected_bitrate * NM3U8DL_SPEED_DEGRADATION_FACTOR
    
    log(f"N_m3u8DL: Stall threshold set to {stall_threshold_kbps:.0f} Kbps")
    
    while not stop_event.is_set() and not stop_flag:
        #time.sleep(check_interval)  # use dynamic interval
        if stop_event.wait(timeout=check_interval):
            break
         # If file hasn't been created yet, wait
        if not os.path.exists(chunk_path):
            continue
            
        try:
            current_size = os.path.getsize(chunk_path)
            
            # Guard: file was truncated/recreated/replaced
            if current_size < prev_size:
                log(f"N_m3u8DL: File size went backwards {prev_size} -> {current_size} (reset baseline)")
                prev_size = current_size
                slow_check_count = 0
                continue
                
            growth_bytes = current_size - prev_size
            growth_kbps = (growth_bytes / check_interval) * 8 / 1000
            
            if growth_kbps < stall_threshold_kbps:
                slow_check_count += 1
                max_checks = NM3U8DL_SLOW_CHECK_THRESHOLD 
                log(f"N_m3u8DL: Slow check {slow_check_count}/{max_checks} - speed {growth_kbps:.0f} Kbps (threshold {stall_threshold_kbps:.0f})")
                
                if slow_check_count >= max_checks:
                    log(f"N_m3u8DL: Stall detected ({slow_check_count} consecutive slow checks) → setting stall flag")
                    nm3u8dl_stall_flag = True
                    break
            else:
                slow_check_count = 0  # reset on good speed
                log(f"N_m3u8DL: Good speed {growth_kbps:.0f} Kbps")
            
            prev_size = current_size
        
        except Exception as e:
            log(f"N_m3u8DL file growth monitor error: {e}")
            break
           
    log("N_m3u8DL: File growth monitor exiting")


def extract_nm3u8dl_startup_info(proc):
    """
    Read N_m3u8DL stdout in ONE PASS until refresh interval is found.
    Returns dict with: bitrate, refresh_interval, and logs stream info along the way.
    """
    bitrate = 0  # fallback
    refresh = 0    # fallback
    in_selected_section = False
    
    try:
        for _ in range(500):  # read up to 500 lines in one pass
            line = proc.stdout.readline() if proc.stdout else ""
            if not line:
                time.sleep(0.01)
                continue
            
            # Log stream extraction/selection info as we see it
            if any(kw in line for kw in ["Extracted", "Vid", "Aud", 
                                          "Live stream", "Selected streams", "Save Name", "Mux with"]):
                # Strip the timestamp prefix (HH:MM:SS.mmm) from N_m3u8DL output
                stripped_line = line.strip()
                if " INFO " in stripped_line or " WARN " in stripped_line:
                    # Remove timestamp: "15:36:50.777 INFO :" → "INFO :"
                    import re
                    stripped_line = re.sub(r'^\d{2}:\d{2}:\d{2}\.\d{3}\s+', '', stripped_line)
                log(f"N_m3u8DL: {stripped_line}")

            
            # Track when we enter "Selected streams:" section
            if "Selected streams:" in line:
                in_selected_section = True
            
            # Extract bitrate ONLY from selected VIDEO stream (ignore audio)
            if in_selected_section and "Vid " in line and "Kbps" in line and "Segments" in line:
                parts = line.split("|")
                if len(parts) >= 2:
                    try:
                        bitrate = int(parts[1].strip().split()[0])
                        log(f"N_m3u8DL: Selected bitrate detected: {bitrate} Kbps")
                    except:
                        pass
            
            # Extract refresh interval when we see it
            if "set refresh interval to" in line.lower():
                import re
                match = re.search(r'set refresh interval to\s+(\d+)\s+seconds', line, re.IGNORECASE)
                if match:
                    try:
                        refresh = int(match.group(1))
                        log(f"N_m3u8DL: Refresh interval detected: {refresh} seconds")
                        # STOP after finding refresh - we have what we need
                        break
                    except:
                        pass
    except Exception as e:
        log(f"Error reading N_m3u8DL startup: {e}")
    
    return {'bitrate': bitrate, 'refresh_interval': refresh}



def start_nm3u8dl_to_chunk():
    """
    Start N_m3u8DL-RE process with monitoring threads.
    Detects crashes via file growth stalls.
    Returns (chunk_path, chunk_name) when process ends.
    """
    global nm3u8dl_stall_flag, nm3u8dl_selected_bitrate, stop_flag
    
    chunk_path, chunk_name = next_chunk_names()
    
    # Reset flags for this run
    nm3u8dl_stall_flag = False
    
    stats["last_run_start"] = time.time()
    
    # Build full command: Part_A + save-name + Part_B
    chunk_name_without_ext = chunk_name.replace('.ts', '')
    cmd = f'{NM3U8DL_PART_A} --save-name "{chunk_name_without_ext}" {NM3U8DL_PART_B}'

    log(f"Starting N_m3u8DL → writing to {chunk_name}...")
    log(f"Command: {cmd}")
    
    # Start process with stdout capture
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=CHUNKS_DIR
    )
    
    # Extract bitrate AND refresh interval AND startup info in ONE PASS
    startup_data = extract_nm3u8dl_startup_info(proc)
    nm3u8dl_selected_bitrate = startup_data['bitrate']
    refresh_interval = startup_data['refresh_interval']
    # startup_data also contains the stream lines already logged

    # IMMEDIATELY after extract_nm3u8dl_startup_info()
    if refresh_interval == 0 or nm3u8dl_selected_bitrate == 0:
        log("No stream/manifest → fail immediately")
        proc.terminate()
        return chunk_path, chunk_name
    
    # Start monitoring threads
    stop_event = threading.Event()
    
    global nm3u8dl_stop_event
    nm3u8dl_stop_event = stop_event

    stdout_thread = threading.Thread(target=monitor_nm3u8dl_stdout, args=(proc, refresh_interval), daemon=True)
    stdout_thread.start()
    
    file_growth_thread = threading.Thread(target=monitor_nm3u8dl_file_growth, args=(chunk_path, stop_event, refresh_interval), daemon=True)
    file_growth_thread.start()
    
    # Main waiting loop
    start_run = time.time()
    good_beep_done = False
    
    while True:
        ret = proc.poll()
        
        # Check for crash/stall signals
        if nm3u8dl_stall_flag:
            reason = "file growth stall"
            log(f"N_m3u8DL: {reason} detected → terminating process...")
            stop_event.set()
            beep_bad()
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log("N_m3u8DL did not terminate gracefully, killing...")
                proc.kill()
                proc.wait()
            break
        
        # Check if process exited naturally
        if ret is not None:
            log(f"N_m3u8DL exited with code {ret}")
            stop_event.set()
            break
        
        # Check if max duration reached
        if RUN_DURATION_MIN is not None:
            if time.time() - start_time >= RUN_DURATION_MIN * 60:
                log(f"Max duration reached → terminating N_m3u8DL...")
                stop_flag = True
                stop_event.set()
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                break
        
        # Check if user pressed Ctrl-C
        if stop_flag:
            log(f"stop_flag detected → terminating N_m3u8DL...")
            stop_event.set()
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            break
        
        # Beep after 30s
        if not good_beep_done and (time.time() - start_run) >= 30:
            beep_good()
            good_beep_done = True
        
        time.sleep(0.5)
    
    log("N_m3u8DL stopped for this run")
    nm3u8dl_stop_event = None
    return chunk_path, chunk_name


def get_file_info(path):
    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_entries", "format=duration,bit_rate",
                path,
            ],
            timeout=5,
        ).decode()
        data = json.loads(out)["format"]
        dur = float(data.get("duration", 0))
        br = int(data.get("bit_rate", 0)) / 1000
        return dur, br
    except:
        return 0, 0

def get_video_params(path):
    """
    Return (width, height, fps) from a video file.
    Falls back to 1920x1080@50 if probe fails.
    """
    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,avg_frame_rate,r_frame_rate",
                "-of", "json",
                path,
            ],
            timeout=5,
        ).decode()
        data = json.loads(out)["streams"][0]
        w = int(data.get("width", 1920))
        h = int(data.get("height", 1080))
       
        fps_str = data.get("avg_frame_rate", data.get("r_frame_rate", "50/1"))  # default 50fps
        
        num, den = fps_str.split("/")
        fps = int(round(float(num) / float(den)))
        return w, h, fps
    except:
        return 1920, 1080, 50
        
def next_chunk_names():
    """Return the name/path for the next chunk number WITHOUT incrementing."""
    ensure_chunks_dir()
    name = f"chunk_{chunk_index + 1:03d}.ts"
    path = os.path.join(CHUNKS_DIR, name)
    return path, name
    
def start_ffmpeg_to_chunk():
    """
    Start one FFmpeg run that writes directly to the 'next' chunk_NNN.ts.
    Does NOT increment chunk_index yet.
    Also checks if max duration is reached and terminates if needed.
    """
    global stop_flag
    
    chunk_path, chunk_name = next_chunk_names()
    
    # record when this recording attempt started
    stats["last_run_start"] = time.time()

    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "info",
        "-hide_banner",

        # Input/network behavior (must be BEFORE -i)
        "-rw_timeout", "15000000",
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_at_eof", "1",
        "-reconnect_delay_max", "10",

        "-nostats",
        "-progress", "pipe:2",
        "-stats_period", str(FFMPEG_PROGRESS_PERIOD),
        
        "-i", LIVE_URL,
        
        # Explicit stream selection:
        # - Take all video streams
        # - Take all audio streams
        # - But exclude MP2 audio (and mp2float if it appears)
        "-map", "0:v",
        "-map", "0:a?",
        "-map", "-0:a:m:codec:mp2",
        "-map", "-0:a:m:codec:mp2float",

        # Output behavior (unchanged)
        "-c", "copy",
        "-f", "mpegts",
        chunk_path,
    ]
    log(f"Starting FFmpeg → writing to {chunk_name} until stream dies...")
    start_run = time.time()
    # proc = subprocess.Popen(cmd)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    
    last_progress_line = None
    progress_line_active = False

    def monitor_ffmpeg(p):
        nonlocal last_progress_line, progress_line_active
        kv = {}
        try:
            while True:
                line = p.stderr.readline()
                if not line:
                    break
                s = line.strip()

                # progress key=value blocks
                m = re.match(r'^([A-Za-z0-9_]+)=(.*)$', s)
                if m:
                    k, v = m.group(1), m.group(2)
                    kv[k] = v
                    if k == "progress":
                        # Build a compact single-line status
                        parts = []
                        for key in ("frame", "fps", "total_size", "out_time", "bitrate", "speed"):
                            if key in kv:
                                label = "time" if key == "out_time" else ("size" if key == "total_size" else key)
                                parts.append(f"{label}={kv[key]}")
                        prog = " ".join(parts)

                        if prog:
                            # Show on screen as ONE updating line (no newlines)
                            sys.stdout.write("\r" + prog + " " * 80)
                            sys.stdout.flush()
                            progress_line_active = True
                            last_progress_line = prog

                        kv = {}
                    continue

                # Non-progress line: end the progress line once, then log message
                if progress_line_active:
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    progress_line_active = False

                if s:
                    log(f"FFmpeg: {s}")
        except Exception as e:
            log(f"FFmpeg stderr monitor error: {e}")

    t = threading.Thread(target=monitor_ffmpeg, args=(proc,), daemon=True)
    t.start()

    good_beep_done = False

    # Simple waiting loop with 0.5s steps
    while True:
        ret = proc.poll()
        if ret is not None:
            # FFmpeg finished naturally
            break
        
        # Check if duration limit reached
        if RUN_DURATION_MIN is not None:
            if time.time() - start_time >= RUN_DURATION_MIN * 60:
                log(f"Max duration reached → terminating FFmpeg...")
                stop_flag = True
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    log("FFmpeg did not terminate gracefully, killing...")
                    proc.kill()
                    proc.wait()
                break
        
        # Check if Ctrl-C was pressed
        if stop_flag:
            log(f"stop_flag detected → terminating FFmpeg...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log("FFmpeg did not terminate gracefully, killing...")
                proc.kill()
                proc.wait()
            break

        # FFmpeg still running
        if not good_beep_done and (time.time() - start_run) >= 30:
            beep_good()
            good_beep_done = True

        time.sleep(0.5)
        
    # Drain stderr thread
    try:
        t.join(timeout=3)
    except threading.ThreadError:
        pass
    proc.wait()  # Ensure proc fully done
        
    # Finish the on-screen progress line cleanly (only if it is active)
    if progress_line_active:
        sys.stdout.write("\n")
        sys.stdout.flush()
        progress_line_active = False

    # Log one final progress snapshot into your capture log
    if last_progress_line:
        log(f"FFmpeg: {last_progress_line}")

    log("FFmpeg stopped for this run")
    return chunk_path, chunk_name


def maybe_accept_chunk(chunk_path, chunk_name, context):
    """
    Decide if chunk is good.
    If good: increment chunk_index, keep file, add to list.txt.
    If bad: delete file, DO NOT increment; number is reused next time.
    Returns True if GOOD, False otherwise.
    """
    global chunk_index, best_w, best_h, best_fps, nm3u8dl_selected_bitrate

    if not os.path.exists(chunk_path):
        log(f"{context}: no chunk file found ({chunk_name})")
        #stats["bad_chunks"] += 1
        return False

    dur, br = get_file_info(chunk_path)
    log(f"{context}: {chunk_name} → {dur:.1f}s, {br:.0f}kbps")
    
    # ynamic bitrate threshold (last GOOD chunk)
    if DOWNLOAD_MODE == "nm3u8dl" and nm3u8dl_selected_bitrate > 0:
        # Keep existing nm3u8dl logic (video bitrate known from tool output)
        min_expected_br = nm3u8dl_selected_bitrate * 0.40
    else:
        # ffmpeg mode: learn from the last accepted GOOD chunk (no hardcoded 500)
        last_good = stats.get("last_good_br_kbps")
        min_expected_br = (last_good * 0.40) if last_good else None
    
    bitrate_ok = (br > min_expected_br) if (min_expected_br is not None) else True    
    if dur > STABILITY_SEC and bitrate_ok:
        # Update best resolution/fps from this chunk and track consistency
        global same_params
        w, h, fps = get_video_params(chunk_path)
        log(f"{context}: {chunk_name} params {w}x{h}@{fps}fps")

        if stats["good_chunks"] == 0:
            # first GOOD chunk defines reference params
            best_w, best_h, best_fps = w, h, fps
            log(f"{context}: FIRST video params {best_w}x{best_h}@{best_fps}fps")
        else:
            # if any GOOD chunk differs, mark params as mixed
            if (w, h, fps) != (best_w, best_h, best_fps):
                same_params = False
                log(f"{context}: MISMATCH params {w}x{h}@{fps}fps (ref {best_w}x{best_h}@{best_fps}fps)")

        # For stats we still keep track of best height/fps
        if (h, fps) > (best_h, best_fps):  # prioritize higher height, then fps
            best_w, best_h, best_fps = w, h, fps
            log(f"{context}: NEW BEST video params {best_w}x{best_h}@{best_fps}fps")

        # Stats: good chunk
        stats["good_chunks"] += 1
        
        # Update ffmpeg baseline ONLY after accepting this chunk as GOOD
        stats["last_good_br_kbps"] = br

        # Media duration from file
        dur_media = dur

        # Wall-clock duration of this FFmpeg run
        run_start = stats.get("last_run_start", time.time())
        dur_run = time.time() - run_start

        # For "GOOD time" we want wall-clock FFmpeg running time
        stats["good_time"] += dur_run

        # Min/max based on media duration (what you see in the file)
        if stats["min_chunk"] is None or dur_media < stats["min_chunk"]:
            stats["min_chunk"] = dur_media
        if stats["max_chunk"] is None or dur_media > stats["max_chunk"]:
            stats["max_chunk"] = dur_media

        # Session timeline: store both media and run durations
        stats["sessions"].append({
            "start": run_start,
            "dur_media": dur_media,
            "dur_run": dur_run,
            "w": w,
            "h": h,
            "fps": fps,
            "name": chunk_name,
        })

        
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            if chunk_index > 0:
                # from second GOOD chunk onward, insert black before the new chunk
                black_path = make_black_clip()
                f.write(f"file '{os.path.basename(black_path)}'\n")
            f.write(f"file '{chunk_name}'\n")
            
        chunk_index += 1
        size_mb = os.path.getsize(chunk_path) / (1024 * 1024)
        log(f"{context}: GOOD → keeping {chunk_name} ({size_mb:.1f}MB)")
        return True
    else:
        if not os.path.basename(chunk_name).startswith("black_"):
            stats["bad_chunks"] += 1
        log(f"{context}: BAD → deleting {chunk_name}")
        try:
            send2trash(chunk_path)   # instead of os.remove(chunk_path)
        except FileNotFoundError:
            pass
        return False

def make_black_clip():
    """
    Create a short black clip matching best_w/best_h/best_fps.
    Only created once per run per resolution/fps.
    """
    global best_w, best_h, best_fps

    # Fallback if best_* not yet set
    if best_h == 0 or best_fps == 0:
        bw, bh, bfps = 1920, 1080, 50
    else:
        bw, bh, bfps = best_w, best_h, best_fps

    name = f"black_{bw}x{bh}_{bfps}fps_{int(BLACK_LEN)}s.ts"
    black_path = os.path.join(CHUNKS_DIR, name)

    if os.path.exists(black_path):
        return black_path

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", f"color=black:s={bw}x{bh}:r={bfps}:d={BLACK_LEN}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-f", "mpegts",
        black_path,
    ]
    log(f"Creating black separator clip {name}...")
    subprocess.run(cmd, check=False)
    return black_path

def write_summary_log(dur, finalized=True):
    """
    Write summary log next to FINAL_FILE.
    """
    try:
        summary_path = os.path.splitext(FINAL_FILE)[0] + "_log.log"
        total_runtime = 0.0
        if stats["process_start"] and stats["process_end"]:
            total_runtime = stats["process_end"] - stats["process_start"]
        good_time = stats["good_time"]

        # Time buckets based on wall-clock
        sessions = sorted(stats["sessions"], key=lambda x: x["start"])
        if sessions:
            first_start = sessions[0]["start"]
            # Last session end in wall-clock
            last_end_run = sessions[-1]["start"] + sessions[-1].get("dur_run", 0.0)
        else:
            first_start = stats["process_start"] or 0.0
            last_end_run = stats["process_start"] or 0.0

        # 1) Time downloading GOOD chunks (wall-clock while FFmpeg was running and produced GOOD data)
        time_good = good_time  # already sum of dur_run

        # 2) Overhead: before first FFmpeg run + after last run/concat
        overhead = 0.0
        if stats["process_start"]:
            overhead += max(0.0, first_start - stats["process_start"])
        if stats["process_end"]:
            overhead += max(0.0, stats["process_end"] - last_end_run)

        # 3) Retry / offline / BAD = everything else
        time_retry_offline = max(0.0, total_runtime - time_good - overhead)

        lines = []
        if finalized:
            lines.append(f"Recording summary for {FINAL_FILE}")
        else:
            lines.append(f"Recording summary (NOT finalized - mixed params) for {FINAL_FILE}")
        lines.append("=" * 68)
        lines.append("")
        
        # Extra metadata
        # Determine mode: scheduled vs manual
        mode = "scheduled" if SCHEDULE_START else "manual"
        lines.append(f"Mode              : {mode}")
        if DOWNLOAD_MODE == "nm3u8dl":
            lines.append(f"Download mode     : N_m3u8DL-RE")
        else:
            lines.append(f"Live URL          : {LIVE_URL}")
        if RUN_DURATION_MIN is not None:
            lines.append(f"Planned duration  : {RUN_DURATION_MIN} minutes")
        else:
            lines.append("Planned duration  : until stopped")
        lines.append("")

        lines.append("Overall")
        lines.append("-------")
        if stats["process_start"]:
            lines.append("Process start : " + datetime.fromtimestamp(stats["process_start"]).strftime("%Y-%m-%d %H:%M:%S"))
        if stats["process_end"]:
            lines.append("Process end   : " + datetime.fromtimestamp(stats["process_end"]).strftime("%Y-%m-%d %H:%M:%S"))
        lines.append("Total runtime : " + fmt_hms(total_runtime))
        lines.append("")
        total_media = sum(s.get("dur_media", 0.0) for s in sessions)

        lines.append("Download time")
        lines.append("-------------")
        lines.append("Active download time    : " + fmt_hms(time_good))
        label = "Final file duration          : " if finalized else "Estimated final duration : "
        lines.append(label + fmt_hms(dur))
        lines.append("Media downloaded        : " + fmt_hms(total_media))
        lines.append("Download efficiency     : " + fmt_hms(total_media) + " / " + fmt_hms(time_good))
        lines.append("")
        lines.append("Gaps and overhead")
        lines.append("-----------------")
        lines.append("Startup / tail overhead : " + fmt_hms(overhead))
        lines.append("Retry / offline / BAD   : " + fmt_hms(time_retry_offline))
        lines.append("")


        lines.append("Chunks")
        lines.append("------")
        lines.append(f"GOOD chunks count : {stats['good_chunks']}")
        lines.append(f"BAD chunks count  : {stats['bad_chunks']}")
        if stats["min_chunk"] is not None:
            lines.append("Min GOOD chunk    : " + fmt_hms(stats["min_chunk"]))
        if stats["max_chunk"] is not None:
            lines.append("Max GOOD chunk    : " + fmt_hms(stats["max_chunk"]))
        lines.append("")
        lines.append("Timeline")
        lines.append("--------")

        sessions = stats["sessions"]
        sessions = sorted(sessions, key=lambda x: x["start"])
        last_end = None
        playhead = 0.0          # position in final file (seconds)
        black_len = BLACK_LEN           # length of black separator clip you generate
        for idx, sess in enumerate(sessions, start=1):
            start_ts = sess["start"]
            dur_media = sess.get("dur_media", 0.0)
            dur_run   = sess.get("dur_run", 0.0)
            end_ts = start_ts + (dur_run if dur_run > 0 else dur_media)
            start_str = datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M:%S")
            end_str = datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M:%S")
            w = sess.get("w")
            h = sess.get("h")
            fps = sess.get("fps")
            chunk_name = sess.get("name", f"chunk_{idx:03d}.ts")

            # print gap BEFORE this session if there was a previous one
            if last_end is not None and start_ts > last_end:
                gap = start_ts - last_end
                lines.append(
                    f"Gap             {fmt_hms(gap)} with no data (retries / stream down)"
                )

            seg_start = playhead
            seg_end = playhead + dur_media

            lines.append(f"Segment {idx:02d}: {chunk_name}, {w}x{h}@{fps}fps")
            lines.append(f"  Connected at     : {start_str}")
            lines.append(f" Recorded for {fmt_hms(dur_media)} media; run {fmt_hms(dur_run)}")
            lines.append(f"  Disconnected at  : {end_str}")
            lines.append(f"  Final file range : {fmt_hms(seg_start)}–{fmt_hms(seg_end)}")

            # advance playhead: session duration + black separator after it
            playhead = seg_end + black_len
            last_end = end_ts
        
        lines.append("")
        lines.append("Chunk details")
        lines.append("-------------")
        for idx, sess in enumerate(sessions, start=1):
            name = sess.get("name", f"chunk_{idx:03d}.ts")
            dur_media = sess.get("dur_media", 0.0)
            dur_run = sess.get("dur_run", 0.0)
            size_str = "unknown"
            try:
                path = os.path.join(CHUNKS_DIR, name)
                if os.path.exists(path):
                    size_mb = os.path.getsize(path) / (1024 * 1024)
                    size_str = f"{size_mb:.1f}MB"
            except:
                pass
            w = sess.get("w")
            h = sess.get("h")
            fps = sess.get("fps")
            lines.append(f"Chunk {idx:02d}: {name}")
            lines.append(f"  Duration / run   : {fmt_hms(dur_media)} / {fmt_hms(dur_run)}")
            lines.append(f"  Size / video     : {size_str} / {w}x{h}@{fps}fps")

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        # Line 1: written INTO the summary file (before terminal section)
        with open(summary_path, "a", encoding="utf-8", errors="replace") as out:
            out.write("\n")
            out.write(f"Wrote summary log to {summary_path}\n")

        log(f"Wrote summary log to {summary_path}")

        # Append terminal capture + get confirmation
        appended_bytes = append_termcap_to_summarylog(summary_path)

        # Line 2: written INTO the summary file (after terminal section)
        with open(summary_path, "a", encoding="utf-8", errors="replace") as out:
            out.write("\n")
            out.write(f"Appended terminal output OK ({appended_bytes} bytes from {TERMCAP_PATH})\n")

        log(f"Appended terminal output OK ({appended_bytes} bytes)")
        
    except Exception as e:
        log(f"Could not write summary log: {e}")
    
def finalize_recording():
    """
    Run ffmpeg concat to build FINAL_FILE, then robust checks and cleanup.
    """
    global best_w, best_h, best_fps, same_params
    
    if not os.path.exists(LIST_FILE):
        log("No list.txt → no chunks to concat. Skipping finalize.")
        return

    if os.path.exists(FINAL_FILE):
        log(f"WARNING: {FINAL_FILE} already exists. Overwriting.")
        send2trash(FINAL_FILE)

    # Fallback if somehow nothing was set (should not happen if any GOOD chunk)
    if best_h == 0 or best_fps == 0:
        best_w, best_h, best_fps = 1920, 1080, 50
        log(f"No best params recorded, falling back to {best_w}x{best_h}@{best_fps}fps")

    # Decide whether we can avoid re-encoding
    if same_params:
        log(f"All GOOD chunks {best_w}x{best_h}@{best_fps}fps → fast concat (no re-encode) → {FINAL_FILE}")
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            
            "-nostats",           
            "-progress", "pipe:2",
            "-stats_period", str(FFMPEG_PROGRESS_PERIOD), 
    
            "-i", "list.txt",
            
            # Keep all video + all audio streams from the concatenated input
            "-map", "0:v",
            "-map", "0:a?",
         
    
            "-c", "copy",
            os.path.join("..", FINAL_FILE),
        ]
    else:
        log("Mixed params → NOT auto-finalizing. Leaving chunks folder for manual analysis.")
        # close out timing so totals are correct in summary
        stats["process_end"] = time.time()

        # Estimate final duration (no FINAL_FILE to probe)
        black_len = BLACK_LEN    # must match make_black_clip() duration
        sessions = stats.get("sessions", [])
        total_media = sum(s.get("dur_media", 0.0) for s in sessions)
        est_final_dur = total_media + black_len * max(0, len(sessions) - 1)

        write_summary_log(est_final_dur, finalized=False)
        return
        # commenting out the below for now. I want to manually handle mixed param cases.
        #log(f"Mixed params → re-encoding to {best_w}x{best_h}@{best_fps}fps → {FINAL_FILE}")
        #cmd = [
        #    "ffmpeg",
        #    "-y",
        #    "-f", "concat",
        #    "-safe", "0",
        #    "-i", "list.txt",
        #    "-vf", f"scale={best_w}:{best_h},fps={best_fps}",
        #    "-c:v", "libx264",
        #    "-preset", "veryfast",
        #    "-c:a", "aac",
        #    "-b:a", "128k",
        #   os.path.join("..", FINAL_FILE),
        #]
    # proc = subprocess.run(cmd, cwd=CHUNKS_DIR)
    rc = run_ffmpeg_with_capture(cmd, CHUNKS_DIR, tag="FFmpeg-ENC")
    if rc != 0:
        log("FINAL CONCAT FAILED → keeping chunks folder for inspection.")
        return
        
    if not os.path.exists(FINAL_FILE):
        log("FINAL FILE MISSING after concat → keeping chunks.")
        return

    final_size = os.path.getsize(FINAL_FILE)
    if final_size <= 0:
        log("FINAL FILE SIZE 0 → keeping chunks.")
        return

    stats["process_end"] = time.time()
    dur, _ = get_file_info(FINAL_FILE)
    if dur <= 0:
        log("FINAL FILE has no valid duration → keeping chunks.")
        return

    log(
        f"FINAL OK → {FINAL_FILE}, duration {dur:.1f}s, size {final_size/1024/1024:.1f}MB"
    )

    # Write summary log next to FINAL_FILE
    write_summary_log(dur)

    # All checks passed → safe to delete chunks folder
    try:
        send2trash(CHUNKS_DIR)       # instead of shutil.rmtree(CHUNKS_DIR)
        log(f"Sent chunks folder {CHUNKS_DIR} to Recycle Bin")
    except Exception as e:
        log(f"Could not delete chunks folder {CHUNKS_DIR}: {e}")


def signal_handler(sig, frame):
    global stop_flag, nm3u8dl_stop_event
    log("")
    log("\nStopping by Ctrl-C...")
    stop_flag = True
    if nm3u8dl_stop_event is not None:
        nm3u8dl_stop_event.set()

        
signal.signal(signal.SIGINT, signal_handler)

def wait_until_start():
    """
    If SCHEDULE_START is set to a future time, wait until then.
    Format: "YYYY-MM-DD HH:MM" in local time.
    """
    if not SCHEDULE_START:
        # Manual start (no scheduling)
        mode = "manual"
        now = datetime.now()
        if RUN_DURATION_MIN is not None:
            end_time = now + timedelta(minutes=RUN_DURATION_MIN)
            log(f"Recording mode    : {mode}")
            log(f"Base name         : {BASE_NAME}")
            if DOWNLOAD_MODE == "ffmpeg":
                log(f"Live URL          : {LIVE_URL}")
            else:
                log(f"Download Mode     : N_m3u8DL-RE")
            log(f"Planned duration  : {RUN_DURATION_MIN} minutes")
            log(f"Expected end time : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            log(f"Recording mode    : {mode}")
            log(f"Base name         : {BASE_NAME}")
            if DOWNLOAD_MODE == "ffmpeg":
                log(f"Live URL          : {LIVE_URL}")
            else:
                log(f"Download Mode     : N_m3u8DL-RE")
            log("Planned duration  : until stopped")
        return  # start immediately
        
    # Scheduled mode
    mode = "scheduled"
    try:
        target = datetime.strptime(SCHEDULE_START, "%Y-%m-%d %H:%M")
    except ValueError:
        log(f"Invalid SCHEDULE_START '{SCHEDULE_START}', starting immediately.")
        return
    # Header printed once
    if RUN_DURATION_MIN is not None:
        end_time = target + timedelta(minutes=RUN_DURATION_MIN)
        log(f"Recording mode    : {mode}")
        log(f"Base name         : {BASE_NAME}")
        if DOWNLOAD_MODE == "ffmpeg":
            log(f"Live URL          : {LIVE_URL}")
        else:
            log(f"Download Mode     : N_m3u8DL-RE")
        log(f"Schedule start    : {SCHEDULE_START}")
        log(f"Planned duration  : {RUN_DURATION_MIN} minutes")
        log(f"Expected end time : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        log(f"Recording mode    : {mode}")
        log(f"Base name         : {BASE_NAME}")
        if DOWNLOAD_MODE == "ffmpeg":
            log(f"Live URL          : {LIVE_URL}")
        else:
            log(f"Download Mode     : N_m3u8DL-RE")
        log(f"Schedule start    : {SCHEDULE_START}")
        log("Planned duration  : until stopped")
        
    log(f"Scheduled start time parsed as {target.strftime('%Y-%m-%d %H:%M:%S')}")
    
    now = datetime.now()
    if now >= target:
        log(f"SCHEDULE_START {SCHEDULE_START} is in the past → starting immediately.")
        return

    while True:
        # CHECK stop_flag FIRST
        if stop_flag:
            log("Cancelled by Ctrl-C")
            sys.exit(0)
            
        now = datetime.now()
        if now >= target:
            break
            
        remaining = (target - now).total_seconds()
        if remaining > 60:
            log("")
            log(f"[WAIT] Waiting for start time {SCHEDULE_START} (remaining {fmt_hms(remaining)})...")
            # Sleep in SHORT 1-second intervals instead of 60 seconds
            for _ in range(min(60, int(remaining))):
                if stop_flag:
                    log("Cancelled by Ctrl-C")
                    sys.exit(0)
                time.sleep(1)
        else:
            # Less than 60 seconds remaining, check every second
            time.sleep(1)
            
        log("")
        log(f"[WAIT] Waiting for start time {SCHEDULE_START} (remaining {fmt_hms(remaining)})...")
        time.sleep(min(60, remaining))  # sleep in chunks up to 60s

    log("")
    log(f"Reached scheduled start time {SCHEDULE_START} → starting recording.")

def main():
    global stop_flag, manifest_fail_count, stall_recovery_count
    MIN_BACKOFF = 5
    MAX_BACKOFF = 30
    backoff_sec = MIN_BACKOFF

    log("")
    log("Live stream recorder started...")
    init_termcap()
    global start_time
    start_time = time.time()
    stats["process_start"] = start_time

    while not stop_flag:
        # stop after MAX_DURATION_SEC (only if enabled)
        if RUN_DURATION_MIN is not None:
            if time.time() - start_time >= RUN_DURATION_MIN * 60:
                beep_good()
                log("Max duration reached → stopping loop.")
                stop_flag = True
                break

        if DOWNLOAD_MODE == "ffmpeg":
            if is_stream_alive():
                log("")
                log("[RUN] Stream ON → start one FFmpeg run...")
                chunk_path, chunk_name = start_ffmpeg_to_chunk()
                ok = maybe_accept_chunk(chunk_path, chunk_name, context="Run end")
                if ok:
                    backoff_sec = MIN_BACKOFF
                else:
                    backoff_sec = min(backoff_sec + 5, MAX_BACKOFF)
                    
                # Check stop_flag before sleeping here too
                if stop_flag:
                    break
                    
                log("")
                log(f"[SLEEP] Waiting {backoff_sec}s before next check...")
                beep_bad()
                time.sleep(backoff_sec)
            else:
                # Check stop_flag before sleeping here too
                if stop_flag:
                    break
                    
                log("[GAP] Stream OFF → wait 15s")
                beep_bad()
                time.sleep(15)
        
        else:  # DOWNLOAD_MODE == "nm3u8dl"
            log("")
            log("[RUN] N_m3u8DL → start download run...")
            chunk_path, chunk_name = start_nm3u8dl_to_chunk()
            time.sleep(1) # Give N_m3u8DL time to fully flush the file
            ok = maybe_accept_chunk(chunk_path, chunk_name, context="Run end")
            
            if ok and not nm3u8dl_stall_flag:
                # Scenarios 1,3 - FOUND → normal monitoring
                manifest_fail_count = 0
                stall_recovery_count = 0
                backoff_sec = MIN_BACKOFF
            else:
                # Scenarios 2,4 - NOT FOUND
                if nm3u8dl_selected_bitrate == 0:  # MANIFEST FAIL
                    manifest_fail_count += 1
                    log(f"Manifest fail #{manifest_fail_count}/2")
                    if manifest_fail_count >= 2:
                        log("Manifest failed 2x → EXIT NO ALARM")
                        stop_flag = True
                        break
                else:  # FILE STALL
                    stall_recovery_count += 1
                    log(f"File stall recovery #{stall_recovery_count}/2")
                    if stall_recovery_count >= 2:
                        log("Stall failed 2x → EXIT + ALARM")
                        alarm_critical()
                        stop_flag = True
                        break
                
                backoff_sec = MIN_BACKOFF  # Always 10s retry
            
            if stop_flag:
                break

            log("")
            log(f"[SLEEP] Waiting {backoff_sec}s before next retry...")
            beep_bad()
            time.sleep(backoff_sec)


    # When loop ends (time reached or stop_flag set), finalize:
    finalize_recording()



if __name__ == "__main__":
    osSleep = None
    if os.name == "nt":
        osSleep = WindowsInhibitor()
        osSleep.inhibit()
    try:
        wait_until_start()
        
        # Initialize timestamped names at actual recording start
        run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        FINAL_FILE = f"{BASE_NAME}_{run_ts}.mkv"
        final_base = os.path.splitext(FINAL_FILE)[0]
        CHUNKS_DIR = f"{final_base}_chunks"
        LIST_FILE = os.path.join(CHUNKS_DIR, "list.txt")
        
        main()
    finally:
        if osSleep:
            osSleep.uninhibit()



