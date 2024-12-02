import pandas as pd

from surprise import Dataset, Reader, SVD
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

## 데이터 불러오기 및 통합
# 영화
movies_path = "/movies.csv"  # movieId, title, genres, tags 정보가 포함된 파일
movie_ratings_path = "/ratings.csv"      # movieId, rating 정보가 포함된 파일

# 공연
performance_path = "/performance.csv"  # performanceId, title, genres, tag
performance_ratings_path = "/performance_rating.csv"  # userId, performanceId, rating

# 전시
exhibition_path = "/exhibition.csv"  # exhibitionId, title, genres, tag
exhibition_ratings_path = "/exhibition_rating.csv"  # userId, exhibitionId, rating

# ratings.csv 및 movies.csv 로드
movies = pd.read_csv(movies_path)
movie_ratings = pd.read_csv(movie_ratings_path)

performances = pd.read_csv(performance_path)
performance_ratings = pd.read_csv(performance_ratings_path)

exhibitions = pd.read_csv(exhibition_path)
exhibition_ratings = pd.read_csv(exhibition_ratings_path)

# 공연, 전시, 영화 데이터에 공통 'itemId' 추가
performances['itemId'] = "P" + performances['performanceId'].astype(str)
exhibitions['itemId'] = "E" + exhibitions['exhibitionId'].astype(str)
movies['itemId'] = "M" + movies['movieId'].astype(str)

# 공연, 전시, 영화 평점 데이터에 'itemId' 추가
performance_ratings['itemId'] = "P" + performance_ratings['performanceId'].astype(str)
exhibition_ratings['itemId'] = "E" + exhibition_ratings['exhibitionId'].astype(str)
movie_ratings['itemId'] = "M" + movie_ratings['movieId'].astype(str)

movies = movies.fillna("")  # NaN 값을 빈 문자열로 채움
exhibitions = exhibitions.fillna("")
performances = performances.fillna("")

# 통합 데이터 생성
all_items = pd.concat([
    movies[['itemId', 'title', 'genres', 'tag']],
    performances[['itemId', 'title', 'genres', 'tag']],
    exhibitions[['itemId', 'title', 'genres', 'tag']]
], ignore_index=True)

all_ratings = pd.concat([
    movie_ratings[['userId', 'itemId', 'rating']],
    performance_ratings[['userId', 'itemId', 'rating']],
    exhibition_ratings[['userId', 'itemId', 'rating']]
], ignore_index=True)

# 데이터 벡터화 함수
def vectorize_item_data(item_data, vectorizer):
    item_texts = []
    for _, item in item_data.iterrows():
        # 장르 분리 방식 결정
        if item['itemId'].startswith(('M', 'P', 'E')):
            genres = item['genres'].split('|')
        else:
            genres = [item['genres']]  # 예외적으로 분리가 필요 없는 경우
        
        # 제목, 장르, 태그 결합
        combined_text = " ".join([str(item['title']), 
                                  " ".join(genres),  # 장르 분리 결과 사용
                                  str(item['tag'])]).strip()
        if combined_text:  # 빈 텍스트 제외
            item_texts.append(combined_text)
    
    return vectorizer.fit_transform(item_texts)



# 유저 프로필 생성 함수
def vectorize_user_profile(user_profile, vectorizer):
    # 유저 프로필의 정보를 하나의 문자열로 결합
    user_features = (
        user_profile.get("genres","") + " " +
        user_profile.get("tags","") + " "
    )

    # 텍스트 벡터화
    user_profile_vector = vectorizer.transform([user_features])
    return user_profile_vector

# 사용자 프로필 생성 - 높은 평점을 매긴 아이템들의 장르와 태그를 반영
def create_user_profile(user_ratings):
    # 평균 평점 계산
    average_rating = user_ratings['rating'].mean()

    # 평균 평점보다 높은 영화 필터링
    high_rated_items = user_ratings[user_ratings['rating'] > average_rating]

    # 평균 평점보다 높은 영화 개수
    high_rated_item_count = len(high_rated_items)

    # movieId 추출
    high_rated_item_ids = high_rated_items['itemId'].unique()

    # 해당 movieId의 태그와 장르 가져오기
    filtered_items = all_items[all_items['itemId'].isin(high_rated_item_ids)]

    # 태그 빈도 계산
    tags_series = filtered_items['tag'].dropna().str.split(r'[,\s]+').explode()  # 쉼표 또는 공백 기준으로 분리
    tags_count = tags_series.value_counts()  # 태그별 빈도 계산

    # 장르 빈도 계산
    genres_series = filtered_items['genres'].dropna().str.split('|').explode()  # '|' 기준으로 장르 분리
    genres_count = genres_series.value_counts()  # 장르별 빈도 계산

    # 태그 필터링: 빈도가 3회 이상인 태그만 추출
    filtered_tags = tags_count[tags_count >= 3].index.tolist()

    # 장르 필터링: 빈도가 3회 이상인 태그만 추출
    filtered_genres = genres_count[genres_count >= 3].index.tolist()

    # user_profile 형식으로 반환
    user_profile = {
        "genres": " ".join(filtered_genres),
        "tags": " ".join(filtered_tags)
    }

    return user_profile

