"""
짭다봇 V#
made by 설망래,이끼 낀 금화
"""
#모듈 불러오기 시작
import asyncio , pickle, discord , os , json
import psutil , time , random , calendar , math , requests
from discord.ext import commands
from discord.ext import tasks
from bs4 import BeautifulSoup
from maze import maze
import Api_lib
import WordDetection
import traceback
#기본 변수지정
error = []
BOT_TOKEN = "봇의 토큰입니다"

try:
    with open('maths.txt' , 'rb') as f:
        pfactors = pickle.load(f)
except:
    pfactors = {}
    with open('maths.txt', 'wb') as f:
        pickle.dump(pfactors, f)
try:
    with open('log.txt' , 'rb') as f:
        log = pickle.load(f)
except:
    log = {}
    with open('log.txt', 'wb') as f:
        pickle.dump(log, f)
global server_count
oper = ['운영자 ID를 넣어주세요']
server_count = 0
BOTGAME = "'ㅉ도움말 ' 로 도움말 확인해주세요!!!!"
re_cahelp = {'운영자명령어' : {'in':'짭다봇을 관리하는 운영자들을 위한 명령어들입니다' , 'ex' : '**디버그** , **상태설정** , **컴퓨터** , **명령어상태**'} ,
              '지원':{'in':'유저들의 편의를 위한 명령어들입니다','ex':'**도움말** , **짭다봇** , **접두사설정** , **접두사초기화**'},
              '잡다한기능들' : { 'in' : '"계륵"같은 명령어들이 모여있습니다!저희 봇의 핵심이죠!!' ,
                                 'ex' : '**골라** , **시간** , **요일** , **아스키변환** , **아스키해독** , **롤** , **코로나** , **테스트** , **번역** , **한글이름변환**'} , 
              '게임' : {'in' : '심심할때 게임한판 어떠신가요? 재미있는 게임들이 있습니다' , 'ex' : '**동전던지기** , **주사위던지기** , **가위바위보** , **미로** , **지뢰찾기** , **숫자야구**'} ,
              '수학' : {'in' : '복잡한 계산, 어려운 공식은 이제 짭다봇에게 맡기세요!! 설망래가 가장 열심히 업데이트 하는 카테고리랍니다!' , 'ex':'**소인수분해** , **계산** , **더하기** , **기호**'} ,
              '짭다봇로그' : {'in' : '누가 자꾸 뒷담화를 하고 메세지를 지운다고요?? 짭다봇이 감시해드립니다!! 설정된 채널로 알림을 보내드려요' , 'ex':'**로그채널설정** , **로그채널삭제**'}
              }
re_cohelp = {'테스트':{'in':'현재 짭다봇 개발진 설망래가 열심히 개발중인 필터링 기능을 위한 명령어 입니다!! 베타 테스트 같은 것이라 생각하시면 됩니다','g':'```ㅉ테스트 (문장)```','s':0},
              '가위바위보':{'in':'우리가 친구들과 하던 가위바위보입니다! 참고로 저희는 주작같은건 하지 않습니다^^','g':'```ㅉ가위바위보``` 입력후 시간내에 (가위/바위/보)중 하나 입력','s':0},
              '골라':{'in':'선택장애를 가지신 분들을 위한 기능입니다. 입력하신 항목중 원하시는 갯수만큼을 골라드려요','g':'```ㅉ골라 (뽑을 항목의 수) (항목 1) --- (항목n)```','s':0},
              '도움말':{'in':'신시대 물건에 어색하신 분들도 이 명령어면 다 알려드리죠!!','g':'```ㅉ도움말 (카테고리 또는 명령어-입력하지 않아도 가능)```','s':0},
              '동전던지기':{'in':'동전을 던져드려요. 앞면 또는 뒷면이 나와야 아니 나오겠죠??','g':'```ㅉ동전던지기```','s':0},
              '디버그':{'in':'벌레 잡다가 빡친 운영진이 만들었어요.운영진이 아닌 여러분은 사용이 불가능 하답니다','g':'```ㅉ디버그 (확인할 변수)```','s':0},
              '미로':{'in':'짭다봇의 가장 거대한 기능!! 미로를 만들어드려요.너무 큰 사이즈는 오히려 재미가 없을 수도 있다는 점 명심하세요!!','g':'```ㅉ미로 (가로) (세로) (스포일러처리여부)```','s':0},
              '상태설정':{'in':'봇의 상태 메세지를 설정할수 있는 기능입니다!! 운영진이 아닌 여러분을 쓸수 없어요','g':'```ㅉ상태설정 (메세지)```','s':0},
              '숫자야구':{'in':'숫자야구를 해요.3자리수이며 규칙은 구글에 검색해보세요.절대로 귀찮아서 이러는거 아닙니다^^','g':'```ㅉ숫자야구``` 입력 후 3자리 숫자를 추측하여 적기','s':0},
              '시간':{'in':'현재시간을 알려드려요','g':'```ㅉ시간```','s':0},
              '아스키변환':{'in':'아스키코드로 변환해드려요.','g':'```ㅉ아스키변환 (메세지)```','s':0},
              '아스키해독':{'in':'아스키코드를 해독해드려요.숫자사이를 "/"로 구분해주세요 ','g':'```ㅉ아스키해독 (아스키코드1) --- (아스키코드n)```','s':0},
              '요일':{'in':'입력하신 날짜의 요일을 알려드려요! 절대로 수학 문제풀다가 넣은거 아닙니다','g':'```ㅉ요일 (년도) (월) (일)```','s':0},
              '주사위던지기':{'in':'주사위를 던져줍니다','g':'```ㅉ주사위던지기```','s':0},
              '지뢰찾기':{'in':'지뢰찾기를 만들어드려요','g':'```ㅉ지뢰찾기 (가로) (세로) (지뢰의 수)```','s':0},
              '컴퓨터':{'in':'현재 짭다봇을 호스팅하고 있는 컴퓨터의 상태를 알려줍니다. 운영자가 아닌 여러분은 사용할수 없어요','g':'```ㅉ컴퓨터```','s':0} ,
              '소인수분해':{'in':'입력하신 수를 소인수분해해요. 빠르고 편리하답니다!' , 'g': '```ㅉ소인수분해 (소인수분해할 수)```','s':0} , 
              '서버정보':{'in':'현재 계신 서버의 정보를 알려드려요' ,  'g':'```ㅉ서버정보```','s':0} ,
              '채널정보':{'in':'현재 계신 채널의 정보를 알려드려요' ,  'g':'```ㅉ채널정보```','s':0} ,
              '계산':{'in':'강력한 울프럼알파api를 사용하여 계산해 드려요. 간단한 식은 기본명령어를 사용하는것이 더 빠를수 있어요!! 어떤 식이든 입력해 보세요!! 아 , 더 많은 수학기호들은 "기호"명령어로 확인하세요!!' , 'g':'```ㅉ계산 (계산할 식)```','s':0} ,
              '명령어상태':{'in':'명령어들의 (활성화/비활성화)상태로 전환할수 있어요. 운영자가 아닌 여러분은 사용하실수 없어요' , 'g':'```ㅉ명령어상태 (명령어) (사유또는 0)```','s':0} ,
              '롤':{'in':'원하시는 사람의 롤티어를 검색해줍니다!! 모든 정보는 OP.GG를 바탕으로 합니다','g':'```ㅉ롤 (사용자이름)```','s':0} ,
              '코로나':{'in':'현재 코로나 사태의 현황을 알려드려요','g':'```ㅉ코로나```','s':0} ,
              '로그채널설정':{'in':'짭다봇로그 채널을 (설정/변경)합니다. 설정하려면 등록할때 채널의 이름이 "짭다봇로그"라고 해주셔야합니다' , 'g':'```ㅉ로그채널설정```','s':0} ,
              '로그채널삭제':{'in':'짭다봇로그 채널을 삭제합니다. 명령어를 사용할때 채널의 이름이 "짭다봇로그"라고 해주셔야합니다' , 'g':'```ㅉ로그채널삭제```','s':0} ,
              '짭다봇':{'in':'짭다봇에 대한 정보를 알려드려요' , 'g':'```ㅉ짭다봇```','s':0} ,
              '더하기':{'in':'입력한 수들을 모두 더해드려요!! 똑똑한 짭다봇은 실수가 아닌 값들은 제외시킨답니다' , 'g':'```ㅉ더하기 (값들)```','s':0} , 
             '접두사설정':{'in':'여러분만의 개인 접두사를 설정해드려요. 5글자 미만으로 정해주세요' , 'g':'```ㅉ접두사설정```','s':0} ,
             '접두사초기화':{'in':'접두사를 "ㅉ"으로 초기화 해드립니다' , 'g':'```ㅉ접두사초기화```','s':0} ,
             '롤':{'in':'입력하신 닉네임의 롤 정보를 알려드려요!!','g':'```ㅉ롤 (유저 닉네임)```','s':0} , 
             '기호' :{'in':'여러가지 수학기호가 있는 기호표를 보여드려요','g':'```ㅉ기호```','s':0} ,
             '번역' :{'in':'네이버의 파파고 api를 이용하여 번역을 해드려요!!','g':'```ㅉ번역 (타겟 언어) (번역할 문장)```','s':0} ,
             '한글이름변환':{'in':'입력하신 한글이름을 로마자로 바꾸어 알려드려요!!','g':'```ㅉ한글이름변환 (변환할 이름)```','s':0}
              }
