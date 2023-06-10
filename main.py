import json
import csv

file = open("1097133_5000.json", "r", encoding='utf-8') # 파일 열기, "r" : 읽기 전용
csv_file = open("word_data_5000.csv", "w", newline='', encoding='UTF-8-sig') # 파일이 존재하지 않으면 새로 생성, "w" : 쓰기
data = json.load(file) # load 함수를 통해 json 파일의 데이터를 가져옴
csv_writer = csv.writer(csv_file) # .csv 파일을 쓰기모드로 오픈하고, 파일 객체(csv.writer)에 넣음
csv_writer.writerow(["target_code", "word_nm", "word_mean"]) # writerow() 메서드를 통해 list 데이터를 한 라인에 추가함(첫 행)

# 딕셔너리의 get() : key 값의 value를 반환함
# dict.get(key, default = None), 해당 key가 없을 때 반환되는 값 : None
channel = data.get("channel") # key:"channel"의 value값을 channel 변수에 대입 {...}
# key:"channel"의 value값으로 "total","title","description","item" 이 있는데, 그 중에 key:"item"의 value값을 item 변수에 대입
item = channel.get("item")
cnt = 0
error_cnt = 0
for item_data in item: # item 리스트의 value들을 차례대로 불러옴
    target_code       = item_data.get("target_code", None) # item 리스트 value 중 key:"target_code"에 해당하는 데이터를 저장
    try: # 예외 발생 없으면 try 블록 수행
        word_info = item_data.get("word_info") # key:"word_info"의 value를 저장
        word = word_info.get("word", None) # key:"word_info"의 value 중 key:"word"의 value를 저장
        pos_info = word_info.get("pos_info")[0] # key:"word_info"의 value 중 key:"pos_info"의 0번째 value를 저장
        pos_code = pos_info.get("pos_code", None) # key:"pos_info"의 0번째 value 중 key:"pos_code"의 value를 저장
        # key:"pos_info"의 value 중 key:"comm_pattern_info"의 0번째 value를 저장
        comm_pattern_info = pos_info.get("comm_pattern_info")[0]
        # key:"comm_pattern_info"의 value 중 key:"comm_pattern_code"의 value 를 저장
        comm_pattern_code = comm_pattern_info.get('comm_pattern_code', None)
        sense_info = comm_pattern_info.get('sense_info') # key:"comm_pattern_info"의 value 중 key:"sense_info"의 value 를 저장
        # sense_info 리스트의 모든 요소(sense_data:"definition","type","definition_original","sense_code")를 하나씩 불러와
        # key:"sense_info"의 value 중 key:"definition"에 해당하는 value를 리스트 안에 저장
        definition_list = [sense_data.get('definition', None) for sense_data in sense_info]
    except: # 예외 발생시 except 블록 수행
        error_cnt += 1
        continue # 다음 item_data를 불러와 for문 수행
    cnt += 1 # 단어명, 단어의미 추가하고 단어 개수 +1
    for definition in definition_list: # 다음 item_data를 가져오기 전에 definition_list의 value를 불러옴
        # 하나의 단어에 뜻이 여러 개인 경우, 뜻 마다 한 라인씩 추가함
        csv_writer.writerow([target_code, word, definition]) # writerow() 메서드를 통해 list 데이터를 한 라인에 추가함
    print(target_code, " / ", word, " / ", definition_list)

file.close()
csv_file.close()