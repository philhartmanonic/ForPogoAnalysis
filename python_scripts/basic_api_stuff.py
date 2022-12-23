import requests as req
import random as rnd
import math as m
import os

def results(pn):
    res = req.get(f"https://pogoapi.net/api/v1/{pn}.json").json()
    rtype = None
    examples = []
    if type(res) == list:
        rtype = 'List'
        examples.append(("Example Value", str(rnd.choice(res))[:150]))
    else:
        rtype = "Dictionary"
        sk = rnd.choice(list(res))
        examples.append(("Example Key", str(sk)))
        examples.append(('Example Value', str(res[sk])[:150]))
    print(f"Gatherered results for {pn}")
    print(f"  Result type: {rtype}")
    print(f"  Number of results: {len(res)}")
    print("\n".join([f"    {':  '.join(x)}" for x in examples]))
    return res


def each_slice(arr, slices):
    return [arr[x::slices] for x in [*range(slices)]]

def weak_against(pokename, fatty=None, catty=None):
  if fatty == None:
    fatty = pjt[pokename]
  elif type(fatty) == str:
    fatty = [fatty]
  if catty == None:
    catty = pjt[pokename]
  elif type(catty) == str:
    catty = [catty]
  attack_vuls = dict([[x, 1.0] for x in tyls])
  def_vuls = dict([[x, 1.0] for x in tyls])
  for ctype in tyls:
    for atty in [fatty, catty]:
      for cat in atty:
        attack_vuls[ctype] *= tef[cat][ctype]
    for cat in pjt[pokename]:
      def_vuls[ctype] *= tef[ctype][cat]
  full_res = dict([[x, [attack_vuls[x], def_vuls[x]]] for x in tyls])
  vulnerable = {}
  weak = {}
  for x in tyls:
    if full_res[x][0] > 1.0:
      vulnerable[x] = full_res[x][0]
    if full_res[x][1] < 1.0:
      weak[x] = full_res[x][1]
  return {'full': full_res, 'vulnerable': vulnerable, 'weak': weak}


def wa_search(war):
  parts = []
  parts.append([f"@1{x}" for x in list(war['vulnerable'])])
  parts.append([f"@2{x}" for x in list(war['vulnerable'])])
  parts.append(list(war['weak']))
  sstr = "&".join([",".join(x) for x in parts])
  print(sstr)
  return sstr
