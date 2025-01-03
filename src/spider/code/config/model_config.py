model_config = [

    {
        "config_name": "ollama_code",  # 模型配置的名称
        "model_type": "openai_chat",  # 模型wrapper的类型

        # 用以初始化模型wrapper的详细参数 codeqwen:7b-chat-v1.5-fp16
        "model_name": "qwen2.5:14b-instruct-q8_0",  # OpenAI API中的模型名
        "api_key": "xxx",  # OpenAI API的API密钥。如果未设置，将使用环境变量OPENAI_API_KEY。
        "organization": "xxx",  # OpenAI API的组织。如果未设置，将使用环境变量OPENAI_ORGANIZATION。

        "client_args": {
            "base_url": "http://47.109.67.130:11435/v1"
        },
        "generate_args": {
            "temperature": 0.5
        }
    },

    {
        "config_name": "ollama_code_embed",  # 模型配置的名称
        "model_type": "openai_chat",  # 模型wrapper的类型

        # 用以初始化模型wrapper的详细参数 codeqwen:7b-chat-v1.5-fp16
        "model_name": "rjmalagon/gte-qwen2-1.5b-instruct-embed-f16:latest",  # OpenAI API中的模型名
        "api_key": "xxx",  # OpenAI API的API密钥。如果未设置，将使用环境变量OPENAI_API_KEY。
        "organization": "xxx",  # OpenAI API的组织。如果未设置，将使用环境变量OPENAI_ORGANIZATION。

        "client_args": {
            "base_url": "http://47.109.67.130:11435/v1"
        },
        "generate_args": {
            "temperature": 0.5
        }
    },

    {
        "config_name": "ollama_qwen2.5_code",  # 模型配置的名称
        "model_type": "openai_chat",  # 模型wrapper的类型

        # 用以初始化模型wrapper的详细参数 codeqwen:7b-chat-v1.5-fp16
        "model_name": "qwen2.5-coder:7b-instruct-fp16",  # OpenAI API中的模型名
        "api_key": "xxx",  # OpenAI API的API密钥。如果未设置，将使用环境变量OPENAI_API_KEY。
        "organization": "xxx",  # OpenAI API的组织。如果未设置，将使用环境变量OPENAI_ORGANIZATION。

        "client_args": {
            "base_url": "http://47.109.67.130:11435/v1"
        },
        "generate_args": {
            "temperature": 0.5
        }
    },

    {
        "model_type": "dashscope_chat",
        "config_name": "qwen_config",
        "model_name": "qwen-plus",
        "api_key": "sk-66188116bb914e6784374de3bb394908",
        "stream": True,
    },
    {
        "model_type": "dashscope_chat",
        "config_name": "qwen_config_embedding",
        "model_name": "text-embedding-v3",
        "api_key": "sk-66188116bb914e6784374de3bb394908",
        "stream": True,
    },
    {
        "model_type": "dashscope_chat",
        "config_name": "qwen_config_max",
        "model_name": "qwen-max",
        "api_key": "sk-66188116bb914e6784374de3bb394908",
        "stream": True,

    },
    {
        "model_type": "dashscope_chat",
        "config_name": "qwen-coder",
        "model_name": "qwen-coder-plus",
        "api_key": "sk-66188116bb914e6784374de3bb394908",
        "stream": True,

    },
    {
        "model_type": "dashscope_chat",
        "config_name": "qwen-coder-preview",
        "model_name": "qwq-32b-preview",
        "api_key": "sk-66188116bb914e6784374de3bb394908",
        "stream": True,

    },
    {
        "model_type": "dashscope_chat",
        "config_name": "qwen2_config",
        "model_name": "qwen2-72b-instruct",
        "api_key": "sk-66188116bb914e6784374de3bb394908"
    },
    {
        "config_name": "deepseek_code",  # 模型配置的名称
        "model_type": "openai_chat",  # 模型wrapper的类型

        # 用以初始化模型wrapper的详细参数 codeqwen:7b-chat-v1.5-fp16
        "model_name": "deepseek-coder",  # OpenAI API中的模型名
        "api_key": "sk-caef67a3c65b40059d12b97a395f8031",  # OpenAI API的API密钥。如果未设置，将使用环境变量OPENAI_API_KEY。
        "organization": "xxx",  # OpenAI API的组织。如果未设置，将使用环境变量OPENAI_ORGANIZATION。
        "client_args": {
            "base_url": "https://api.deepseek.com/v1"
        },
        "generate_args": {
            "temperature": 0.5
        }
    },

]
