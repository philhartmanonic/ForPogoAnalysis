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

# defining the main variables so there's a list of them up here
pokemon_by_name = {}
forms_by_name = {}
species_form_ids = {}

pokemon_names = results('pokemon_names')

# this relies on having 2 environment variables, PGPGUSER (postgres user for your pokemongo database) and PGPGPASSWORD (password for that user)
connection = pg.connect(dbname="pokemongo", user=os.environ['PGPGUSER'], password=os.environ['PGPGPASSWORD'], host="localhost")
cursor = connection.cursor()

# for creating all of the pokemon species
def create_species():
    cursor.execute("select species_id, name from species;")
    preexisting_ids = []

    for row in cursor.fetchall():
        pokemon_by_name[row[1]] = row[0]
        preexisting_ids.append(str(row[0]))

    query_arguments = []

    for psid in list(set(list(pokemon_names)) - set(preexisting_ids)):
        query_arguments += [int(psid), pokemon_names[psid]['name']]

    query_string = f"insert into species (species_id, name) values {", ".join(["(%s, %s)"] * (len(query_arguments) / 2))} returning species_id, name;"

    cursor.execute(query_string, query_arguments)
    for row in cursor.fetchall():
        pokemon_by_name[row[1]] = row[0]

create_species()

# creating all of the pokemon forms
def create_forms():
    query_arguments = results('pokemon_forms')
    query_string = f"insert into forms (name) values {", ".join(["(%s)"] * len(query_arguments))} on conflict do nothing returning form_id, name;"

    cursor.execute(query_string, query_arguments)

    return dict([[row[1], row[0]] for row in cursor.fetchall()])

forms_by_name = create_forms()

# using genders to create species_forms and then assigning gender details to species forms
def create_species_forms():
    species_form_info = {}
    raw_genders = results('pokemon_genders')
    species_form_arguments = []
    gender_keys = [['male_percent', 'gender_male'], ['female_percent', 'gender_female'], ['genderless', 'genderless']]
    for gender_key in list(raw_genders):
        for row in raw_genders[gender_key]:
            pid = row['pokemon_id']
            form_name = "Normal" if 'form' not in row else row['form'] if row['form'] != 'Standard' else 'Normal'
            fid = forms_by_name[form_name]
            species_form_info[[pid, fid]] = dict([[x[1], 0.0 if x[0] not in row else row[x[0]]] for x in gender_keys])
    raw_mcp = results('pokemon_max_cp')
    for row in raw_mcp:
        form_name = "Normal" if 'form' not in row else row['form'] if row['form'] != 'Standard' else 'Normal'
        fid = forms_by_name[form_name]
        species_form_info[[row['pokemon_id'], fid]]['max_cp'] = row['max_cp']
    
