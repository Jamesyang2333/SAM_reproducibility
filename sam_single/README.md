# SAM for single-relation database generation
### Getting Started

**Datasets** For single-relation database, we conduct our experiments on two datasets, Census and DMV. We have uploaded Census at [`./datasets/census.csv`](./datasets/census.csv). You can download the DMV dataset by running the script.
```
bash scripts/download_dmv.sh
```
**Pretrained Models** We have provided a pretrained model for each dataset.
[`./models/census_pretrained.pt`](./models/census_pretrained.pt): Trained from 20000 queries in the generated workload ([`./queries/census_21000.txt`](./queries/census_21000.txt)).

[`./models/dmv_pretrained.pt`](./models/dmv_pretrained.pt): Trained from 20000 queries in the generated workload ([`./queries/dmv_21000.txt`](./queries/dmv_21000.txt)).

**Database Generation** To generate database from trained models using SAM, use the following commands. For each dataset, we generate two databases, one from the model trained on the full dataset and another from the model trained on very few input queries (to compare with baseline).
```
python gen_data_model.py --dataset census --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob census_pretrained.pt --save-name census
python gen_data_model.py --dataset census --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob census_12_pretrained.pt --save-name census_12
python gen_data_model.py --dataset dmv --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob dmv_pretrained.pt --save-name dmv
python gen_data_model.py --dataset dmv --residual --layers=2 --fc-hiddens=128 --direct-io --column-masking --glob dmv_7_pretrained.pt --save-name dmv_7
```
The generated relations are saved at `./generated_data_tables`.

**Reproduce result of Table 1** : Run the 20000 training queries on the generated database. The first 20000 queries in the generated workload are training queries.
```
python query_execute_single.py --dataset census --trainSet
python query_execute_single.py --dataset dmv --trainSet
```

**Reproduce result of Table 2** Run the 20000 training queries on the generated database. The first 20000 queries in the generated workload are training queries.
```
python query_execute_single.py --dataset census --trainSet
python query_execute_single.py --dataset dmv --trainSet
```

**Reproduce result of Table 5**: Run the 1000 training queries on the generated database. The last 1000 queries in the generated workload are training queries.
```
python query_execute_single.py --dataset census --testSet
python query_execute_single.py --dataset dmv --testSet
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

