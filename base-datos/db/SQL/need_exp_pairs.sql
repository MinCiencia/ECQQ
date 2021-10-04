CREATE TABLE need_exp_pairs
(
	need_id integer references need(need_id),
	pair_id integer references pair_exp(pair_id)
);