# # 예측 평점이 높은 영화만 필터링 (최적화)
# def get_top_high_rated_item_ids(predictions, threshold=4.0, top_n=100):
#     high_rating_predictions = [pred for pred in predictions if pred.est >= threshold]
#     #print(high_rating_predictions)
#     high_rating_predictions.sort(key=lambda x: x.est, reverse=True)  # 평점 순 정렬
#     return [pred.iid for pred in high_rating_predictions[:top_n]]  # 상위 top_n movieId 반환


# 예측 평점이 높은 영화만 필터링 (최적화)
def get_top_high_rated_item_ids(predictions, threshold=4.0):
    high_rating_predictions = [pred for pred in predictions if pred.est >= threshold]
    #print(high_rating_predictions)
    high_rating_predictions.sort(key=lambda x: x.est, reverse=True)  # 평점 순 정렬
    return [pred.iid for pred in high_rating_predictions]  # 상위 top_n movieId 반환

def calculate_similarity_for_high_rated_items(user_profile_vector, high_rated_item_ids, item_data, vectorizer, user_id, model, ratings_data):
    """
    평점이 높은 영화들에 대해 유사도 계산 및 예측 평점과 실제 평점 추가.
    """
    # 해당 영화들의 데이터 필터링
    filtered_items = item_data[item_data["itemId"].isin(high_rated_item_ids)]
    
    if filtered_items.empty:
        raise ValueError("No items to transform. The filtered_items DataFrame is empty.")


    # 영화 벡터화 (vectorizer는 이미 학습된 상태로 사용)
    filtered_item_vector = vectorizer.transform(
    [
        " ".join([
            str(row['title']), 
            " ".join(
                row['genres'].split('|')
            ),
            str(row['tag'])
        ]).strip()
        for _, row in filtered_items.iterrows()
        if not pd.isna(row['title']) and not pd.isna(row['genres']) and not pd.isna(row['tag'])
    ]
    )
    
    # 유사도 계산
    similarity_scores = cosine_similarity(user_profile_vector, filtered_item_vector)
    
    # 유사도가 높은 순으로 정렬
    sorted_indices = similarity_scores[0].argsort()[::-1]
    top_similar_items = []
    
    for idx in sorted_indices:
        item_id = filtered_items.iloc[idx]["itemId"]
        title = filtered_items.iloc[idx]["title"]
        genres = filtered_items.iloc[idx]["genres"]
        similarity = similarity_scores[0][idx]
        
        # 예측 평점
        predicted_rating = model.predict(user_id, item_id).est
        
        # 실제 평점 조회
        actual_rating_row = ratings_data[
            (ratings_data["userId"] == int(user_id)) & (ratings_data["itemId"] == item_id)
        ]
        actual_rating = actual_rating_row["rating"].values[0] if not actual_rating_row.empty else "N/A"
        
        # 유사도 * 예측 평점의 곱을 추천 점수로 계산
        recommend_score = similarity * predicted_rating

        top_similar_items.append({
            "title": title,
            "genres": genres,
            "recommend_score": recommend_score,
            "similarity": similarity,
            "predicted_rating": predicted_rating,
            "actual_rating": actual_rating,
        })
    
    # 추천 점수(recommend_score)를 기준으로 정렬
    top_similar_items.sort(key=lambda x: x["recommend_score"], reverse=True)

    return top_similar_items

