# 개인정보 고래상 점수 집계 웹앱

구글폼 응답 엑셀 파일을 업로드하면 평가자별 가중치, 상피제, 항목별 배점을 적용해
피평가자별 점수와 순위를 계산하는 Streamlit 웹앱입니다.

## 사용자 이용 방법

1. 웹앱 주소에 접속합니다.
2. `구글폼 응답 엑셀 파일 선택`을 누릅니다.
3. 구글폼에서 내려받은 `.xlsx` 응답 파일을 선택합니다.
4. 화면에 표시된 점수와 검증 결과를 확인합니다.
5. `평가 결과 엑셀 다운로드`를 누릅니다.

## 내 컴퓨터에서 시험 실행

PowerShell에서 프로젝트 폴더로 이동한 뒤 아래 명령을 실행합니다.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

브라우저가 자동으로 열리지 않으면 PowerShell에 표시된 `Local URL` 주소로 접속합니다.

## Streamlit Community Cloud에 배포

1. GitHub 계정을 만들고 새 저장소를 만듭니다.
2. 이 폴더의 아래 파일을 GitHub 저장소에 올립니다.
   - `streamlit_app.py`
   - `whale_award_scores.py`
   - `requirements.txt`
   - `README.md`
3. `https://share.streamlit.io`에 접속해 GitHub 계정으로 로그인합니다.
4. `Create app`을 누르고 GitHub 저장소를 선택합니다.
5. 실행 파일 경로에 `streamlit_app.py`를 입력하고 배포합니다.
6. 생성된 `streamlit.app` 주소를 사용자에게 공유합니다.

## 개인정보 주의

Streamlit Community Cloud에 배포하면 업로드한 응답 파일은 외부 클라우드 서버에서
처리됩니다. 응답 파일에 개인정보가 포함되어 있다면 조직의 보안 정책을 먼저 확인하고,
필요한 경우 조직 내부 서버에 배포하세요.
