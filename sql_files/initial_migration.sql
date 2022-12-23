create table if not exists species (
  species_id serial primary key,
  name varchar(300) not null,
  released boolean not null default false,
  mega_evolves boolean not null default false,
  baby boolean not null default false,
  generation int
);

create table if not exists forms (
  form_id serial primary key,
  name varchar(300) not null
);

create table if not exists species_forms (
  species_form_id serial primary key,
  species_id int,
  form_id int,
  base_attack int not null default 0,
  base_defense int not null default 0,
  base_stamina int not null default 0,
  attack_probability real not null default 0.0,
  base_capture_rate real not null default 0.0,
  base_flee_rate real not null default 0.0,
  dodge_probability real not null default 0.0,
  max_action_frequency real not null default 0.0,
  min_action_frequency real not null default 0.0,
  max_cp int not null default 0,
  gender_male real not null default 0.0,
  gender_female real not null default 0.0,
  genderless real not null default 0.0,
  constraint fk_species
    foreign key(species_id)
      references species(species_id),
  constraint fk_form
    foreign key(form_id)
      references forms(form_id)
);

create table if not exists levels (
  level_id varchar not null primary key,
  next_level_id varchar,
  candy_to_upgrade int not null default 0,
  cp_multiplier float not null default 1.0
);

create table if not exists types (
  type_id serial primary key,
  name varchar not null
);

create table if not exists type_effectiveness (
  type_effectiveness_id serial primary key,
  attack_type_id int not null,
  defense_type_id int not null,
  effectiveness real not null,
  constraint fk_attacker_type
    foreign key(attack_type_id)
      references types(type_id),
  constraint fk_defender_type
    foreign key(defense_type_id)
      references types(type_id)
);

create table if not exists weather_types (
  weather_id serial primary key,
  name varchar not null
);

create table if not exists weather_boost_types (
  id serial primary key,
  weather_id int not null,
  type_id int not null,
  constraint fk_weather
    foreign key(weather_id)
      references weather_types(weather_id),
  constraint fk_type
    foreign key(type_id)
      references types(type_id)
);

create table if not exists buffs (
  buff_id serial primary key,
  activation_chance real not null,
  target_defense_change real not null default 0.0,
  attacker_defense_change real not null default 0.0,
  target_attack_change real not null default 0.0,
  attacker_attack_change real not null default 0.0,
  target_defense boolean generated always as (target_defense_change != 0.0) stored,
  attacker_defense boolean generated always as (attacker_defense_change != 0.0) stored,
  target_attack boolean generated always as (target_attack_change != 0.0) stored,
  attacker_attack boolean generated always as (attacker_attack_change != 0.0) stored
);

create table if not exists moves (
  move_id serial primary key,
  name varchar not null,
  type_id int not null references types (type_id),
  duration int not null,
  turn_duration int,
  pve_energy_delta int not null,
  pvp_energy_delta int,
  move_power int not null,
  critical_chance real,
  heal_scalar real,
  charged boolean not null default false,
  buff_id int references buffs(buff_id)
);

create table if not exists species_form_moves (
  form_move_id serial primary key,
  species_form_id int not null references species_forms(species_form_id),
  move_id int not null references moves(move_id)
);

create table if not exists shiny_pokemon (
  shiny_id serial primary key,
  species_id int references species(species_id),
  egg boolean not null default false,
  evolution boolean not null default false,
  photobomb boolean not null default false,
  raid boolean not null default false,
  research boolean not null default false,
  wild boolean not null default false
);