#pickle로 저장되어 있는 도움말이 최신 도움말인지 확인 후, 업데이트 하는 코드
try:
    with open('bot_base.txt' , 'rb') as f:
        cahelp = pickle.load(f)
        cohelp = pickle.load(f)
except:
    with open('bot_base.txt', 'wb') as f:
        pickle.dump(re_cahelp, f)
        pickle.dump(re_cohelp, f)
for i in re_cahelp:
    if i not in cahelp:
        cahelp[i] = re_cahelp[i]
    elif cahelp[i]['in'] != re_cahelp[i]['in'] or cahelp[i]['ex'] != re_cahelp[i]['ex']:
        cahelp[i]['in'] = re_cahelp[i]['in']
        cahelp[i]['ex'] = re_cahelp[i]['ex']
    else:
        pass
for i in re_cohelp:
    if i not in cohelp:
        cohelp[i] = re_cohelp[i]
    elif cohelp[i]['in'] != re_cohelp[i]['in'] or cohelp[i]['g'] != re_cohelp[i]['g']:
        cohelp[i]['in'] = re_cohelp[i]['in']
        cohelp[i]['g'] = re_cohelp[i]['g']
    else:
        pass
with open('bot_base.txt', 'wb') as f:
    pickle.dump(cahelp, f)
    pickle.dump(cohelp, f)

TWD = WordDetection.WordDetection()   # Test WordDetection
TWD.LoadData()
TWD.LoadBadWordData()





#함수만들기
def is_number(num):   #복소수인지 확인하는데 쓰임
    try:
        judge = str(complex(num))
        return False if(judge=='nan' or judge=='inf' or judge =='-inf') else True
    except: #num을 complex으로 변환 할 수 없는 경우
        return False


    
def pfactor(num):    #소인수분해 1차 개조판
    num = int(num)
    answer = {2:0 , 3:0}
    while num %2 == 0:
        answer[2] += 1
        num = num//2
    while num %3 == 0:
        answer[3] += 1
        num = num//3
    n = 1
    while num != 1:
        a = 6*n - 1
        b = a + 2
        if a > math.sqrt(num):
            if num in answer:
                answer[num] += 1
            else:
                answer[num] = 1
            num = 1
        elif num %a != 0 and num %b !=0:
            n += 1
        else:
            if num %a == 0:
                num = num//a
                if a in answer:
                    answer[a] += 1
                else:
                    answer[a] = 1
            else:
                num = num//b
                if b in answer:
                    answer[b] += 1
                else:
                    answer[b] = 1
    return answer




def mazemaker(maze_width , maze_height , userid):
    a = maze()
    a.create(maze_width , maze_height)
    a.save(f"{str(userid)}Noneanswer.png" , False , 10)
    a.save(f"{str(userid)}answer.png" , True , 10)
    return None

def get_prefix(app , message):
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/prefix.json', "r") as f:
        prefix = json.load(f)
    if str(message.author.id) not in prefix:
        return commands.when_mentioned_or('ㅉ')(app , message)
    pr = prefix[str(message.author.id)]
    return commands.when_mentioned_or(pr)(app , message)

def wolframalphaapi(what):
    a = Api_lib.Jjapdabot_api()
    return a.api_wolfram(what)

def riot_api(name):
    a = Api_lib.Jjapdabot_api()
    return a.riot_api(name)

def test_word_detection(word):
    TWD.input=word
    TWD.W2NR()
    TWD.lime_compare(TWD.BwT , TWD.WTD[0] , 0.9,False)
    result = TWD.result
    TWD.lime_compare(TWD.NewBwT , TWD.WTD[1] , 0.9,True)
    result += TWD.result
    return result

def naver_papago_api(lan , word):
    a = Api_lib.Jjapdabot_api()
    word_lan = a.api_naver_findlan(word)
    if 'langCode' not in word_lan or word_lan['langCode'] == 'unk':
        return 'cant_find_lan'
    word_lan = word_lan['langCode']
    result = a.api_naver_papago(word_lan , lan , word)
    if 'Error' in result:
        return 'papago_not_found'
    return result

