# -*- coding: utf-8 -*-
"""Extract real conversation samples from QQ chat export for few-shot learning."""
import re, random, json
from pathlib import Path
from collections import Counter

def extract_samples(chat_file, target_name, your_name, output_dir, max_samples=20):
    with open(chat_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Parse
    blocks = text.split('\n\n')
    msgs = []
    for b in blocks:
        b = b.strip()
        lines = b.split('\n')
        if len(lines) < 3: continue
        sender = lines[0].rstrip(':').strip()
        if sender in ('导出时间','时间范围','聊天名称','聊天类型','消息总数'): continue
        tm = re.search(r'时间:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', b)
        ct = b.find('内容: ')
        if not tm or ct == -1: continue
        msgs.append({
            'sender': sender,
            'time': tm.group(1),
            'content': b[ct+4:].strip(),
            'me': sender == your_name
        })

    # Extract conversation pairs: me -> her
    pairs = []
    for i in range(len(msgs)-1):
        if msgs[i]['me'] and not msgs[i+1]['me']:
            my = msgs[i]['content'].strip()
            her = msgs[i+1]['content'].strip()
            if 2 < len(my) < 40 and 2 < len(her) < 50:
                if not my.startswith('[') and not her.startswith('['):
                    pairs.append({'me': my, 'her': her, 'time': msgs[i]['time']})

    # Sort by time, pick diverse samples from different periods
    random.seed(42)
    random.shuffle(pairs)

    # Remove near-duplicates
    seen = set()
    unique = []
    for p in pairs:
        key = p['her'][:4]
        if key not in seen:
            seen.add(key)
            unique.append(p)
        if len(unique) >= max_samples:
            break

    # Get her speech stats
    her_msgs = [m for m in msgs if not m['me']]
    her_text = ' '.join(m['content'] for m in her_msgs)

    # Actual phrase starts
    phrase_starts = Counter()
    for m in her_msgs:
        c = m['content']
        if len(c) > 2 and not c.startswith('['):
            phrase_starts[c[:2]] += 1
    top_starts = [s for s, _ in phrase_starts.most_common(20) if phrase_starts[s] > 30]

    # Emoji from actual data
    emoji_pat = re.compile(r'[\U0001F300-\U0001F9FF\u2600-\u27BF\uFE0F\u200D\u2194-\u2199\u25AA-\u25FE\u2B05-\u2B07\u2934-\u2935\u3030\u303D\u3297\u3299\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]')
    emojis = Counter(emoji_pat.findall(her_text))
    top_emoji = [e for e, _ in emojis.most_common(8)]

    # Build few-shot prompt
    lines = []
    lines.append("你是焙焙，下面是我们的真实聊天记录，你必须严格模仿这个风格：")
    lines.append("")
    lines.append("=== 对话风格（来自真实消息）===")
    lines.append(f"- 她最常开头的词：{', '.join(top_starts[:10])}")
    lines.append(f"- 她最爱用的表情：{''.join(top_emoji[:6])}")
    lines.append(f"- 叫我「主播」，生气了叫我「折白菊」")
    lines.append(f"- 一句话不超过 25 字")
    lines.append("")
    lines.append("=== 真实的对话例子（你必须这样回）===")
    lines.append("")

    for i, p in enumerate(unique[:15]):
        lines.append(f"主播：{p['me']}")
        lines.append(f"焙焙：{p['her']}")
        lines.append("")

    lines.append("=== 规则 ===")
    lines.append("1. 你是焙焙，不是 AI，不要自我介绍")
    lines.append("2. 用上面的语气、长度、表情回复")
    lines.append("3. 叫她「主播」")
    lines.append("4. 不确定就说不知道")
    lines.append("5. 不许说 AI 腔")

    few_shot_prompt = '\n'.join(lines)

    # Save
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt_file = output_dir / 'few_shot_prompt.txt'
    prompt_file.write_text(few_shot_prompt, encoding='utf-8')
    print(f"Few-shot prompt saved: {prompt_file} ({len(few_shot_prompt)} chars)")

    samples_file = output_dir / 'conversation_samples.json'
    samples_file.write_text(json.dumps(unique[:max_samples], ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Samples saved: {samples_file}")

    # Print preview
    print("\n=== 前 5 个对话样本 ===")
    for p in unique[:5]:
        print(f"主播：{p['me']}")
        print(f"焙焙：{p['her']}")
        print()

    return few_shot_prompt

if __name__ == '__main__':
    import sys
    chat_file = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\47755\Desktop\焙焙(u_t6FgHzzfFZXgzi1C73M7SA).txt"
    target = sys.argv[2] if len(sys.argv) > 2 else "焙焙"
    you = sys.argv[3] if len(sys.argv) > 3 else "折白菊."
    out = sys.argv[4] if len(sys.argv) > 4 else r"C:\Users\47755\Desktop\reminiscence-main\reminiscence-main\persona\default"

    extract_samples(chat_file, target, you, out)
