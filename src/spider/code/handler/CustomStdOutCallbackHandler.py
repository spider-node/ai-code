from langchain.callbacks.base import BaseCallbackHandler


class CustomStdOutCallbackHandler(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        try:
            # 打印链的开始信息
            if serialized is not None:
                print(f"Chain started: {serialized}")
            else:
                print("Chain started with no serialized data")

            # 处理 inputs 为 None 的情况
            if inputs is not None:
                print(f"Inputs: {inputs}")

                # 如果需要调用 get 方法，确保对象不是 None
                if 'some_key' in inputs:
                    value = inputs.get('some_key')
                    print(f"Value for some_key: {value}")
                else:
                    print("some_key not found in inputs")
            else:
                print("No inputs provided")
        except Exception as e:
            print(f"Error in on_chain_start: {e}")