def naver_ko2en_api(name):
    a = Api_lib.Jjapdabot_api()
    en_name = a.api_naver_ko2en(name)
    if 'Error' in en_name:
        return 'ko2en_not_found'
    return en_name


app = commands.Bot(command_prefix=get_prefix , help_command = None , owner_ids = oper)






#봇 코드 시작


"""
켜졌을떄 코드
"""
@app.event
async def on_ready():
    print('-----준비됨-----')
    g = discord.Game(' "ㅉ도움말" 로 도움말 보기!! ')
    await app.change_presence(status=discord.Status.online, activity=g)
    print("짭다봇 가동 성공")
    count_server.start()
    coro.start()



"""
채팅이 들어왔을떄 코드
"""
@app.event
async def on_message(message):
    if message.author.bot == 1:
        return None
    await app.process_commands(message)


"""
에러가 발생했을때 코드
"""

@app.event
async def on_command_error(ctx , error):
    if isinstance(error , commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'무언가 꼭 필요한 값이 없네요. || "ㅉ도움말 {ctx.command}"으로 문법을 학인해주세요!!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'무언가 제가 원하던 값과 다릅니다. || "ㅉ도움말 {ctx.command}"으로 문법을 학인해주세요!!')
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"아직 봇의 쿨타임이 남았어요 || {ctx.command}명령어를 이용하시려면 {int(error.retry_after)}초만 더 기다려주세요")
        return
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.send("워워 진정하세요.. 명령어는 한번에 하나씩만....")
        return
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send(f"{ctx.command}명령어는 개인메세지에서는 사용이 불가능해요")
        return
    if isinstance(error , commands.errors.NotOwner):
        await ctx.send(f'{ctx.command}명령어는 운영자 전용 명령어입니다')
        return

    embed = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000)
    embed.set_footer(text = '명령어에 버그가 발생하면 짭다봇의 운영진에게 정보가 갑니다.')
    embed.add_field(name = '버그가 반복될시 제보하는 곳' , value = '버그가 발생했다고요?? 스크린 샷과 함께 askjjapdabot@gmail.com 에 보내주세요\n더 빠르고 편리하답니다' , inline = True)
    embed.set_image(url = "https://media.discordapp.net/attachments/801337603861381140/828608368649961482/d9ba95c9b857fb7a.png")
    await ctx.send(embed=embed)
    embed = discord.Embed(title="오류!!", description=f"'**{ctx.command}**'명령어에서 오류가 발생했습니다. \n {ctx.author}(ID : {ctx.author.id}) 에 의해 발생함", color=0xFF0000)
    error_message = '\n'.join(traceback.format_exception(type(error),error,error.__traceback__,limit=1))
    embed.add_field(name="상세", value=f"```{error_message}```\n{'='*50}\n {error}")
    embed.set_footer(text = f'발생시간 : {time.ctime()}')
    await app.get_channel("오류 로그를 받을 서버 id").send(embed=embed)





"""
짭다봇 삭제 감지 코드
"""
@app.event
async def on_message_delete(message):
    if message.author.bot == 1:
        return None
    if message.guild.id in log:
        embed = discord.Embed(title = "삭제 감지", color = 0xFF0000)
        embed.add_field(name = "삭제된 내용", value =  message.content, inline = False)
        embed.add_field(name = "세부정보", value = f"```UserName  :  {str(message.author)}\nUserID : {str(message.author.id)}\nDeletedTime : {str(time.ctime())}```" , inline = False)
        embed.set_footer(text = '짭다봇은 12월에 서비스가 종료됩니다.')
        try:
            await app.get_channel(log[message.guild.id]).send(embed = embed)
        except AttributeError:
            del log[message.guild.id]
            with open('log.txt', 'wb') as f:
                pickle.dump(log, f)
    else:
        return None

@app.event
async def on_message_edit(before, after):
    if before.author.bot == 1:
        return None
    if before.content == after.content:
        return None
    if before.guild.id in log:
        embed = discord.Embed(title = "변경 감지", color = 0xFF0000)
        embed.add_field(name = "이전 내용", value = before.content , inline = False)
        embed.add_field(name = "변경된 내용" , value = after.content, inline = False)
        embed.add_field(name = "세부정보", value = f"```Name  : {str(before.author)}\nID : {str(before.author.id)}\nDeletedTime : {str(time.ctime())}```", inline = False)
        embed.set_footer(text = '짭다봇은 12월에 서비스가 종료됩니다.')
        try:
            await app.get_channel(log[before.guild.id]).send(embed = embed)
        except AttributeError:
            del log[before.guild.id]
            with open('log.txt', 'wb') as f:
                pickle.dump(log, f)
    else:
        return None



    

"""
command들
"""
#OPER - embed color:0x8b00ff
@app.command(pass_context=True)
@commands.is_owner()
async def 디버그(ctx ,*,var):
    if cohelp['디버그']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['디버그']['s']) + '를 사유로 사용을 금지했어요')
        return
    try:
        answer=eval(var)
    except Exception as e:
        answer = e
    await ctx.send(answer)

@app.command(pass_context=True)
@commands.is_owner()
async def 상태설정(ctx , * , var):
    if cohelp['상태설정']['s'] != 0:
        await ctx.send(f"운영자가 {str(cohelp['상태설정']['s'])}(을)를 사유로 사용을 금지했어요")
        return
    if var == '기본':
        game = discord.Game("   'ㅉ도움말 ' 로 도움말 확인해주세요!!!!")
    else:
        game = discord.Game(str(var))
    await app.change_presence(status=discord.Status.online, activity=game)
    await ctx.send('상태변경이 완료되었습니다')
    global BOTGAME
    BOTGAME = var

@app.command(pass_context=True)
@commands.is_owner()
async def 컴퓨터(ctx):
    if cohelp['컴퓨터']['s'] != 0:
        await ctx.send(f"운영자가 {str(cohelp['컴퓨터']['s'])}를 사유로 사용을 금지했어요")
        return
    embed = discord.Embed(title = "컴퓨터 상태", color = 0x8b00ff)
    embed.add_field(name = "CPU잔량" , value = str(psutil.cpu_times_percent(interval=None, percpu=False).idle) + "%")
    embed.add_field(name = "메모리(RAM)잔량" , value = str(psutil.virtual_memory().available/psutil.virtual_memory().total*100) + "%")
    embed.add_field(name = "저장공간(디스크)잔량" , value = str(psutil.disk_usage(path = "/").free/psutil.disk_usage(path = "/").total*100) + "%")
    await ctx.send(embed = embed)

