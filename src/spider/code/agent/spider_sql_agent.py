from typing import Optional, Union, Sequence
from langchain.agents import AgentExecutor
from agentscope.agents import AgentBase
from agentscope.message import Msg


class SpiderSqlAgent(AgentBase):

    sql_agents: AgentExecutor

    def __init__(
            self,
            name: str,
            sys_prompt: str,
            model_config_name: str,
            use_memory: bool = True,
            memory_config: Optional[dict] = None,
            sql_agent: AgentExecutor = None
    ) -> None:
        """Initialize the dialog agent.

        Arguments:
            name (`str`):
                The name of the agent.
            sys_prompt (`Optional[str]`):
                The system prompt of the agent, which can be passed by args
                or hard-coded in the agent.
            model_config_name (`str`):
                The name of the model config, which is used to load model from
                configuration.
            use_memory (`bool`, defaults to `True`):
                Whether the agent has memory.
            memory_config (`Optional[dict]`):
                The config of memory.
        """
        super().__init__(
            name=name,
            sys_prompt=sys_prompt,
            model_config_name=model_config_name,
            use_memory=use_memory,
            memory_config=memory_config,
        )
        self.sql_agents = sql_agent

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Msg:
        """Reply function of the agent. Processes the input data,
        generates a prompt using the current dialogue memory and system
        prompt, and invokes the language model to produce a response. The
        response is then formatted and added to the dialogue memory.

        Args:
            x (`Optional[Union[Msg, Sequence[Msg]]]`, defaults to `None`):
                The input message(s) to the agent, which also can be omitted if
                the agent doesn't need any input.

        Returns:
            `Msg`: The output message generated by the agent.
        """
        # record the input if needed
        if self.memory:
            self.memory.add(x)

        # prepare prompt
        prompt = self.model.format(
            Msg("system", self.sys_prompt, role="system"),
            self.memory
            and self.memory.get_memory()
            or x,  # type: ignore[arg-type]
        )
        response = self.sql_agents.run(prompt.encode("utf-8"))
        # call llm and generate response
        msg = Msg(self.name, response, role="assistant")

        # Print/speak the message in this agent's voice
        self.speak(msg)

        # Record the message in memory
        if self.memory:
            self.memory.add(msg)
        return msg