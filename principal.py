import arq
import igscraper
import twittervid
import cbf_scraper
import stories
import iglogin
#pega os links da midia do instagram
def get_insta_post(url):

    headers = { 'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'}
    cookies = {'sessionid':'2113549053%3Abrb9tvModZWPZf%3A24'}

    page = igscraper.get_photo_page(url,headers,cookies)
    print(page)
    json_text = igscraper.get_json_media_page(page)
    print(json_text)
    vetor = igscraper.get_download_link(json_text)
    print(vetor)
    return vetor

#envia multiplas midias
def envio_sidecar(update,vetor):
        cont=0
        print(vetor)
        for i in vetor:
            if i == 1:
                arq.download(vetor[cont+1],'midia/'+str(cont),'.jpeg')
                update.message.reply_photo(photo=open('midia/'+str(cont)+'.jpeg','rb'))
            elif i == 2:
                arq.download(vetor[cont+1],'midia/'+str(cont),'.mp4')
                update.message.reply_photo(video=open('midia/'+str(cont)+'.mp4','rb'))


            cont = cont+1
   
#envia unica foto
def envio_single_photo(update,vetor):
    print(vetor)
    arq.download(vetor,'midia/1','.jpeg')
    update.message.reply_photo(photo=open('midia/1.jpeg','rb'))

#envia unico video
def envio_single_video(update,vetor):
    arq.download(vetor,'midia/1','.mp4')
    update.message.reply_video(video=open('midia/1.mp4','rb'))

#envia unico video do twitter
def envio_twitter(update,url):

    id = twittervid.spliturl(url)
    print(id)
    url = twittervid.getvideourl(id)
    arq.download(url,'ttvid/1','.mp4')
    update.message.reply_text('Enviando video!')
    update.message.reply_video(video=open('ttvid/1.mp4','rb'))
    
def envia_info_jogos(update,info_time):
    rodada = info_time['rodada']
    time = info_time['time']
    divisao = info_time['div']
    rodada = int(rodada)
    cont=rodada
    if cont > 0:
        cont=rodada-1
    num = int(rodada)+3
    for i in range(cont,num):
        jogo = cbf_scraper.get_jogo(i,time,divisao)
        info = cbf_scraper.get_info_jogo(jogo)
        link = info['link']
        transmissao = cbf_scraper.get_info_partida(link)
        update.message.reply_text('Rodada '+str(i+1)+'\n'+'Data:'+ info['desc']+'\n'+info['casa'] + " " + info['info_geral'] + " " + info['fora']+'\n'+'Transmissao: '+transmissao)
        
def envia_stories(update,url):
    sessionid = igscraper.login(iglogin.user,iglogin.senha)

    headers = { 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}
    cookies = {'sessionid':str(sessionid)}

    info = stories.split_link(url)
    user_id = stories.get_stories_info_page("https://www.instagram.com/stories/"+info['user']+"/?__a=1",headers,cookies)
    obj_json = stories.get_stories_page("https://i.instagram.com/api/v1/feed/reels_media/?reel_ids="+user_id,headers,cookies,user_id)
    item = stories.nav_stories(obj_json,info['reels_id'])
    link = stories.get_download_link(item)
    if link['type'] == 1:
        arq.download(link['url'],"1",".jpeg")
        update.message.reply_photo(photo=open("1.jpeg",'rb'))
    if link['type'] == 2:
        arq.download(link['url'],"1",".mp4")
        update.message.reply_video(video=open("1.mp4",'rb'))