@app.command(pass_context=True)
@commands.is_owner()
async def 명령어상태(ctx , command , * , text):
    if command not in cohelp:
        await ctx.send(command + ' 명령어는 명령어 목록에 존재하지 않습니다')
        return
    if command == '명령어상태':
        await ctx.send('"명령어상태"명령어는 상태변경이 불가능합니다')
        return
    if text == '0':
        cohelp[command]['s'] = 0
        await ctx.send(f'{command} 명령어의 상태를 "활성화"로 바꾸었어요')
        with open('bot_base.txt', 'wb') as f:
            pickle.dump(cahelp, f)
            pickle.dump(cohelp, f)
        return
    else:
        cohelp[command]['s'] = text
        await ctx.send(f'{command} 명령어를 "{text}"를 사유로 "비활성화" 시켰어요')
        with open('bot_base.txt', 'wb') as f:
            pickle.dump(cahelp, f)
            pickle.dump(cohelp, f)
        return


    
    

    
    

#MATH - embed color : 0xFFE400
@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,10.0 , type=commands.BucketType.user)
async def 더하기(ctx,*nums):
    if cohelp['더하기']['s'] != 0:
        await ctx.send(f"운영자가 {str(cohelp['더하기']['s'])}(을)를 사유로 사용을 금지했어요")
        return
    answer = 0
    not_num = []
    if len(nums) > 100:
        await ctx.send('항목의 수가 너무 많아요')
    for i in nums:
        j = i.replace('i','j')
        if not is_number(j):
            not_num.append(i)
        else:
            answer += complex(j)
    await ctx.send(f'답은 {str(answer)}입니다\n```복소수가 아니라서 제외된 값들 : {str(not_num)}```')        


@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,10.0 , type=commands.BucketType.user)
async def 소인수분해(ctx,num):
    if cohelp['소인수분해']['s'] != 0:
        await ctx.send(f"운영자가 {str(cohelp['소인수분해']['s'])}(을)를 사유로 사용을 금지했어요")
        return
    if not num.isdigit():
        await ctx.send('소인수분해는 정수만 분해할 수 있어요')
        소인수분해.reset_cooldown(ctx)
        return
    if len(num) > 15 and ctx.author.id not in oper:
        await ctx.send('너무 큰 숫자입니다!! 15자리 이내로 입력해 주세요')
        소인수분해.reset_cooldown(ctx)
        return
    if int(num) < 1:
        await ctx.send('너무 작은 숫자입니다!!')
        소인수분해.reset_cooldown(ctx)
        return
    st = time.time()
    if num in pfactors:
        await ctx.send(f"{pfactors[num][:-1]}\n```소인수분해 하는데 걸린시간 {str(time.time()-st)}초입니다```")
        return
    loop = asyncio.get_event_loop()
    n = await loop.run_in_executor(None, pfactor , num)
    a = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    answer = num + '='
    for i in n:
        if n[i] > 1:
            more = ''
            for j in str(n[i]):
                more = more + a[int(j)]
            answer = answer+ str(i) + more + '×'
        elif n[i] == 0:
            pass
        else:
            answer = answer + str(i) + '×'
    et = time.time()
    if et - st > 1:
        pfactors[num] = answer
        with open('maths.txt', 'wb') as f:
            pickle.dump(pfactors, f)
    await ctx.send(f"{answer[:-1]}\n```소인수분해 하는데 걸린시간 {str(et-st)} 초입니다```")

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,10.0 , type=commands.BucketType.user)
async def 계산(ctx , * , what):
    if cohelp['계산']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['계산']['s']) + '를 사유로 사용을 금지했어요')
        return
    msg1 = await ctx.send('계산 중 입니다')
    start_time = time.time()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None , wolframalphaapi , what)
    embed = discord.Embed(title = '계산결과' , color = 0xFFE400)
    for i in result:
        if result[i] != None:
            embed.add_field(name = i , value = result[i])
        else:
            pass
    timing = time.time() - start_time
    await msg1.edit(content=f'```걸린시간 : {timing} ```',embed=embed)

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 기호(ctx):
    if cohelp['기호']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['기호']['s']) + '를 사유로 사용을 금지했어요')
        return
    await ctx.send('π ° ∞ √ ∫ ∑ ∂ ∏ ∀ ∃ ∪ ∩ ∇ Δ α β γ δ ε ζ η θ κ λ μ ν ξ σ τ φ χ ψ ω Γ Θ Λ Ξ ϒ Φ Ѱ ℧ Å ℏ ℵ ⇌ → ⊕ ⊙ ♂ ♀ † ≠ ≥ ≤')
     


#MESSAGELOG - embed color : 0xFF0000


@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,1.0 , type=commands.BucketType.user)
async def 로그채널설정(ctx):
    if cohelp['로그채널설정']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['로그채널설정']['s']) + '를 사유로 사용을 금지했어요')
        return
    if not ctx.channel.name == "짭다봇로그":
        await ctx.send("짭다봇 로그를 설정하시려면 채널의 이름을 짭다봇로그로 한뒤 이 명령어를 사용해주십시오." + "\n" + "설정후에는 채널을 이름을 변경해도 아무런 문제가 없습니다")
        return
    """
    log[ctx.guild.id] = ctx.channel.id
    with open('log.txt', 'wb') as f:
        pickle.dump(log, f)
    await ctx.send("로그 출력 채널을 " + str(ctx.channel.name) + "으로 정했어요")
    """
    embed = discord.Embed(title = '짭다봇 로그v2' , color = 0xFF0000)
    embed.add_field(name = '개인정보 처리방침' , value = 'https://www.github.com/ten-humans/Seolmango/tree/main/JjapdaBot%2FDocs%2FPrivacyPolicy-A.md')
    embed.add_field(name = '설정하기' , value = '아래 화살표 이모지를 누르신다면 위 약관에 동의하는것으로 간주합니다\n동의하지 않으신다면 30초후 이창이 사라질때까지 기다려주세요')
    embed.set_footer(text = '이 창은 60초가 지나면 사라집니다. 해당 기능은 약관을 동의하신분들에게만 제공됩니다')
    msg1 = await ctx.send(embed=embed)
    await msg1.add_reaction("\U00002714")
    def check(reaction, user):
        return reaction.emoji == '\U00002714' and reaction.message.id == msg1.id and user.bot == False and user.id == ctx.author.id
    try:
        reaction , user = await app.wait_for('reaction_add' , timeout = 60.0 , check = check)
    except asyncio.TimeoutError:
        await msg1.delete()
        await ctx.send('설정 절차가 중지 되었습니다')
        return
    log[ctx.guild.id] = ctx.channel.id
    with open('log.txt', 'wb') as f:
        pickle.dump(log, f)
    del embed
    embed = discord.Embed(title = '짭다봇 로그v2' , color = 0xFF0000)
    embed.add_field(name = '진행 결과' , value = '정상적으로 완료되었습니다')
    embed.add_field(name = '이 점을 알아주세요!!' , value = '짭다봇 로그 관련 안내사항은 본 채널을 통해서 전달됩니다')
    embed.set_footer(text = '개발진은 오늘도 일하....나..?')
    await ctx.send(embed=embed)
      

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,1.0 , type=commands.BucketType.user)
async def 로그채널삭제(ctx):
    if cohelp['로그채널삭제']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['로그채널삭제']['s']) + '를 사유로 사용을 금지했어요')
        return
    if not ctx.channel.name == "짭다봇로그":
        await ctx.send("짭다봇 로그채널을 삭제하시려면 채널의 이름을 짭다봇로그로 한뒤 이 명령어를 사용해주십시오." + "\n" + "삭제후에는 채널을 이름을 변경해도 아무런 문제가 없습니다")
        return
    if ctx.guild.id in log:
        del log[ctx.guild.id]
        with open('log.txt', 'wb') as f:
            pickle.dump(log, f)
        await ctx.send("짭다봇 로그 기능을 사용 중지했어요")
    else:
        await ctx.send('이 서버에는 짭다봇로그가 설정된 적이 없습니다')

