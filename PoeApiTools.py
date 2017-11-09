import requests
import json
import time

# <editor-fold desc="Poe.Ninja Api Endpoints">
poeNinjaEndpoints = {'currency': 'https://api.poe.ninja/api/Data/GetCurrencyOverview',
                     'map': 'https://api.poe.ninja/api/Data/GetMapOverview',
                     'unique map': 'https://api.poe.ninja/api/Data/GetUniqueMapOverview',
                     'unique weapon': 'https://api.poe.ninja/api/Data/GetUniqueWeaponOverview',
                     'unique armor': 'https://api.poe.ninja/api/Data/GetUniqueArmourOverview',
                     'unique accessory': 'https://api.poe.ninja/api/Data/GetUniqueAccessoryOverview',
                     'unique flask': 'https://api.poe.ninja/api/Data/GetUniqueFlaskOverview',
                     'unique jewel': 'https://api.poe.ninja/api/Data/GetUniqueJewelOverview',
                     'prophecy': 'https://api.poe.ninja/api/Data/GetProphecyOverview',
                     'divination card': 'https://api.poe.ninja/api/Data/GetDivinationCardsOverview',
                     'essence': 'https://api.poe.ninja/api/Data/GetEssenceOverview',
                     'fragment': 'https://api.poe.ninja/api/Data/GetFragmentOverview',
                     'next id': 'https://poe.ninja/api/Data/GetStats'
                     }
# </editor-fold>

# <editor-fold desc="Poe.Ninja Related Variables">
atziriDrops = {"atziri's promise": 'unique flask', "Atziri's Step": 'unique armor',
               "Doryani's Invitation1": '1', "Doryani's Invitation2": '2', "Doryani's Invitation3": '3', "Doryani's Invitation4": '4',
               "Doryani's Catalyst": 'unique weapon', "Mortal Hope": 'fragment', "Mortal Ignorance": 'fragment',
               "Mortal Grief": 'fragment', "Mortal Rage": 'fragment'
               }

atziriDropProbabilities = {'f': .65, 'bt': .15, 'belF': .0375, 'belC': .0375, 'belL': .0375,'belP': .0375, 's': .05,
                           'h': .05, 'i': .07, 'g': .15, 'r': .1}

atziriPortalFragments = ["Mortal Hope", "Mortal Ignorance", "Mortal Grief", "Mortal Rage"]
# </editor-fold>

# <editor-fold desc="Poe.Ninja Functions">


def PoeNinjaQuery(itemCategory='Map', league='standard'):
    """Pass in a key from poeNinjaEndpoints to get the json of that type returned to you."""
    if itemCategory.lower() in poeNinjaEndpoints.keys():
        params = {'league': league.lower().title()}
        return requests.get(poeNinjaEndpoints[itemCategory.lower()], params=params).json()


def PoeNinjaGetNextID():
    """Returns the next change ID from Poe.Ninja."""
    return requests.get(poeNinjaEndpoints['next id']).json()['next_change_id']


def PoeNinjaGetSingleItemPrice(itemName='The Doctor', itemValueType='c', itemCategory='Divination Card', league='Standard', optional=None):
    """Pass in a key from poeNinjaEndpoints, an item name and a league to get the price in chaos or exalts.
    itemValueType should be ex or c
    optional is for specific kinds of items currently only '1'=fire, '2'=cold, '3'=light, '4'=phys are supported
    to check for dorynani's invitation variants."""
    if itemCategory.lower() == 'currency':
        print('For currency/fragments use PoeNinjaGetCurrencyPrice() instead')
        return None
    j = PoeNinjaQuery(itemCategory, league)
    for item in j['lines']:
        if itemName.lower().translate({ord(ch): None for ch in '0123456789'}) == item['name'].lower():
            if optional == '1':
                if item['variant'] == 'Fire':
                    if itemValueType == 'c':
                        return item['chaosValue']
                    elif itemValueType == 'ex':
                        return item['exaltedValue']
                else:
                    continue
            elif optional == '2':
                if item['variant'] == 'Cold':
                    if itemValueType == 'c':
                        return item['chaosValue']
                    elif itemValueType == 'ex':
                        return item['exaltedValue']
                else:
                    continue
            elif optional == '3':
                if item['variant'] == 'Lightning':
                    if itemValueType == 'c':
                        return item['chaosValue']
                    elif itemValueType == 'ex':
                        return item['exaltedValue']
                else:
                    continue
            elif optional == '4':
                if item['variant'] == 'Physical':
                    if itemValueType == 'c':
                        return item['chaosValue']
                    elif itemValueType == 'ex':
                        return item['exaltedValue']
                else:
                    continue
            if itemValueType == 'c':
                return item['chaosValue']
            elif itemValueType == 'ex':
                return item['exaltedValue']
            else:
                print('itemValueType should be either c or ex')


def PoeNinjaGetChaosEquiv(currencyTypeName='Exalted Orb', categoryName='Currency', league='Standard'):
    """Pass a currency/fragment type and a league to return the chaos equivalent."""
    j = PoeNinjaQuery(categoryName, league)
    for item in j['lines']:
        if currencyTypeName.lower() == item['currencyTypeName'].lower():
            return item['chaosEquivalent']


def PoeNinjaGetCurrencyComparison(currencyTypeNameA='Exalted Orb', numCurrencyA=1,
                                  currencyTypeNameB='Orb of Alteration', league='Standard'):
    """Returns the number of currency B you can get for the number of currency A you have.
    Example: you have 2 ex and want to know how many alterations that is so you pass exalted orb for A and alt for B."""
    aChaos = float(PoeNinjaGetChaosEquiv(currencyTypeNameA, league))
    bChaos = float(PoeNinjaGetChaosEquiv(currencyTypeNameB, league))
    return (aChaos/bChaos) * numCurrencyA


