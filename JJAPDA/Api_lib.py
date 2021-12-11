import wolframalpha
import urllib
import requests
import json
import discord


class Jjapdabot_api():
    """
    짭다봇이 사용하는 모든 api를 효과적으로 관리하기 위하여
    하나로 묶어 만든 모듈입니다
    현재 울프럼알파 , 네이버번역 , 롤 티어검색을 지원합니다
    """

    def __init__(self):
        self.wolfram_id = ''    #울프럼알파 api key
        self.naver_id = ""   #네이버 api key
        self.naver_secret = ""         #네이버 api secret
        self.riot_secret = ""       #롤 api secret


    def api_wolfram(self,what):
        """
        울프럼 알파 api입니다
        what 에 입력된 것에 대한 query를 보낸후 result로 return 합니다
        """
        wolfram = wolframalpha.Client(self.wolfram_id)
        res = wolfram.query(what)
        result = {}
        for i in res.pod:
            if i.error != 'true':
                b=[]
                for a in list(i.subpod):
                    if a['plaintext'] == '':
                        pass
                    else:
                        b.append(str(a['plaintext']))
                c = '\n'.join(b)
                result[i.title] = c
            else:
                pass
        return result

    def api_naver_findlan(self , word):
        """
        네이버 언어감지 api입니다
        word에 입력된 언어에 따른 코드를 반환합니다
        """
        encQuery = urllib.parse.quote(word)
        data = "query=" + encQuery
        url = "https://openapi.naver.com/v1/papago/detectLangs"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.naver_id)
        request.add_header("X-Naver-Client-Secret",self.naver_secret)
        try:
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except urllib.error.HTTPError as e:
            print(e)
            return {'Error':e}
        rescode = response.getcode()
        response_body = response.read()
        return eval(response_body.decode('utf-8'))


    def api_naver_papago(self , source , target , word):
        """
        네이버 파파고 번역 api입니다
        """
        encText = urllib.parse.quote(word)
        data = f"source={source}&target={target}&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.naver_id)
        request.add_header("X-Naver-Client-Secret",self.naver_secret)
        try:
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except urllib.error.HTTPError as e:
            print(e)
            return {'Error':e}
        response_body = response.read()
        null = 'null'
        return eval(response_body.decode('utf-8'))

    def api_naver_ko2en(self , name):
        """
        네이버 한글 인명-로마자 변환 api입니다
        """
        encText = urllib.parse.quote(name)
        url = "https://openapi.naver.com/v1/krdict/romanization?query=" + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.naver_id)
        request.add_header("X-Naver-Client-Secret",self.naver_secret)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e)
            return {'Error':e}
        response_body = response.read()
        return eval(response_body.decode('utf-8'))
        

    def riot_api(self , UserName):
        UserInfoUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + UserName
        res = requests.get(UserInfoUrl, headers={"X-Riot-Token":self.riot_secret})
        resjs = json.loads(res.text)

        if res.status_code == 200:
            UserIconUrl = "http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/{}.png"
            embed = discord.Embed(title=f"{resjs['name']} 님의 정보", description=f"**{resjs['summonerLevel']} 레벨**", color=0x00aaaa)

            UserInfoUrl_2 = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + resjs["id"]
            res_2 = requests.get(UserInfoUrl_2, headers={"X-Riot-Token":self.riot_secret})
            res_2js = json.loads(res_2.text)

            if res_2js == []: # 언랭크일때
                embed.add_field(name=f"{resjs['name']} 님은 언랭크입니다.", value="**언랭크 유저의 정보는 확인이 불가능합니다**", inline=False)

            else: # 언랭크가 아닐때
                for rank in res_2js:
                    if rank["queueType"] == "RANKED_SOLO_5x5":
                        embed.add_field(name="솔로랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                           f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)

                    else:
                        embed.add_field(name="자유랭크", value=f"**티어 : {rank['tier']} {rank['rank']} - {rank['leaguePoints']} LP**\n"
                                                            f"**승 / 패 : {rank['wins']} 승 {rank['losses']} 패**", inline=True)

            embed.set_author(name=resjs['name'], url=f"http://fow.kr/find/{UserName.replace(' ', '')}", icon_url=UserIconUrl.format(resjs['profileIconId']))
            return embed

        else: # 존재하지 않는 소환사일때
            error = discord.Embed(title="존재하지 않는 소환사명입니다.\n다시 한번 확인해주세요.", color=0x00aaaa)
            return error








            


        
        