#HELPER - embed color : 0xFFE400
@app.command(pass_context=True , aliases = ['도움','ㄷ'])
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 도움말(ctx , more=None):
    if cohelp['도움말']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['도움말']['s']) + '를 사유로 사용을 금지했어요')
        return
    if more is None:
        embed = discord.Embed(title = '도움말' , color = 0xFFE400)
        for i in cahelp:
            embed.add_field(name = i , value = str(cahelp[i]['ex'])[1:-1])
        embed.set_footer(text = '각 카테고리,명령어당 상세도움말은 ㅉ도움말 (항목)을 통해 검색 가능합니다')
        await ctx.send(embed = embed)
    elif more in cahelp:
        embed = discord.Embed(title = '"'+more+'"카테고리의도움말' , color = 0xFFE400)
        embed.add_field(name = '설명' , value = cahelp[more]['in'])
        embed.add_field(name = '목록' , value = cahelp[more]['ex'])
        embed.set_footer(text = '다음 카테고리 업데이트는 언제일까요?그건 저희도 모릅니다')
        await ctx.send(embed=embed)
    elif more in cohelp:
        embed = discord.Embed(title = '"'+more+'"명령어의도움말' , color = 0xFFE400)
        embed.add_field(name = '설명' , value = cohelp[more]['in'])
        embed.add_field(name = '문법' , value = cohelp[more]['g'])
        embed.set_footer(text = '명령어에 버그가 발생하면 짭다봇의 운영진에게 정보가 갑니다')
        await ctx.send(embed=embed)
    else:
        await ctx.send('아직 상세도움말이 구현되지 않았습니다....조금만 기다려 주세요')

@app.command(pass_context=True , aliases = ['ㅉ'])
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 짭다봇(ctx):
    if cohelp['짭다봇']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['짭다봇']['s']) + '를 사유로 사용을 금지했어요')
        return
    global server_count
    embed = discord.Embed(title = "잡다한 기능이 있는봇", description = "잡다한 기능을 통해 디스코드를 더욱 더\n재밌고 편리하게 만들어주는 봇입니다!", color = 0xffe400)
    embed.add_field(name = "초대코드", value = "https://discord.com/api/oauth2/authorize?client_id=712898282979983420&permissions=3529792&scope=bot", inline = False)
    embed.add_field(name = "문의방법", value = "askjjapdabot@gmail.com", inline = False)
    embed.add_field(name = "공식 커뮤니티", value = "https://discord.gg/jasaUW4833", inline = False)
    embed.add_field(name = "서버수", value =server_count, inline = True)
    embed.set_thumbnail(url = "https://media.discordapp.net/attachments/722797114647904296/735323638890233876/663bd596a48b6202.png?width=630&height=630")
    embed.set_footer(text = "개발자 - 설망래, 이끼 낀 금화//짭다봇은 12월에 서비스가 종료됩니다.")
    await ctx.send(embed = embed)

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 접두사설정(ctx , new_pr=None):
    if new_pr is None:
        await ctx.send('설정할 접두사가 없어요~~눈 씻고 찾아봐도 없다니깐요~~')
        return
    if len(new_pr) > 5:
        await ctx.send('원하시는 접두사의 길이가 너무 길어요')
        return
    with open(f'{os.getcwd()}/prefix.json', 'r') as f:
        prefix = json.load(f)
        prefix[str(ctx.author.id)]=new_pr
    with open(f'{os.getcwd()}/prefix.json', 'w') as f:
        json.dump(prefix, f, indent='\t')
    await ctx.send(f"이제부터 {new_pr}로 명령어를 시작해주세요.또는 접두사 대신 저를 맨션 하시며 시작하셔도 됩니다")


@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 접두사초기화(ctx):
    with open(f'{os.getcwd()}/prefix.json', 'r') as f:
        prefix=json.load(f)
    if str(ctx.author.id) not in prefix:
        await ctx.send("접두사를 커스텀한 적이 없습니다.")
        return
    prefix.pop(str(ctx.author.id))
    with open(f'{os.getcwd()}/prefix.json', 'w') as f:
        json.dump(prefix, f, indent='\t')
    await ctx.send("접두사가 초기화되었습니다.")
    


#JAPPDA - embed color : 0x00aaaa
@app.command(pass_context=True , aliases = ['ㅌ'])
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,5.0 , type=commands.BucketType.user)
async def 테스트(ctx , * , word):
    if len(word) > 500:
        await ctx.send("너무 긴 문장입니다!! 500자 미만으로 테스트해주세요")
        return
    loop = asyncio.get_event_loop()
    st = time.time()
    msg1 = await ctx.send(f"필터링|| 단어 글자수 : {len(word)}")
    result = await loop.run_in_executor(None , test_word_detection , word)
    embed = discord.Embed(title="욕설탐지 결과",description=f"입력된 문장 : {word}", color=0x00aaaa)
    cen_word = word
    for i in result:
        if len(i) == 0:
            pass
        else:
            for j in i:
                cen_word = cen_word[:j[0]] + '-'*(j[1]-j[0]+1) + cen_word[j[1]+1:]          
    embed.add_field(name="욕설을 제거한 문장",value = cen_word)
    embed.set_footer(text = f'걸린시간 : {time.time()-st}초')
    await msg1.edit(embed = embed)
            
    


@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,10.0 , type=commands.BucketType.user)
async def 롤(ctx , * , name):
    loop = asyncio.get_event_loop()
    n = await loop.run_in_executor(None, riot_api , name)
    await ctx.send(embed = n)


