CREATE TABLE need_role_pairs
(
	need_id integer references need(need_id),
	pair_id integer references pair_roles(pair_id)
);
