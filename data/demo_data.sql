truncate gnc_sites.t_typesite restart identity cascade
;

truncate gnc_sites.t_sites restart identity cascade
;

insert into gnc_sites.t_typesite(category, type, timestamp_create)
values ('Zone humide', 'Mare', now())
;