@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,1.0 , type=commands.BucketType.user)
async def 골라(ctx , count  , * , var):
    if cohelp['골라']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['골라']['s']) + '를 사유로 사용을 금지했어요')
        return
    var = var.split(' ')
    if not count.isdigit():
        await ctx.send('뽑을 갯수는 당연히 정수로 적어주셔야죠....')
        골라.reset_cooldown(ctx)
        return
    if len(var) < 2:
        await ctx.send('선택지를 2개이상은 줘야 고를수 있어요!!')
        골라.reset_cooldown(ctx)
        return
    if len(var) < int(count):
        await ctx.send('선택지가 뽑을 수보단 많아야 하겠죠?')
        골라.reset_cooldown(ctx)
        return
    choose = []
    count = int(count)
    while count != 0:
        choose.append(var.pop(random.randint(0 , len(var) -1)))
        count += -1
    embed = discord.Embed(title="골라드립니다",description=str(choose) + "를 뽑았어요!!!!", color=0x00aaaa)
    await ctx.send(embed = embed)
    
@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 시간(ctx):
    if cohelp['시간']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['시간']['s']) + '를 사유로 사용을 금지했어요')
        return
    await ctx.send(str(time.ctime()))

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,0.0 , type=commands.BucketType.user)
async def 요일(ctx , y , m , d):
    if cohelp['요일']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['요일']['s']) + '를 사유로 사용을 금지했어요')
        return
    try:
        a = calendar.weekday(int(y) , int(m) , int(d))
    except:
        await ctx.send('문법은 "ㅉ요일 (연도) (월) (일)" 입니다!!어딘가 이상해요')
        요일.reset_cooldown(ctx)
        return
    days = ["월요일" , "화요일" , "수요일" , "목요일" , "금요일" , "토요일" , "일요일"]
    await ctx.send( y + '년' + m + '월' + d + '일은 ' + days[a] + '입니다')

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,1.0 , type=commands.BucketType.user)
async def 아스키변환(ctx , * , word):
    if cohelp['아스키변환']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['아스키변환']['s']) + '를 사유로 사용을 금지했어요')
        return
    ans = ''
    try:
        for i in range(0 , len(word)):
            ans = ans + str(ord(word[i])) + '/'
    except:
        await ctx.send('무언가 에러가 일어났어요')
        아스키변환.reset_cooldown(ctx)
        return
    await ctx.send(word + '의 아스키코드 변환값은 ```' + ans[:-1] + '``` 입니다')

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,1.0 , type=commands.BucketType.user)
async def 아스키해독(ctx, * , word):
    if cohelp['아스키해독']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['아스키해독']['s']) + '를 사유로 사용을 금지했어요')
        return
    try:
        bil = word.split('/')
        ans = ''
        for i in range(0 , len(bil)):
            ans = ans + chr(int(bil[i]))
    except:
        await ctx.send('아스키코드 해독을하려면 (숫자)/(숫자)...(숫자) 이여야 해요!!')
        아스키해독.reset_cooldown(ctx)
        return
    await ctx.send(word+ '의 해독 결과는 ' + ans + ' 입니다')

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,5.0 , type=commands.BucketType.user)
async def 번역(ctx , lan , * , word):
    if cohelp['번역']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['번역']['s']) + '를 사유로 사용을 금지했어요')
        return
    lancode = {'한국어': 'ko', '영어': 'en', '일본어': 'ja', '중국어간체': 'zh-CN',
           '중국어번체': 'zh-TW', '베트남어': 'vi', '인도네시아어': 'id', '태국어': 'th',
           '독일어': 'de', '러시아어': 'ru', '스페인어': 'es', '이탈리아어': 'it', '프랑스어': 'fr'}
    tarlan = 'v'
    if lan in lancode:
        tarlan = lancode[lan]
    if lan in lancode.values():
        tarlan = lan
    if tarlan == 'v':
        a = list(lancode.keys())
        await ctx.send('번역할 언어는 ```'+' '.join(a)+'```만 가능합니다')
        return
    loop = asyncio.get_event_loop()
    st = time.time()
    result = await loop.run_in_executor(None ,naver_papago_api, tarlan , word)
    if result == 'cant_find_lan':
        await ctx.send('입력하신 문장이 번역이 불가능합니다 ~~해독이 안돼요~~')
        return
    if result == 'papago_not_found':
        await ctx.send('번역과정에서 무언가 에러가 생겼어요')
        return
    res = result['message']['result']
    embed = discord.Embed(title = "번역 결과", description = f'걸린 시간 : ```{str(round(time.time() - st))}초```', color = 0x00aaaa)
    embed.add_field(name = "입력 언어", value = str(res['srcLangType']), inline = False)
    embed.add_field(name = "출력 언어", value = str(res['tarLangType']), inline = False)
    embed.add_field(name = "번역 결과", value = str(res['translatedText']), inline = False)
    embed.set_footer(text = f'version : {result["message"]["@version"]}')
    await ctx.send(embed = embed)

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,1.0 , type=commands.BucketType.user)
async def 한글이름변환(ctx , name):
    if cohelp['한글이름변환']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['한글이름변환']['s']) + '를 사유로 사용을 금지했어요')
        return
    loop = asyncio.get_event_loop()
    st = time.time()
    result = await loop.run_in_executor(None ,naver_ko2en_api, name)
    if result == 'ko2en_not_found':
        await ctx.send('변환 과정에서 무언가 에러가 생겼어요')
        한글이름변환.reset_cooldown(ctx)
        return
    elif len(result['aResult']) == 0:
        await ctx.send("변환이 불가능한 이름입니다")
        한글이름변환.reset_cooldown(ctx)
        return
    res = result['aResult'][0]['aItems'][0]
    embed = discord.Embed(title = "변환 결과", description = f'변환 결과 : {res["name"]}', color = 0x00aaaa)
    embed.set_footer(text = f"걸린시간 : {time.time()-st}")
    await ctx.send(embed=embed)
    
    

@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,5.0 , type=commands.BucketType.user)
async def 코로나(ctx):
    if cohelp['코로나']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['코로나']['s']) + '를 사유로 사용을 금지했어요')
        return
    global Coroembed
    await ctx.send(embed=Coroembed)





#GAMES - embed color: 0x00aaaa
@app.command(pass_context = True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,3.0 , type=commands.BucketType.user)
async def 동전던지기(ctx):
    if cohelp['동전던지기']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['동전던지기']['s']) + '를 사유로 사용을 금지했어요')
        return
    msg1 = await ctx.send('동전을 던지는 중!!(핑그르르)')
    await asyncio.sleep(1.0)
    await msg1.delete()
    a = ["앞면","뒷면","~~옆면~~"]
    check = random.randint(0,1001)
    if check == 1000:
        check = 2
    elif check <= 500:
        check = 1
    else:
        check = 0
    embed = discord.Embed(title = "동전을 던져보니 " + a[check] + "이 나왔어요" , color = 0x00aaaa )
    await ctx.send(embed = embed)

