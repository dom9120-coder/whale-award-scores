"""브라우저에서 사용하는 개인정보 고래상 점수 집계 웹앱."""

from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st

from whale_award_scores import calculate_scores, read_latest_responses, write_results


st.set_page_config(
    page_title="개인정보 고래상 점수 집계",
    page_icon=":material/calculate:",
    layout="centered",
)

st.title("개인정보 고래상 점수 집계")
st.write("구글폼에서 내려받은 응답 엑셀 파일을 올리면 점수와 순위를 자동 계산합니다.")

st.warning(
    "응답 파일에 개인정보가 포함되어 있다면, 조직의 보안 정책상 외부 웹 서비스에 "
    "업로드해도 되는지 먼저 확인하세요."
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
    "구글폼 응답 엑셀 파일 선택",
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

        st.success("계산이 완료되었습니다.")

        st.subheader("점수 및 순위")
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
st.caption("업로드한 파일과 생성된 결과 파일은 계산 중 임시로 사용된 뒤 삭제됩니다.")
