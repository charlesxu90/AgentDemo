# Agentic AI framework
A general framework for agentic AI development

## Install

```shell
# create conda environment
mamba create -y -n agent_demo python=3.12 pip
mamba activate agent_demo

pip install uv
uv sync # uv pip install -r pyproject.toml
```


## Debug
```shell
# debug backend with langsmith
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking

# debug frontend
pnpm dev

# debug the whole
./bootstrap.sh -d
```


## Deployment
```shell

```

## Acknowledgement

Some codes are adapted from [Deer-Flow](https://github.com/bytedance/deer-flow) and [Open-Deep-Research](https://github.com/langchain-ai/open_deep_research).
We thank the contributors for their fantastic projects.