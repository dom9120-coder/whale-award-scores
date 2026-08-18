"""브라우저에서 사용하는 개인정보 고래상 점수 집계 웹앱."""

import base64
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st

from whale_award_scores import calculate_scores, read_latest_responses, write_results
CANDIDATE_NAMES = {
    "a": "기획팀",
    "b": "국외출장팀",
    "c": "법제팀",
    "d": "임수연",
    "e": "전창민",
    "f": "윤상은",
    "g": "인력예산팀",
    "h": "공공실태점검팀",
    "i": "전략기획팀",
}


def candidate_label(candidate: object) -> str:
    candidate = str(candidate)
    return CANDIDATE_NAMES.get(candidate, candidate)

WHALE_IMAGE = Path(__file__).with_name("whale_hero.png")
whale_data = base64.b64encode(WHALE_IMAGE.read_bytes()).decode("ascii")

st.set_page_config(
    page_title="개인정보 고래상 점수 집계",
    page_icon=":material/calculate:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(15, 118, 110, 0.12), transparent 28rem),
            linear-gradient(180deg, #f7fbfb 0%, #ffffff 34%);
    }
    .block-container {
        max-width: 860px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.3rem 2.4rem;
        padding-right: 19rem;
        min-height: 245px;
        border-radius: 24px;
        color: white;
        background: linear-gradient(135deg, #0f766e 0%, #155e75 100%);
        box-shadow: 0 18px 45px rgba(15, 118, 110, 0.20);
        margin-bottom: 1.4rem;
    }
    .hero-content {
        position: relative;
        z-index: 2;
    }
    .hero-whale {
        position: absolute;
        z-index: 1;
        width: 315px;
        right: -18px;
        bottom: -42px;
        filter: drop-shadow(0 18px 20px rgba(0, 36, 54, 0.22));
        transform: rotate(-3deg);
    }
    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.30);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.12);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 0.9rem;
    }
    .hero h1 {
        color: white;
        margin: 0;
        font-size: 2.25rem;
        letter-spacing: -0.04em;
    }
    .hero p {
        margin: 0.8rem 0 0;
        color: rgba(255, 255, 255, 0.88);
        line-height: 1.7;
    }
    .steps {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin: 1.2rem 0 1.4rem;
    }
    .step {
        border: 1px solid #dcebea;
        border-radius: 16px;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.85);
    }
    .step-number {
        color: #0f766e;
        font-size: 0.78rem;
        font-weight: 800;
    }
    .step-title {
        margin-top: 0.35rem;
        font-weight: 750;
        color: #173b3a;
    }
    [data-testid="stFileUploader"] {
        padding: 1.1rem;
        border: 1px solid #cfe4e2;
        border-radius: 18px;
        background: white;
        box-shadow: 0 10px 28px rgba(24, 78, 74, 0.08);
    }
    [data-testid="stMetric"] {
        border: 1px solid #dcebea;
        border-radius: 16px;
        padding: 1rem;
        background: white;
        box-shadow: 0 8px 22px rgba(24, 78, 74, 0.06);
    }
    .section-title {
        margin-top: 1.8rem;
        color: #173b3a;
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .privacy-note {
        margin-top: 1.2rem;
        padding: 0.9rem 1rem;
        border-left: 4px solid #d97706;
        border-radius: 10px;
        background: #fffbeb;
        color: #78350f;
        line-height: 1.6;
        font-size: 0.92rem;
    }
    @media (max-width: 700px) {
        .hero {
            padding: 1.6rem;
            padding-bottom: 11rem;
            min-height: auto;
        }
        .hero h1 { font-size: 1.75rem; }
        .hero-whale {
            width: 235px;
            right: -20px;
            bottom: -45px;
            opacity: 0.92;
        }
        .steps { grid-template-columns: 1fr; }
    }
</style>

<div class="hero">
    <div class="hero-content">
        <div class="hero-badge">PRIVACY WHALE AWARD</div>
        <h1>개인정보 고래상<br>점수 집계</h1>
        <p>구글폼 응답 엑셀을 올리면 평가자별 가중치와 상피제를 적용해
        최종 점수, 순위, 검증 결과를 한 번에 계산합니다.</p>
    </div>
    <img class="hero-whale" src="data:image/png;base64,WHALE_IMAGE_DATA" alt="고래 일러스트">
</div>

<div class="steps">
    <div class="step"><div class="step-number">STEP 01</div><div class="step-title">응답 엑셀 선택</div></div>
    <div class="step"><div class="step-number">STEP 02</div><div class="step-title">자동 계산·검증</div></div>
    <div class="step"><div class="step-number">STEP 03</div><div class="step-title">결과 엑셀 다운로드</div></div>
</div>
""".replace("WHALE_IMAGE_DATA", whale_data),
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="privacy-note">
<strong>업로드 전 확인</strong><br>
응답 파일에 개인정보가 포함되어 있다면 조직의 보안 정책상 외부 웹 서비스에
업로드해도 되는지 먼저 확인해 주세요.
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("적용되는 계산 규칙"):
    st.markdown(
        """
- 평가자별 가중치 적용
- 평가자와 피평가자 간 상피제 적용
- 평가 항목명에 표시된 상·중·하 배점 적용
- 평가자별 가장 최근 응답 사용
- 응답 누락, 중복, 상피 위반, 가중치 합 자동 검증
"""
    )

uploaded_file = st.file_uploader(
    "응답 엑셀 파일을 선택해 주세요",
    type=["xlsx"],
    help="구글폼 응답 시트를 수정하지 않은 상태로 올려주세요.",
)

if uploaded_file is not None:
    try:
        with st.spinner("점수와 순위를 계산하고 있습니다..."):
            with TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                input_path = temp_path / "응답.xlsx"
                output_path = temp_path / "평가결과.xlsx"

                input_path.write_bytes(uploaded_file.getvalue())
                headers, responses = read_latest_responses(input_path)
                summaries, details, errors = calculate_scores(headers, responses)
                write_results(output_path, summaries, details, errors)
                result_bytes = output_path.read_bytes()

        st.success("계산이 완료되었습니다. 아래에서 결과를 확인하고 엑셀 파일을 내려받으세요.")

        st.markdown('<div class="section-title">상위 결과</div>', unsafe_allow_html=True)
        top_three = summaries[:3]
        metric_columns = st.columns(3)
        rank_labels = ["1위", "2위", "3위"]
        for column, label, row in zip(metric_columns, rank_labels, top_three):
            column.metric(
                label=label,
                value=str(row["피평가자"]),
                delta=f"{float(row['최종점수']):.3f}점",
                delta_color="off",
            )

        st.markdown('<div class="section-title">전체 점수 및 순위</div>', unsafe_allow_html=True)
        st.dataframe(
            [
                {
                    "순위": row["순위"],
                    "피평가자": row["피평가자"],
                    "최종점수": round(float(row["최종점수"]), 3),
                }
                for row in summaries
            ],
            hide_index=True,
            use_container_width=True,
        )

        st.markdown('<div class="section-title">검증 결과</div>', unsafe_allow_html=True)
        if errors:
            st.error(f"검증 결과: 확인이 필요한 항목이 {len(errors)}건 있습니다.")
            with st.expander("검증 항목 확인"):
                for error in errors:
                    st.write(f"- {error}")
        else:
            st.info("검증 결과: 모든 검증을 정상적으로 통과했습니다.")

        result_name = f"{Path(uploaded_file.name).stem}_평가결과.xlsx"
        st.download_button(
            "평가 결과 엑셀 다운로드",
            data=result_bytes,
            file_name=result_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
        )

    except Exception as exc:
        st.error("파일을 처리하지 못했습니다. 구글폼에서 내려받은 원본 응답 엑셀인지 확인해 주세요.")
        with st.expander("오류 내용"):
            st.code(str(exc))

st.divider()
st.caption("업로드한 파일과 생성된 결과 파일은 계산 중 임시로 사용된 뒤 삭제됩니다. · 개인정보 고래상 점수 집계")
