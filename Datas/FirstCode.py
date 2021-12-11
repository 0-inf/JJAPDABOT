"""
저장되어 있는 가장 첫번째 짭다봇 코드입니다.
"""

import discord , random , time , math , asyncio , calendar  #discord 1.3.3 
codelist = []
wantlist = []
userlist = []
client = discord.Client()



@client.event
async def on_ready():
    print("------\n준비됨\n------")
    game = discord.Game("'ㅉ도움말'  ")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message_delete(message):
    botlist = [] #봇 리스트
    id = str(message.author.id)
    danger = "아직 측정 불가"
    if id in botlist:
        return None
    else:
        embed = discord.Embed(title = "삭제 감지", color = 0xFF0000)
        embed.add_field(name = "삭제된 내용", value ="@" + str(message.author) + "님의 " + message.content + "라는 내용", inline = False)
        embed.add_field(name = "위험도", value = danger, inline = False)
        await message.channel.send(embed = embed)

@client.event
async def on_message_edit(before, after):
    botlist = [] #봇 리스트
    id = str(before.author.id)
    danger = "아직 측정불가"
    if id in botlist:
        return None
    else:
        embed = discord.Embed(title = "변경 감지", color = 0xFF0000)
        embed.add_field(name = "내용", value = before.content + " 에서 " + after.content + "로 변경되었습니다", inline = False)
        embed.add_field(name = "위험도", value = danger, inline = True)
        embed.add_field(name = "메시지의 주인", value = before.author, inline = True)
        await after.channel.send(embed = embed)
    
