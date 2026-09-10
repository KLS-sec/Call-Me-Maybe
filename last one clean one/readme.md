*This project has been created as part of the 42 curriculum by kle-scor.*

# Description:

Call Me Maybe is an AI project with Qwen 3.0.

Given a JSON of pseudo functions and a JSON of prompts the AI has to give the adapted function to solve the prompt and the arguments needed for the function. Then a JSON with the prompt, arguments and function name has to be created.

To do so we have to use constrained decoding: Restraining the list of authorised tokens to guide the AI answer.

# Instructions:

-Make install:  
Install the project locally.

-Make run:  
Run the project with default values.

-Make lint / Make lint-strict:  
Test mypy and flake8, or test it strict.

-Make clean:  
Erase the caches, .venv and the output file.

Can also be run with:  
uv run python -m src --functions_definition <function_definition_file> --input <input_file> --output <output_file>
To chose the 2 files to read and the output location.

Default values:  
uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json

All files must be of .JSON format

# Ressources:

### Instructions about the AI

Instructions and data about the Ai qwen.

Used AI:  
https://huggingface.co/Qwen/Qwen3-0.6B  
doc:  
https://qwen.readthedocs.io/en/latest/getting_started/concepts.html#

### Multiple tutorials

Various tutorials about the functions used in the code and prompting.  
function calling:  
https://www.promptingguide.ai/applications/function_calling  
constrained codding:  
https://www.aidancooper.co.uk/constrained-decoding/  
https://zeroentropy.dev/concepts/constrained-decoding/  
AI in general:  
https://www.w3schools.com/gen_ai/  
https://www.w3schools.com/ai/  
learn how to use JSON:  
https://www.w3schools.com/python/python_json.asp  
https://www.w3schools.com/python/ref_module_json.asp  

### Exemple

Not a single line was copied from this repo. But the various explanations and example are usefull to understand some principles.  
Tuto CMM:  
https://github.com/SaraFreitas-dev/Call-me-maybe  

### AI:

GPT was used to find some specific functions, a bit of debuging, mypy/flake8 corrections and perfecting the Makefile.

# Additional:

### Algorithm / design decision:

Step 1:  
The constraint decoding was simple but extremely strict on the function name obtention. I made a list of every function name and any token not present in any name is refused. To avoid hallucinations the instant the result is similar to any function name the loop stops.

I did it this way to have more precision and control over the AI with shorter answers. First the functions names, then using it I guide the AI to produce the parameters for this function specifically. The hallucination problem is very annoying, getting an accurate answer from the AI is not so hard but it has to stop producing, or giving a clear signal, once the "sane" answer is finished.

Step 2:  
The adapted function (chosen beforehand by the AI) is put in the new prompt.
It produced all the parameters but with a somewhat messy formatting. The parameters list is finished by a "}", afterward the AI starts hallucinating. I constrained it to produce a EOS token tight after the "}" thus ending the program. Multiple cleaning operations are done afterward to get only the parameters.

The prompt was enough to produce the parameters. So I only had to kill the token generation once the answer was completed.

Step 3:  
The parameters are then fused to create a string with the exact format needed, the output file is created and the string is written in it.

I chosed to organise it by hand instead of using a JSON function. It was purely arbitrary, both ways were equally viable in my case.

### Performance:

By generating almost only the answers instead of the whole JSON it shortens the number of token to produce. Only the regex consumes some time.  
The total generation time is around 2:50 total.  
One of the regex could not be solved, but I have 100% accuracy on every other prompts even with slight modifications.
It is reliable, fast and efficient for the simple functions but has chances of loss with regex.

### Challenges faced:

The regex. From a prompt to another some regex worked, others did not and constrained decoding didn't limit it enough with hardcoding a big chunk of it.

### Testing strategy:

-Multiple different prompts were tested until I found some pushing the AI in the correct reflexion. it took some time but helped a lot.

-Forcing the first token with constrained decoding. It did not work, if the answer is forced to start with "fn_" but the Ai wanted to print "fn" then "_g" next it starts hallucinating.

-Full answer in one prompt. It worked for others but not with me. No matter the constraint it printed uter nonsense

### Exemple usage:

This work is just a simulation. but a completed version of this work could become an API selector to lower the AI work.

Exemple: instead of searching info about the meteo in a country it calls a specific API, gives it the adapted arguments and uses the result to answer. Instead of generating token to do 1+1 a small function does the job and gives the answer.

# Other:

To get faster answers:  
Use the Ai once, you will get the message: "Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads."

You have to create an account on hugging face and follow these steps.

hf auth login  
start the loggin, give a links

click the link, take the token and enter it

uvx hf auth login  
make sure you are connected