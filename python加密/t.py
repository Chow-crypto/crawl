# import requests
 
# request_header = {
 
#     "t": "这里是微信小程序token值"
# }
 
# def game():
#     for i in range(989):
#         requests.get("http://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time=15&rank_role=1&skin=1", headers=request_header)
#         print(f"通过{i+1}次")
 
# if __name__ == '__main__':
#     game()
import base64
sta = ['@jum123456789','Jum123456789','Jum123456789','Jum123456789','YAsUg6,LE=!Cn-6','@Zhou123456789','jum123456789','#Zhou123456789','Jum123456','jum123456789','yqtfcksjfucycchf','yinghepower123']
for i in sta:
    print(base64.b64encode(i.encode()).decode())