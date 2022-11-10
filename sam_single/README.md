# SAM for single-relation database generation
### Getting Started

**Datasets** For single-relation database, we conduct our experiments on two datasets, Census and DMV. We have uploaded Census at [`./datasets/census.csv`](./datasets/census.csv). You can download the DMV dataset by running the script.
```
bash scripts/download_dmv.sh
```
**Pretrained Models** We have provided two pretrained models for each dataset.

[`models/census_pretrained.pt`](models/census_pretrained.pt): Trained from a generated workload of 20000 queries ([`queries/census_train.txt`](queries/census_train.txt)).

[`models/dmv_pretrained.pt`](models/dmv_pretrained.pt): Trained from a generated workload of 20000 queries ([`queries/dmv_train.txt`](queries/dmv_21000.txt)).

[`models/census_12_pretrained.pt`](models/census_12_pretrained.pt): Trained from 12 queries in the generated workload ([`queries/census_12.txt`](queries/census_12.txt)).

[`models/dmv_7_pretrained.pt`](models/dmv_7_pretrained.pt): Trained from 7 queries in the generated workload ([`queries/dmv_7.txt`](queries/dmv_7.txt)).

**Database Generation** To generate database from trained models using SAM, use the following commands. For each dataset, we generate two databases, one from the model trained on the full dataset and another from the model trained on very few input queries.
```
python gen_data_model.py --dataset census --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob census_pretrained.pt --save-name census
python gen_data_model.py --dataset census --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob census_12_pretrained.pt --save-name census_12
python gen_data_model.py --dataset dmv --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob dmv_pretrained.pt --save-name dmv
python gen_data_model.py --dataset dmv --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob dmv_7_pretrained.pt --save-name dmv_7
```
The generated relations are saved at `./generated_data_tables`.

**Reproduce result of Table 1** : Run the full training queries on the generated database.
```
python query_execute_single.py --dataset census --data-file ./generated_data_tables/census.csv --query-file ./queries/census_train.txt
python query_execute_single.py --dataset dmv --data-file ./generated_data_tables/dmv.csv --query-file ./queries/dmv_train.txt
```

**Reproduce result of Table 2** Run the very few training queries on the generated database.
```
python query_execute_single.py --dataset census --data-file ./generated_data_tables/census_12.csv --query-file ./queries/census_12.txt
python query_execute_single.py --dataset dmv --data-file ./generated_data_tables/dmv_7.csv --query-file ./queries/dmv_7.txt
```

**Reproduce result of Table 5**: Run the 1000 test queries on the generated database.
```
python query_execute_single.py --dataset census --data-file ./generated_data_tables/census.csv --query-file ./queries/census_test.txt
python query_execute_single.py --dataset dmv --data-file ./generated_data_tables/dmv.csv --query-file ./queries/dmv_test.txt
```

### SAM model training
SAM uses [UAE-Q](https://github.com/pagegitss/UAE) to train a deep autoregressive model from query workloads, 

To train the model from the full MSCN dataset
```
python train_uae.py --num-gpus=1 --dataset=census --epochs=50 --constant-lr=5e-4 --run-uaeq  --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --workload-size 20000 --q-bs 200
python train_uae.py --num-gpus=1 --dataset=dmv --epochs=50 --constant-lr=5e-4 --run-uaeq  --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --workload-size 20000 --q-bs 200
```

To test the model
```
python eval_model.py --dataset census --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob dmv_pretrained.pt
python eval_model.py --dataset dmv --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob census_pretained.pt
```