@app.command(pass_context = True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,3.0 , type=commands.BucketType.user)
async def 주사위던지기(ctx):
    if cohelp['주사위던지기']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['주사위던지기']['s']) + '를 사유로 사용을 금지했어요')
        return
    msg1 = await ctx.send('주사위를 던지는 중(데구르르)')
    await asyncio.sleep(1.0)
    await msg1.delete()
    check = random.randint(1,6)
    embed = discord.Embed(title = "주사위를 던져보니 " + str(check) + "이 나왔어요" , color = 0x00aaaa )
    await ctx.send(embed = embed)
    
@app.command(pass_context=True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,3.0 , type=commands.BucketType.user)
async def 가위바위보(ctx):
    if cohelp['가위바위보']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['가위바위보']['s']) + '를 사유로 사용을 금지했어요')
        return
    rsp = ["가위","바위","보"]
    embed = discord.Embed(title="가위바위보",description="가위바위보를 합니다 3초내로 (가위/바위/보)를 써주세요!", color=0x00aaaa)
    msg1 = await ctx.send(embed = embed)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg2 = await app.wait_for('message' , timeout = 3.0, check = check)
    except asyncio.TimeoutError:
        await msg1.delete()
        embed = discord.Embed(title="가위바위보",description="앗 3초가 지났네요...!", color=0x00aaaa)
        await ctx.send(embed=embed)
        return
    else:
        await msg1.delete()
        bot_rsp = str(random.choice(rsp))
        user_rsp = str(msg2.content)
        answer = ""
        if bot_rsp == user_rsp:
            answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 비겼습니다."
        elif (bot_rsp == "가위" and user_rsp == "바위") or (bot_rsp == "보" and user_rsp == "가위") or (bot_rsp == "바위" and user_rsp == "보"):
            answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 제가 졌습니다."
        elif (bot_rsp == "바위" and user_rsp == "가위") or (bot_rsp == "가위" and user_rsp == "보") or (bot_rsp == "보" and user_rsp == "바위"):
            answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
        else:
            embed = discord.Embed(title="가위바위보",description="앗, 가위, 바위, 보 중에서만 내셔야죠...", color=0x00aaaa)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
        await ctx.send(embed=embed)
        return

@app.command(pass_context= True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,15.0 , type=commands.BucketType.user)
async def 미로(ctx , maze_width , maze_height , spoiler=None):
    Nospoiler = ['false','False','아니요','No','no']
    if cohelp['미로']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['미로']['s']) + '를 사유로 사용을 금지했어요')
        return
    if not maze_width.isdigit() or not maze_height.isdigit():
        await ctx.send('올바른 문법은 "ㅉ미로 (가로) (세로)"입니다.물론 모두 정수 이여야 하겠죠? ')
        미로.reset_cooldown(ctx)
        return
    maze_width , maze_height , userid = int(maze_width) , int(maze_height) , ctx.author.id
    if maze_width > 70 or maze_height > 70:
        await ctx.send('미로 명령어의 가로세로의 최대길이는 70입니다!!')
        미로.reset_cooldown(ctx)
        return
    if maze_width < 1 or maze_height < 1:
        await ctx.send('미로 명령어의 가로세로의 최소길이는 1입니다!!')
        미로.reset_cooldown(ctx)
        return
    startTime = time.time()
    loop = asyncio.get_event_loop()
    n = await loop.run_in_executor(None, mazemaker , maze_width , maze_height , userid)
    spendTime = time.time() - startTime
    if spoiler == None or spoiler in Nospoiler:
        await ctx.send(file = discord.File(str(userid) + "Noneanswer.png"))
    else:
        await ctx.send(file = discord.File(str(userid) + "Noneanswer.png" , spoiler = True))
    await ctx.send(file = discord.File(str(userid) + "answer.png" , spoiler = True))
    await ctx.send("```소요시간  :  " + str(spendTime) + "초```")
    os.unlink(str(userid) + "Noneanswer.png")
    os.unlink(str(userid) + "answer.png")
    
    

    

@app.command(pass_context = True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,10.0 , type=commands.BucketType.user)
async def 지뢰찾기(ctx , width , height , mine_count):
    if cohelp['지뢰찾기']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['지뢰찾기']['s']) + '를 사유로 사용을 금지했어요')
        return
    if width.isdigit() and height.isdigit() and mine_count.isdigit():
        number_English = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',0:'zero'}
        width = int(width)
        height = int(height)
        mine_count = int(mine_count)
        if width > 10 or height > 10:
            await ctx.send("가로와 세로의 길이는 10 이하여야 해요!")
            지뢰찾기.reset_cooldown(ctx)
            return
        if width < 1 or height < 1 or mine_count < 1:
            await ctx.send('가로 , 세로 , 지뢰의 갯수는 1 이상이여야 해요')
            지뢰찾기.reset_cooldown(ctx)
            return
        if mine_count > width * height:
            await ctx.send("지뢰의 갯수는 칸의 갯수보다 많으면 안돼요!")
            지뢰찾기.reset_cooldown(ctx)
            return
        mine_map = []
        for i in range(height):
            mine_map.append([])
            for j in range(width):
                mine_map[i].append(0)
        check = 0
        while check < mine_count:
            mine_x, mine_y = random.randint(0, width - 1), random.randint(0, height - 1)
            if mine_map[mine_y][mine_x] != 9:
                mine_map[mine_y][mine_x] = 9
                if mine_x != 0:
                    if mine_map[mine_y][mine_x - 1] != 9:
                        mine_map[mine_y][mine_x - 1] += 1
                    if mine_y != 0:
                        if mine_map[mine_y - 1][mine_x - 1] != 9:
                            mine_map[mine_y - 1][mine_x - 1] += 1
                    if mine_y != height - 1:
                        if mine_map[mine_y + 1][mine_x - 1] != 9:
                            mine_map[mine_y + 1][mine_x - 1] += 1
                if mine_x != width - 1:
                    if mine_map[mine_y][mine_x + 1] != 9:
                        mine_map[mine_y][mine_x + 1] += 1
                    if mine_y != 0:
                        if mine_map[mine_y - 1][mine_x + 1] != 9:
                            mine_map[mine_y - 1][mine_x + 1] += 1
                    if mine_y != height - 1:
                        if mine_map[mine_y + 1][mine_x + 1] != 9:
                            mine_map[mine_y + 1][mine_x + 1] += 1
                if mine_y != 0:
                    if mine_map[mine_y - 1][mine_x] != 9:
                        mine_map[mine_y - 1][mine_x] += 1
                if mine_y != height - 1:
                    if mine_map[mine_y + 1][mine_x] != 9:
                        mine_map[mine_y + 1][mine_x] += 1
                check += 1
        word = ''
        for i in range(height):
            for j in range(width):
                if mine_map[i][j] == 9:
                    word = word + '||:boom:||'
                elif mine_map[i][j] == 0:
                    word = word + ':blue_square:'
                else:
                    word = word + '||:' + number_English[mine_map[i][j]] + ':||'
            word = word + '\n'
        word = word + '지뢰갯수 : ' + str(mine_count)
        await ctx.send(word)
    else:
        await ctx.send("바른 문법은 'ㅉ지뢰찾기 (가로) (세로) (지뢰갯수)' 입니다!!그리고 정수만 넣어야 겠죠?")

