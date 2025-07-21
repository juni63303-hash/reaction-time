import streamlit as st
import time
import random
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="반응 속도 테스트")

count = st_autorefresh(interval=100, limit=None, key="refresh")

for key, default in {
    "state": "idle",
    "reaction_times": [],
    "trial_count": 0,
    "start_time": 0,
    "change_time": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("🎯 반응 속도 테스트 (5회)")

def start_trial():
    st.session_state.state = "waiting"
    delay = random.uniform(2, 5)
    st.session_state.change_time = time.time() + delay

def update_state():
    if st.session_state.state == "waiting" and time.time() >= st.session_state.change_time:
        st.session_state.state = "ready"
        st.session_state.start_time = time.time()

update_state()

message_area = st.empty()
record_area = st.empty()
graph_area = st.empty()

if st.session_state.trial_count > 0 and st.session_state.trial_count < 5:
    message_area.info(f"🔄 {st.session_state.trial_count}회차 완료, {5 - st.session_state.trial_count}회 남음")
else:
    message_area.empty()

if st.session_state.reaction_times:
    with record_area.container():
        st.write("### 지금까지 측정된 반응속도 (ms)")
        for i, rt in enumerate(st.session_state.reaction_times, start=1):
            st.write(f"{i}회차: {rt} ms")
else:
    record_area.empty()

if st.session_state.trial_count >= 5:
    avg_time = sum(st.session_state.reaction_times) / len(st.session_state.reaction_times)
    st.subheader("최종 반응 속도 결과")
    st.write(f"평균 반응 속도: **{int(avg_time)}ms**")

    fig, ax = plt.subplots()
    ax.plot(range(1, 6), st.session_state.reaction_times, marker='o')
    ax.set_xlabel("시도 횟수")
    ax.set_ylabel("반응 속도 (ms)")
    ax.set_title("반응 속도 추이")
    graph_area.pyplot(fig)

    if st.button("🔄 다시 시작하기"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

else:
    graph_area.empty()

    if st.session_state.state == "idle":
        if st.button("테스트 시작"):
            start_trial()
    else:
        if st.session_state.state == "waiting":
            btn_color = "#ff4b4b"
            btn_text = "기다려 주세요"
        elif st.session_state.state == "ready":
            btn_color = "#4CAF50"
            btn_text = "지금 클릭!"

        btn_style = f"""
        <style>
        .stButton > button {{
            background-color: {btn_color};
            color: white;
            font-size: 30px;
            height: 120px;
            width: 300px;
            border-radius: 10px;
        }}
        </style>
        """
        st.markdown(btn_style, unsafe_allow_html=True)

        clicked = st.button(btn_text, key="main_button")

        if clicked and st.session_state.state == "ready":
            reaction_time = int((time.time() - st.session_state.start_time) * 1000)
            st.session_state.reaction_times.append(reaction_time)
            st.session_state.trial_count += 1
            message_area.success(f"{st.session_state.trial_count}회차: {reaction_time}ms")
            st.session_state.state = "idle"
