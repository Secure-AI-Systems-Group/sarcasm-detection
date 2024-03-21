### [[LREC-COLING 2024]](https://lrec-coling-2024.org/) When Do "More Contexts" Help with Sarcasm Recognition?

----

This repository contains the code for reproducing the results of our paper:

- [When Do "More Contexts" Help with Sarcasm Recognition?](https://arxiv.org/abs/2403.12469)
- [Ojas Nimase](mailto:ojasnimase@gmail.com) and [Sanghyun Hong](https://sanghyun-hong.com).

&nbsp;

----

### TL;DR

- Can we achieve SoTA sarcasm recognition performance by simply concatenating embeddings to provide more contexts? Yes
- Then, is it desirable to incorporate more and more contexts into a model to further improve the performance? Not sure; beyond a certain performance point, the model needs to learn undesirable biases.

&nbsp;

### Abstract

Sarcasm recognition is challenging because it needs an understanding of the true intention, which is opposite to or different from the literal meaning of the words. Prior work has addressed this challenge by developing a series of methods that provide richer *contexts*, e.g., sentiment or cultural nuances, to models. While shown to be effective individually, no study has systematically evaluated their collective effectiveness. As a result, it remains unclear to what extent additional contexts can improve sarcasm recognition. In this work, we explore the improvements that existing methods bring by incorporating more contexts into a model. To this end, we develop a framework where we can integrate multiple contextual cues and test different approaches. In evaluation with four approaches on three sarcasm recognition benchmarks, we achieve existing state-of-the-art performances and also demonstrate the benefits of sequentially adding more contexts. We also identify inherent drawbacks of using more contexts, highlighting that in the pursuit of even better results, the model may need to adopt societal biases.

&nbsp;

----

## Pre-requisites

This code was written in Google Colab. We recommend checking out the Colab files (links contained in Python code) and using them. Note that you need to swap out the Google Drive links in the code with yours.

&nbsp;

----

## Generating Embeddings

You can use this Colab code to generate embeddings [here](Code/iac_v2,_iac_v1,_and_tweets_data_embedding_creation.py). 

To reproduce the embeddings from our approach that fine-tunes a model using contrastive learning (A3), we provide our fine-tuned BERTweet model [here](https://drive.google.com/file/d/1FKF0TI1RbhTyJtKo3xNUM2wgi-l26ZII/view?usp=sharing). You can also find the script for fine-tuning any pre-trained model [here](Code/fine_tuning_bertweet_via_simclr.py). We used the SarcasmSign dataset to fine-tune the BERTweet model. The script for pre-processing the dataset is in [here](Code/sarcasmsign_data_cleaning.py).

&nbsp;

----

## Sarcasm Recognition

Now we can refer to this script to run sarcasm recognition on three benchmarking datasets (IAC-V1 IAC-V2 and Tweets): [link](iac_v1,_iac_v2,_and_tweets_a1,_a2,_a3,_a4.py)

&nbsp;

----

## Cite Our Work

Please cite our work if you find this source code helpful. Thanks!
```
@inproceedings{nimase2024more,
      title={When Do "More Contexts" Help with Sarcasm Recognition?}, 
      author={Ojas Nimase and Sanghyun Hong},
      booktitle={The 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation}
      year={2024}
}
```

&nbsp;

----

Please contact [Ojas](mailto:ojasnimase@gmail.com) with any suggestions or questions.
