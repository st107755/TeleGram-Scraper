## sentiment analysis = text classification
#%%
from transformers import pipeline

import torch
import torch.nn.functional as F

#%%
##pipeline= great and easy way to use models or inferenz, extract much things for user
classifier = pipeline ("sentiment-analysis")
result = classifier("We are happy with our food")

print (result)
# %%
