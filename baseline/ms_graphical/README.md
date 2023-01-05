**Reproduce result of Table 2** : Train the PGM model on the census and dmv dataset
```
python model.py --dataset census --train_num 12
python model.py --dataset dmv --train_num 7
```

**Reproduce result of Table 4** : Train the PGM model on the IMDB dataset
```
python model_join.py --train_queries ../../sam_multi/queries/mscn_400.csv --train_num 400
```
