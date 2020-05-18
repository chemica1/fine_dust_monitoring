from File_class import File_class
import serial, requests, time

class barcode:
    def __init__(self):
        comport = File_class('com').call_the_list()
        tmp_location = File_class('location').call_the_list()
        self.location = str(tmp_location[0])
        self.serialFromArduino = serial.Serial(str(comport[0]), 9600, timeout=1)

    def main(self):
        line = []
        while True:  # 데이터가 있다면
            for c in self.serialFromArduino.read():
                if not c == 124:  # 아스키코드 |
                    line.append(chr(c))
                if c == 124:
                    tmp = self.parsing_data(line)  # 데이터 처리 함수로 호출
                    if 'a' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('a', '')
                        tmp = tmp[:(len(tmp) )]
                        dust_1p0 = tmp
                    elif 'b' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('b', '')
                        tmp = tmp[:(len(tmp))]
                        dust_2p5 = tmp
                    elif 'c' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('c', '')
                        tmp = tmp.replace('-', '')
                        tmp = tmp[:(len(tmp))]
                        dust_10p0 = tmp
                    elif 'd' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('d', '')
                        tmp = tmp.replace('-', '')
                        tmp = tmp[:(len(tmp))]
                        temperature = tmp
                    elif 'e' in tmp:
                        tmp = tmp.lstrip()
                        tmp = tmp.replace('e', '')
                        tmp = tmp.replace('-', '')
                        tmp = tmp[:(len(tmp))]
                        humidity = tmp

                        now = time.localtime()
                        print(f'{now.tm_year}/{now.tm_mon}/{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec}  ->  pm1.0 : {dust_1p0}   pm2.5 : {dust_2p5}   pm10.0 : {dust_10p0}   {temperature}°C   {humidity}%')

                        if now.tm_sec < 2 or now.tm_sec > 58 :
                            try:
                                URL = f'http://175.118.126.63/dnsm_dust/api.cfm?temperature={temperature}&humidity={humidity}&dust1={dust_1p0}&dust2={dust_2p5}&dust3={dust_10p0}&idx_location={self.location}'
                                requests.get(URL)
                                print("데이터 전송 완료")
                                time.sleep(7)
                            except:
                                print("인터넷 연결 / 서버 확인 필요")

                    del line[:]

    def parsing_data(self, data): # 리스트 구조로 들어 왔기 때문에 작업하기 편하게 스트링으로 합침
        tmp = ''.join(data)
        return tmp

def run():
    a = barcode()
    a.main()

if __name__ == "__main__":
    run()