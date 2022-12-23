for x in pgef:
    cf = x['form'] if 'form' in x else "No Form"
    if cf in pbf:
        pbf[cf].append(x['pokemon_name'])
    else:
        pbf[cf] = [x['pokemon_name']]
    if x['pokemon_name'] in fbp:
        fbp[x['pokemon_name']].append(cf)
    else:
        fbp[x['pokemon_name']] = [cf]
