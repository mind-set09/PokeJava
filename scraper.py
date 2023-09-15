import requests
from bs4 import BeautifulSoup
import os
from github import Github
from github.GithubException import UnknownObjectException
from github import InputGitAuthor
from github import InputGitTreeElement

# Auth 
g = Github("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")
repo = g.get_repo("mind-set09/PokeJava")

sprite_dir = 'sprites/'  

url = 'https://pokemondb.net/pokedex/all'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

pokemon = soup.find_all('span', class_='infocard-lg-img')

for p in pokemon:

  # Get Pokemon name and download sprite 
  name = p.get('data-img').split('/')[5].split('.')[0]
  img_url = f'https://img.pokemondb.net/sprites/home/normal/{name}.png'
  response = requests.get(img_url)
  with open(os.path.join(sprite_dir, f"{name}.png"), 'wb') as f:
    f.write(response.content)
    
  # Commit and push sprite
  commit_message = f"Add {name} sprite"
  try:
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
  except UnknownObjectException:
    master_sha = None
  
  base_tree = repo.get_git_tree(master_sha)
  element = InputGitTreeElement(f"Assets/Sprites/Pokemon/{name}.png", '100644', 'blob', content=open(f"{name}.png", 'rb').read())
  tree = repo.create_git_tree([element], base_tree)
  parent = repo.get_git_commit(master_sha)
  commit = repo.create_git_commit(commit_message, tree, [parent])
  master_ref.edit(commit.sha)

  repo.push()
