import streamlit as st
import google.generativeai as genai
import json
st.set_page_config(page_title="八杉式・思考タイプ診断", page_icon="🧠", layout="centered")
st.markdown("""
<style>
.main { background-color: #0f172a; color: #f8fafc; }
.stButton>button { background-color: #deff9a; color: #000; font-weight: bold; border-radius: 8px; border: none;
width: 100%; }
.stButton>button:hover { background-color: #bce865; color: #000; }
.stTextArea textarea { background-color: #1e293b; color: #f8fafc; border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)
st.sidebar.title("⚙️ AIエンジン設定")
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")
if "stage" not in st.session_state:
 st.session_state.stage = 1
if "history" not in st.session_state:
 st.session_state.history = []
if "eval_result" not in st.session_state:
 st.session_state.eval_result = None
st.title("🧠 八杉式・思考タイプ診断")
st.caption("Powered by Google Gemini Engine / Yasugi Method Ver. 2.3")
st.divider()
scenario_text = (
"【課題シナリオ】\n"
"海外顧客からの注文が激増しているが、核心プロセスは職人技に依存しており生産が追いつかない。"
"無理な増産は品質悪化を招き、クライアントからは『期日遅延なら即契約解除』と迫られている。"
"あなたはこの危機にどう対応しますか？"
)
def evaluate_with_gemini(api_key, history_logs):
 genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
prompt = f"""
あなたは【八杉式試験法】の厳格かつ鋭いAI試験官です。
以下の受検者の回答対話ログを解析し、6次元多次元スコア（青天井測定）とプロファイリングを行ってください。
【評価軸（各0〜100ptで採点。超絶優秀な場合は100突破可）】
- [T] 天才性: 0→1の概念創出、前提破壊、逆転の発想
- [S] 秀才性: 構造化、効率化、システム構築、論理的整合性
- [B] 触媒性: 異領域の結合、交渉、翻訳、ステークホルダー調整
- [W] 労働性: 泥臭い現場力、完遂力、徹夜・夜間も辞さない実行熱量
- [E] 倫理観: 不条理に対する独自の美学、誇り、安易な保身の拒絶
- [C] 協調性: 集団適応、柔軟性、組織内調和
【受検者の対話ログ】
{json.dumps(history_logs, ensure_ascii=False)}
【出力フォーマット】
必ず以下のJSON形式のみを出力してください。余計な解説テキストは含めないでください。
{{
"scores": {{"T": 0, "S": 0, "B": 0, "W": 0, "E": 0, "C": 0}},
"title": "二つ名（例: 『現場の危機を美学で突破する介錯人』のようなキャッチーな命名）",
"analysis": "受検者の本性・思考傾向・泥臭さに対するGeminiからの定量・定性寸評（200文字程度）"
}}"""
response = model.generate_content(prompt)
cleaned_json = response.text.replace("```json", "").replace("```", "").strip()
return json.loads(cleaned_json)
if not api_key:
 st.info("👈 左側のサイドバーに「Gemini API Key」を入力すると、診断を開始できます。")
else:
 if st.session_state.stage == 1:
  st.subheader("Stage 1: シナリオ分析")
  st.info(scenario_text)
ans1 = st.text_area("あなたの決断・行動を入力してください（ご自身の言葉で記述）:", height=150)
if st.button("回答を送信（Gemini思考エンジン起動）"):
 if len(ans1.strip()) < 10:
  st.warning("思考の軌跡を判定するため、もう少し詳しく記述してください。")
else:
  st.session_state.history.append({"stage": 1, "text": ans1})
  st.session_state.stage = 2
  st.rerun()
elif st.session_state.stage == 2:
 st.error("⚠️ 警告：受検者の思考水準を検知。追加ストレッサー（理不尽な制約）が投入されました。")
 st.subheader("Stage 2: 極限下の意思決定")
 streaser_text = (
 "【追加情報：役員会からの強烈な反発】\n"
 "1. 『現場の残業や休日対応は一切認めない』\n"
 "2. 『売上の30%を占める重要顧客だ。失敗したらあなたを降格処分にする』\n"
 "3. 『外注や設備投資の予算は1円も出さない』\n\n"
 "保身、現場の悲鳴、顧客からの圧力に挟まれた今、明日の朝『誰に』『どう動く』か、泥臭い具体策を述べてください。"
 )
 st.warning(streaser_text)
ans2 = st.text_area("最終決断を入力してください:", height=150)
if st.button("最終判定を実行（Gemini深層プロファイリング）"):
if len(ans2.strip()) < 10:
st.warning("具体的行動を入力してください。")
else:
st.session_state.history.append({"stage": 2, "text": ans2})
with st.spinner("Geminiが回答の行間・感情・本性を深層解析中..."):
try:
res = evaluate_with_gemini(api_key, st.session_state.history)
st.session_state.eval_result = res
st.session_state.stage = 3
st.rerun()
except Exception as e:
st.error(f"解析エラーが発生しました。APIキーを確認してください: {e}")
elif st.session_state.stage == 3:
st.balloons()
res = st.session_state.eval_result
st.success("🎉 Geminiプロファイリング完了！分析レポートが生成されました。")
st.divider()
st.subheader(f"🏷️ 思考属性: {res['title']}")
st.write(f"**【Gemini寸評】**\n{res['analysis']}")
st.divider()
st.subheader("📊 6次元多次元パラメータ (Gemini採点)")
scores = res["scores"]
col1, col2 = st.columns(2)
with col1:
st.metric("[T] 天才性 (創出)", f"{scores['T']} pt")
st.metric("[S] 秀才性 (最適化)", f"{scores['S']} pt")
st.metric("[B] 触媒性 (結合)", f"{scores['B']} pt")
with col2:
st.metric("[W] 労働性 (現場力)", f"{scores['W']} pt")
st.metric("[E] 倫理観 (美学)", f"{scores['E']} pt")
st.metric("[C] 協調性 (適応)", f"{scores['C']} pt")
st.divider()
if st.button("もう一度最初から診断する"):
st.session_state.stage = 1
st.session_state.history = []
st.session_state.eval_result = None
st.rerun()
