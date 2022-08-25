# SAM
SAM is a learning-based method for high-fidelity database generation using deep autoregressive models.

Your can learn more about SAM in our SIGMOD 2022 paper, [SAM: Database Generation from Query Workloads with Supervised Autoregressive Models](https://dl.acm.org/doi/abs/10.1145/3514221.3526168).

<p align="center">
    <br>
    <img src="./assets/overview.png" width="600"/>
<p>

## Getting Started
This project contains two main directories:

[`sam_single`](sam_single): Reproducibility result on single-relation database

[`sam_multi`](sam_multi): Reproducibility result on multi-relation database

## Citation
```bibtex
@inproceedings{
  title={SAM: Database Generation from Query Workloads with Supervised Autoregressive Models},
  author={Yang, Jingyi and Wu, Peizhi and Cong, Gao and Zhang, Tieying and He, Xiao},
  booktitle={Proceedings of the 2022 International Conference on Management of Data},
  pages={1542--1555},
  year={2022},
  location = {Philadelphia, PA, USA},
  publisher = {Association for Computing Machinery}
}
```

## Acknowledgements
This project builds on top of [UAE](https://github.com/pagegitss/UAE) and [NeuroCard](https://github.com/neurocard/neurocard).
