"""
    LoginServiceImpl
"""
import numpy as np
import pandas as pd
import os
import json

from sklearn.ensemble import RandomForestClassifier


def userCheckMl(params):
    # 성별 구분
    if float(params["gender"]) == 1.0:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/남자회원정보.csv'))
        df2 = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/남자상품정보.csv'))
    else:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/여자회원정보.csv'))
        df2 = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/여자상품정보.csv'))

    user_feature = np.array(df[['금액', '연령', '개수']])
    user_target = np.array(df['가격 카테고리'])
    user_feature_nm = list(df[['금액', '연령', '개수']])

    # 3. 모델 생성 --> DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.linear_model import LogisticRegression  # 로지스틱 회귀(분류)
    from sklearn.ensemble import VotingClassifier

    # 2. ensemble 분류기
    clf1 = GaussianNB()
    clf2 = RandomForestClassifier(n_estimators=50)  # bagging 대표적 분류기
    clf3 = LogisticRegression(max_iter=10000)
    # clf4 = LinearSVC(C=0.1) # 확률 처리할 함수가 미제공 ==> predict_proba

    # 3. VotingClassifer 로 묶기
    model = VotingClassifier(estimators=[('gnb', clf1), ('rf', clf2), ('lr', clf3)], voting='soft')  # , ('lsv', clf4)

    # 4. 데이터 훈련: model.fit(feature, target)
    model.fit(user_feature, user_target)

    # 5. 예측: model.predict(임의의값)
    pred = model.predict(user_feature)

    # 6. 예측 정확도 -> accuracy_score(my_data_feature, pred)
    from sklearn.metrics import accuracy_score
    score = accuracy_score(user_target, pred)

    # 7. 사용자 데이터
    user_data = [[float(params["price"]), float(params["age"]), float(params["cnt"])]]
    pred = model.predict(user_data)

    result_df = df2.loc[df2['가격 카테고리'] == int(pred[0])]

    result = "가격 카테고리 : " + str(result_df["가격 카테고리"].values[0]) + " / 상품 카테고리(상품 명) : " + str(
        result_df["상품 카테고리"].values[0]) + "(" + str(result_df["상품 명"].values[0]) + ")" + " / 상품 가격 : " + str(
        result_df["상품 가격"].values[0])

    json_result = {}
    json_result["result"] = result
    json_result["pred"] = str(pred)
    json_result["accuracy"] = float(score)

    return json.dumps(json_result, ensure_ascii=False)


def select_golden_zone(params):
    gender = float(params["gender"])
    ct = params["ct"]
    ct = str(ct[1])

    # 성별 구분
    if gender == 1.0:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/남자상품정보.csv'))
    else:
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/여자상품정보.csv'))
    result_df = df[df['가격 카테고리'].astype(str).str.contains(ct)]


    # 골든존 2개 뽑기
    data = np.array(result_df.index.array)
    n1 = [-1]
    n2 = [-1]

    for a in range(100):
        if n1 == [-1]:
            n1 = np.random.randint(data[0], data[data.size - 1] + 1, 1)  # (start,end,len)
        else:
            value = np.random.randint(data[0], data[data.size - 1] + 1, 1)  # (start,end,len)
            if n1 == value:
                continue
            else:
                n2 = value
                break

    product_1 = df.loc[n1]
    product_2 = df.loc[n2]

    # 골든존 세번째 상품 뽑기
    result_df2 = df[df['고객사 추천여부(시즌상품, 에디션 등)'].astype(str).str.contains("네")]
    data2 = np.array(result_df2.index.array)
    n3 = [-1]

    for a in range(100):
        n3 = np.random.randint(data2[0], data2[data2.size - 1] + 1, 1)  # (start,end,len)
        if n1 != n3 and n2 != n3:
            break
        else:
            continue

    product_3 = df.loc[n3]

    result = {
        "product_1": {'nm': product_1["상품 명"].values[0], 'pr': format(product_1["상품 가격"].values[0], ','),
                      'img': product_1["상품 이미지 명"].values[0]}
        , "product_2": {'nm': product_2["상품 명"].values[0], 'pr': format(product_2["상품 가격"].values[0], ','),
                        'img': product_2["상품 이미지 명"].values[0]}
    }

    result2 = {'nm': product_3["상품 명"].values[0], 'pr': format(product_3["상품 가격"].values[0], ','), 'img': product_3["상품 이미지 명"].values[0]}

    from flask import render_template
    return render_template('/main/main.html', result=result, result2=result2)
