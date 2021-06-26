#해당 코드는 사용자로부터 입력받은 신호와 미리 저장해둔 코드가 일치하는지 확인하는 코드입니다. 일치한다면 잠금해제합니다.


from datetime import datetime
import configparser 
config = configparser.ConfigParser()
config.read('pattern.ini')
pattern=str(config['pattern']['1'])
print(pattern)
split_pattern=pattern.split(" - ")
count=0
time=[]
signal=[]
for i in split_pattern:
    if(count%2==0):
        time.append(i)
    else:
        signal.append(i)
    count=count+1
count=0
for i in time:
    FMT = '%H:%M:%S,%f'#마이크로초 고려 O
    #FMT = '%H:%M:%S' #마이크로초 고려 X
    time[count] = str(datetime.strptime(time[count+1], FMT) - datetime.strptime(time[count], FMT))
    #마이크로초 고려 O 여기 아래서부터 del 위까지 
    count2=0
    for i in time[count]:
        if(i=='.'):
            time[count]=time[count][:count2]+','+time[count][count2+1:]
            break
        else:
            count2=count2+1
    else:
        time[count]=time[count][:count2]+',0'
            
    count=count+1
    if(count==len(time)-1):
        break

#패턴 마지막은 0초나까 제외
del time[len(time)-1]
del signal[len(signal)-1]

print(time)
print(signal)

count=0

'''
#마이크로초 고려 X
for i in time:
    pt = datetime.strptime(str(time[count]),'%H:%M:%S')
    time[count] =pt.second + pt.minute*60 + pt.hour*3600
    if(count==len(time)-1):
        break
    count=count+1
'''
    
#마이크로초 고려 O
for i in time:
    pt = datetime.strptime(str(time[count]),'%H:%M:%S,%f')
    time[count] =pt.microsecond/1000000.0 + pt.second + pt.minute*60 + pt.hour*3600
    print(pt.second)
    if(count==len(time)-1):
        break
    count=count+1


print(time)
print(signal)

print(time)
print(signal)
k=0
#측정 시간을 소요 시간으로 변환
'''while True:
    time[k]=float(time[k+1])-float(time[k])
    k=k+1
    if(k==len(time)):
        #del time[k]
        #del signal[k]
        break
'''
systems=(zip(time, signal))

print(systems)
users=[['open1',0.3], ['close1',2.43], ['open2',0.08], ['close2',0.09]]
count=0
if(len(users)==len(signal)):
    for user, system in zip(users, systems):
        i=0
        if(user[i][:-1]!=system[i+1]):
            print("잠금 해제 실패(깜빡임 순서가 다름)")
            count=count+1
            break
        i=i+1
        
        if(abs(user[i]-float(system[i-1]))>0.1):
            print("잠금 해제 실패(시간이 다름)")
            count=count+1
            break   

else:
    print("잠금 해제 실패(갯수가 다름)")
    count=count+1
if(count==0):
    print("잠금 해제 성공")