@client.event
async def on_message(message):
    name = str(message.author)
    id = str(message.author.id)
    word = str(message.content)

    print(name + " : " + word)
    print(id)

    
    if message.channel.id == "관리용 채널":
        if word.startswith("ㅉ답변"):
            await message.channel.send("전달되었습니다")
            binlist = word.split("/")
            global codelist
            global wantlist
            global userlist
            username = userlist[codelist.index(int(binlist[1]))]
            channel = await username.create_dm()
            if int(binlist[1]) in codelist:
                clear = codelist.index(int(binlist[1]))
                embed = discord.Embed(title = "건의사항에 대한 답변", color = 0xFFE400)
                embed.add_field(name = "건의해주신내용", value = wantlist[codelist.index(int(binlist[1]))], inline = False)
                codelist.remove(codelist[clear])
                wantlist.remove(wantlist[clear])
                embed.add_field(name = "답변해드리는 내용", value = "안녕하세요!!짭다봇 팀입니다!!!건의해주신 내용은 감사드립니다!!!!" + binlist[2], inline = False)
                await channel.send(embed = embed)
            else:
                await message.channel.send("답변 코드가 일치하지 않습니다!!! ㅉ건의리스트 로 확인하세요")
        elif word.startswith("ㅉ건의리스트"):
            await message.channel.send(codelist)
        else:
            return None        
        
    else: 
        if message.author.bot:
            return None
        elif word.startswith("ㅉ도움"):
            binlist = word.split(" ")
            binlist.append("아")
            if binlist[1] == "수학":
                embed = discord.Embed(title = "수학도움말", color = 0xFFE400)
                embed.add_field(name = "ㅉ(더하기/곱하기) (1번 항목) (2번항목) ~~ (n번쨰 항목)", value = "항목들을 모두 더하거나 곱해 줍니다.", inline = False)
                embed.add_field(name = "ㅉ(빼기/나누기) (항목1) (항목2)", value = "1번 항목에서 2번 항목으로 빼거나 나누어 줍니다.", inline = False)
                embed.add_field(name = "ㅉ거듭제곱 (밑) (지수)" , value = "거듭제곱의 값을 알려줍니다" , inline = False)
                embed.add_field(name = "ㅉ요일 (년도) (월) (일)" , value = "입력한 날의 요일을 보여줍니다" , inline = False)
                embed.add_field(name = "ㅉ((단위의 종류)변환) (숫자) (입력단위) (출력단위#생략가능)" , value = "단위를 변환해 줍니다" , inline = False)
                embed.add_field(name = "ㅉ분석 (첫번째 값) .... (마지막 값) #숫자만 넣어주세요" , value = "평균과 분산을 구해줍니다." , inline = False)
                await message.channel.send(embed = embed)
            elif binlist[1] == "채팅관리":
                embed = discord.Embed(title = "채팅 관리 도움말", color = 0xFFE400)
                embed.add_field(name = "설명" , value = "비속어,욕 등이 들어간 말이 삭제되면 짭다봇이 잡아냅니다!!!" , inline = False)
                embed.add_field(name = "채널설정법" , value = "짭다봇이 로그를 출력할 서버를 설정하려면 채널이름을 (짭다봇로그)로 시작시키세요" , inline = False)
                await message.channel.send(embed = embed)
            else:    
                embed = discord.Embed(title = "도움말", color = 0xFFE400)
                embed.add_field(name = "ㅉ도움", value = "도움말을 보여줍니다.", inline = False)
                embed.add_field(name = "ㅉ골라 <항목1>/<항목2>/...", value = "항목중에 하나를 골라줍니다.", inline = False)
                embed.add_field(name = "ㅉ게임목록" , value = "게임 목록을 보여줍니다." , inline = False)
                embed.add_field(name = "ㅉ기능" , value = "기능~~지 자랑~~을 보여줍니다" , inline = False)
                embed.add_field(name = "ㅉ시간" , value = "시간을 알려줍니다" , inline = False)
                await message.channel.send(embed = embed)


        elif word.startswith("ㅉ기능"):
            embed = discord.Embed(title = "잡다봇의 기능들", color = 0xFFE400)
            embed.add_field(name = "명령어들", value = "여러 명령어들이 있습니다.ㅉ도움말로 확인하세요", inline = False)
            embed.add_field(name = "즐길거리들", value = "ㅉ게임목록으로 간단한 게임들을 확인하세요", inline = False)
            embed.add_field(name = "채팅 감시" , value = "누군가를 비방하는 등의 글 삭제시 로그가 남아서 증거가 남습니다" , inline = False)
            await message.channel.send(embed = embed)


        elif word.startswith("ㅉ게임목록"):
            embed = discord.Embed(title = "게임목록", color = 0xFFE400)
            embed.add_field(name = "ㅉ가위바위보", value = "가위바위보를 합니다.", inline = False)
            embed.add_field(name = "ㅉ동전던지기", value = "동전을던집니다.", inline = False)
            embed.add_field(name = "ㅉ주사위던지기", value = "주사위를 던집니다.", inline = False)
            await message.channel.send(embed = embed)
        
        elif word.startswith("ㅉ상태"):
            await message.channel.send("온라인!! 라저댓" + str(message.author) + "님")

        elif word.startswith("ㅉ안녕"):
            await message.channel.send("안녕하세요 " + str(message.author) + "님")
        
        elif word.startswith("ㅉ골라"):
            word = word[4:]
            if word.count("/") == 0:
                await message.channel.send("항목은 2개이상으로 해주세요!")
            else:
                check = random.randint(0, word.count("/"))
                embed = discord.Embed(title = "[" + str(check + 1) + "]. " + word.split("/")[check] + "을/를 골랐습니다.", color = 0xFFE400)
                await message.channel.send(embed = embed)

        elif word.startswith("ㅉ동전던지기"):
            embed = discord.Embed(title="동전던지기",description="던지는 중!!!", color=0x00aaaa)
            msg1 = await message.channel.send(embed=embed)
            time.sleep(5)
            await msg1.delete()
            a = ["앞면","뒷면"]
            check = random.randint(0,1)
            embed = discord.Embed(title = "동전을 던져보니 " + a[check] + "이 나왔어요" , color = 0x00aaaa )
            await message.channel.send(embed = embed)

        elif word.startswith("ㅉ주사위던지기"):
            embed = discord.Embed(title="주사위던지기",description="던지는 중!!!", color=0x00aaaa)
            msg1 = await message.channel.send(embed=embed)
            time.sleep(5)
            await msg1.delete()
            check = random.randint(1,6)
            embed = discord.Embed(title = "주사위를 던져보니 " + str(check) + "이 나왔어요" , color = 0x00aaaa )
            await message.channel.send(embed = embed)

        elif word.startswith('ㅉ가위바위보'):
            rsp = ["가위","바위","보"]
            embed = discord.Embed(title="가위바위보",description="가위바위보를 합니다 3초내로 (가위/바위/보)를 써주세요!", color=0x00aaaa)
            channel = message.channel
            msg1 = await message.channel.send(embed=embed)
            def check(m):
                return m.author == message.author and m.channel == channel
            try:
                msg2 = await client.wait_for('message', timeout=3.0, check=check)
            except asyncio.TimeoutError:
                await msg1.delete()
                embed = discord.Embed(title="가위바위보",description="앗 3초가 지났네요...!", color=0x00aaaa)
                await message.channel.send(embed=embed)
                return
            else:
                await msg1.delete()
                bot_rsp = str(random.choice(rsp))
                user_rsp  = str(msg2.content)
                answer = ""
                if bot_rsp == user_rsp:
                    answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 비겼습니다."
                elif (bot_rsp == "가위" and user_rsp == "바위") or (bot_rsp == "보" and user_rsp == "가위") or (bot_rsp == "바위" and user_rsp == "보"):
                    answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 제가 졌습니다."
                elif (bot_rsp == "바위" and user_rsp == "가위") or (bot_rsp == "가위" and user_rsp == "보") or (bot_rsp == "보" and user_rsp == "바위"):
                    answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
                else:
                    embed = discord.Embed(title="가위바위보",description="앗, 가위, 바위, 보 중에서만 내셔야죠...", color=0x00aaaa)
                    await message.channel.send(embed=embed)
                    return
                embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
                await message.channel.send(embed=embed)
                return

        elif word.startswith("ㅉ더하기"):
            binlist = word.split(" ")
            if len(binlist) > 2:
                answer = 0
                a = int(len(binlist)) - 1
                while a != 0:
                    answer = answer + int(binlist[a])
                    a = a - 1
                await message.channel.send("답은 " + str(answer) + "입니다")
            else:
                await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

        elif word.startswith("ㅉ곱하기"):
            binlist = word.split(" ")
            if len(binlist) > 2:
                answer = 1
                a = int(len(binlist)) - 1
                while a != 0:
                    answer = answer * int(binlist[a])
                    a = a - 1
                await message.channel.send("답은 " + str(answer) + "입니다")
            else:
                await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

        elif word.startswith("ㅉ빼기"):
            binlist = word.split(" ")
            if len(binlist) == 3:
                answer = 0
                answer = int(binlist[1]) - int(binlist[2])            
                await message.channel.send("답은 " + str(answer) + "입니다")
            else:
                await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

        elif word.startswith("ㅉ나누기"):
            binlist = word.split(" ")
            if len(binlist) == 3:
                answer = 0
                answer = int(binlist[1]) / int(binlist[2])            
                await message.channel.send("답은 " + str(answer) + "입니다")
            else:
                await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

        elif word.startswith("ㅉ거듭제곱"):
            binlist = word.split(" ")
            if len(binlist) == 3:
                if int(binlist[2]) > 1999:
                    await message.channel.send("입력하신 숫자가 너무 ~~크고 아름다워서~~ 게산이 안되요 지수를 2000미만으로 해주세요")
                else:    
                    if len(binlist) == 3:
                        answer = pow(int(binlist[1]) , int(binlist[2]))
                        await message.channel.send("답은 " + str(answer) + "입니다")
            else:
                await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

        elif word.startswith("ㅉ시간"):
            await message.channel.send(str(time.ctime()))

        elif word.startswith("ㅉ분석"):
            a = word.split(" ")
            d = len(a) - 1
            b = []
            while d != 0:
                b.append(int(a[d]))
                d = d-1
            c = len(b)
            qnstks = 0
            vudrbs = int(sum(b)) / c
            while c != 0:
                qnstks = qnstks + pow(int(b[c-1] - vudrbs) , 2)
                c = c - 1 
            qnstks = qnstks / int(len(b) - 1)
            embed = discord.Embed(title = "데이터 분석", color = 0xFFE400)
            embed.add_field(name = "입력된 값들", value = b, inline = False)
            embed.add_field(name = "평균", value = vudrbs , inline = False)
            embed.add_field(name = "분산", value = qnstks, inline = False)
            await message.channel.send(embed = embed)



        elif word.startswith("ㅉ요일"):
            binlist = word.split(" ")
            a = calendar.weekday(int(binlist[1]) , int(binlist[2]) , int(binlist[3]))
            days = ["월요일" , "화요일" , "수요일" , "목요일" , "금요일" , "토요일" , "일요일"]
            await message.channel.send(str(days[a]) + "입니다")

        elif word.startswith("ㅉ길이변환"):
            wordlist = word.split(" ")
            if len(wordlist) == 3 or 4:
                if str(wordlist[2]) == "km" or "m" or "cm" or "mm" or "nm" or "in":    #길이변환 코드
                    if wordlist[2] == "km":
                        mm = int(wordlist[1]) * 1000000
                    elif wordlist[2] == "m":
                        mm = int(wordlist[1]) * 1000
                    elif wordlist[2] == "cm":
                        mm = int(wordlist[1]) * 10
                    elif wordlist[2] == "nm":
                        mm = int(wordlist[1]) * 0.000001
                    elif wordlist[2] == "in":
                        mm = int(wordlist[1]) * 25.4
                    else:
                        mm = int(wordlist[1])
                    if len(wordlist) == 3:
                        embed = discord.Embed(title = "길이 단위", color = 0xFFE400)
                        embed.add_field(name = "입력된 수", value = str(wordlist[1]) + str(wordlist[2]) , inline = False)
                        embed.add_field(name = "km(킬로미터)", value = int(mm) / 1000000, inline = False)
                        embed.add_field(name = "m(미터)", value = int(mm) / 1000, inline = False)
                        embed.add_field(name = "cm(센티미터)", value = int(mm) / 10, inline = False)
                        embed.add_field(name = "mm(밀리미터)", value = int(mm) , inline = False)
                        embed.add_field(name = "nm(나노미터)", value = int(mm) / 0.000001 , inline = False)
                        embed.add_field(name = "in(인치)", value = int(mm) / 25.4 , inline = False)
                        await message.channel.send(embed = embed)
                    else:
                        if wordlist[3] == "km":
                            need = int(mm) / 1000000                  
                        elif wordlist[3] == "m":
                            need = int(mm) / 1000
                        elif wordlist[3] == "cm":
                            need= int(mm) / 10
                        elif wordlist[3] == "nm":
                            need = int(mm) / 0.000001
                        elif wordlist[3] == "in":    
                            need = int(mm) / 25.4
                        else:
                            need = int(mm)
                        embed = discord.Embed(title = "길이 변환", color = 0xFFE400)
                        embed.add_field(name = wordlist[1] + wordlist[2], value = str(need) + wordlist[3] , inline = False)
                        await message.channel.send(embed = embed)
                else:
                    await message.channel.send("없는 단위입니다")
            else:
                await message.channel.send("문법오류!! ㅉ도움 수학 을 통해서 문법확인하세요")
        
        elif word.startswith("ㅉ면적변환"):
            wordlist = word.split(" ")
            if len(wordlist) == 3 or 4:
                if str(wordlist[2]) == "km2" or "m2" or "cm2" or "평" or "mm2":    #면적변환 코드
                    if wordlist[2] == "km2":
                        cm2 = int(wordlist[1]) * 10000000000
                    elif wordlist[2] == "m2":
                        cm2 = int(wordlist[1]) * 10000
                    elif wordlist[2] == "cm2":
                        cm2 = int(wordlist[1]) 
                    elif wordlist[2] == "평":
                        cm2 = int(wordlist[1]) * 33057
                    else:
                        cm2 = int(wordlist[1]) / 100
                    if len(wordlist) == 3:
                        embed = discord.Embed(title = "면적 단위", color = 0xFFE400)
                        embed.add_field(name = "입력된 수", value = str(wordlist[1]) + str(wordlist[2]) , inline = False)
                        embed.add_field(name = "km2(제곱킬로미터)", value = int(cm2) / 10000000000, inline = False)
                        embed.add_field(name = "m2(제곱미터)", value = int(cm2) / 10000, inline = False)
                        embed.add_field(name = "cm2(제곱센티미터)", value = int(cm2) , inline = False)
                        embed.add_field(name = "mm2(제곱밀리미터)", value = int(cm2) / 0.01, inline = False)
                        embed.add_field(name = "평", value = int(cm2) / 33057.85 , inline = False)
                        await message.channel.send(embed = embed)
                    else:
                        if wordlist[3] == "km2":
                            need = int(cm2) / 10000000000                
                        elif wordlist[3] == "m2":
                            need = int(cm2) / 10000
                        elif wordlist[3] == "cm2":
                            need= int(cm2)
                        elif wordlist[3] == "mm2":
                            need = int(cm2) * 100
                        else:
                            need = int(cm2) / 33057
                        embed = discord.Embed(title = "면적 변환", color = 0xFFE400)
                        embed.add_field(name = wordlist[1] + wordlist[2], value = str(need) + wordlist[3] , inline = False)
                        await message.channel.send(embed = embed)
                else:
                    message.channel.send("없는 단위입니다")
            else:
                message.channel.send("문법 오류!! ㅉ도움 수학 을 통해 문법확인 하세요")

        elif word.startswith("ㅉ부피변환"):
            wordlist = word.split(" ")
            if len(wordlist) == 3 or 4:
                if str(wordlist[2]) == "ml" or "l" or "cm3" or "m3" :    #부피변환 코드
                    if wordlist[2] == "ml":
                        l = int(wordlist[1]) * 0.001
                    elif wordlist[2] == "cm3":
                        l = int(wordlist[1]) * 0.001
                    elif wordlist[2] == "m3":
                        l = int(wordlist[1]) * 1000
                    else:
                        l = int(wordlist[1])
                    if len(wordlist) == 3:
                        embed = discord.Embed(title = "부피 단위", color = 0xFFE400)
                        embed.add_field(name = "입력된 수", value = str(wordlist[1]) + str(wordlist[2]) , inline = False)
                        embed.add_field(name = "m3(세제곱미터)", value = int(l) / 1000, inline = False)
                        embed.add_field(name = "cm3(세제곱센티미터)", value = int(cm2) * 1000 , inline = False)
                        embed.add_field(name = "ml(밀리리터)", value = int(l) * 1000, inline = False)
                        embed.add_field(name = "l(리터)", value = int(l)  , inline = False)
                        await message.channel.send(embed = embed)
                    else:
                        if wordlist[3] == "m3":
                            need = int(l) / 1000                
                        elif wordlist[3] == "ml":
                            need= int(l) * 1000
                        elif wordlist[3] == "cm3":
                            need = int(l) * 10000
                        else:
                            need = int(l)
                        embed = discord.Embed(title = "부피 변환", color = 0xFFE400)
                        embed.add_field(name = wordlist[1] + wordlist[2], value = str(need) + wordlist[3] , inline = False)
                        await message.channel.send(embed = embed)
                else:
                    message.channel.send("없는 단위입니다")
            else:
                message.channel.send("문법 오류!! ㅉ도움 수학 을 통해 문법확인 하세요")
        elif word.startswith("ㅉ건의하기"):    
            if 1 == 1:
                await message.channel.send("엄청난 에러가 있어 현재 고치는 중입니다!!!(뚝딱뚝딱)")    
            else:    
                code = int(message.author.id)
                if code in codelist:
                    await message.channel.send("이미 건의를 하셨네요!!! 운영진이 답변을 해줄떄까지 기다리시거나 ㅉ건의사항삭제로 건의를 취소하세요")    
                else:    
                    codelist.append(code)
                    wantlist.append(word[5:])
                    userlist.append(message.author)
                    embed = discord.Embed(title = "건의사항", color = 0xFFE400)
                    embed.add_field(name = "작성자", value = message.author.name , inline = True)
                    embed.add_field(name = "인식코드", value = code , inline = True)
                    embed.add_field(name = "건의 내용", value = word[5:] , inline = False)
                    await message.channel.send("건의가 완료되었습니다!!! 빠르게 확인한 뒤 DM 거부가 아니시면 답변드릴게요!!!!!")
                    await client.get_channel("관리용 채널 ID").send(embed = embed)
        
        elif word.startswith("ㅉ건의사항삭제"):
            if 1 == 1:
                await message.channel.send("엄청난 에러가 있어 현재 고치는 중입니다!!!(뚝딱뚝딱)")
            else:
                code = int(message.author.id)
                if code in codelist:
                    clear = codelist.index(code)
                    codelist.remove(codelist[clear])
                    wantlist.remove(wantlist[clear])
                    await message.channel.send("정상적으로 진행되었습니다...만 ~~바보같은~~운영진이 답변을 쓸수도 있으니 참고해 주세요")
                else:
                    msg1 = await message.channel.send("음....~~건의사항을 보낸적이 없는데 지우라고???? 확 컴퓨터를 지워버릴까??~~")
                    time.sleep(5)
                    await msg1.delete()
                    await message.channel.send("건의사항을 보내신적이 없어요")

        elif word.startswith("ㅉ아스키코드변환"):
            scr = word[9:]
            count = len(scr)
            answer = ""
            for i in range(0,count):
                answer = answer + str(ord(scr[i])) + "/"
            answer = answer[:-1]
            await message.channel.send(scr + "의 아스키코드 변환값은 " + answer + "입니다!!!!!")

        elif word.startswith("ㅉ아스키코드해독"):
            scr = word[9:]
            if scr.find(" ") != -1:
                key = " "
            elif scr.find("/") != -1:
                key = "/"
            else:
                await message.channel.send("Error!! Cannot find key!! Ask for Zapdateam")
            binlist = scr.split(key)
            answer = ""
            for i in range(0 , len(binlist)):
                answer = answer + chr(int(binlist[i]))
            await message.channel.send(scr + "의 해독 결과는 " + answer + "입니다!!")

        elif word.startswith("ㅉ실행"):
            doword = word[4:]
            await message.channel.send(eval(doword))


        



client.run("봇의 토큰")