쇼핑 위시리스트 콜렉터 (파이썬 기반 쇼핑 검색 및 위시리스트 웹 서비스)
파이썬 기반 웹 프레임워크와 네이버 쇼핑 검색 API를 활용하여, 관심 있는 상품들을 검색하고 한곳에 모아 관리할 수 있는 나만의 쇼핑 위시리스트 웹사이트 프로젝트입니다.

Links
배포 주소: [쇼핑 위시리스트 콜렉터 배포 링크를 입력하세요]

GitHub 저장소: https://github.com/seokhyeon09/miniproject-python-scraping

Tech Stack (사용 기술)
Backend & Framework: Python 3, FastAPI

Frontend: HTML5, CSS3 (MVP.css)

Database & ORM: MongoDB Atlas, Odmantic

API & Deployment: Naver Open API, Vercel

Key Features (주요 기능)
실시간 데이터 스크래핑 및 파싱 연동: 네이버 쇼핑 Open API와 aiohttp 비동기 통신 라이브러리를 활용하여 실시간으로 정확한 쇼핑 검색 결과 데이터를 서버로 불러와 화면에 출력합니다.

데이터 정제 및 전처리 최적화: API 응답에 포함된 불필요한 HTML 태그들을 파이썬의 정규표현식(re 라이브러리)을 사용해 정제하였으며, 딕셔너리와 리스트로 가공하여 필요한 정보(이미지, 가격, 브랜드 등)만 선별 추출했습니다.

클라우드 데이터베이스 연동 즐겨찾기: 마음에 드는 상품의 카드 버튼을 누르면 MongoDB Atlas에 데이터베이스 형태로 저장되며, favorites 경로를 통해 별도의 위시리스트 페이지에서 내가 담은 항목들만 조회하거나 삭제할 수 있도록 구성했습니다.

모던 레이아웃 및 UI 디테일 개선: 외부 스타일시트(MVP.css)를 커스텀하여 모던한 상단 헤더 레이아웃과 버튼 반응형 Hover 효과를 구현했으며, 브랜드 정보가 없는 경우 쇼핑몰 이름으로 대체하거나 null 처리하는 등 꼼꼼한 UI 분기 처리를 적용했습니다.

Troubleshooting (트러블슈팅 및 문제 해결 과정)
1. 서버리스 배포 환경 한계와 스크래핑 방식 변경
문제점: 초기에는 BeautifulSoup과 같은 라이브러리를 통해 네이버 쇼핑 페이지에서 직접 텍스트를 크롤링하는 방식을 고려했습니다. 그러나 Vercel과 같은 무료 서버리스 환경에서는 용량이 부족하고 응답 지연(Timeout)이 발생할 위험이 커, 무거운 크롤링 로직을 돌리기에는 한계가 있었습니다.

해결 방안: 직접 HTML 페이지를 긁어오는 방식 대신, 가볍고 빠른 응답을 보장하는 네이버 Open API JSON 통신 방식으로 전환하여 안정성과 속도를 크게 확보할 수 있었습니다.

2. 즐겨찾기 해제 시 Form 데이터 전송 오류 해결
문제점: 위시리스트 화면에서 상품 삭제 버튼을 눌렀을 때 422 Unprocessable Entity 에러가 발생하는 문제가 있었습니다. 원인을 분석해보니, 홈 화면과 달리 위시리스트 화면에서는 검색어(keyword) 변수가 없어서 서버에 빈 값이 전달되며 서버의 필수 입력 검증에서 막히는 것이었습니다.

해결 방안: HTML에서 상품 고유의 검색어 정보를 전달하도록 수정하고, 파이썬 서버 코드에서도 해당 값을 선택적으로 받을 수 있도록 코드를 유연하게 수정하여 문제를 해결했습니다.

느낀점 / 개선할 점
느낀점: 단순히 파이썬으로 데이터를 뽑아오는 것을 넘어서, 프레임워크를 통해 백엔드 서버를 만들고, 프론트엔드 화면으로 전달해 DB에까지 연결해 보는 전체 웹 풀스택 과정을 경험할 수 있어 큰 배움이 되었습니다.

개선할 점: 즐겨찾기를 누르거나 지울 때마다 새로고침이 발생하는 구조인데, 앞으로 자바스크립트를 이용해 새로고침 없이 비동기적으로 버튼 색상만 변경되도록 성능과 사용자 경험을 개선해보고 싶습니다.

Getting Started (로컬 실행 방법)
저장소 클론 (Clone the repository)
git clone https://github.com/seokhyeon09/miniproject-python-scraping

패키지 설치 (Install dependencies)
pip install -r requirements.txt

환경 변수 설정 (Set up environment variables)
최상위 경로에 .env 파일을 생성하고 네이버 API 키 및 MongoDB URI 등을 입력하세요.

개발 서버 실행 (Run the dev server)
uvicorn main:app --reload
