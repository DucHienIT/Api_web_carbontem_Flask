import numpy as np
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import NearestNeighbors
from matplotlib.colors import ListedColormap
from sklearn import metrics
import json
import warnings
import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)
import pyodbc 
# s = 'DUCTHINHPC' #Your server name 
# d = 'Hackathon' #Your database name
# str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';Trusted_Connection=yes'
str = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:hackathon-server-carbon.database.windows.net,1433;Database=hackathon-db-new;Uid=ducthinh-carbon;Pwd=th@nCarbo;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def ret_cluster_knn(new_student_input):
    cols = ["MSSV","Cau1","Cau2","Cau3","Cau4","Cau5","Cau6","Cau7","Cau8","Cau9","Cau10","Cau11","Cau12","Cau13","Cau14","Cau15", "Cau16","Cau17","Cau18","Cau19","Cau20","Cau21","Cau22","Cau23","Cau24","Cau25","Cau26","Cau27","Cau28","Cau29","Cau30","Cau31","Cau32","Cau33","Cau34","Cau35"]
    
    input_df = pd.DataFrame(columns=cols)
    input_df.loc[len(input_df)] = new_student_input


    conn = pyodbc.connect(str)
    sql_query = pd.read_sql_query('select * from dbo.Quiz',conn) 
    sql_query_road_mssv = pd.read_sql_query('select MSSV from dbo.Road',conn)
    # here, the 'conn' is the variable that contains your database connection information from step 2
    mssv_df = pd.DataFrame(sql_query_road_mssv)
    mssv_lst = mssv_df["MSSV"].values.tolist()
    
    data = pd.DataFrame(sql_query)
    data = data[data["MSSV"].isin(mssv_lst)]
    print("Xem co thua ko", data)
    dropped_na_df = data.dropna(axis=0,inplace=False)

    all_mssv = dropped_na_df["MSSV"] #keep all mssv for later use
    #reset the existing index, not inserting a new column
    dropped_na_df = dropped_na_df.reset_index(drop=True)
    dropped_na_df = dropped_na_df.drop(columns="MSSV",axis=1)


    #remove mssv in df khi scale
    #keep the mssv col
    input_mssv = input_df["MSSV"]
    input_df = input_df.drop(columns="MSSV",axis=1)
    dropped_na_df.reset_index(drop=True, inplace=True)
    #print("Sau khi reset:",dropped_temp_na_df)

    # ko dua cot mssv vào
    knn = NearestNeighbors(n_neighbors=5,radius=1,algorithm='brute',metric='minkowski')
    knn.fit(dropped_na_df)
    nn_input_idxs = knn.kneighbors(input_df, return_distance=False).flatten() #shape: (5,) before flat: (1,5) [[1, 55,22,33,44]]

    joined_mssv_df = dropped_na_df.join(all_mssv, how="right")
    joined_mssv_df = joined_mssv_df[joined_mssv_df.index.isin(nn_input_idxs)]
    mssv_np = joined_mssv_df["MSSV"].to_numpy()
    mssv_lst = mssv_np.tolist()
    return mssv_lst


def get_learning_path_knn(input_quiz):
    #pipe1 trả về index cluster của input và ndarray(numpy) mssv thuộc cùng cluster đó
    mssv_nn = ret_cluster_knn(input_quiz)
    #print("MSSVs:", mssv_nn)
    conn = pyodbc.connect(str)
    sql_query = pd.read_sql_query('select * from dbo.Road',conn)
    df_learning_path = pd.DataFrame(sql_query)
    print("Thu connect db:",df_learning_path)

    df_learning_path = df_learning_path[df_learning_path['MSSV'].isin(mssv_nn)]
    #sort by dtb descending and get 5 value

    ret_df_learning_path = df_learning_path[df_learning_path.columns[0:19]]
    return ret_df_learning_path.to_json(orient='records')
# input_quiz = [78110003,0,1,1,0,1,9,6,2,1,6,5,6,9,3,7,4,9,3,7,9,5,7,5,0,6,0,3,2,6,8,9,3,5,7,6]
# print(get_learning_path_knn(input_quiz))
