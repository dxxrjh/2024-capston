# 가상 사용자 프로필 반영
# 일별 박스오피스 API 서비스 | 주간/주말 박스오피스 API 서비스에서 영화 코드
# 영화상세정보 조회 API 서비스에서 영화 코드로 영화명, 영화유형, 장르명, 감독명, 배우명
# 영상물등급위원회_영화 등급분류정보 조회 서비스 api 에서 영화의 종별, 줄거리, 감독, 제작국 정보

import pandas as pd
import requests
import xml.etree.ElementTree as ET

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# API 정보 & 발급 받은 키
DATA_API_KEY = "API_KEY"
KMRB_MOVIE_URL = "http://apis.data.go.kr/B551008/movie/v1/movie_search"

KOFIC_API_KEY = "API_KEY"
DAILY_BOX_OFFICE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
MOVIE_INFO_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"

# 일별 박스오피스 영화 코드 가져오기 함수
def fetch_box_office_codes(target_date):
    params = {
        "key": KOFIC_API_KEY,
        "targetDt": target_date

    }
    response = requests.get(DAILY_BOX_OFFICE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        box_office_list = data["boxOfficeResult"]["dailyBoxOfficeList"]
        # 영화 코드 리스트 추출
        movie_codes = [movie["movieCd"] for movie in box_office_list]
        return movie_codes
    else:
        print(f"박스오피스 API 호출 실패. 상태 코드: {response.status_code}")
        return []

# 영화명, 영화유형, 장르명, 감독명, 배우명, 상영형태명 가져오기 함수
def fetch_movie_details(movie_code):
    params = {
        "key": KOFIC_API_KEY,
        "movieCd": movie_code
    }
    response = requests.get(MOVIE_INFO_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        movie_info = data["movieInfoResult"]["movieInfo"]

        # 필요한 정보 추출
        movie_details = {
            "영화명": movie_info["movieNm"],
            "영화유형": movie_info["typeNm"],
            "장르명": ", ".join([genre["genreNm"] for genre in movie_info["genres"]]),
            "감독명": ", ".join([director["peopleNm"] for director in movie_info["directors"]]),
            "배우명": ", ".join([actor["peopleNm"] for actor in movie_info["actors"][:5]]),  # 상위 5명만
            "상영형태명": ", ".join([show["showTypeGroupNm"] for show in movie_info["showTypes"]])
        }

        movie_details_list = list(movie_details.values())

        return movie_details_list
    else:
        print(f"영화 상세 정보 API 호출 실패. 상태 코드: {response.status_code}")
        return None

# 코사인 유사도 계산을 위해 영화 데이터 벡터화
def vectorize_movie_data(movie_data, vectorizer):
    # 각 영화에 대해 모든 텍스트를 하나로 결합 (제목, 장르, 줄거리, 감독, 배우 등)
    movie_texts = []
    for movie in movie_data:
        # 영화의 다양한 정보를 하나의 텍스트로 결합
        combined_text = " ".join(movie[1:])  # 첫 번째 항목은 영화명, 제외하고 나머지 항목들 결합
        movie_texts.append(combined_text)

    # TF-IDF 벡터화
    movie_vector = vectorizer.fit_transform(movie_texts)

    return movie_vector

# 영화 줄거리, 종별, 제작국 데이터 가져오기 함수
def fetch_movie_rating_info(movie_name):
    params = {
        "serviceKey": DATA_API_KEY,
        "pageNo" : "1",
        "numOfRows" : "1",
        "title": movie_name
    }
    
    response = requests.get(KMRB_MOVIE_URL, params=params)
    
    if response.status_code == 200:
        try:
            # XML 파싱
            root = ET.fromstring(response.text)
            item = root.find(".//item")
            
            if item is not None:
                movie_details = {
                    "영화명": item.find("useTitle").text if item.find("useTitle") is not None else "정보 없음",
                    "종별": item.find("gradeName").text if item.find("gradeName") is not None else "정보 없음",
                    "줄거리": item.find("workCont").text if item.find("workCont") is not None else "정보 없음",
                    "제작국": item.find("prodcNatnlName").text if item.find("prodcNatnlName") is not None else "정보 없음",
                }

                movie_info_list = list(movie_details.values())

                return movie_info_list
            else:
                return {"영화명": movie_name, "종별": "결과 없음", "줄거리": "", "감독": "", "제작국": ""}
        except ET.ParseError:
            print("XML 파싱 오류")
            return None
    else:
        print(f"API 호출 실패. 상태 코드: {response.status_code}")
        return None

# 따로 저장된 영화 데이터 병합
def merge_movie_info(detail_info, rating_info):
    merged_info = rating_info.copy()
    for key, value in detail_info.items():
        if key not in merged_info:
            merged_info[key] = value
        else:
            # 중복 키 처리
            if merged_info[key] != value:   # 값이 다를 경우
                merged_info[key] = f"{merged_info[key]}, {value}" if key != "영화명" else value
    return merged_info

# 유저 프로필 생성 및 벡터화
def create_user_profile(preferences, vectorizer):
    # 유저의 선호도를 하나의 문자열로 결합
    user_features = (
        preferences.get("장르명", "") + " " +
        preferences.get("감독명", "") + " " +
        preferences.get("배우명", "") + " " +
        preferences.get("상영형태명", "")
    )
    
    # 텍스트 벡터화
    user_vector = vectorizer.transform([user_features])
    return user_vector    

# 영화 추천 리스트 생성
def get_movie_recommendation(user_profile_vector, movie_vector, movie_titles):
    # 유저와 영화들 간의 유사도 계산
    user_similarities = cosine_similarity(user_profile_vector, movie_vector).tolist()

    # 유사도와 영화 제목을 묶어서 (유사도, 제목) 튜플 형태로 리스트에 저장
    movie_similarities = [(user_similarities[0][i], movie_titles[i]) for i in range(len(movie_titles))]
    
    # 유사도가 높은 순서대로 정렬
    movie_similarities.sort(reverse=True, key=lambda x: x[0])
    
    # 유사도가 높은 순으로 영화 제목 출력
    sorted_movie_titles = [movie for _, movie in movie_similarities]
    
    return sorted_movie_titles

# 통합 실행
def main():

    # TF-IDF 초기화
    vectorizer = TfidfVectorizer(stop_words="english")

    # 가상 유저 선호 데이터
    user_preferences = {
        "장르명" : "액션 스릴러",
        "감독명" : "",
        "배우명" : "",
        "상영형태명" : "2D 4D"
    }

    target_date = "20241110"  # 조회할 날짜 (YYYYMMDD 형식)
    
    # 1. 일별 박스오피스에서 영화 코드 가져오기
    movie_codes = fetch_box_office_codes(target_date)
    if not movie_codes:
        print("영화 코드를 가져오지 못했습니다.")
        return
    
    print(f"박스오피스 영화 코드 리스트: {movie_codes}")
    
    # 2. 영화 상세 정보 가져오기
    # all_movie_details, movie_names = fetch_all_movie_details(movie_codes)
    all_movie_details = []
    movie_names = []
    for code in movie_codes:
        details = fetch_movie_details(code)
        if details:
            all_movie_details.append(details)
            movie_names.append(details[0])
            #print(f"{details}")

    print("\n\n\n")

    # 3. 영화 등급분류정보 조회
    all_rating_details = []
    for movie_name in movie_names:
        rating_details = fetch_movie_rating_info(movie_name)
        if rating_details:
            all_rating_details.append(rating_details)
            #print(f"{rating_details}")



    # 영화 데이터 병합
    merged_info = []
    # 영화명 기준으로 정보를 합침
    for rating, detail in zip(all_rating_details, all_movie_details):
        # 영화 정보가 동일한 순서대로 합쳐짐
        merged_info.append(rating + detail[1:])  # 첫 번째 항목(영화명)은 제외하고 합침


    # 영화 정보 벡터화
    feature_matrix = vectorize_movie_data(merged_info, vectorizer)

    # 유저 프로필 벡터 생성
    user_vector = create_user_profile(user_preferences, vectorizer)

    # 영화들 간의 유사도 계산
    cosine_sim = cosine_similarity(feature_matrix)

    # 첫번째 영화와 다른 영화들 간의 유사도
    print("영화들 간의 유사도:",cosine_sim[0])

    print("\n")

    # 영화 추천 리스트
    recommended_movies = get_movie_recommendation(user_vector, feature_matrix, movie_names)

    # 추천 영화 출력
    print("유저와 유사도가 높은 순서대로 추천 영화 목록:")
    for movie in recommended_movies:
        print(movie)

if __name__ == "__main__":
    main()
