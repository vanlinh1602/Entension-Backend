def handleGetImage(data: any):
    name = data['name']
    src = f'https://assets.reedpopcdn.com/Genshin-Impact-anime.jpg'
    return {'src': src, 'name': name}
