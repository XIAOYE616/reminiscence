# 馃懟 ex-bot 鈥?璁╁墠浠汇€屾椿杩囨潵銆嶇殑 QQ 鑱婂ぉ鏈哄櫒浜?
> 馃挕 鎶婁綘浠浘缁忕殑鑱婂ぉ璁板綍鍙樻垚 AI 浜烘牸锛岀敤 DeepSeek 椹卞姩锛岄€氳繃 QQ 灏忓彿 7脳24 闄綘鑱婂ぉ銆?
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![骞冲彴](https://img.shields.io/badge/骞冲彴-Windows%2010%2F11-lightgrey)]()

---

## 馃 杩欐槸浠€涔堬紵

浣犳湁娌℃湁鎯宠繃鈥斺€旀妸鍓嶄换鐨勮亰澶╄褰曞杺缁?AI锛岃瀹冨浼氥€岀敤 ta 鐨勮姘斿洖澶嶄綘銆嶏紵

ex-bot 灏辨槸骞茶繖涓殑锛?
```
浣犵殑 QQ 鑱婂ぉ璁板綍 (.txt)
        鈫? 鑷姩鍒嗘瀽
   ta 鐨勪汉鏍肩敾鍍?(persona)
        鈫? 鍠傜粰 AI
   DeepSeek + persona = ta 鐨勮姘?        鈫? 鑷姩鍥炲
   QQ 灏忓彿 鈫?浣犵殑澶у彿 鈫?灏卞儚 ta 鍦ㄥ拰浣犺亰
```

**鍏ㄧ▼鑷姩**锛屼綘鍙渶瑕侊細
1. 瀵煎嚭 QQ 鑱婂ぉ璁板綍锛堢偣鍑犱笅榧犳爣锛?2. 鍑嗗涓€涓?DeepSeek API Key锛堝厤璐规敞鍐屽氨鏈夛級
3. 鍑嗗涓€涓?QQ 灏忓彿锛堝拰澶у彿鏄ソ鍙嬶級
4. 杩愯 `python setup.py`

---

## 馃搵 浣犻渶瑕佸噯澶?
| 涓滆タ | 鎬庝箞鑾峰彇 | 鑺辫垂 |
|------|---------|------|
| **QQ 鑱婂ぉ璁板綍** | QQ 娑堟伅绠＄悊鍣ㄥ鍑?`.txt` | 鍏嶈垂 |
| **DeepSeek API Key** | [platform.deepseek.com](https://platform.deepseek.com) 娉ㄥ唽鈫扐PI Keys | 娉ㄥ唽閫?500 涓?token锛堝鑱婂緢涔咃級 |
| **QQ 灏忓彿** | 娉ㄥ唽涓€涓柊 QQ锛屽姞澶у彿涓哄ソ鍙?| 鍏嶈垂 |
| **Windows 鐢佃剳** | Win10/11 閮借 | 浣犳湁 |
| **Python** | [python.org](https://python.org) 涓嬭浇 3.10+ | 鍏嶈垂 |

---

## 馃殌 5 鍒嗛挓涓婃墜

### 绗竴姝ワ細涓嬭浇椤圭洰

```bash
# 鎵撳紑 PowerShell 鎴?CMD锛岃緭鍏ワ細
git clone https://github.com/XIAOYE616/reminiscence.git
cd reminiscence
```

> 娌℃湁 git锛熺偣椤甸潰鍙充笂瑙掔豢鑹?`Code` 鈫?`Download ZIP` 鈫?瑙ｅ帇涔熻

### 绗簩姝ワ細杩愯瀹夎鍚戝

```bash
python setup.py
```

鐒跺悗璺熺潃鎻愮ず璧帮細

```
  馃懟 ex-bot v1.0

  [1/5] 璇疯緭鍏?DeepSeek API Key: sk-xxxx
        锛堝幓 platform.deepseek.com 娉ㄥ唽灏辨湁锛?
  [2/5] QQ 鑱婂ぉ璁板綍鍦ㄥ摢閲岋紵
        [1] 鎴戠敤 QCE 瀵煎嚭浜嗭紙鎺ㄨ崘锛?        [2] 鏂囦欢宸茬粡鍦ㄦ闈簡
        [3] 鎴戠敤 QQ 鑷甫鐨勬秷鎭鐞嗗櫒瀵煎嚭浜?
  [3/5] ta 鍙粈涔堬紵鈫?鐒欑剻
        浣犲彨浠€涔堬紵 鈫?鎶樼櫧鑿?        姝ｅ湪鍒嗘瀽 13363 鏉℃秷鎭?..
        鉁?persona 宸茬敓鎴?
  [4/5] 姝ｅ湪閰嶇疆 NapCat...
        璇疯緭鍏?QQ 灏忓彿锛?460673995
        璇风敤鎵嬫満 QQ 鎵弿灞忓箷涓婄殑浜岀淮鐮?
  [5/5] 馃帀 Bot 鍚姩锛佺粰 QQ 灏忓彿鍙戞秷鎭瘯璇?```

### 绗笁姝ワ細鑱婂ぉ锛?
鎵撳紑 QQ锛岀粰浣犵殑**灏忓彿**鍙戞秷鎭€斺€攖a 浼氱敤 DeepSeek + 鍓嶄换璇皵鑷姩鍥炲浣犮€?
---

## 馃搳 鎬庝箞瀵煎嚭 QQ 鑱婂ぉ璁板綍锛?
### 鏂规硶 A锛歈Q 鑷甫娑堟伅绠＄悊鍣紙鏈€绠€鍗曪級

1. 鎵撳紑 QQ锛屾壘鍒板拰 ta 鐨勮亰澶╃獥鍙?2. 鍙抽敭娑堟伅鍖哄煙 鈫?**娑堟伅绠＄悊鍣?* 鈫?**瀵煎嚭娑堟伅璁板綍**
3. 鏍煎紡閫?**鏂囨湰鏂囦欢 (.txt)**
4. 鏃堕棿鑼冨洿閫?**鍏ㄩ儴**
5. 淇濆瓨鍒版闈?
### 鏂规硶 B锛歈CE锛堝姛鑳芥洿寮猴紝鏀寔鎵€鏈夋牸寮忥級

濡傛灉浣犲凡缁忚浜?NapCat Framework锛堝惈 QCE锛夛細

1. 鎵撳紑 `http://localhost:40653/qce-v4-tool`
2. Token 鍦?`C:\Users\浣犵殑鐢ㄦ埛鍚峔.qq-chat-exporter\security.json`
3. 閫夋嫨鑱旂郴浜?鈫?瀵煎嚭

---

## 馃彈 鍘熺悊鏋舵瀯

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鍙戞秷鎭?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  WebSocket   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?浣犵殑澶у彿  鈹?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈫? 鈹?QQ 灏忓彿   鈹?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈫? 鈹?ex-bot   鈹?鈹?4775...  鈹?鈫愨攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ 鈹?NapCat)  鈹?鈫愨攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ 鈹?(Python) 鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鑷姩鍥炲    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  HTTP API    鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?                                                          鈹?                                                    璋冪敤 DeepSeek
                                                          鈹?                                                   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹?                                                   鈹? DeepSeek   鈹?                                                   鈹?+ persona   鈹?                                                   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

**鍏抽敭缁勪欢锛?*

| 缁勪欢 | 浣滅敤 |
|------|------|
| **NapCat** | 璁?QQ 鑳借绋嬪簭鎺у埗锛堟敞鍏?QQ NT 杩涚▼锛?|
| **OneBot** | QQ 鏈哄櫒浜虹殑鏍囧噯鎺ュ彛鍗忚 |
| **bot.py** | 鐩戝惉娑堟伅 鈫?璋?AI 鈫?鍙戝洖澶?|
| **DeepSeek** | 鍥戒骇澶фā鍨嬶紝渚垮疁濂界敤锛屼腑鏂囩悊瑙ｅ姏寮?|
| **Persona** | 浠庤亰澶╄褰曢噷鎻愬彇鐨勪汉鏍肩敾鍍忥紙system prompt锛?|

---

## 馃搧 椤圭洰缁撴瀯

```
reminiscence/
鈹溾攢鈹€ setup.py                鈫?馃幆 涓绘帶鑴氭湰锛堜竴閿畨瑁?閰嶇疆/鍚姩锛?鈹溾攢鈹€ scripts/
鈹?  鈹斺攢鈹€ bot.py              鈫?QQ bot 鏍稿績锛圵ebSocket 鏈嶅姟绔級
鈹溾攢鈹€ persona/
鈹?  鈹斺攢鈹€ SKILL.md.sample     鈫?瑙掕壊鍗℃ā鏉匡紙鐢熸垚鍚庡湪杩欓噷锛?鈹溾攢鈹€ config/
鈹?  鈹斺攢鈹€ config.json         鈫?浣犵殑閰嶇疆锛堣嚜鍔ㄧ敓鎴愶紝涓嶈鎻愪氦锛侊級
鈹溾攢鈹€ tools/                  鈫?NapCat 鑷姩涓嬭浇鍒拌繖閲?鈹溾攢鈹€ README.md               鈫?浣犳鍦ㄧ湅鐨勮繖涓?鈹溾攢鈹€ LICENSE                 鈫?MIT
鈹斺攢鈹€ .gitignore
```

---

## 馃幃 鍛戒护鍙傝€?
| 鍛戒护 | 浣滅敤 |
|------|------|
| `python setup.py` | 棣栨瀹夎鍚戝 |
| `python setup.py bot` | 鍙惎鍔?bot锛堝凡閰嶇疆杩囩殑璇濓級 |
| `python setup.py persona` | 鍙噸鏂扮敓鎴?persona |

**Bot 杩愯鏃舵敮鎸佺殑鑱婂ぉ鎸囦护锛?*

| 鎸囦护 | 鏁堟灉 |
|------|------|
| `/reset` | 娓呯┖瀵硅瘽璁板繂锛坱a 浼氬繕璁板垰鎵嶈亰浜嗕粈涔堬級 |
| `/status` | 鏌ョ湅 bot 杩愯鐘舵€?|

---

## 馃敡 甯歌闂

<details>
<summary><b>Q: DeepSeek 瑕侀挶鍚楋紵</b></summary>

娉ㄥ唽灏遍€?500 涓?token銆備竴鏉℃秷鎭ぇ绾︽秷鑰?500 token锛屼篃灏辨槸鑳借亰 **1 涓囨潯娑堟伅**銆傜敤瀹屼箣鍚庯細
- 鍏呭€?10 鍧楅挶 鈮?鑱婂埌澶╄崚鍦拌€?- 鎴栬€呮崲鐢ㄥ叾浠栧吋瀹?OpenAI 鏍煎紡鐨?API锛堝 Qwen銆丟LM 绛夛級
</details>

<details>
<summary><b>Q: QQ 灏忓彿浼氳灏佸悧锛?/b></summary>

姝ｅ父浣跨敤涓嶄細銆備絾娉ㄦ剰锛?- 涓嶈鐢?bot 鍙戝箍鍛娿€侀獨鎵?- 鎺у埗娑堟伅棰戠巼锛坆ot 榛樿姝ｅ父璇€熷洖澶嶏級
- 寤鸿鐢ㄥ皬鍙疯€岄潪涓诲彿
</details>

<details>
<summary><b>Q: 瀵煎嚭鑱婂ぉ璁板綍澶辫触鎬庝箞鍔烇紵</b></summary>

1. 鍏虫帀 QQ 閲嶈瘯
2. 鎹?`.mht` 鏍煎紡璇曡瘯
3. 鐢?QCE 宸ュ叿锛坢ethods B锛?4. 鐩存帴鎶婂鍑烘枃浠舵嫋鍒伴」鐩枃浠跺す锛岃繍琛?`python setup.py persona`
</details>

<details>
<summary><b>Q: Bot 涓嶅洖澶嶆€庝箞鍔烇紵</b></summary>

1. 纭 QQ 灏忓彿宸茬粡鎵爜鐧诲綍锛堣兘鐪嬪埌 QQ 鍦ㄧ嚎锛?2. 纭 `python setup.py bot` 鐨勭獥鍙ｆ病鍏?3. 纭 DeepSeek API Key 娌¤緭閿?4. 纭澶у彿鍜屽皬鍙锋槸濂藉弸鍏崇郴
5. 鐪嬬湅 bot 绐楀彛鏈夋病鏈夋姤閿欐棩蹇?</details>

<details>
<summary><b>Q: ta 鐨勮姘斾笉鍍忔€庝箞鍔烇紵</b></summary>

1. 瀵煎嚭鏇村鑱婂ぉ璁板綍锛堣秺澶氳秺鍍忥級
2. 瀵煎嚭鏃堕€夈€屽叏閮ㄦ椂闂淬€?3. 杩愯 `python setup.py persona` 閲嶆柊鐢熸垚
4. 鍦?persona/SKILL.md 閲屾墜鍔ㄨ皟鏁?</details>

<details>
<summary><b>Q: 鑳芥敮鎸佸井淇＄兢鑱婂悧锛?/b></summary>

鐩墠鍙敮鎸佺鑱婏紙涓€瀵逛竴锛夈€傜兢鑱婃敮鎸佽鍒掍腑銆?</details>

<details>
<summary><b>Q: Mac/Linux 鑳界敤鍚楋紵</b></summary>

NapCat锛圦Q 娉ㄥ叆妗嗘灦锛夌洰鍓嶅彧鏀寔 Windows銆傚洜涓?QQ NT 鍙湁 Windows 鐗堟湰鑳界敤 NapCat 娉ㄥ叆銆?</details>

---

## 鈿狅笍 鍏嶈矗澹版槑

- 鏈」鐩粎渚?**涓汉鍥炲繂鏁寸悊銆佹儏鎰熷洖椤俱€佸垱浣滃疄楠?*
- **涓ョ**鐢ㄤ簬锛氶獨鎵扮湡浜恒€佸啋鍏呯湡浜恒€佷镜鐘殣绉併€佹姤澶嶆垨浠讳綍杩濇硶鐢ㄩ€?- 鐢熸垚鐨勪竴鍒囧唴瀹归兘鏄熀浜庢湰鍦版潗鏂欑殑 AI 妯℃嫙锛?*涓嶄唬琛ㄧ湡瀹炰汉鐗╂湰浜?*
- 璇峰皧閲嶇湡瀹炴矡閫氥€佺湡瀹炶竟鐣屽拰鐪熷疄鐢熸椿
- 浣跨敤鑰呰嚜琛屾壙鎷呬竴鍒囧悗鏋?
---

## 馃檹 鑷磋阿

绔欏湪宸ㄤ汉鐨勮偐鑶€涓婏細

- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 鈥?QQ NT 鍗忚妗嗘灦
- [QCE (QQ Chat Exporter)](https://github.com/shuakami/qq-chat-exporter) 鈥?QQ 鑱婂ぉ瀵煎嚭绁炲櫒
- [DeepSeek](https://platform.deepseek.com) 鈥?鍥戒骇鑹績澶фā鍨?- [OneBot 11](https://github.com/botuniverse/onebot-11) 鈥?鏈哄櫒浜烘爣鍑嗗崗璁?
---

## 馃搫 License

MIT 漏 2026

---

猸?濡傛灉甯埌浣犱簡锛岀粰涓?Star 鍛梸