def PoeNinjaCompareSplinterToStone(league='standard'):
    """Returns a dict of boss/bool.
    The bool is true if it's cheaper to buy the splinters of a breachstone individually."""
    breachlords = {'Chayula': None, 'Uul-Netol': None, 'Esh': None, 'Xoph': None, 'Tul': None}
    for i in breachlords:
        chaosPerSplinter = PoeNinjaGetChaosEquiv(currencyTypeName='Splinter of ' + i, categoryName='Currency', league=league)
        breachstoneCost = PoeNinjaGetChaosEquiv(currencyTypeName=i + "'s Breachstone", categoryName='Fragment', league=league)
        if chaosPerSplinter * 100 < breachstoneCost:
            breachlords[i] = True
        else:
            breachlords[i] = False
    return breachlords


def PoeNinjaBossProfitability(dropProbabilities=None, itemDrops=None, portalFragments=None, league='Harbinger'):
    """Returns True if Boss is profitable."""
    itemValues = {}
    for item in itemDrops:
        if "Invitation" in item:
            itemValues[item] = PoeNinjaGetSingleItemPrice(itemName=item.translate({ord(ch): None for ch in '0123456789'}),
                                                          itemCategory='unique accessory', league=league, optional=itemDrops[item]
                                                          )
        elif itemDrops[item].lower() == 'fragment' or itemDrops[item].lower() == 'currency':
            itemValues[item] = PoeNinjaGetChaosEquiv(currencyTypeName=item, categoryName=itemDrops[item], league=league)
        else:
            itemValues[item] = PoeNinjaGetSingleItemPrice(itemName=item, itemCategory=itemDrops[item], league=league)
    itemValList = []
    itemProbList = []
    for i in itemValues:
        itemValList.append(itemValues[i])
    for i in dropProbabilities:
        itemProbList.append(dropProbabilities[i])
    costToRun = 0
    for frag in range(0, len(portalFragments)):
        costToRun += PoeNinjaGetChaosEquiv(currencyTypeName=portalFragments[frag], categoryName='fragment', league=league)
    if costToRun < ExpectedValue(itemProbList, itemValList):
        return True
    else:
        return False
# </editor-fold>

# <editor-fold desc="GGG Api Endpoints">


gggEndpoints = {'public stash': 'http://api.pathofexile.com/public-stash-tabs',
                'leagues': 'http://api.pathofexile.com/leagues',
                'league rules': 'http://api.pathofexile.com/league-rules',
                'ladder': 'http://api.pathofexile.com/ladders',
                'stash': 'https://www.pathofexile.com/character-window/get-stash-items',
                'character gear': 'https://www.pathofexile.com/character-window/get-items',
                'character jewels': 'https://www.pathofexile.com/character-window/get-passive-skills'
                }
# </editor-fold>

# <editor-fold desc="GGG Functions">


def GGGQuery(queryType='public stash', params=None, cookie=None, league=None):
    """Pass key from gggEndpoints and optional params to receive back the json for that endpoint.
    Params, cookie and league are optional. League is used for grabbing the ladder since it's a seperate url per league."""
    if league is None:
        return requests.get(gggEndpoints[queryType.lower()], params=params, cookies=cookie).json()
    else:
        return requests.get(gggEndpoints[queryType.lower()] + '/' + league, params=params, cookies=cookie).json()


def GGGGetPublicStashData(changeID=PoeNinjaGetNextID()):
    """Returns the most recent public stash json by default. a next_change_id can be passed optionally."""
    return GGGQuery('public stash', changeID)


def GGGGetPlayerStash(league='Standard', accountName=None, tabs=1, tabIndex=None):
    """Returns a json containing the specified stashIndex. tabs={0,1}: 0 means only specified stash, 1 means all.
    tabIndex is optional. Passing tabs=1 and no tabIndex returns a json of all tabs on that league/account."""
    params = {'league': league, 'accountName': accountName, 'tabs': tabs, 'tabIndex': tabIndex}
    cookie = {'POESESSID': PlayerCookie()}
    return GGGQuery(queryType='stash', params=params, cookie=cookie)


def GGGGetLadderClassCount(league='Standard'):
    classCount = {}
    # 15000 possible on ladder divided by 200 gives 75. i * 200 is the offset we want so we end up at 14800 when i=74.
    for i in range(0, 75):
        r = GGGQuery(queryType='ladder', params={'limit': 200, 'offset': i * 200}, league=league)
        for character in r['entries']:
            if character['character']['class'] in classCount:
                classCount[character['character']['class']] += 1
            else:
                classCount[character['character']['class']] = 1
        time.sleep(2)
    return classCount


# </editor-fold>

# <editor-fold desc="General Use Functions">


def ExpectedValue(probabilities, values):
    """Returns expected value (inner product) of the values of two lists."""
    return sum(i * j for i, j in zip(probabilities, values)) if len(probabilities) == len(values) else 0


def PlayerCookie(set=False, poesessid=None):
    """Returns the player's POESESSID from secret.json. Optional flag to True to change the id stored in secret.json."""
    if set:
        with open("secret.json", 'w+', encoding='utf-8') as f:
            data = {}
            data["POESESSID"] = poesessid
            json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
    else:
        with open("secret.json") as f:
            data = json.load(f)
            return data["POESESSID"]

def Unzip(dictionary):
    return dictionary.keys(), dictionary.values()
# </editor-fold>
