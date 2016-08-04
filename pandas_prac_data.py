#coding:utf-8

import pandas as pd

df_sample =\
pd.DataFrame([["day1","day2","day1","day2","day1","day2"],
              ["A","B","A","B","C","C"],
              [100,150,200,150,100,50],
              [120,160,100,180,110,80]] ).T  #とりあえず適当なデータを作ります

df_sample.columns = ["day_no","class","score1","score2"]  #カラム名を付ける
df_sample.index   = [11,12,13,14,15,16]  #インデックス名を付ける

df_sample.columns   #列名を取得 
df_sample.index     #インデックス名を取得


df_sample.columns = ["day_no","class","point1","point2"]   # カラム名を上書き
df_sample.index   = [11,12,13,14,15,16]   # インデックス名を上書きする


# Renameメソッドを使う
df_sample.rename(columns={'score1': 'point1'})  #対応関係を辞書型で入れてやる

# 行数の確認
len(df_sample)

# 次元数の確認
df_sample.shape #（行数、列数）の形で返す

# カラム情報の一覧
df_sample.info() #カラム名とその型の一覧

# 各列の基礎統計量の確認
# Rでいうところのsummary()
df_sample.describe() # 平均、分散、4分位など

# head / tail
df_sample.head(10) #先頭10行を確認
df_sample.tail(10) #先頭10行を確認


# ilocを使った列選択
# 文法 ：iloc[rows番号, columns番号]の形で書く
df_sample.iloc[:,0]  # 番号で選択
df_sample.iloc[:,0:2] #複数で連番の場合。リスト表記でも行ける


# ixを使った列選択
# 列名と列番号両方が使える。基本これを使っておけば良い感
df_sample.ix[:,"day_no"] # なお、単列選択の場合には結果はPandas.Series Object
df_sample.ix[:,["day_no","score1"]] # 複数列選択の場合には結果はPandas.Dataframeになる

df_sample.ix[0:4,"score1"] # 行は番号で、列は列名で選択することもできる


series_bool = [True,False,True,False]
df_sample.ix[:,series_bool]  #また、Booleanの配列でも選択できる


#列名の部分一致による選択
#R DplyrにはSelect(Contains()）という、列名部分一致選択のための便利スキームがある
#Pandasにはそれに該当する機能はないため、少し工程を踏む必要がある

score_select = pd.Series(df_sample.columns).str.contains("score") #"score"を列名に含むかどうかの論理判定
df_sample.ix[:,np.array(score_select)]   # 論理配列を使って列選択