@app.command(pass_context = True)
@commands.max_concurrency(1,per=commands.BucketType.user,wait=False)
@commands.cooldown(1,8.0 , type=commands.BucketType.user)
async def 숫자야구(ctx):
    if cohelp['숫자야구']['s'] != 0:
        await ctx.send('운영자가 ' + str(cohelp['숫자야구']['s']) + '를 사유로 사용을 금지했어요')
        return
    pt = random.sample(range(1,10),3)
    tr = 0
    st = 0
    bl = 0
    ans = ''
    while st < 3 and tr < 20:
        msg1 = await ctx.send('각자리 숫자가 모두 다른 3자리수 입력하기')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        try:
            msg2 = await app.wait_for('message' , timeout = 20.0 , check = check)
        except asyncio.TimeoutError:
            await msg1.delete()
            await ctx.send('앗 제한시간이 끝났네요')
            st = 4
            return
        msg = str(msg2.content)
        await msg1.delete()
        try:
            await msg3.delete()
        except:
            pass
        try:
            await msg5.delete()
        except:
            pass
        if not len(msg) == 3 or msg[0] == msg[1] or msg[1] == msg[2] or msg[2] == msg[0]:
            tr += 1
            msg3 = await ctx.send('각자리 숫자가 "모두 다른" "3"자리수를 입력해주세요' + '\n' + '도전횟수   :     ' + str(tr) )
            ans = ans + '\n' + str(tr) + '차 시도 : ' + "올바르지 않은 입력"
            embed = discord.Embed(title = "숫자야구", color = 0x00aaaa)
            embed.add_field(name = "결과들", value = ans, inline = False)
            msg5 = await ctx.send(embed = embed)
            continue
        st = 0
        bl = 0
        tr += 1
        for i in range(0 , 3):
            for j in range(0 , 3):
                if str(pt[i]) == msg[j] and i == j:
                    st += 1
                elif str(pt[i]) == msg[j]:
                    bl += 1
                else:
                    pass
        ans = ans + '\n' + str(tr) + '차 시도 : ' + msg + '-' + str(st) + '스트라이크' + str(bl) + '볼'
        embed = discord.Embed(title = "숫자야구", color = 0x00aaaa)
        embed.add_field(name = "결과들", value = ans, inline = False)
        msg5 = await ctx.send(embed = embed)
    if st == 4:
        await ctx.send('다음에는 더 빨리 입력해주세요')
    elif st == 3:
        await ctx.send('정답을 맞추셨습니다!!..수고하셨습니다')
    elif tr == 20:
        await ctx.send('최대 실행 횟수(20회)를 초과하였습니다')




"""
10분마다 서버 수 개정
"""
@tasks.loop(seconds=600)
async def count_server():
    global server_count
    server_count = len(app.guilds)
    global BOTGAME
    if BOTGAME == '기본':
        BOTGAME = "'ㅉ도움말 ' 로 도움말 확인해주세요!!!!"
    g = discord.Game(str(BOTGAME) + ' ||| '+ str(server_count) + '개 서버')
    await app.change_presence(status=discord.Status.online, activity=g)
    
    

@tasks.loop(seconds=3600)
async def coro():
    global Coroembed
    res = requests.get("http://ncov.mohw.go.kr/").text
    soup = BeautifulSoup(res, "html.parser")
    ko_v = soup.find("div", attrs={"class":"datalist"}).find_all("span", attrs={"class":"data"})
    kov_list = []
    for kov in ko_v:
        kov_list.append(kov.get_text())
    all_per = soup.find("ul", attrs={"class":"liveNum"}).find_all("span", attrs={"class":"num"})
    all_per_list = []
    for allper in all_per:
        all_per_list.append(allper.get_text().replace("(누적)", ""))
    before_per = soup.find("ul", attrs={"class":"liveNum"}).find_all("span", attrs={"class":"before"})
    before_per_list = []
    for beforper in before_per:
        before_per_list.append(beforper.get_text().replace("전일대비 ", ""))
    new_briefing = soup.find("ul", attrs={"class":"m_text_list"}).find_all("a")
    new_briefing_list = []
    for briefing in new_briefing:
        new_briefing_list.append(briefing.get_text())   
        new_briefing_list.append(briefing["href"])
    whentotaldata = soup.find("span", attrs={"class":"livedate"}).get_text().strip().replace("(", "").replace(")", "").replace(", ", " | ")
    Coroembed = discord.Embed(title="코로나 19 현황", description="", color=0x00aaaa)
    Coroembed.set_author(name="코로나 바이러스 감염증 - 19 (COVID-19)", url="http://ncov.mohw.go.kr/", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
    Coroembed.add_field(name="마지막 갱신 시간", value="**" + whentotaldata + "**", inline=False)
    Coroembed.add_field(name="총 확진환자", value=all_per_list[0] + before_per_list[0] , inline=True)
    Coroembed.add_field(name="완치환자", value=all_per_list[1] + before_per_list[1], inline=True)
    Coroembed.add_field(name="격리 중 환자", value=all_per_list[2] + before_per_list[2], inline=True)
    Coroembed.add_field(name="사망자", value=all_per_list[3] + before_per_list[3], inline=True)
    Coroembed.add_field(name="국내발생", value="+ " + kov_list[0], inline=True)
    Coroembed.add_field(name="해외발생", value="+ " + kov_list[1], inline=True)
    Coroembed.add_field(name="최신 브리핑", value="[{}](http://ncov.mohw.go.kr{})".format(new_briefing_list[0], new_briefing_list[1]) + "\n"
                                                + "[{}](http://ncov.mohw.go.kr{})".format(new_briefing_list[2], new_briefing_list[3]) , inline=False)
    Coroembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
    Coroembed.set_footer(text="프로필 버튼의 사이트에 방문하여 자세한 정보를 볼 수 있어요")
    
    
    















app.run(BOT_TOKEN)
del BOT_TOKEN
