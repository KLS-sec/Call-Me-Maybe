Possible error message:
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.

hf auth login
start the loggin, give a links

click the link, take the token and enter it

uvx hf auth login
make sure you are connected

###################

balises
permet de mettre la pre reflection la dedans specifiquement
<think> </think>

symbole important
Ġ

###################
balises:
eod token
<|endoftext|>
end of document, which are inserted between documents inside a packed training sequence

bot token
<|im_start|>
start of each turn, which is prepended to each turn

eot token
<|im_end|>
end of each turn, which is appended to each turn

unk token
no unk token
BBPE ensures no unknown tokens for Qwen.

pad token
no pad token
Qwen does not make use of padded sequence in training. One could use any special token together with the attention masks returned by the tokenizer. It is commonly set the same as eod for Qwen.

bos token
no bos token
Qwen does not prepend a fixed token to each packed training sequence.[2]

eos token
no eos token
Qwen does not append a fixed token to each packed training sequence. However, as most frameworks do not have the concept of eot and use eos instead for stopping criteria in inference, eos token is set to eot for Qwen.[2]
+ system assistant user




sources
https://qwen.readthedocs.io/en/latest/getting_started/concepts.html#