"""
FreeUI · PyWebView Launcher
检测宿主机电源状态并通过 js_api 暴露给前端
"""

import os
import sys
import webview
import psutil

# 为致敬ShxUwU对Scr动画圈做出的巨大贡献，特此用HTML模拟出：FreeUI in HTML!

def resource_path(rel):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


import asyncio, base64, io, edge_tts

async def _tts_generate(text, voice="zh-CN-XiaoxiaoNeural"):
    communicate = edge_tts.Communicate(text, voice)
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return base64.b64encode(buf.getvalue()).decode()


class Api:
    def tts_speak(self, text):
        try:
            b64 = asyncio.run(_tts_generate(text))
            return {"audio_base64": b64}
        except Exception as e:
            return {"error": str(e)}
        
    def minimize(self):
        webview.windows[0].minimize()

    def toggle_fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def quit(self):
        webview.windows[0].destroy()

    def get_power_status(self):
        """返回电源状态：{available, percent, plugged, secsleft}"""
        try:
            b = psutil.sensors_battery()
            if b is None:
                return {'available': False, 'reason': 'no_battery'}
            secs = int(b.secsleft)
            if secs < 0 or secs == psutil.POWER_TIME_UNLIMITED:
                secs = -1
            return {
                'available': True,
                'percent': int(round(b.percent)),
                'plugged': bool(b.power_plugged),
                'secsleft': secs,
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}


def main():
    webview.create_window(
        title='FreeUI · v2.05.11.8',
        url=resource_path('index.html'),
        width=380, height=780,
        min_size=(380, 780),
        resizable=False,
        background_color='#0a0a15',
        text_select=False,
        js_api=Api(),
    )
    webview.start(
        http_server=True,
        debug=os.getenv('FREEUI_DEBUG', '0') == '1',
        private_mode=True,
    )


if __name__ == '__main__':
    main()
# Robin-KK-Lab,PythonOS,Cheers!