def test_model(model, testset, trainset, all_items_data):
    # 모델 평가
    predictions = model.test(testset)
    accuracy.rmse(predictions)

    # 훈련 세트에 대해 예측
    train_predictions = model.test(trainset.build_testset())
    train_rmse = accuracy.rmse(train_predictions)

    # 테스트 세트에 대해 예측
    test_predictions = model.test(testset)
    test_rmse = accuracy.rmse(test_predictions)

    print(f"훈련 세트 RMSE: {train_rmse}")
    print(f"테스트 세트 RMSE: {test_rmse}")

    #과적합 확인
    if train_rmse < test_rmse:
        print("과적합이 발생했을 수 있습니다.")
    else:
        print("과적합이 발생하지 않았습니다.")

    # 교차 검증으로 모델 성능 확인
    cross_val_results = cross_validate(model, all_items_data, measures=['RMSE'], cv=5, verbose=True)

    # 교차 검증 결과 출력
    print(f"교차 검증 결과 (RMSE): {cross_val_results['test_rmse']}")

def get_recommendations_based_on_similarity(user_profile_vector, item_vectors, item_data, top_n=30):
      # 유사도 계산
    similarity_scores = cosine_similarity(user_profile_vector, item_vectors)
    
    # 유사도 순으로 정렬 (내림차순)
    sorted_indices = similarity_scores.argsort()[0][::-1]
    
    # 상위 N개의 아이템을 추천
    top_items = []
    for idx in sorted_indices[:top_n]:
        item_id = item_data.iloc[idx]["itemId"]  # item_data는 아이템 정보를 담고 있는 데이터프레임
        title = item_data.iloc[idx]["title"]
        genres = item_data.iloc[idx]["genres"]
        similarity = similarity_scores[0][idx]
        
        top_items.append({
            "item_id": item_id,
            "title": title,
            "genres": genres,
            "similarity": similarity,
        })
    
    return top_items

# 통합 실행
def main():

    # TF-IDF 초기화
    vectorizer = TfidfVectorizer(stop_words=None)

    # 모든 항목 정보 벡터화
    item_vector = vectorize_item_data(all_items, vectorizer)

    initial_user_profile = {
        "genres": "romance horor musical dance sci-fi fantasy",
        "tags": "live playful space future festival"
    }

    # 사용자 평점 기반 유저 프로필 벡터 생성 - genres tags
    user_id = 1     # 임시로 user_id 를 1로 설정
    user_ratings = all_ratings[all_ratings['userId'] == user_id]
    user_profile = create_user_profile(user_ratings)
    user_profile_vector = vectorize_user_profile(user_profile, vectorizer)

    # Surprise Reader 객체 생성(user-item-rating)j
    reader = Reader(line_format="user item rating", sep=",", skip_lines=1, rating_scale=(0.5, 5.0))
    all_items_data = Dataset.load_from_df(all_ratings[['userId', 'itemId', 'rating']], reader=reader)

    # 데이터셋 분리 및 모델 학습
    trainset, testset = train_test_split(all_items_data, test_size=0.2)
    model = SVD(reg_all=0.1)    # reg_all = 0.02 ~ 0.1
    model.fit(trainset)

    # 1. 사용자 1번의 영화 예측 평점 계산
    all_predictions = [model.predict(user_id, item_id) for item_id in all_items["itemId"]]

    # 2,3 필터링 및 movieId 추출 - 평점 4.0 이상 상위 nn개 (실행 시간 감소)
    #high_rated_item_ids = get_top_high_rated_item_ids(all_predictions, threshold=4.0, top_n=100)
    high_rated_item_ids = get_top_high_rated_item_ids(all_predictions, threshold=4.0)


    # 4. 유사도가 높은 영화 계산 + 예측/실제 평점 출력
    similar_items = calculate_similarity_for_high_rated_items(
        user_profile_vector, high_rated_item_ids, all_items, vectorizer, user_id, model, all_ratings
    )

    # 5. 추천 결과 출력 (협력 필터링과 유사도 모두 반영)
    print("예측 평점과 유사도를 모두 반영한 추천 결과:")
    for i, item in enumerate(similar_items[:30], start=1):
        print(
            f"{i}. 제목: {item['title']}, "
            f"추천 점수: {item['recommend_score']:.4f}, "
            f"유사도: {item['similarity']:.4f}, "
            f"예측 평점: {item['predicted_rating']:.2f} "
        )



    # 5. 유사도 기반 추천 결과 출력
    initial_user_vector = vectorize_user_profile(initial_user_profile, vectorizer)
    
    similar_only_items = get_recommendations_based_on_similarity(initial_user_vector, item_vector, all_items, top_n=30)

    print("\n유사도만 반영된 추천 결과:")
    for i, item in enumerate(similar_only_items[:30], start=1):
        print(
            f"{i}. 제목: {item['title']}, "
            f"유사도: {item['similarity']:.4f}"
        )


if __name__ == "__main__":
    main()
