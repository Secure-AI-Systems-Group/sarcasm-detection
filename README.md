## When Do "More Contexts" Help with Sarcasm Recognition? [[LREC-COLING 2024]](https://lrec-coling-2024.org/)

This repository contains the code for reproducing the results of our paper:

- [When Do "More Contexts" Help with Sarcasm Recognition?](https://arxiv.org/abs/2403.12469)
- **[Ojas Nimase](mailto:ojasnimase@gmail.com)**, [Sanghyun Hong](https://sanghyun-hong.com).

&nbsp;

----

### TL;DR

Improved performance on sarcasm detection can introduce undesirable biases.

&nbsp;

----
### Abstract
Sarcasm recognition is challenging because it needs an understanding of the true intention, which is opposite to or different from the literal meaning of the words. Prior work has addressed this challenge by developing a series of methods that provide richer contexts, e.g., sentiment or cultural nuances, to models. While shown to be effective individually, no study has systematically evaluated their collective effectiveness. As a result, it remains unclear to what extent additional contexts can improve sarcasm recognition. In this work, we explore the improvements that existing methods bring by incorporating more contexts into a model. To this end, we develop a framework where we can integrate multiple contextual cues and test different approaches. In evaluation with four approaches on three sarcasm recognition benchmarks, we achieve existing state-of-the-art performances and also demonstrate the benefits of sequentially adding more contexts. We also identify inherent drawbacks of using more contexts, highlighting that in the pursuit of even better results, the model may need to adopt societal biases.

&nbsp;

----
## Running The Code

Since this code was written in Google Colab, we recommend checking out the Colab files (links contained in Python code) and copying them. Also, please don't forget to swap out the google drive links in the code with your own google drive links.

&nbsp;

----
## Generating The Embeddings

The embeddings can be generated by following the code [here](Code/iac_v2,_iac_v1,_and_tweets_data_embedding_creation.py). For the A3 embeddings, the fine-tuned BERTweet model can be found here: https://drive.google.com/file/d/1FKF0TI1RbhTyJtKo3xNUM2wgi-l26ZII/view?usp=sharing or you can fine-tune your own model following the code [here](Code/fine_tuning_bertweet_via_simclr.py).

&nbsp;

----
## Cite Our Work

Please cite our work if you find this source code helpful. Thanks!
```
@misc{nimase2024more,
      title={When Do "More Contexts" Help with Sarcasm Recognition?}, 
      author={Ojas Nimase and Sanghyun Hong},
      year={2024},
      eprint={2403.12469},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
&nbsp;
Please contact [Ojas](mailto:ojasnimase@gmail.com) with any suggestions or questions.
